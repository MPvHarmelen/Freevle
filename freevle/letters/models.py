from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from freevle.custom.validators import validate_pdf

# Create your models here.
class Letter(models.Model):

    def _update_filename(self, filename):
        path = 'letters/'
        new_file_name = self.slug
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    publish = models.DateTimeField(auto_now_add=True)
    content = models.FileField(upload_to=_update_filename,
                               validators=[validate_pdf])

    @models.permalink
    def get_absolute_url(self):
        return ('django.views.static.serve', '', {'path':self.content.url})
