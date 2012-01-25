from django.db import models

# Create your models here.
class Letter(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='publish')
    publish = models.DateTimeField(auto_now_add=True)
#    content = FileField(Upload_to='files/')
