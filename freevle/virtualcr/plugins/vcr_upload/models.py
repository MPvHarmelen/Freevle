from django.db import models
from django.contrib.auth.models import User, Group
from freevle.virtualcr.plugins import PluginBase

# Create your models here.
class Assignment(PluginBase):
    slug = models.SlugField(unique=True)
    publish = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    groups = models.ManyToManyField(Group)
    due_date = models.DateTimeField(blank=True, null=True)
    drafts = models.BooleanField(default=False)

    @models.permalink
    def get_url(self):
        return ('virtualcr-upload-detail', (), {'slug':self.slug,
                'vcr_slug':self.attachment.section.virtualcr.slug})

class File(models.Model):
    def _update_filename(self, filename):
        path = 'vcr_upload/' + self.assignment.slug
        new_file_name = self.slug
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension

    author = models.OneToOneField(User)
    assignment = models.ManyToManyField(Assignment)
    publish = models.DateTimeField(auto_now_add=True)
    final_version = models.BooleanField()

    content = models.FileField(upload_to=_update_filename)
