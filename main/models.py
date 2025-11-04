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
    privacy_consent = models.BooleanField(verbose_name="Datenschutz zugestimmt", 
                                        help_text="Einverständnis zur Datenschutzerklärung")
    newsletter_consent = models.BooleanField(default=False, verbose_name="Newsletter-Anmeldung",
                                           help_text="Möchte Newsletter erhalten")
    photo_consent = models.BooleanField(default=False, verbose_name="Fotoerlaubnis",
                                      help_text="Einverständnis zur Anfertigung und Veröffentlichung von Fotos")
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


class Document(models.Model):
    """Document model for downloadable files"""
    CATEGORY_CHOICES = [
        ('general', 'Allgemeine Dokumente'),
        ('forms', 'Formulare'),
        ('brochures', 'Broschüren'),
        ('reports', 'Berichte'),
        ('guidelines', 'Richtlinien'),
        ('certificates', 'Zertifikate'),
        ('other', 'Sonstiges'),
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
