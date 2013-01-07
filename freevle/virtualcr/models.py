from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

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

    @models.permalink
    def get_url(self):
        return ('virtualcr-detail', (), {'vcr_slug':self.slug})

    def __unicode__(self):
        return self.name

class Section(models.Model):
    virtualcr = models.ForeignKey(VirtualClassroom)
    content = models.TextField(help_text=_('Content of the page.'))

class Attachment(models.Model):
    section = models.ForeignKey(Section)
    order = models.IntegerField()

    def __unicode__(self):
        return '{}.{}'.format(self.section.virtualcr, self.order)

    def get_plugin(self):
        plugin_list = [x for x in dir(self) if x[:7] == 'plugin_']
        for related_name in plugin_list:
            try:
                plugin = self.__getattribute__(related_name)
                return plugin
            except ObjectDoesNotExist:
                pass

        raise AttributeError('No plugin found for {}'.format(self))
