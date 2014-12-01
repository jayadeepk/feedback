from django.db import models
from django.contrib.auth.models import User, Group, Permission

class Course(models.Model):
    """
    Each course has many users and many tasks.
    """ 
    name = models.CharField(max_length=128)
    message = models.TextField()
    user = models.ManyToManyField(User, through='CourseUser')
    starting_date = models.DateField(null=True)
    ending_date = models.DateField(null=True)

    def __str__(self):
        return self.name

class CourseUser(models.Model):
    """
    Many to many relation between Course and User
    """
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    feedback_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Task(models.Model):
    """
    Stores the feedback content of student, on overall course.
    Every task corresponds to a single course and a single
    student.
    """
    student = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    courseuser = models.ForeignKey(CourseUser)
    opinion = models.TextField()
    suggestions = models.TextField()
    created_at = models.DateTimeField( auto_now_add = True, blank = True)

    def __str__(self):
        return self.student.username


class TaskProfessor(models.Model):
    """
    Feedback(task) on each professor
    """
    task = models.ForeignKey(Task)
    strong_points = models.TextField()
    weak_points = models.TextField()

class UserProfile(models.Model):
    """
    Collection of students and professors
    """
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    is_professor = models.BooleanField(default=False)

    class Meta:
        permissions = (('can_access_professor_views', 'Can access professor views'),
            ('can_access_student_views', 'Can access student views'),)
    def __str__(self):
        return self.user.username

#-----------------------------------
# class TaskProfessor(models.Model):
#     """
#     Many to many relation between Task and Professor
#     """
#     task = models.ForeignKey(Task)
#     user = models.ForeignKey(Professor)
#     # Fields of the feedback specific to user
#     text = models.TextField()