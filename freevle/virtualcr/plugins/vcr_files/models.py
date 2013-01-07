from django.db import models
from django.core.exceptions import ValidationError
from freevle.virtualcr.plugins import PluginBase

# Create your models here.
class File(PluginBase):
    def _update_filename(self, filename):
        path = 'vcr_files/'
        new_file_name = self.slug
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension

    slug = models.SlugField(unique=True)
    publish = models.DateTimeField(auto_now_add=True)
    content = models.FileField(upload_to=_update_filename)

    @models.permalink
    def get_url(self):
        return ('virtualcr-file-detail', (), {'slug':self.slug,
                'vcr_slug':self.attachment.section.virtualcr.slug})
