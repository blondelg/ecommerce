from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ungettext_lazy
from django_tables2 import A, Column, LinkColumn, TemplateColumn

from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')
AttributeOptionGroup = get_model('catalogue', 'AttributeOptionGroup')
Option = get_model('catalogue', 'Option')


class ProductTable(DashboardTable):
    partner = TemplateColumn(
        verbose_name=_('Partner'),
        template_name='oscar/dashboard/catalogue/product_row_partner.html',
        order_by='partner')
    title = TemplateColumn(
        verbose_name=_('Title'),
        template_name='oscar/dashboard/catalogue/product_row_title.html',
        order_by='title', accessor=A('title'))
    structure = TemplateColumn(
        verbose_name=_('Product Structure'),
        template_name='oscar/dashboard/catalogue/product_row_structure.html',
        order_by='structure')
    image = TemplateColumn(
        verbose_name=_('Image'),
        template_name='oscar/dashboard/catalogue/product_row_image.html',
        orderable=False)
    product_class = TemplateColumn(
        verbose_name=_('Product type'),
        template_name='oscar/dashboard/catalogue/product_row_product_class.html')
    # add product attributes
    attributes = TemplateColumn(
        verbose_name=_('Attributes'),
        template_name='oscar/dashboard/catalogue/product_row_attributes.html',
        orderable=False)
    # add real stock level
    stock = TemplateColumn(
        verbose_name=_('Stock level'),
        template_name='oscar/dashboard/catalogue/product_row_stock.html')
    stock_records = TemplateColumn(
        verbose_name=_('Has stock record'),
        template_name='oscar/dashboard/catalogue/product_row_has_stockrecords.html',
        orderable=False)
    price_excl_tax = TemplateColumn(
        verbose_name=_('HT Price'),
        template_name='oscar/dashboard/catalogue/product_row_price_ht.html',
        orderable=False)
    price_incl_tax = TemplateColumn(
        verbose_name=_('TTC Price'),
        template_name='oscar/dashboard/catalogue/product_row_price_ttc.html',
        orderable=False)
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='oscar/dashboard/catalogue/product_row_actions.html',
        orderable=False)

    icon = "sitemap"

    class Meta(DashboardTable.Meta):
        model = Product
        fields = ('upc', 'date_updated')
        sequence = ('partner', 'title', 'upc', 'image', 'product_class', #'variants',
                    #'stock_records', '...', 'date_updated', 'actions')
                    '...', 'date_updated', 'actions')
        order_by = '-date_updated'


class CategoryTable(DashboardTable):
    name = LinkColumn('dashboard:catalogue-category-update', args=[A('pk')])
    description = TemplateColumn(
        template_code='{{ record.description|default:""|striptags'
                      '|cut:"&nbsp;"|truncatewords:6 }}')
    # mark_safe is needed because of
    # https://github.com/bradleyayers/django-tables2/issues/187
    num_children = LinkColumn(
        'dashboard:catalogue-category-detail-list', args=[A('pk')],
        verbose_name=mark_safe(_('Number of child categories')),
        accessor='get_num_children',
        orderable=False)
    actions = TemplateColumn(
        template_name='oscar/dashboard/catalogue/category_row_actions.html',
        orderable=False)

    icon = "sitemap"
    caption = ungettext_lazy("%s Category", "%s Categories")

    class Meta(DashboardTable.Meta):
        model = Category
        fields = ('name', 'description')


class AttributeOptionGroupTable(DashboardTable):
    name = TemplateColumn(
        verbose_name=_('Name'),
        template_name='oscar/dashboard/catalogue/attribute_option_group_row_name.html',
        order_by='name')
    option_summary = TemplateColumn(
        verbose_name=_('Option summary'),
        template_name='oscar/dashboard/catalogue/attribute_option_group_row_option_summary.html',
        orderable=False)
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='oscar/dashboard/catalogue/attribute_option_group_row_actions.html',
        orderable=False)

    icon = "sitemap"
    caption = ungettext_lazy("%s Attribute Option Group", "%s Attribute Option Groups")

    class Meta(DashboardTable.Meta):
        model = AttributeOptionGroup
        fields = ('name',)
        sequence = ('name', 'option_summary', 'actions')
        per_page = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE


class OptionTable(DashboardTable):
    name = TemplateColumn(
        verbose_name=_('Name'),
        template_name='oscar/dashboard/catalogue/option_row_name.html',
        order_by='name')
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='oscar/dashboard/catalogue/option_row_actions.html',
        orderable=False)

    icon = "reorder"
    caption = ungettext_lazy("%s Option", "%s Options")

    class Meta(DashboardTable.Meta):
        model = Option
        fields = ('name', 'type')
        sequence = ('name', 'type', 'actions')
        per_page = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE
