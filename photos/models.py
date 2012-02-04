from django.db import models

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=32)
    slug = models.SlugField()
    publish = models.DateField(auto_now_add=True)
    content = models.ImageField()
