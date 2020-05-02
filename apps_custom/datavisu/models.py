from django.db import models
from django.utils.translation import gettext_lazy as _
from django_pandas.managers import DataFrameManager

class ProductView(models.Model):

    user_id = models.IntegerField(
        null=True,
        default='0',
        verbose_name=_("User id"))
    product_id = models.IntegerField(
        null=True,
        verbose_name=_("Product id"))
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    objects = DataFrameManager()

    class Meta:
        app_label = 'datavisu'
        verbose_name = _('Product view')
        verbose_name_plural = _('Product views')

    def __str__(self):
        return _("product id : '%(product)s' has been viewed") % {'product': self.product_id}
