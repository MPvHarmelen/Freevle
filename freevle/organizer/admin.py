from django.contrib import admin
from schoolr.organizer.models import Topic, Course, Lesson, HomeworkType, Homework
from schoolr.organizer.models import PeriodMeta

class PeriodMetaAdmin(admin.ModelAdmin):
    list_display = ('start_date','end_date','day_of_week')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('topic','teacher')

class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'day_of_week', 'period')

class HomeworkTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('homework_type', 'content',)


admin.site.register(PeriodMeta,PeriodMetaAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(HomeworkType,HomeworkTypeAdmin)
admin.site.register(Homework,HomeworkAdmin)