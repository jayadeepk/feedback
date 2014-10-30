from feedback import models
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from django.forms import ModelForm
from django import forms

class TaskForm(ModelForm):
    """
    Generate form from 'Task' model
    """
    class Meta:
        model = models.Task
        fields = ('subject', 'description',)