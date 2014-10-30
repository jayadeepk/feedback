from django.db import models
from django.contrib.auth.models import User, Group, Permission


class Professor(User):
    """
    Professor is a special User.
    He can be allotted to many courses.
    """
    is_professor = models.BooleanField( default = True)
    pass

class Course(models.Model):
    """
    Each course has many professors and many tasks.
    """
    name = models.CharField(max_length=128)
    professor = models.ManyToManyField(Professor, through='CourseProfessor')

    def __str__(self):
        return self.name

class Task(models.Model):
    """
    Stores the feedback content of student, on overall course.
    Every task corresponds to a single course and a single
    student.
    """
    student = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    subject = models.CharField( max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField( auto_now_add = True, blank = True)

    def __str__(self):
        return self.subject

class CourseProfessor(models.Model):
    """
    Many to many relation between Course and Professor
    """
    course = models.ForeignKey(Course)
    professor = models.ForeignKey(Professor)

class TaskProfessor(models.Model):
    """
    Many to many relation between Task and Professor
    """
    task = models.ForeignKey(Task)
    professor = models.ForeignKey(Professor)
    # Fields of the feedback specific to professor
    text = models.TextField()