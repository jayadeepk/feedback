from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from feedback.models import Task, Course, Student, Professor, CourseStudent, CourseProfessor

class CourseStudentInline(admin.TabularInline):
    model = CourseStudent
    extra = 2

class CourseProfessorInline(admin.TabularInline):
    model = CourseProfessor
    extra = 2

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        CourseStudentInline,
        CourseProfessorInline,
    ]
    

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('student',)
    readonly_fields = ('course')

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False

class UserAdmin(DjangoUserAdmin):
    inlines = (StudentInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(CourseStudent)
admin.site.register(CourseProfessor)
admin.site.register(Task)



