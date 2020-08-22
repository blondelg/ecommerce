from django.db import models
from oscar.core.loading import get_model
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel,PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag



ContentPage = get_model('content', 'ContentPage')
ContentIndexAsso = get_model('content', 'ContentIndexAsso')
ContentIndexProject = get_model('content', 'ContentIndexProject')
Tag = get_model('content', 'Tag')



@register_setting
class MarketplaceSettings(BaseSetting):
    couverture_marketplace = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text='Couverture de la marketplace'
    )
    
    comment_ca_marche = models.ForeignKey(
        ContentPage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text='Lien vers la page de description du concept'
    )
    
    index_asso = models.ForeignKey(
        ContentIndexAsso, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text='Lien vers l\'index des associations'
    )
    
    index_project = models.ForeignKey(
        ContentIndexProject, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text='Lien vers l\'index des projets'
    )

    menu_tag_1 = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="")
    menu_tag_2 = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="")
    menu_tag_3 = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="")
    menu_tag_4 = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="")
    menu_tag_5 = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="")
    menu_tag_6 = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="")
    
    
    menu_label_1 = models.CharField(verbose_name='Label 1', max_length=30, null=True, blank=True)
    menu_url_1 = models.CharField(max_length = 200, verbose_name='URL 1', null=True, blank=True)
    
    menu_label_2 = models.CharField(verbose_name='Label 2', max_length=30, null=True, blank=True)
    menu_url_2 = models.CharField(max_length = 200, verbose_name='URL 2', null=True, blank=True)
    
    menu_label_3 = models.CharField(verbose_name='Label 3', max_length=30, null=True, blank=True)
    menu_url_3 = models.CharField(max_length = 200, verbose_name='URL 3', null=True, blank=True)
    
    favicon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text='Favicon'
    )
    
    
    
    panels = [
        ImageChooserPanel('couverture_marketplace'),
        PageChooserPanel('comment_ca_marche'),
        PageChooserPanel('index_asso'),
        PageChooserPanel('index_project'),

        
        MultiFieldPanel(
            [
                FieldPanel('menu_tag_1'),
                FieldPanel('menu_tag_2'),
                FieldPanel('menu_tag_3'),
                FieldPanel('menu_tag_4'),
                FieldPanel('menu_tag_5'),
                FieldPanel('menu_tag_6'),
            ],
            heading="Tags produits barre menu",
            classname="collapsible",

        ),
        
        MultiFieldPanel(
            [
                FieldPanel('menu_label_1'),
                FieldPanel('menu_url_1'),
                FieldPanel('menu_label_2'),
                FieldPanel('menu_url_2'),
                FieldPanel('menu_label_3'),
                FieldPanel('menu_url_3'),
            ],
            heading="Liens additionnels barre menu",
            classname="collapsible"
        ),
        
        ImageChooserPanel('favicon'),
        
    ]


    class Meta:
        verbose_name = 'Parametres site'
    

