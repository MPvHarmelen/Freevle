import os
from django.db import models
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
    attachment = models.OneToOneField(Attachment, related_name='plugin_%(app_label)s')

    class Meta:
        abstract = True

def get_plugins():
    plugins = []
    for filename in os.listdir(ROOT_DIR + 'virtualcr/plugins/'):
        if filename[-3:] == '.py' or filename[-4:] == '.pyc':
            continue

        plugins.append([filename, 'freevle.virtualcr.plugins.' + filename])
    return plugins
