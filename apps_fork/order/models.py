from oscar.apps.order.abstract_models import AbstractOrder
from django.utils.translation import gettext_lazy as _
from django.db import models

class Order(AbstractOrder):

    # add structure field
    # STANDALONE -> only 1 partner
    # PARENT -> multi-partner, client view
    # CHILD -> mutli-partner, partner view

    STANDALONE, PARENT, CHILD = 'standalone', 'parent', 'child'
    STRUCTURE_CHOICES = (
        (STANDALONE, _('Stand-alone order')),
        (PARENT, _('Parent order')),
        (CHILD, _('Child order'))
    )
    structure = models.CharField(
        _("Order structure"), max_length=10, choices=STRUCTURE_CHOICES,
        default=STANDALONE)

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name=_("Parent order"))


from oscar.apps.order.models import *  # noqa isort:skip
