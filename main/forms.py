from django import forms
from .models import Contact, EventRegistration


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


class EventRegistrationAdminForm(forms.ModelForm):
    """Custom admin form for EventRegistration with duplicate detection"""
    
    class Meta:
        model = EventRegistration
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        event = cleaned_data.get('event')
        email = cleaned_data.get('email')
        
        if event and email:
            # Check if this email is already registered for this event
            # Exclude current instance if editing (not creating)
            existing = EventRegistration.objects.filter(event=event, email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError(
                    f'Die E-Mail-Adresse "{email}" ist bereits für die Veranstaltung '
                    f'"{event.title}" registriert. Bitte verwenden Sie eine andere E-Mail-Adresse '
                    f'oder bearbeiten Sie die bestehende Anmeldung.'
                )
        
        return cleaned_data