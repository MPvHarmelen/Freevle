from django.contrib import admin
from freevle.news.models import NewsMessage

class NewsMessageAdmin(admin.ModelAdmin):
    date_hierarchy = 'publish'
    include = ('title', 'content',)
    exclude = ('writer',)
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'writer', 'publish', )

    def save_form(self, request, form, change):
        obj = super(NewsMessageAdmin, self).save_form(request, form, change)
        if not change:
            obj.writer = request.user
        return obj


admin.site.register(NewsMessage, NewsMessageAdmin)
