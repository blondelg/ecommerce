from django.urls import reverse

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem

@hooks.register('register_admin_menu_item')
def register_dashboard_menu_item():
  return MenuItem('Dashboard', '/dashboard', classnames='icon icon-cog', order=10000)
  
@hooks.register('register_settings_menu_item')
def register_frank_menu_item():
  return MenuItem('Marketplace Config', '/dashboard', classnames='icon icon-cog', order=10000)
