from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class VirtualClassroom(models.Model):
    def _update_filename(self, filename):
        path = 'virtualcr/'
        new_file_name = self.slug
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension

    name = models.CharField(max_length=18)
    slug = models.SlugField(unique=True)
    header = models.ImageField(upload_to=_update_filename)
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name

class Section(models.Model):
    virtualcr = models.ForeignKey(VirtualClassroom)
    content = models.TextField(help_text=_('Content of the page.'))

class Attachment(models.Model):
    def _get_icon_name(self, filename):
        return filename

    def _update_filename(self, filename):
        path = 'virtualcr/plugins/icons/'
        new_file_name = self._get_icon_name(filename)
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension

    section = models.ForeignKey(Section)
    order = models.IntegerField()
    icon = models.ImageField(upload_to=_update_filename)
