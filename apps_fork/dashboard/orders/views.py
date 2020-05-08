from oscar.apps.dashboard.orders.views import OrderDetailView as CoreOrderDetailView
from oscar.apps.dashboard.orders.views import OrderListView as CoreOrderListView
from oscar.apps.dashboard.orders.views import OrderStatsView as CoreOrderStatsView
from apps_fork.order.models import Order
from oscar.core.loading import get_model


Partner = get_model('partner', 'Partner')



def queryset_orders_for_user(user):
    """
    Returns a queryset of all orders that a user is allowed to access.
    A staff user may access all orders.
    To allow access to an order for a non-staff user, at least one line's
    partner has to have the user in the partner's list.
    """
    queryset = Order._default_manager.select_related(
        'billing_address', 'billing_address__country',
        'shipping_address', 'shipping_address__country',
        'user',
    ).prefetch_related('lines', 'status_changes')
    if user.is_staff:
        return queryset
    else:
        partner = Partner.objects.get(users=user)
        return queryset.filter(partner=partner)

def get_order_for_user_or_404(user, number):
    try:
        return queryset_orders_for_user(user).get(number=number)
    except ObjectDoesNotExist:
        raise Http404()

class OrderStatsView(CoreOrderStatsView):

    def get_stats(self, filters):
        orders = queryset_orders_for_user(self.request.user).filter(**filters)
        stats = {
            'total_orders': orders.count(),
            'total_lines': Line.objects.filter(order__in=orders).count(),
            'total_revenue': orders.aggregate(
                Sum('total_incl_tax'))['total_incl_tax__sum'] or D('0.00'),
            'order_status_breakdown': orders.order_by('status').values(
                'status').annotate(freq=Count('id'))
        }
        return stats

class OrderDetailView(CoreOrderDetailView):

    def get_order_lines(self):
        if self.object.is_child:
            return Order(id=self.object.parent_id).lines.filter(partner_id=self.object.partner_id)
        else:
            return self.object.lines.all()


class OrderListView(CoreOrderListView):

    def dispatch(self, request, *args, **kwargs):
        # base_queryset is equal to all orders the user is allowed to access
        self.base_queryset = queryset_orders_for_user(
            request.user).order_by('-date_placed')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = self.form
        ctx['order_statuses'] = Order.all_statuses()
        ctx['search_filters'] = self.get_search_filter_descriptions()
        ctx['is_staff'] = self.request.user.is_staff
        return ctx
