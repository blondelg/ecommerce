from oscar.apps.order.abstract_models import AbstractOrder
from django.utils.translation import gettext_lazy as _
from django.db import models
from oscar.core.loading import get_model

projet = get_model('content', 'ContentProjet')


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
        _("Order structure"),
        max_length=10,
        choices=STRUCTURE_CHOICES,
        default=STANDALONE)

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name=_("Parent order"))

    partner = models.ForeignKey(
        'partner.Partner',
        on_delete=models.SET_NULL,
        null=True,
        default=0,
        db_constraint=False,
        verbose_name=_("Partner"),
        related_name='partner')
        
    project = models.ForeignKey(projet, on_delete=models.SET_NULL, null=True)

    @property
    def is_child(self):
        if self.structure == 'child':
            return True
        else:
            return False

class Donation(models.Model):
    
    """
    table that accounts for every donations done during orders
    """
    project = models.ForeignKey('content.ContentProjet', null=True, on_delete=models.SET_NULL)
    project_name = models.CharField(max_length=250, null=True, blank=True)
    asso_name = models.CharField(max_length=250, null=True, blank=True)
    order = models.ForeignKey('order.Order', null=False, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, blank=True)

        
    def save(self, *args, **kwargs):
        """ to keep a track of asso and project even if the will be deleted """
        self.project_name = self.project.title
        self.asso_name = self.project.asso.title
        self.update_project_levels()
        super().save(*args, **kwargs)
        
    def update_project_levels(self):
        """ update project levels """
        self.project.achievement += self.amount
        self.project.achievement_percent = round(self.project.achievement / self.project.target, 4)
        if self.project.achievement > self.project.target:
            self.project.achievement = self.project.target
            self.project.achievement_percent = Decimal('1')
            self.project.achieved = True
        
        self.project.save()
            

    


from oscar.apps.order.models import *  # noqa isort:skip
