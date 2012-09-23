from freevle.virtualcr.plugins import Plugin
from django.db import models

# Create your models here.
class UrlsPlugin(Plugin):
    name = models.CharField(max_length=32)
    slug = models.SlugField()
    url = models.CharField(max_length=255)

    def get_list_data(self):
        return (self.url, self.name)
