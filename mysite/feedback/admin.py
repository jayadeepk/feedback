from django.contrib import admin
from feedback.models import Task, Course, User, CourseUser

class CourseUserInline(admin.TabularInline):
    model = CourseUser
    extra = 2

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        CourseUserInline,
    ]
    

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('student',)
    readonly_fields = ('course')

admin.site.register(Course, CourseAdmin)
admin.site.register(Task)
admin.site.register(CourseUser)