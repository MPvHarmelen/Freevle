from django.db import models
from django.utils.translation import ugettext_lazy as _
from freevle.virtualcr.plugins import PluginBase

# Create your models here.
class Page(PluginBase):
    last_edit = models.DateTimeField(auto_now=True)
    slug = models.SlugField(
        unique=True,
        help_text=_('URL-friendly version of the title, '
                    'can be left alone most of the time.')
    )
    content = models.TextField(help_text=_('Content of the page.'))

    @models.permalink
    def get_url(self):
        return ('virtualcr-page-detail', (), {'slug':self.slug,
                'vcr_slug':self.attachment.section.virtualcr.slug})


