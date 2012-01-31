from django.db import models
import os.path

# Create your models here.
class Letter(models.Model):
    def update_filename(instance, filename):
        path = "letters/"
        format = instance.slug
        return path.join(path, format)
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='publish')
    publish = models.DateTimeField(auto_now_add=True)
    content = models.FileField(upload_to=update_filename)
