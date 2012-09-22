from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class VirtualClassroom(models.Model):
    def _update_filename(self, filename):
        path = 'classes/'
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
