from django.urls import path
from django.views.generic import FormView

from theme.forms import ExampleForm

urlpatterns = [
    path("forms/", FormView.as_view(template_name="forms.html", form_class=ExampleForm))
]
