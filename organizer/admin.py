from django.contrib import admin
from cygy.organizer.models import Topic, Lesson, TimeTable, HomeworkType, Homework

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('topic', 'teacher',)

class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_monday',)

class HomeworkTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('type', 'content',)


admin.site.register(Topic,TopicAdmin)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(TimeTable,TimeTableAdmin)
admin.site.register(HomeworkType,HomeworkTypeAdmin)
admin.site.register(Homework,HomeworkAdmin)
