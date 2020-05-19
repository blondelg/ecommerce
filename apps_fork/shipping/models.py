from django.db import models
from django.utils.translation import gettext_lazy as _
from oscar.core.utils import get_default_currency
from django.conf import settings
from decimal import Decimal as D

class ShippingRule(models.Model):
    """
    this table aims at allowing each partner to define their own
    shipping rules
    """


    partner = models.ForeignKey(
        'partner.Partner',
        on_delete=models.CASCADE,
        verbose_name=_("Partner"))

    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Description'), blank=True)
    charge_excl_tax = models.DecimalField(
        _("Charge (excl. tax)"),
        decimal_places=2,
        max_digits=12,
        blank=True,
        null=True)

    charge_incl_tax = models.DecimalField(
        _("Charge (incl. tax)"),
        decimal_places=2,
        max_digits=12,
        blank=True,
        null=True)

    free_shipping_threshold = models.DecimalField(
        _("Free shipping threshold"),
        decimal_places=2,
        max_digits=12,
        default=0,
        null=True)

    charge_currency = models.CharField(
        _("Currency"), max_length=12, default=get_default_currency)

    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True,
                                        db_index=True)


    def __str__(self):
        msg = "Partner: %s, name: %s" % (
            self.partner.display_name, self.name,)
        return msg

    class Meta:
        app_label = 'shipping'
        verbose_name = _("Shipping rule")
        verbose_name_plural = _("Shipping Rules")

    def save(self, *args, **kwargs):
        try:
            tax_rate = D(settings.OSCAR_DEFAULT_TAX_RATE)
            self.charge_excl_tax = self.charge_incl_tax / (1 + tax_rate)
        except:
            pass

        super(ShippingRule, self).save(*args, **kwargs)



from oscar.apps.shipping.models import *  # noqa isort:skip
