from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    # Honeypot field (renamed to avoid autofill by extensions)
    hp_field = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'autocomplete': 'off', 'aria-hidden': 'true'})
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']  # honeypot excluded
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': ''}),
        }

    def clean_hp_field(self):
        value = self.cleaned_data.get('hp_field')
        if value:
            raise forms.ValidationError("Spam erkannt")
        return value