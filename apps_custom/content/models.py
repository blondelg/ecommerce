from django.db import models
from django.db import connection
from django.db.models import Sum
from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField,StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel,PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


import datetime

from taggit.managers import TaggableManager
from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase

from oscar.core.loading import get_model




class ContentIndexPage(Page):
    intro = RichTextField(blank=True)
    image = models.ForeignKey(
    'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )


    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        contentpages = self.get_children().live().exclude(title='Tag').order_by('-first_published_at')


        context['contentpages'] = contentpages
        return context

    def get_tag(self):
        # Get weighted tag list
        pass

    def __init__(self, *args, **kwargs):
        super(ContentIndexPage, self).__init__(*args, **kwargs)
        self._meta.get_field('title').verbose_name = 'Titre de l\'index'

    class Meta:
        verbose_name = 'Index - Standard'
        
        
        
class ContentIndexAsso(Page):
    intro = RichTextField(blank=True)
    image = models.ForeignKey(
    'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )


    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        contentpages = self.get_children().live().exclude(title='Tag').order_by('-first_published_at')


        context['contentpages'] = contentpages
        return context

    def get_tag(self):
        # Get weighted tag list
        pass

    def __init__(self, *args, **kwargs):
        super(ContentIndexAsso, self).__init__(*args, **kwargs)
        self._meta.get_field('title').verbose_name = 'Titre de l\'index'

    class Meta:
        verbose_name = 'Index - Asso'
        
        
        
class ContentIndexProject(Page):
    intro = RichTextField(blank=True)
    image = models.ForeignKey(
    'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )


    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        contentpages = self.get_children().live().exclude(title='Tag').order_by('-first_published_at')


        context['contentpages'] = contentpages
        return context

    def get_tag(self):
        # Get weighted tag list
        pass

    def __init__(self, *args, **kwargs):
        super(ContentIndexProject, self).__init__(*args, **kwargs)
        self._meta.get_field('title').verbose_name = 'Titre de l\'index'

    class Meta:
        verbose_name = 'Index - Projets'

        
        
class ContentIndexCategoryPage(ContentIndexPage):

    category = models.ForeignKey('content.ContentPageCategory', on_delete=models.SET_NULL, null=True)
    
    content_panels = ContentIndexPage.content_panels + [
        FieldPanel('category'),
    ]
    
    def get_context(self, request):
        # Update context to include only published posts, by category ordered by reverse-chron
        context = super().get_context(request)
        contentpages = ContentPage.objects.filter(category=self.category).order_by('-first_published_at')
        context['contentpages'] = contentpages.set_levels()
        return context
        
    class Meta:
        verbose_name = 'Index - Catégories'


class ContentPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ContentPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ContentProductTag(TaggedItemBase):
    content_object = models.ForeignKey(
        'catalogue.Product',
        related_name='tagged_items',
        on_delete=models.CASCADE,
        null=True
    )


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class ContentPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=ContentPageTag, blank=True)
    category = models.ForeignKey('content.ContentPageCategory', on_delete=models.SET_NULL, null=True)
    couverture = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]


    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('tags'),
        FieldPanel('category'),
        ImageChooserPanel('couverture'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]
    
    class Meta:
        verbose_name = 'Page - Standard'

    def __init__(self, *args, **kwargs):
        super(ContentPage, self).__init__(*args, **kwargs)
        self._meta.get_field('title').verbose_name = 'Titre de la page'


class ContentPageGalleryImage(Orderable):
    page = ParentalKey(ContentPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class ContentTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        contentpages = ContentPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['contentpages'] = contentpages
        return context
        
    class Meta:
        verbose_name = 'Index - Tags'


@register_snippet
class ContentPageCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        


class ContentAsso(ContentPage):

    # additionnal fields
    site = models.URLField(max_length = 200, blank=True, null=True)
    twitter = models.URLField(max_length = 200, blank=True, null=True)
    facebook = models.URLField(max_length = 200, blank=True,  null=True)
    instagram = models.URLField(max_length = 200, blank=True, null=True)
    youtube = models.URLField(max_length = 200, blank=True, null=True)

    # hide category from panels
    content_panels = [e for e in ContentPage.content_panels if 'category' not in str(e.field_type)]
    content_panels += [
        MultiFieldPanel(
            [
                FieldPanel('site'),
                FieldPanel('twitter'),
                FieldPanel('facebook'),
                FieldPanel('instagram'),
                FieldPanel('youtube'),
            ],
            heading="Visibilité"
        ),
    ]



    def __init__(self, *args, **kwargs):
        super(ContentAsso, self).__init__(*args, **kwargs)
        self.category = ContentPageCategory.objects.get(name='Association')
        self.date = datetime.date.today()
        self._meta.get_field('title').verbose_name = 'Nom de l\'association'


    class Meta:
        verbose_name = "Page - Association"


class ContentPartner(ContentPage):

    # additionnal fields
    site = models.URLField(max_length = 200, blank=True, null=True)
    twitter = models.URLField(max_length = 200, blank=True, null=True)
    facebook = models.URLField(max_length = 200, blank=True,  null=True)
    instagram = models.URLField(max_length = 200, blank=True, null=True)
    youtube = models.URLField(max_length = 200, blank=True, null=True)

    # hide category from panels
    content_panels = [e for e in ContentPage.content_panels if 'category' not in str(e.field_type)]
    content_panels += [
        MultiFieldPanel(
            [
                FieldPanel('site'),
                FieldPanel('twitter'),
                FieldPanel('facebook'),
                FieldPanel('instagram'),
                FieldPanel('youtube'),
            ],
            heading="Visibilité"
        ),
    ]

    def __init__(self, *args, **kwargs):
        super(ContentPartner, self).__init__(*args, **kwargs)
        self.category = ContentPageCategory.objects.get(name='Partenaire')
        self.date = datetime.date.today()
        self._meta.get_field('title').verbose_name = 'Nom du partenaire'

    class Meta:
        verbose_name = "Page - Partenaire"


class ContentProjet(ContentPage):


    # add project funding target
    target = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Objectif de financement €')
    # add asso
    asso = models.ForeignKey('content.ContentAsso', on_delete=models.SET_NULL, null=True)
    achievement = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    achievement_percent = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    achieved = models.BooleanField(default=False)

    # hide category from panels
    content_panels = [e for e in ContentPage.content_panels if 'category' not in str(e.field_type)]
    content_panels += [FieldPanel('target'), FieldPanel('asso')]

    def __init__(self, *args, **kwargs):
        super(ContentProjet, self).__init__(*args, **kwargs)
        self.category = ContentPageCategory.objects.get(name='Projet')
        self.date = datetime.date.today()
        self._meta.get_field('title').verbose_name = 'Nom du projet'
        
    
    class Meta:
        verbose_name = "Page - Projet"
        
