from django.db import models
from oscar.core.compat import AUTH_USER_MODEL
from oscar.models.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

class Asso (models.Model):
    code = AutoSlugField(_("Code"), max_length=128, unique=True, db_index=True,
                         populate_from='name')
    name = models.CharField(
        pgettext_lazy("Asso's name", "Name"), max_length=128, blank=True, db_index=True)

    #: A partner can have users assigned to it. This is used
    #: for access modelling in the permission-based dashboard
    users = models.ManyToManyField(
        AUTH_USER_MODEL, related_name="assos",
        blank=True, verbose_name=_("Users"))


