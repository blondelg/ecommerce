from django.db import models
from django.db import connection
from django import forms
from django.utils.text import slugify

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField,StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from wagtail.snippets.models import register_snippet

import datetime


class BlogIndexPage(Page):
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
        blogpages = self.get_children().live().exclude(title='Tag').order_by('-first_published_at')


        context['blogpages'] = blogpages
        return context

    def get_tag(self):
        # Get weighted tag list
        pass

    def __init__(self, *args, **kwargs):
        super(BlogIndexPage, self).__init__(*args, **kwargs)
        self._meta.get_field('title').verbose_name = 'Titre de l\'index'

    class Meta:
        verbose_name = 'Blog - Index'
        
        
class BlogIndexCategoryPage(BlogIndexPage):

    category = models.ForeignKey('blog.BlogPageCategory', on_delete=models.SET_NULL, null=True)
    
    content_panels = BlogIndexPage.content_panels + [
        FieldPanel('category'),
    ]
    
    def get_context(self, request):
        # Update context to include only published posts, by category ordered by reverse-chron
        context = super().get_context(request)
        blogpages = BlogPage.objects.filter(category=self.category).order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
        
    class Meta:
        verbose_name = 'Blog - Index par catégorie'


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    category = models.ForeignKey('blog.BlogPageCategory', on_delete=models.SET_NULL, null=True)
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
        verbose_name = 'Page standard'

    def __init__(self, *args, **kwargs):
	    super(BlogPage, self).__init__(*args, **kwargs)
	    self._meta.get_field('title').verbose_name = 'Titre de la page'


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


@register_snippet
class BlogPageCategory(models.Model):
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
        
@register_snippet
class MarketplaceConfig(models.Model):
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
        
    def __init__(self):
        pass

    class Meta:
        verbose_name = 'Marketplace Configuration'



class BlogAsso(BlogPage):

	# additionnal fields
	site = models.URLField(max_length = 200, blank=True, null=True)
	twitter = models.URLField(max_length = 200, blank=True, null=True)
	facebook = models.URLField(max_length = 200, blank=True,  null=True)
	instagram = models.URLField(max_length = 200, blank=True, null=True)
	youtube = models.URLField(max_length = 200, blank=True, null=True)

    # hide category from panels
	content_panels = [e for e in BlogPage.content_panels if 'category' not in str(e.field_type)]
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
		super(BlogAsso, self).__init__(*args, **kwargs)
		self.category = BlogPageCategory.objects.get(name='Association')
		self.date = datetime.date.today()
		self._meta.get_field('title').verbose_name = 'Nom de l\'association'


	class Meta:
		verbose_name = "Association - Page de présentation"


class BlogPartner(BlogPage):

	# additionnal fields
	site = models.URLField(max_length = 200, blank=True, null=True)
	twitter = models.URLField(max_length = 200, blank=True, null=True)
	facebook = models.URLField(max_length = 200, blank=True,  null=True)
	instagram = models.URLField(max_length = 200, blank=True, null=True)
	youtube = models.URLField(max_length = 200, blank=True, null=True)

    # hide category from panels
	content_panels = [e for e in BlogPage.content_panels if 'category' not in str(e.field_type)]
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
		super(BlogPartner, self).__init__(*args, **kwargs)
		self.category = BlogPageCategory.objects.get(name='Partenaire')
		self.date = datetime.date.today()
		self._meta.get_field('title').verbose_name = 'Nom du partenaire'

	class Meta:
		verbose_name = "Partenaire - Page de présentation"


class BlogProjet(BlogPage):

	# add project funding target
	target = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Objectif de financement €')
	# add asso
	asso = models.ForeignKey('blog.BlogAsso', on_delete=models.SET_NULL, null=True)

	# hide category from panels
	content_panels = [e for e in BlogPage.content_panels if 'category' not in str(e.field_type)]
	content_panels += [FieldPanel('target'), FieldPanel('asso')]

	def __init__(self, *args, **kwargs):
		super(BlogProjet, self).__init__(*args, **kwargs)
		self.category = BlogPageCategory.objects.get(name='Projet')
		self.date = datetime.date.today()
		self._meta.get_field('title').verbose_name = 'Nom du projet'
	
	class Meta:
		verbose_name = "Projet - Page de présentation"


