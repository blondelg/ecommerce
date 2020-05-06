from oscar.apps.dashboard.orders.views import OrderDetailView as CoreOrderDetailView
from apps_fork.order.models import Order

class OrderDetailView(CoreOrderDetailView):

    def get_order_lines(self):
        if self.object.is_child:
            return Order(id=self.object.parent_id).lines.filter(partner_id=self.object.partner_id)
        else:
            return self.object.lines.all()
