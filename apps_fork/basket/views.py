from oscar.core.loading import get_class, get_model
from extra_views import ModelFormSetView

OrderTotalCalculator = get_class('checkout.calculators', 'OrderTotalCalculator')
BasketVoucherForm = get_class('basket.forms', 'BasketVoucherForm')
Repository = get_class('shipping.repository', 'Repository')
Applicator = get_class('offer.applicator', 'Applicator')


class BasketView(ModelFormSetView):
    model = get_model('basket', 'Line')
    basket_model = get_model('basket', 'Basket')
    formset_class = get_class('basket.formsets', 'BasketLineFormSet')
    form_class = get_class('basket.forms', 'BasketLineForm')
    factory_kwargs = {
        'extra': 0,
        'can_delete': True
    }
    template_name = 'oscar/basket/basket.html'

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs['strategy'] = self.request.strategy
        return kwargs

    def get_queryset(self):
        """
        Return list of :py:class:`Line <oscar.apps.basket.abstract_models.AbstractLine>`
        instances associated with the current basket.
        """  # noqa: E501
        return self.request.basket.all_lines()

    def get_shipping_methods(self, basket):
        return Repository().get_shipping_methods(
            basket=self.request.basket, user=self.request.user,
            request=self.request)

    def get_default_shipping_address(self):
        if self.request.user.is_authenticated:
            return self.request.user.addresses.filter(is_default_for_shipping=True).first()

    def get_default_shipping_method(self, basket):
        return Repository().get_default_shipping_method(
            basket=self.request.basket, user=self.request.user,
            request=self.request, shipping_addr=self.get_default_shipping_address())

    def get_free_shipping_method(self, basket):
        return Repository().get_free_shipping_method(basket=self.request.basket)

    def get_basket_warnings(self, basket):
        """
        Return a list of warnings that apply to this basket
        """
        warnings = []
        for line in basket.all_lines():
            warning = line.get_warning()
            if warning:
                warnings.append(warning)
        return warnings

    def get_upsell_messages(self, basket):
        offers = Applicator().get_offers(basket, self.request.user,
                                         self.request)
        applied_offers = list(basket.offer_applications.offers.values())
        msgs = []
        for offer in offers:
            if offer.is_condition_partially_satisfied(basket) \
                    and offer not in applied_offers:
                data = {
                    'message': offer.get_upsell_message(basket),
                    'offer': offer}
                msgs.append(data)
        return msgs

    def get_basket_voucher_form(self):
        """
        This is a separate method so that it's easy to e.g. not return a form
        if there are no vouchers available.
        """
        return BasketVoucherForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voucher_form'] = self.get_basket_voucher_form()

        # Shipping information is included to give an idea of the total order
        # cost.  It is also important for PayPal Express where the customer
        # gets redirected away from the basket page and needs to see what the
        # estimated order total is beforehand.
        context['shipping_methods'] = self.get_shipping_methods(
            self.request.basket)
        method = self.get_free_shipping_method(self.request.basket)
        context['shipping_method'] = method
        shipping_charge = method.calculate(self.request.basket)
        context['shipping_charge'] = shipping_charge
        if method.is_discounted:
            excl_discount = method.calculate_excl_discount(self.request.basket)
            context['shipping_charge_excl_discount'] = excl_discount

        context['order_total'] = OrderTotalCalculator().calculate(
            self.request.basket, shipping_charge)
        context['basket_warnings'] = self.get_basket_warnings(
            self.request.basket)
        context['upsell_messages'] = self.get_upsell_messages(
            self.request.basket)

        if self.request.user.is_authenticated:
            try:
                saved_basket = self.basket_model.saved.get(
                    owner=self.request.user)
            except self.basket_model.DoesNotExist:
                pass
            else:
                saved_basket.strategy = self.request.basket.strategy
                if not saved_basket.is_empty:
                    saved_queryset = saved_basket.all_lines()
                    formset = SavedLineFormSet(strategy=self.request.strategy,
                                               basket=self.request.basket,
                                               queryset=saved_queryset,
                                               prefix='saved')
                    context['saved_formset'] = formset
        return context

    def get_success_url(self):
        return safe_referrer(self.request, 'basket:summary')

    def formset_valid(self, formset):
        # Store offers before any changes are made so we can inform the user of
        # any changes
        offers_before = self.request.basket.applied_offers()
        save_for_later = False

        # Keep a list of messages - we don't immediately call
        # django.contrib.messages as we may be returning an AJAX response in
        # which case we pass the messages back in a JSON payload.
        flash_messages = ajax.FlashMessages()

        for form in formset:
            if (hasattr(form, 'cleaned_data')
                    and getattr(form.cleaned_data, 'save_for_later', False)):
                line = form.instance
                if self.request.user.is_authenticated:
                    self.move_line_to_saved_basket(line)

                    msg = render_to_string(
                        'oscar/basket/messages/line_saved.html',
                        {'line': line})
                    flash_messages.info(msg)

                    save_for_later = True
                else:
                    msg = _("You can't save an item for later if you're "
                            "not logged in!")
                    flash_messages.error(msg)
                    return redirect(self.get_success_url())

        if save_for_later:
            # No need to call super if we're moving lines to the saved basket
            response = redirect(self.get_success_url())
        else:
            # Save changes to basket as per normal
            response = super().formset_valid(formset)

        # If AJAX submission, don't redirect but reload the basket content HTML
        if self.request.is_ajax():
            # Reload basket and apply offers again
            self.request.basket = get_model('basket', 'Basket').objects.get(
                id=self.request.basket.id)
            self.request.basket.strategy = self.request.strategy
            Applicator().apply(self.request.basket, self.request.user,
                               self.request)
            offers_after = self.request.basket.applied_offers()

            for level, msg in BasketMessageGenerator().get_messages(
                    self.request.basket, offers_before, offers_after, include_buttons=False):
                flash_messages.add_message(level, msg)

            # Reload formset - we have to remove the POST fields from the
            # kwargs as, if they are left in, the formset won't construct
            # correctly as there will be a state mismatch between the
            # management form and the database.
            kwargs = self.get_formset_kwargs()
            del kwargs['data']
            del kwargs['files']
            if 'queryset' in kwargs:
                del kwargs['queryset']
            formset = self.get_formset()(queryset=self.get_queryset(),
                                         **kwargs)
            ctx = self.get_context_data(formset=formset,
                                        basket=self.request.basket)
            return self.json_response(ctx, flash_messages)

        BasketMessageGenerator().apply_messages(self.request, offers_before)

        return response

    def json_response(self, ctx, flash_messages):
        basket_html = render_to_string(
            'oscar/basket/partials/basket_content.html',
            context=ctx, request=self.request)

        return JsonResponse({
            'content_html': basket_html,
            'messages': flash_messages.as_dict()
        })

    def move_line_to_saved_basket(self, line):
        saved_basket, _ = get_model('basket', 'basket').saved.get_or_create(
            owner=self.request.user)
        saved_basket.merge_line(line)

    def formset_invalid(self, formset):
        flash_messages = ajax.FlashMessages()
        flash_messages.warning(_(
            "Your basket couldn't be updated. "
            "Please correct any validation errors below."))

        if self.request.is_ajax():
            ctx = self.get_context_data(formset=formset,
                                        basket=self.request.basket)
            return self.json_response(ctx, flash_messages)

        flash_messages.apply_to_request(self.request)
        return super().formset_invalid(formset)
