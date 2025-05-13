from django import forms

from myapp.models import Flight


class AddFlightForm(forms.ModelForm):
    #za da zememe flight forma kako bi bila, odime so meta klasa
    class Meta:
        model = Flight
        exclude = ("user_that_created",)