from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NieuwsBericht(models.Model):
    schrijver = models.ForeignKey(User)
    titel = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='publiceer', help_text='URL-vriendelijke versie van de titel, kan meestal met rust gelaten worden.')
    publiceer = models.DateTimeField(auto_now_add=True)

    inhoud = models.TextField(help_text='Het nieuwsbericht.')
    korte_inhoud = models.TextField(help_text='Korte samenvatting van het nieuwsbericht.')

#    def get_absolute_url(self):
#        return '/nieuws/{}/{}/{}/{}/'.format(
#                    self.publiceer.year, self.publiceer.strftime('%m'), self.publiceer.strftime('%d'), self.slug)

    @models.permalink
    def get_absolute_url(self):
        return ('nieuwsbericht-detail', (), {
                    'year': self.publiceer.year,
                    'month': self.publiceer.strftime('%m'),
                    'day': self.publiceer.strftime('%d'),
                    'slug': self.slug})


    class Meta:
        verbose_name = 'nieuwsbericht'
        verbose_name_plural = 'nieuwsberichten'

