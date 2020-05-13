from oscar.apps.dashboard.views import IndexView as CoreIndexView


class IndexView(CoreIndexView):

    def get_stats(self):
        datetime_24hrs_ago = now() - timedelta(hours=24)

        orders = Order.objects.all()
        orders_pending = Order.objects.filter(status='Pending')
        alerts = StockAlert.objects.all()
        baskets = Basket.objects.filter(status=Basket.OPEN)
        customers = User.objects.filter(orders__isnull=False).distinct()
        lines = Line.objects.filter()
        products = Product.objects.all()

        user = self.request.user
        if not user.is_staff:
            partners_ids = tuple(user.partners.values_list('id', flat=True))
            orders = orders.filter(
                lines__partner_id__in=partners_ids
            ).distinct()
            orders_pending = orders.filter(
                lines__partner_id__in=partners_ids
            ).distinct()
            alerts = alerts.filter(stockrecord__partner_id__in=partners_ids)
            baskets = baskets.filter(
                lines__stockrecord__partner_id__in=partners_ids
            ).distinct()
            customers = customers.filter(
                orders__lines__partner_id__in=partners_ids
            ).distinct()
            lines = lines.filter(partner_id__in=partners_ids)
            products = products.filter(stockrecords__partner_id__in=partners_ids)

        orders_last_day = orders.filter(date_placed__gt=datetime_24hrs_ago)

        open_alerts = alerts.filter(status=StockAlert.OPEN)
        closed_alerts = alerts.filter(status=StockAlert.CLOSED)

        total_lines_last_day = lines.filter(order__in=orders_last_day).count()
        stats = {
            'total_orders_last_day': orders_last_day.count(),
            'total_lines_last_day': total_lines_last_day,

            'average_order_costs': orders_last_day.aggregate(
                Avg('total_incl_tax')
            )['total_incl_tax__avg'] or D('0.00'),

            'total_revenue_last_day': orders_last_day.aggregate(
                Sum('total_incl_tax')
            )['total_incl_tax__sum'] or D('0.00'),

            'hourly_report_dict': self.get_hourly_report(orders),
            'total_customers_last_day': customers.filter(
                date_joined__gt=datetime_24hrs_ago,
            ).count(),

            'total_open_baskets_last_day': baskets.filter(
                date_created__gt=datetime_24hrs_ago
            ).count(),

            'total_products': products.count(),
            'total_open_stock_alerts': open_alerts.count(),
            'total_closed_stock_alerts': closed_alerts.count(),

            'total_customers': customers.count(),
            'total_open_baskets': baskets.count(),
            'total_orders': orders.count(),
            'total_orders_pending': orders_pending.count(),
            'total_lines': lines.count(),
            'total_revenue': orders.aggregate(
                Sum('total_incl_tax')
            )['total_incl_tax__sum'] or D('0.00'),

            'order_status_breakdown': orders.order_by(
                'status'
            ).values('status').annotate(freq=Count('id'))
        }
        if user.is_staff:
            stats.update(
                total_site_offers=self.get_active_site_offers().count(),
                total_vouchers=self.get_active_vouchers().count(),
            )
        return stats
