from django.contrib import admin
from cygy.letters.models import Letter

class LetterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', )


admin.site.register(Letter,LetterAdmin)
