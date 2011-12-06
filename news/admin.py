from django.contrib import admin
from cygy.nieuws.models import NieuwsBericht

class NieuwsBerichtAdmin(admin.ModelAdmin):
    date_hierarchy = 'publiceer'
    include = ('titel', 'inhoud',)
    exclude = ('schrijver',)
    prepopulated_fields = {"slug": ("titel",)}

    def save_form(self, request, form, change):
        obj = super(NieuwsBerichtAdmin, self).save_form(request, form, change)
        if not change:
            obj.schrijver = request.user
        return obj


admin.site.register(NieuwsBericht, NieuwsBerichtAdmin)
