import os
from django.db import models

from freevle.settings import ROOT_DIR

# Baseclass for VirtualCR plugins
class Plugin(models.Model):
    def _get_icon_name(self, filename):
        return filename

    def _update_filename(self, filename):
        path = 'virtualcr/plugins/icons/'
        new_file_name = self._get_icon_name(filename)
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension

    icon = models.ImageField(upload_to=_update_filename)

def get_plugins():
    plugins = []
    for filename in os.listdir(ROOT_DIR + 'virtualcr/plugins/'):
        if filename[-3:] == '.py' or filename[-4:] == '.pyc':
            continue

        plugins.append([filename, 'freevle.virtualcr.plugins.' + filename])
    return plugins
