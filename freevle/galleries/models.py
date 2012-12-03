from django.db import models

# Create your models here.
class Gallery(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    date = models.DateField()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('gallery-detail', (), {'slug':self.slug})

class Photo(models.Model):

    def _upload_to(self, filename):
        path = 'galleries/' + self.gallery.slug + '/'
        new_file_name = self.slug
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension

    title = models.CharField(max_length=32)
    slug = models.SlugField()
    gallery = models.ForeignKey(Gallery)
    date = models.DateField()
    image = models.ImageField(upload_to=_upload_to)

    class Meta:
        unique_together = ('gallery','slug')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        pass
