# -*- coding: utf-8 -*-

from django.conf import settings
from forked_apps.catalogue.signals import product_viewed
from django.dispatch import receiver
from custom_apps.datavisu.models import ProductView


@receiver(product_viewed)
def product_view_callback(sender, **kwargs):

    record = ProductView(user_id=sender.get_user_id(), product_id=sender.kwargs['pk'])
    record.save()


if settings.OSCAR_DELETE_IMAGE_FILES:
    from django.db import models
    from django.db.models.signals import post_delete

    from oscar.core.loading import get_model
    from oscar.core.thumbnails import get_thumbnailer

    ProductImage = get_model('catalogue', 'ProductImage')
    Category = get_model('catalogue', 'Category')

    def delete_image_files(sender, instance, **kwargs):
        """
        Deletes the original image and created thumbnails.
        """
        image_fields = (models.ImageField,)
        thumbnailer = get_thumbnailer()
        for field in instance._meta.fields:
            if isinstance(field, image_fields):
                # Make Django return ImageFieldFile instead of ImageField
                field_file = getattr(instance, field.name)
                thumbnailer.delete_thumbnails(field_file)

    # Connect for all models with ImageFields - add as needed
    models_with_images = [ProductImage, Category]
    for sender in models_with_images:
        post_delete.connect(delete_image_files, sender=sender)
