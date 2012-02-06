from django.db.models.signals import post_syncdb
from django.contrib.auth import models

def create_groups(sender, **kwargs):
    models.Group(name='Teachers').save()
    models.Group(name='Students').save()

post_syncdb.connect(create_groups, sender=models)

