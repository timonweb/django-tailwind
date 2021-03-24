from django import forms
from django.db import models


class Colors(models.TextChoices):
    RED = "RED", "Red"
    GREEN = "GREEN", "Green"
    BLUE = "BLUE", "Blue"


class ExampleForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput)
    textarea = forms.CharField(widget=forms.Textarea)
    checkbox = forms.ChoiceField(widget=forms.CheckboxInput)
    file = forms.FileField()
    select = forms.ChoiceField(choices=Colors.choices)
    multiselect = forms.MultipleChoiceField(choices=Colors.choices)
    radios = forms.ChoiceField(choices=Colors.choices, widget=forms.RadioSelect)
    checkboxes = forms.MultipleChoiceField(
        choices=Colors.choices, widget=forms.CheckboxSelectMultiple
    )
