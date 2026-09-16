from django import forms

from .models import StoryElement

class StoryElementAdminForm(forms.ModelForm):
    class Meta:
        model = StoryElement
        fields = "__all__"
        widgets = {
            "variant": forms.TextInput(attrs={"type": "color"}),
            "background_color": forms.TextInput(attrs={"type": "color"}),
        }