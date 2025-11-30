from django.db import models
from django.utils import timezone
from django.urls import reverse
import os

# Event category / color choices mapped to calendar legend colors
EVENT_CATEGORY_CHOICES = [
    ('primary', 'Kulturelle Veranstaltungen'),
    ('secondary', 'Workshops & Seminare'),
    ('success', 'Integrationsprojekte'),
    ('accent', 'Sprachkurse'),
    ('purple', 'Begegnungen'),
    ('orange', 'Feste & Feiern'),
]

class Event(models.Model):
    """Event model"""
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    date = models.DateTimeField(verbose_name="Datum")
    location = models.CharField(max_length=200, verbose_name="Ort")
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="Bild")
    is_featured = models.BooleanField(default=False, verbose_name="Hervorgehoben")
    is_public = models.BooleanField(default=True, verbose_name="Öffentlich zugänglich", 
                                   help_text="Wenn aktiviert, ist die Veranstaltung für alle offen und benötigt Datenschutzerklärung")
    registration_required = models.BooleanField(default=False, verbose_name="Anmeldung erforderlich",
                                              help_text="Wenn aktiviert, wird ein Anmeldeformular angezeigt")
    invitation_only = models.BooleanField(default=False, verbose_name="Nur mit Einladung",
                                         help_text="Wenn aktiviert, ist ein Einladungscode für die Anmeldung erforderlich")
    max_participants = models.PositiveIntegerField(blank=True, null=True, verbose_name="Maximale Teilnehmerzahl",
                                                 help_text="Leer lassen für unbegrenzte Teilnehmer")
    category = models.CharField(
        max_length=20,
        choices=EVENT_CATEGORY_CHOICES,
        default='primary',
        verbose_name="Kategorie",
        help_text="Wählen Sie die Kategorie zur Farbkodierung im Kalender"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Veranstaltung"
        verbose_name_plural = "Veranstaltungen"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

class News(models.Model):
    """News model"""
    title = models.CharField(max_length=200, verbose_name="Titel")
    content = models.TextField(verbose_name="Inhalt")
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Bild")
    is_featured = models.BooleanField(default=False, verbose_name="Hervorgehoben")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Veröffentlichungsdatum")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "Nachricht"
        verbose_name_plural = "Nachrichten"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})

class TeamMember(models.Model):
    """Team member model"""
    name = models.CharField(max_length=100, verbose_name="Name")
    position = models.CharField(max_length=100, verbose_name="Position")
    bio = models.TextField(blank=True, verbose_name="Biografie")
    image = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name="Bild")
    email = models.EmailField(blank=True, verbose_name="E-Mail")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    order = models.PositiveIntegerField(default=0, verbose_name="Reihenfolge")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Teammitglied"
        verbose_name_plural = "Teammitglieder"

    def __str__(self):
        return f"{self.name} - {self.position}"

class Gallery(models.Model):
    """Gallery model"""
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    image = models.ImageField(upload_to='gallery/', verbose_name="Bild")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Veranstaltung")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Galerie"
        verbose_name_plural = "Galerie"

    def __str__(self):
        return self.title

class Contact(models.Model):
    """Contact model"""
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="E-Mail")
    subject = models.CharField(max_length=200, verbose_name="Betreff")
    message = models.TextField(verbose_name="Nachricht")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="Gelesen")
    is_answered = models.BooleanField(default=False, verbose_name="Beantwortet")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kontaktnachricht"
        verbose_name_plural = "Kontaktnachrichten"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class EventRegistration(models.Model):
    """Event registration model"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Veranstaltung", related_name="registrations")
    first_name = models.CharField(max_length=100, verbose_name="Vorname")
    last_name = models.CharField(max_length=100, verbose_name="Nachname")
    email = models.EmailField(verbose_name="E-Mail")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    message = models.TextField(blank=True, verbose_name="Nachricht/Anmerkungen")
    privacy_consent = models.BooleanField(default=False, verbose_name="Datenschutz zugestimmt", 
                                        help_text="Einverständnis zur Datenschutzerklärung")
    newsletter_consent = models.BooleanField(default=False, verbose_name="Newsletter-Anmeldung",
                                           help_text="Möchte Newsletter erhalten")
    photo_consent = models.BooleanField(default=False, verbose_name="Fotoerlaubnis",
                                      help_text="Einverständnis zur Anfertigung und Veröffentlichung von Fotos")
    invitation_code = models.ForeignKey('InvitationCode', on_delete=models.SET_NULL, blank=True, null=True,
                                       verbose_name="Einladungscode", related_name="registrations",
                                       help_text="Falls mit Einladungscode angemeldet")
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False, verbose_name="Bestätigt")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Veranstaltungsanmeldung"
        verbose_name_plural = "Veranstaltungsanmeldungen"
        unique_together = ['event', 'email']  # Prevent duplicate registrations
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event.title}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class InvitationCode(models.Model):
    """Invitation code model for exclusive event invitations"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Veranstaltung", related_name="invitation_codes")
    code = models.CharField(max_length=50, unique=True, verbose_name="Einladungscode",
                          help_text="Eindeutiger Code für diese Einladung (nur Großbuchstaben A-Z, Zahlen 0-9 und Bindestrich)")
    invited_name = models.CharField(max_length=200, blank=True, verbose_name="Name des Eingeladenen",
                                   help_text="Name der eingeladenen Person (optional, nur zur Erinnerung)")
    max_uses = models.PositiveIntegerField(default=1, verbose_name="Maximale Nutzungen",
                                          help_text="Wie oft dieser Code verwendet werden kann")
    times_used = models.PositiveIntegerField(default=0, verbose_name="Bereits verwendet")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    expires_at = models.DateTimeField(blank=True, null=True, verbose_name="Gültig bis",
                                     help_text="Leer lassen für unbegrenzte Gültigkeit")
    notes = models.TextField(blank=True, verbose_name="Notizen",
                            help_text="Interne Notizen zu dieser Einladung")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Einladungscode"
        verbose_name_plural = "Einladungscodes"
    
    def __str__(self):
        return f"{self.code} - {self.event.title}"
    
    def clean(self):
        """Validate invitation code format"""
        import re
        from django.core.exceptions import ValidationError
        
        if self.code:
            # Convert to uppercase
            self.code = self.code.upper().strip()
            
            # Validate format: only A-Z, 0-9, and hyphen
            if not re.match(r'^[A-Z0-9-]+$', self.code):
                raise ValidationError({
                    'code': 'Einladungscode darf nur Großbuchstaben (A-Z), Zahlen (0-9) und Bindestriche (-) enthalten.'
                })
            
            # Minimum length check
            if len(self.code) < 3:
                raise ValidationError({
                    'code': 'Einladungscode muss mindestens 3 Zeichen lang sein.'
                })
            
            # Check uniqueness (excluding current instance if editing)
            existing = InvitationCode.objects.filter(code=self.code)
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            
            if existing.exists():
                raise ValidationError({
                    'code': f'Der Einladungscode "{self.code}" existiert bereits. Bitte wählen Sie einen anderen Code.'
                })
    
    def save(self, *args, **kwargs):
        # Always convert to uppercase before saving
        if self.code:
            self.code = self.code.upper().strip()
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Check if invitation code is still valid"""
        if not self.is_active:
            return False, "Dieser Einladungscode wurde deaktiviert."
        
        if self.times_used >= self.max_uses:
            return False, "Dieser Einladungscode wurde bereits vollständig verwendet."
        
        if self.expires_at and timezone.now() > self.expires_at:
            return False, "Dieser Einladungscode ist abgelaufen."
        
        # Check if event is in the past
        if self.event.date < timezone.now():
            return False, "Diese Veranstaltung hat bereits stattgefunden."
        
        return True, "Code ist gültig."
    
    def use_code(self):
        """Increment usage counter"""
        self.times_used += 1
        self.save()


class Document(models.Model):
    """Document model for downloadable files"""
    CATEGORY_CHOICES = [
        ('general', 'Alle Dokumente'),
        ('forms', 'Formulare'),
        ('brochures', 'Broschüren'),
        ('reports', 'Berichte'),
        ('certificates', 'Zertifikate'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general',
        verbose_name="Kategorie"
    )
    file = models.FileField(
        upload_to='documents/',
        verbose_name="Datei",
        help_text="Unterstützte Formate: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, RTF"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Hervorgehoben")
    is_public = models.BooleanField(default=True, verbose_name="Öffentlich zugänglich")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Anzahl Downloads")
    file_size = models.PositiveIntegerField(blank=True, null=True, verbose_name="Dateigröße (Bytes)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Dokument"
        verbose_name_plural = "Dokumente"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    @property
    def file_extension(self):
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ''

    @property
    def formatted_file_size(self):
        if not self.file_size:
            return "Unknown"
        
        # Convert bytes to human readable format
        size = self.file_size  # Use local variable instead of modifying instance variable
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def get_download_url(self):
        return reverse('document_download', kwargs={'pk': self.pk})


class Certificate(models.Model):
    """Certificate model for downloadable participant certificates"""
    first_name = models.CharField(max_length=100, verbose_name="Vorname")
    last_name = models.CharField(max_length=100, verbose_name="Nachname")
    participant_number = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Teilnehmernummer",
        help_text="Eindeutige Nummer für den Teilnehmer"
    )
    event_title = models.CharField(max_length=200, verbose_name="Veranstaltungstitel")
    completion_date = models.DateField(verbose_name="Abschlussdatum")
    certificate_file = models.FileField(
        upload_to='certificates/',
        verbose_name="Zertifikat",
        help_text="PDF-Datei des Zertifikats"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Zertifikat"
        verbose_name_plural = "Zertifikate"
        ordering = ['-completion_date', 'last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event_title} ({self.participant_number})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_download_url(self):
        return reverse('certificate_download', kwargs={'pk': self.pk})


class Announcement(models.Model):
    """Pop-up announcement model for homepage"""
    ANNOUNCEMENT_TYPES = [
        ('event', 'Wichtiges Ereignis'),
        ('invitation', 'Einladung'),
        ('funeral', 'Traueranzeige'),
        ('news', 'Wichtige Nachricht'),
        ('warning', 'Warnung'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titel")
    message = models.TextField(verbose_name="Nachricht", help_text="Haupttext der Ankündigung")
    announcement_type = models.CharField(
        max_length=20, 
        choices=ANNOUNCEMENT_TYPES, 
        default='news',
        verbose_name="Typ"
    )
    image = models.ImageField(
        upload_to='announcements/', 
        blank=True, 
        null=True, 
        verbose_name="Bild",
        help_text="Optionales Bild für die Ankündigung"
    )
    background_music = models.FileField(
        upload_to='announcements/audio/', 
        blank=True, 
        null=True,
        verbose_name="Hintergrundmusik",
        help_text="Optionale Audiodatei (MP3, WAV)"
    )
    
    # Display settings
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    start_date = models.DateTimeField(verbose_name="Startdatum", help_text="Ab wann soll die Ankündigung angezeigt werden?")
    end_date = models.DateTimeField(verbose_name="Enddatum", help_text="Bis wann soll die Ankündigung angezeigt werden?")
    auto_close_seconds = models.PositiveIntegerField(
        default=10, 
        verbose_name="Automatisches Schließen (Sekunden)",
        help_text="Nach wie vielen Sekunden soll das Pop-up automatisch schließen? (0 = nie)"
    )
    
    # Styling
    background_color = models.CharField(
        max_length=7, 
        default='#ffffff',
        verbose_name="Hintergrundfarbe",
        help_text="Hex-Farbe (z.B. #ffffff)"
    )
    text_color = models.CharField(
        max_length=7,
        default='#000000', 
        verbose_name="Textfarbe",
        help_text="Hex-Farbe (z.B. #000000)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ankündigung"
        verbose_name_plural = "Ankündigungen"
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} ({self.get_announcement_type_display()})"
    
    def is_currently_active(self):
        """Check if announcement should be shown now"""
        now = timezone.now()
        return (
            self.is_active and 
            self.start_date <= now <= self.end_date
        )
