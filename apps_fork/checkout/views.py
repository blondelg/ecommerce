from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView



class PaymentDetailsView(CorePaymentDetailsView):

    def handle_place_order_submission(self, request):
        """
        Handle a request to place an order.

        This method is normally called after the customer has clicked "place
        order" on the preview page. It's responsible for (re-)validating any
        form information then building the submission dict to pass to the
        `submit` method.

        If forms are submitted on your payment details view, you should
        override this method to ensure they are valid before extracting their
        data into the submission dict and passing it onto `submit`.
        """
        submissions = self.build_submission()
        # delete setting added only for template for mix baskets
        submissions.pop("order_total_mix", None)
        return self.submit(**submissions)
