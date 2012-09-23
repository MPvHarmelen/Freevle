from django.contrib import admin
from freevle.organizer.models import *

class PeriodMetaAdmin(admin.ModelAdmin):
    list_display = ('start_date','end_date','day_of_week')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('topic','teacher')

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'day_of_week', 'period')

class HomeworkTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('homework_type', 'content',)

class ChangedLessonAdmin(admin.ModelAdmin):
    pass
class CancelledTeacherAdmin(admin.ModelAdmin):
    pass
class CancelledClassroomAdmin(admin.ModelAdmin):
    pass

admin.site.register(PeriodMeta,PeriodMetaAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Classroom,ClassroomAdmin)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(HomeworkType,HomeworkTypeAdmin)
admin.site.register(Homework,HomeworkAdmin)
admin.site.register(ChangedLesson,ChangedLessonAdmin)
admin.site.register(CancelledTeacher,CancelledTeacherAdmin)
admin.site.register(CancelledClassroom,CancelledClassroomAdmin)