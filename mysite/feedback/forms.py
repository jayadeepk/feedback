from feedback import models
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from captcha.fields import CaptchaField

class TaskForm(ModelForm):
    """
    Generates a form from 'Task' model with fields related to a course.
    """
    model = models.Task
    rating1 = forms.IntegerField(label='', initial=2, widget = forms.HiddenInput())
    rating2 = forms.IntegerField(label='', initial=2, widget = forms.HiddenInput())
    rating3 = forms.IntegerField(label='', initial=2, widget = forms.HiddenInput())
    opinion = forms.CharField(label='How do you feel about the course?',
                                widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}))
    suggestions = forms.CharField(label='What can we do to make the course better next year?',
                                    widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}))

    class Meta:
        model = models.Task
        fields = ('rating1', 'rating2', 'rating3', 'opinion', 'suggestions',)
        labels = {
            'opinion': _('How do you feel about the course?'),
            'suggestions': _('What can we do to make the course better next year?'),
        }
class TaskProfessorForm(ModelForm):
    """
    Generates a form from 'Task' model with fields related to a course.
    """
    model = models.Task
    rating1 = forms.IntegerField(label='', initial=2, widget = forms.HiddenInput())
    rating2 = forms.IntegerField(label='', initial=2, widget = forms.HiddenInput())
    rating3 = forms.IntegerField(label='', initial=2, widget = forms.HiddenInput())
    strong_points = forms.CharField(label='Strong points about the professor:',
                                widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}))
    weak_points = forms.CharField(label='Weak points about the professor:',
                                    widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}))
    class Meta:
        model = models.TaskProfessor
        fields = ('rating1', 'rating2', 'rating3', 'strong_points', 'weak_points',)


class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()