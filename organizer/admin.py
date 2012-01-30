from django.contrib import admin
from cygy.organizer.models import Topic, Lesson, Timetable, HomeworkType, Homework

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('topic', 'teacher',)

class TimetableAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_monday',)

class HomeworkTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('type', 'content',)


admin.site.register(Topic,TopicAdmin)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(Timetable,TimetableAdmin)
admin.site.register(HomeworkType,HomeworkTypeAdmin)
admin.site.register(Homework,HomeworkAdmin)
