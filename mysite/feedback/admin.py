from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from feedback.models import Task, Course, User, CourseUser, UserProfile

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

class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserAdmin(DjangoUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseUser)

admin.site.register(Task)

