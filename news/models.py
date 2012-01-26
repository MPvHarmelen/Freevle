from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class NewsMessage(models.Model):
    writer = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='publish', help_text=_('URL-friendly version of the title, can be left alone most of the time.'))
    publish = models.DateTimeField(auto_now_add=True)

    content = models.TextField(help_text=_('The news message.'))

    @models.permalink
    def get_absolute_url(self):
        return ('newsmessage-detail', (), {
                    'year': self.publish.year,
                    'month': self.publish.strftime('%m'),
                    'day': self.publish.strftime('%d'),
                    'slug': self.slug})


    class Meta:
        verbose_name = 'news message'
