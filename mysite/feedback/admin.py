from django.contrib import admin
from feedback.models import Task, Course, Professor, CourseProfessor

class CourseProfessorInline(admin.TabularInline):

    model = CourseProfessor
    extra = 2

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        CourseProfessorInline,
    ]
    

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('student',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Task)
admin.site.register(Professor)
# admin.site.register(TemplateGroup)