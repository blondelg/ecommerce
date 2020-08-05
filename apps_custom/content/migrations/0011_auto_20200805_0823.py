# Generated by Django 2.2.13 on 2020-08-05 08:23

from django.db import migrations


def set_default_categories(apps, schema_editor):
    ContentPageCategory = apps.get_model('content', 'ContentPageCategory')
    categories = [
        'Association',
        'Partenaire',
        'Projet'
    ]
    
    for c in categories:
        category = ContentPageCategory(name=c)
        category.save()
        
def drop_welcome_page(apps, schema_editor):
    Page = apps.get_model('wagtailcore', 'Page')
    welcome_page = Page.objects.get(title='Welcome to your new Wagtail site!')
    welcome_page.delete()
    

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0010_auto_20200804_0946'),
    ]

    operations = [
        migrations.RunPython(set_default_categories),
        migrations.RunPython(drop_welcome_page),
    ]
