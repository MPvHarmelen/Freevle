from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Page(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True,
                               limit_choices_to={'parent':None})
    last_edit = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=18)
    slug = models.SlugField(
#        unique=True,
        help_text=_('URL-friendly version of the title,\
                    can be left alone most of the time.')
    )
    content = models.TextField(help_text=_('Content of the page.'))
    
    def save(self, *args, **kwargs):
        sibling_slugs = [sibling.slug for sibling in Page.objects.filter(parent=self.parent)]
        if self.slug in sibling_slugs:
            raise IntegrityError(_("There's already a page with this parent and slug"))
        else:
            super(Page, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        if self.parent:
            return ('cms-child-detail', (), {
                'parent':self.parent.slug,
                'slug':self.slug,
            })
        else:
            return ('cms-parent-detail', (), {
                'slug':self.slug,
            })
    
    def __unicode__(self):
        return self.title

