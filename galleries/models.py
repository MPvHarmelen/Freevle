from django.db import models

# Create your models here.
class Gallery(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)
    date = models.DateField()
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        pass

class Photo(models.Model):
    
    def _update_filename(self, filename):
        path = self.gallery.slug + '/photos/'
        new_file_name = self.slug
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension
    
    title = models.CharField(max_length=32)
    slug = models.SlugField()
    gallery = models.ForeignKey(Gallery)
    date = models.DateField()
    content = models.ImageField(upload_to=_update_filename)
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        pass
