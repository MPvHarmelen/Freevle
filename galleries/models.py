from django.db import models

# Create your models here.
class Photo(models.Model):
    
    def update_filename(instance, filename):
        path = 'photos/'
        new_file_name = instance.slug
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension
    
    title = models.CharField(max_length=32)
    slug = models.SlugField()
    publish = models.DateField(auto_now_add=True)
    content = models.ImageField(upload_to=update_filename)
