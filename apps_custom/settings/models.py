from django.db import models
from oscar.core.loading import get_model
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel,PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag



ContentPage = get_model('content', 'ContentPage')


class SettingProductTag(TaggedItemBase):
    content_object = models.ForeignKey(
        'catalogue.Product',
        on_delete=models.CASCADE,
        null=True
    )

@register_setting
class MarketplaceSettings(BaseSetting):
    couverture_marketplace = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text='Couverture de la marketplace'
    )
    comment_ca_marche = models.ForeignKey(
        ContentPage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text='Lien vers la page de description du concept'
    )

    product_tags = ClusterTaggableManager(through=SettingProductTag, blank=True)
    
    panels = [
        ImageChooserPanel('couverture_marketplace'),
        PageChooserPanel('comment_ca_marche'),
        FieldPanel('product_tags'),
    ]
    
    

