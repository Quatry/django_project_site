from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import TextInput
from django.utils.dateparse import parse_duration
from django.utils.translation import gettext_lazy as _

from .models import Project, Participant, ProjectUpdate, ProjectEvent

User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User


class ProjectCreationForm(forms.ModelForm):
    class Meta():
        model = Project
        fields = ['name', 'info']


class ParticipantAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['participant'].empty_label = "Участник не выбран"

    class Meta():
        model = Participant
        fields = ['participant']


class ProjectEditForm(forms.ModelForm):
    class Meta():
        model = Project
        fields = ['name', 'info']


class ProjectUpdateAddForm(forms.ModelForm):
    class Meta():
        model = ProjectUpdate
        fields = ['update']


class ProjectEventAddForm(forms.ModelForm):
    class Meta():
        model = ProjectEvent
        fields = ['info', 'date', 'duration']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'info': forms.Textarea(attrs={
                'cols': 80,
                'rows': 2,
            }),
        }
