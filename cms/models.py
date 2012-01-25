from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Page(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True)
    last_edit = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text=_('URL-friendly version of the title, can be left alone most of the time.'))
    content = models.TextField(help_text=_('Content of the page.'))
