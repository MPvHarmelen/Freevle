from django.db import models

class Album(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    creation_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('album-detail', (), {'slug':self.slug})

class Photo(models.Model):

    def _upload_to(self, filename):
        path = 'photos/' + self.album.slug + '/'
        new_file_name = self.slug
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension

    title = models.CharField(max_length=32)
    slug = models.SlugField()
    album = models.ForeignKey(Album)
    upload_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to=_upload_to)

    class Meta:
        unique_together = ('album','slug')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        pass
