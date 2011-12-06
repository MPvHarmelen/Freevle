from django.db import models

# Create your models here.
class Page(models.Model):
    last_edit = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text='URL-friendly version of the title, can be left alone most of the time.')
    content = models.TextField(help_text='This is the content.')
    
