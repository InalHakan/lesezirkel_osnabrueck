from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from .models import Contact, EventRegistration, Event, News, Gallery
from datetime import datetime


class GermanDateInput(forms.DateInput):
    """Custom Date input widget that accepts German date format (DD.MM.YYYY or DD/MM/YYYY)"""
    
    def __init__(self, attrs=None, format=None):
        default_attrs = {
            'placeholder': 'TT.MM.JJJJ',
            'class': 'vDateField',
            'type': 'text',  # Use text instead of date for manual entry
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, format='%d.%m.%Y')
    
    def format_value(self, value):
        """Format the value for display in German format"""
        if value:
            if isinstance(value, str):
                try:
                    # Try parsing ISO format first
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                except ValueError:
                    try:
                        # Try German format
                        value = datetime.strptime(value, '%d.%m.%Y').date()
                    except ValueError:
                        return value
            if hasattr(value, 'strftime'):
                return value.strftime('%d.%m.%Y')
        return value


class GermanTimeInput(forms.TimeInput):
    """Custom Time input widget that accepts German time format (HH:MM)"""
    
    def __init__(self, attrs=None, format=None):
        default_attrs = {
            'placeholder': 'HH:MM',
            'class': 'vTimeField',
            'type': 'text',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, format='%H:%M')
    
    def format_value(self, value):
        """Format the value for display as HH:MM (no seconds)"""
        if value:
            if isinstance(value, str):
                try:
                    # Parse and reformat to remove seconds
                    value = datetime.strptime(value, '%H:%M:%S').time()
                except ValueError:
                    try:
                        value = datetime.strptime(value, '%H:%M').time()
                    except ValueError:
                        return value
            if hasattr(value, 'strftime'):
                return value.strftime('%H:%M')
        return value


class GermanSplitDateTimeWidget(forms.MultiWidget):
    """Split DateTime widget with German date format and time without seconds"""
    
    def __init__(self, attrs=None):
        widgets = [
            GermanDateInput(),
            GermanTimeInput(),
        ]
        super().__init__(widgets, attrs)
    
    def decompress(self, value):
        if value:
            if isinstance(value, str):
                try:
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    try:
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M')
                    except ValueError:
                        return [None, None]
            return [value.date(), value.time()]
        return [None, None]


class GermanSplitDateTimeField(forms.MultiValueField):
    """Field for split date and time with German format support"""
    widget = GermanSplitDateTimeWidget
    
    def __init__(self, *args, **kwargs):
        fields = [
            forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y', '%Y-%m-%d']),
            forms.TimeField(input_formats=['%H:%M', '%H:%M:%S']),
        ]
        super().__init__(fields, *args, **kwargs)
    
    def compress(self, data_list):
        if data_list:
            date_value = data_list[0]
            time_value = data_list[1]
            if date_value and time_value:
                return datetime.combine(date_value, time_value)
        return None


class EventAdminForm(forms.ModelForm):
    """Custom admin form for Event with German date format support and default location"""
    
    date = GermanSplitDateTimeField(
        label='Datum',
        help_text='Format: TT.MM.JJJJ HH:MM (z.B. 25.12.2024 15:30)'
    )
    
    class Meta:
        model = Event
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default location to "Vor Ort" for new events
        if not self.instance.pk:  # Only for new instances
            self.fields['location'].initial = 'Vor Ort'


class NewsAdminForm(forms.ModelForm):
    """Custom admin form for News with German date format support"""
    
    published_date = GermanSplitDateTimeField(
        label='Veröffentlichungsdatum',
        help_text='Format: TT.MM.JJJJ HH:MM (z.B. 25.12.2024 15:30)'
    )
    
    class Meta:
        model = News
        fields = '__all__'


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


class MultipleFileInput(forms.FileInput):
    """Custom widget that allows multiple file selection"""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Custom field that handles multiple files"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={
            'accept': 'image/*',
            'class': 'vTextField',
        }))
        super().__init__(*args, **kwargs)
    
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class GalleryBulkUploadForm(forms.Form):
    """Form for bulk uploading multiple images to Gallery"""
    images = MultipleFileField(
        label='Bilder auswählen',
        help_text='Sie können mehrere Bilder gleichzeitig auswählen (Strg/Cmd + Klick)'
    )
    event = forms.ModelChoiceField(
        queryset=Event.objects.all().order_by('-date'),
        required=False,
        label='Veranstaltung',
        help_text='Optional: Verknüpfen Sie die Bilder mit einer Veranstaltung'
    )
    title_prefix = forms.CharField(
        max_length=100,
        required=False,
        label='Titel-Präfix',
        help_text='Optional: Präfix für alle Bildtitel (z.B. "Sommerfest 2024 - ")'
    )


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