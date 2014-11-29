from feedback import models
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _


class CourseTaskForm(ModelForm):
    """
    Generates a form from 'Task' model with fields related to a course.
    """
    opinion = forms.CharField(label='How do you feel about the course?',
    							widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}))
    suggestions = forms.CharField(label='What can we do to make the course better next year?',
    								widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}))

    class Meta:
        model = models.Task
        fields = ('opinion', 'suggestions',)
        labels = {
            'opinion': _('How do you feel about the course?'),
            'suggestions': _('What can we do to make the course better next year?'),
        }	