import os
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from freevle.settings import ROOT_DIR
from freevle.virtualcr.models import Attachment

# Baseclass for VirtualCR plugins
class PluginBase(models.Model):
    def _get_icon_name(self, filename):
        return filename

    def _update_filename(self, filename):
        path = 'virtualcr/plugins/icons/'
        new_file_name = self._get_icon_name(filename)
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension

    icon = models.ImageField(upload_to=_update_filename)
    title = models.CharField(max_length=32)
    attachment = models.OneToOneField(Attachment, related_name='plugin_%(app_label)s')

    def get_url(self):
        raise ImproperlyConfigured("You must write youre own `get_url`")

    def get_list_data(self):
        return (self.icon, self.get_url(), self.title)

    class Meta:
        abstract = True

def get_plugin_urls():
    plugins = []
    plugin_root = ROOT_DIR + 'virtualcr/plugins/'
    for filename in os.listdir(plugin_root):
        if not os.path.isdir(plugin_root + '/' + filename):
            continue
        module_name = 'freevle.virtualcr.plugins.' + filename
        module = __import__(module_name, fromlist=['urls']).urls
        try:
            url_root = module.get_url_root()
        except AttributeError as e:
            print e
            print module_name
            print dir(module)
            url_root = None
        if url_root in (None, '', '/'):
            url_root = filename + '/'
        plugins.append((url_root, module_name))
    return plugins
