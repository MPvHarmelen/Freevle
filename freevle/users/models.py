from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    def update_filename(self, filename):
        path = 'avatars/'
        new_file_name = self.user.username
        extension = filename.split('.')[-1]
        return path + new_file_name + '.' + extension

    user = models.OneToOneField(User)

    designation = models.CharField(max_length=32, blank=True)
    avatar = models.ImageField(upload_to=update_filename, blank=True)

    def __unicode__(self):
        return '{}: <{}>'.format(self.designation, self.user.username)

    def get_display_name(self):
        '''
        Returns the (sort of) longest possible name smaller than max_length
        '''
        full_name = self.user.get_full_name()
        if full_name == '':
            display_name = self.user.username
        else:
            display_name = full_name
        
        return display_name


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User,
        dispatch_uid='users-profilecreation-signal')
