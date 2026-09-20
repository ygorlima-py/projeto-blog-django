from django import forms

from .models import StoryElement, StorySlide

class StoryElementAdminForm(forms.ModelForm):
    use_background_color = forms.BooleanField(
        required=False,
        label="Usar cor de fundo",
    )
    
    class Meta:
        model = StoryElement
        fields = "__all__"
        widgets = {
            "variant": forms.TextInput(attrs={"type": "color"}),
            "background_color": forms.TextInput(attrs={"type": "color"}),
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["use_background_color"].initial = bool(
            self.instance.background_color
        )
        
    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get("use_background_color"):
            cleaned_data["background_color"] = ""

        return cleaned_data

class StorySlideAdminForm(forms.ModelForm):
    class Meta:
        model = StorySlide
        fields = "__all__"
        widgets = {
            "background_color": forms.TextInput(
                attrs={"type": "color"}
            ),
        }