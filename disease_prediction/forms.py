from django import forms
from .models import *

class disease_form(forms.ModelForm):
    class Meta:
        model = Post_image
        fields = ['image',]