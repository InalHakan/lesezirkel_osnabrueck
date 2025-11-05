from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import format_html

# Optional PDF dependencies
try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from .models import Event, News, TeamMember, Gallery, Contact, EventRegistration, Document, Certificate

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'category', 'is_featured', 'is_public', 'registration_required', 'created_at']
    list_filter = ['category', 'is_featured', 'is_public', 'registration_required', 'date', 'created_at']
    search_fields = ['title', 'description', 'location']
    list_editable = ['category', 'is_featured', 'is_public', 'registration_required']
    date_hierarchy = 'date'
    ordering = ['-date']
    actions = ['export_event_participant_list', 'export_event_participant_list_pdf']
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('title', 'description', 'date', 'location', 'image', 'category'),
            'description': 'Allgemeine Informationen über die Veranstaltung'
        }),
        ('Sichtbarkeit und Anmeldung', {
            'fields': ('is_featured', 'is_public', 'registration_required', 'max_participants'),
            'description': 'Öffentliche Veranstaltungen benötigen Datenschutzerklärung bei Anmeldungen.',
            'classes': ('wide',)
        }),
    )
    
    def export_event_participant_list(self, request, queryset):
        """Export participant list for selected events"""
        # Get all registrations for selected events
        registrations = EventRegistration.objects.filter(
            event__in=queryset
        ).select_related('event').order_by('event__date', 'last_name', 'first_name')
        
        # Use the same export function as EventRegistrationAdmin
        return EventRegistrationAdmin.export_participant_list(self, request, registrations)
    
    export_event_participant_list.short_description = "📋 Teilnehmerliste für ausgewählte Events exportieren"
    
    def export_event_participant_list_pdf(self, request, queryset):
        """Export participant list for selected events as PDF"""
        # Get all registrations for selected events
        registrations = EventRegistration.objects.filter(
            event__in=queryset
        ).select_related('event').order_by('event__date', 'last_name', 'first_name')
        
        # Use the same PDF export function as EventRegistrationAdmin
        return EventRegistrationAdmin.export_participant_list_pdf(self, request, registrations)
    
    export_event_participant_list_pdf.short_description = "📄 Teilnehmerliste als PDF exportieren"

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'published_date', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['is_featured']
    date_hierarchy = 'published_date'
    ordering = ['-published_date']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'email', 'order']
    list_filter = ['position']
    search_fields = ['name', 'position', 'email']
    list_editable = ['order']
    ordering = ['order', 'name']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'created_at']
    list_filter = ['event', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_answered', 'created_at']
    list_filter = ['is_read', 'is_answered', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read', 'is_answered']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'event', 'is_confirmed', 'privacy_consent', 'newsletter_consent', 'photo_consent', 'created_at']
    list_filter = ['is_confirmed', 'privacy_consent', 'newsletter_consent', 'photo_consent', 'event', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'event__title']
    list_editable = ['is_confirmed']
    readonly_fields = ['first_name', 'last_name', 'email', 'phone', 'message', 'privacy_consent', 'newsletter_consent', 'photo_consent', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    actions = ['export_participant_list', 'export_participant_list_pdf']
    
    fieldsets = (
        ('Teilnehmer', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Anmeldung', {
            'fields': ('event', 'message', 'is_confirmed')
        }),
        ('Einverständnisse', {
            'fields': ('privacy_consent', 'newsletter_consent', 'photo_consent', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def export_participant_list(self, request, queryset):
        """Export participant list as printable HTML"""
        # Group registrations by event
        events_data = {}
        for registration in queryset.select_related('event'):
            event_title = registration.event.title
            if event_title not in events_data:
                events_data[event_title] = {
                    'event': registration.event,
                    'registrations': []
                }
            events_data[event_title]['registrations'].append(registration)
        
        # Create HTML response
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Teilnehmerliste</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .event-section { margin-bottom: 40px; page-break-after: always; }
                .event-header { background-color: #f8f9fa; padding: 15px; margin-bottom: 20px; border-left: 5px solid #007bff; }
                .event-title { color: #007bff; margin: 0; font-size: 24px; }
                .event-info { color: #666; margin: 5px 0 0 0; }
                table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                th, td { padding: 12px 8px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f8f9fa; font-weight: bold; color: #495057; }
                tr:nth-child(even) { background-color: #f8f9fa; }
                .checkbox { width: 20px; height: 20px; border: 2px solid #007bff; display: inline-block; margin-right: 5px; }
                .consent-icons { font-size: 12px; }
                .consent-yes { color: #28a745; }
                .consent-no { color: #dc3545; }
                .footer { margin-top: 30px; padding-top: 20px; border-top: 2px solid #007bff; }
                .signature-line { margin-top: 40px; }
                .print-info { color: #666; font-size: 12px; }
            </style>
        </head>
        <body>
        """
        
        for event_title, data in events_data.items():
            event = data['event']
            registrations = data['registrations']
            confirmed_count = sum(1 for r in registrations if r.is_confirmed)
            
            html_content += f"""
            <div class="event-section">
                <div class="event-header">
                    <h1 class="event-title">{event.title}</h1>
                    <p class="event-info">
                        <strong>Datum:</strong> {event.date.strftime('%d.%m.%Y um %H:%M')} | 
                        <strong>Ort:</strong> {event.location}
                    </p>
                    <p class="event-info">
                        <strong>Anmeldungen:</strong> {len(registrations)} gesamt | 
                        <strong>Bestätigt:</strong> {confirmed_count}
                        {f' | <strong>Kapazität:</strong> {event.max_participants}' if event.max_participants else ''}
                    </p>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th style="width: 30px;">#</th>
                            <th>Name</th>
                            <th>E-Mail</th>
                            <th>Telefon</th>
                            <th style="width: 80px;">Bestätigt</th>
                            <th style="width: 60px;">Foto OK</th>
                            <th style="width: 100px;">Anwesend ☐</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for i, registration in enumerate(registrations, 1):
                html_content += f"""
                        <tr>
                            <td>{i}</td>
                            <td><strong>{registration.full_name}</strong></td>
                            <td>{registration.email}</td>
                            <td>{registration.phone or '-'}</td>
                            <td>
                                <span class="consent-{'yes' if registration.is_confirmed else 'no'}">
                                    {'✓ Ja' if registration.is_confirmed else '✗ Nein'}
                                </span>
                            </td>
                            <td>
                                <span class="consent-{'yes' if registration.photo_consent else 'no'}">
                                    {'✓' if registration.photo_consent else '✗'}
                                </span>
                            </td>
                            <td><span class="checkbox"></span></td>
                        </tr>
                """
            
            html_content += """
                    </tbody>
                </table>
                
                <div class="footer">
                    <div class="signature-line">
                        <p><strong>Organisator/Verantwortlicher:</strong> _______________________</p>
                        <p style="margin-top: 30px;"><strong>Datum & Unterschrift:</strong> _______________________</p>
                    </div>
                </div>
            </div>
            """
        
        from datetime import datetime
        
        html_content += f"""
            <div class="print-info">
                <p><em>Teilnehmerliste erstellt am {datetime.now().strftime('%d.%m.%Y um %H:%M')} | 
                Lesezirkel Osnabrück e.V.</em></p>
            </div>
        </body>
        </html>
        """
        
        response = HttpResponse(html_content, content_type='text/html')
        response['Content-Disposition'] = 'attachment; filename="teilnehmerliste.html"'
        return response
    
    export_participant_list.short_description = "📋 Teilnehmerliste als Tabelle exportieren"
    
    def export_participant_list_pdf(self, request, queryset):
        """Export participant list as PDF"""
        # Group registrations by event
        events_data = {}
        for registration in queryset.select_related('event'):
            event_title = registration.event.title
            if event_title not in events_data:
                events_data[event_title] = {
                    'event': registration.event,
                    'registrations': []
                }
            events_data[event_title]['registrations'].append(registration)
        
        # Create HTML content with PDF-optimized CSS
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Teilnehmerliste</title>
            <style>
                @page {
                    size: A4;
                    margin: 2cm 1.5cm;
                    @bottom-center {
                        content: "Seite " counter(page) " von " counter(pages);
                        font-size: 10px;
                        color: #666;
                    }
                }
                
                body { 
                    font-family: 'DejaVu Sans', Arial, sans-serif; 
                    margin: 0; 
                    font-size: 12px;
                    line-height: 1.4;
                    color: #333;
                }
                
                .event-section { 
                    margin-bottom: 30px; 
                    page-break-after: always; 
                }
                
                .event-section:last-child {
                    page-break-after: avoid;
                }
                
                .event-header { 
                    background-color: #f8f9fa; 
                    padding: 15px; 
                    margin-bottom: 20px; 
                    border-left: 5px solid #007bff;
                    border-radius: 3px;
                }
                
                .event-title { 
                    color: #007bff; 
                    margin: 0; 
                    font-size: 20px; 
                    font-weight: bold;
                }
                
                .event-info { 
                    color: #666; 
                    margin: 5px 0 0 0; 
                    font-size: 11px;
                }
                
                table { 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-top: 10px;
                    font-size: 11px;
                }
                
                th, td { 
                    padding: 8px 6px; 
                    text-align: left; 
                    border: 1px solid #ddd; 
                    vertical-align: middle;
                }
                
                th { 
                    background-color: #f8f9fa; 
                    font-weight: bold; 
                    color: #495057;
                    font-size: 11px;
                }
                
                tr:nth-child(even) { 
                    background-color: #f9f9f9; 
                }
                
                .checkbox { 
                    width: 15px; 
                    height: 15px; 
                    border: 2px solid #007bff; 
                    display: inline-block;
                }
                
                .consent-yes { 
                    color: #28a745; 
                    font-weight: bold;
                }
                
                .consent-no { 
                    color: #dc3545; 
                }
                
                .footer { 
                    margin-top: 25px; 
                    padding-top: 15px; 
                    border-top: 1px solid #007bff;
                    page-break-inside: avoid;
                }
                
                .signature-line { 
                    margin-top: 25px;
                    font-size: 11px;
                }
                
                .print-info { 
                    color: #666; 
                    font-size: 10px;
                    margin-top: 20px;
                    text-align: center;
                }
                
                .logo-header {
                    text-align: center;
                    margin-bottom: 30px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #007bff;
                }
                
                .logo-title {
                    color: #007bff;
                    font-size: 24px;
                    font-weight: bold;
                    margin: 0;
                }
            </style>
        </head>
        <body>
            <div class="logo-header">
                <h1 class="logo-title">Lesezirkel Osnabrück e.V.</h1>
                <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">Teilnehmerliste</p>
            </div>
        """
        
        for event_title, data in events_data.items():
            event = data['event']
            registrations = data['registrations']
            confirmed_count = sum(1 for r in registrations if r.is_confirmed)
            
            html_content += f"""
            <div class="event-section">
                <div class="event-header">
                    <h2 class="event-title">{event.title}</h2>
                    <p class="event-info">
                        <strong>Datum:</strong> {event.date.strftime('%d.%m.%Y um %H:%M')} | 
                        <strong>Ort:</strong> {event.location}
                    </p>
                    <p class="event-info">
                        <strong>Anmeldungen:</strong> {len(registrations)} gesamt | 
                        <strong>Bestätigt:</strong> {confirmed_count}
                        {f' | <strong>Kapazität:</strong> {event.max_participants}' if event.max_participants else ''}
                    </p>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th style="width: 8%;">#</th>
                            <th style="width: 25%;">Name</th>
                            <th style="width: 28%;">E-Mail</th>
                            <th style="width: 15%;">Telefon</th>
                            <th style="width: 8%;">Best.</th>
                            <th style="width: 6%;">Foto</th>
                            <th style="width: 10%;">Anwesend</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for i, registration in enumerate(registrations, 1):
                html_content += f"""
                        <tr>
                            <td>{i}</td>
                            <td><strong>{registration.full_name}</strong></td>
                            <td>{registration.email}</td>
                            <td>{registration.phone or '-'}</td>
                            <td>
                                <span class="consent-{'yes' if registration.is_confirmed else 'no'}">
                                    {'✓' if registration.is_confirmed else '✗'}
                                </span>
                            </td>
                            <td>
                                <span class="consent-{'yes' if registration.photo_consent else 'no'}">
                                    {'✓' if registration.photo_consent else '✗'}
                                </span>
                            </td>
                            <td><span class="checkbox"></span></td>
                        </tr>
                """
            
            html_content += """
                    </tbody>
                </table>
                
                <div class="footer">
                    <div class="signature-line">
                        <p><strong>Organisator/Verantwortlicher:</strong> _______________________</p>
                        <p style="margin-top: 20px;"><strong>Datum & Unterschrift:</strong> _______________________</p>
                    </div>
                </div>
            </div>
            """
        
        from datetime import datetime
        
        html_content += f"""
            <div class="print-info">
                <p><em>Teilnehmerliste erstellt am {datetime.now().strftime('%d.%m.%Y um %H:%M')} | 
                Lesezirkel Osnabrück e.V.</em></p>
            </div>
        </body>
        </html>
        """
        
        # Generate PDF using ReportLab
        if not REPORTLAB_AVAILABLE:
            # Fallback to HTML if ReportLab is not available
            response = HttpResponse(html_content, content_type='text/html')
            response['Content-Disposition'] = 'attachment; filename="teilnehmerliste.html"'
            return response
            
        try:
            from io import BytesIO
            from datetime import datetime
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=60,
                bottomMargin=40
            )
            
            # Create styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#007bff')
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=12,
                textColor=colors.HexColor('#007bff')
            )
            
            normal_style = styles['Normal']
            
            # Build PDF content
            story = []
            
            # Main title
            story.append(Paragraph("Lesezirkel Osnabrück e.V.", title_style))
            story.append(Paragraph("Teilnehmerliste", styles['Heading2']))
            story.append(Spacer(1, 20))
            
            for event_title, data in events_data.items():
                event = data['event']
                registrations = data['registrations']
                confirmed_count = sum(1 for r in registrations if r.is_confirmed)
                
                # Event header
                story.append(Paragraph(event.title, heading_style))
                
                event_info = f"""
                <b>Datum:</b> {event.date.strftime('%d.%m.%Y um %H:%M')}<br/>
                <b>Ort:</b> {event.location}<br/>
                <b>Anmeldungen:</b> {len(registrations)} gesamt | <b>Bestätigt:</b> {confirmed_count}
                {f' | <b>Kapazität:</b> {event.max_participants}' if event.max_participants else ''}
                """
                story.append(Paragraph(event_info, normal_style))
                story.append(Spacer(1, 15))
                
                # Participants table
                table_data = [
                    ['#', 'Name', 'E-Mail', 'Telefon', 'Best.', 'Foto', 'Anwesend']
                ]
                
                for i, registration in enumerate(registrations, 1):
                    table_data.append([
                        str(i),
                        registration.full_name,
                        registration.email,
                        registration.phone or '-',
                        '✓' if registration.is_confirmed else '✗',
                        '✓' if registration.photo_consent else '✗',
                        '☐'
                    ])
                
                # Create table
                table = Table(table_data, colWidths=[0.4*inch, 1.8*inch, 2.2*inch, 1.2*inch, 0.5*inch, 0.5*inch, 0.8*inch])
                
                table.setStyle(TableStyle([
                    # Header style
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#495057')),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    
                    # Body style
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ddd')),
                    
                    # Alternating row colors
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
                    
                    # Alignment
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    
                    # Status columns (Best., Foto)
                    ('ALIGN', (4, 0), (5, -1), 'CENTER'),
                ]))
                
                story.append(table)
                story.append(Spacer(1, 20))
                
                # Signature section
                signature_text = """
                <b>Organisator/Verantwortlicher:</b> _______________________<br/><br/>
                <b>Datum & Unterschrift:</b> _______________________
                """
                story.append(Paragraph(signature_text, normal_style))
                story.append(Spacer(1, 30))
            
            # Footer
            footer_text = f"<i>Teilnehmerliste erstellt am {datetime.now().strftime('%d.%m.%Y um %H:%M')} | Lesezirkel Osnabrück e.V.</i>"
            story.append(Paragraph(footer_text, styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            pdf = buffer.getvalue()
            buffer.close()
            
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="teilnehmerliste.pdf"'
            return response
            
        except Exception as e:
            # Fallback to HTML if PDF generation fails
            response = HttpResponse(html_content, content_type='text/html')
            response['Content-Disposition'] = 'attachment; filename="teilnehmerliste.html"'
            return response
    
    export_participant_list_pdf.short_description = "📄 Teilnehmerliste als PDF exportieren"


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'file_extension', 'formatted_file_size', 'download_count', 'is_featured', 'is_public', 'created_at']
    list_filter = ['category', 'is_featured', 'is_public', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['category', 'is_featured', 'is_public']
    readonly_fields = ['file_size', 'download_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Dokumentinformationen', {
            'fields': ('title', 'description', 'category', 'file')
        }),
        ('Einstellungen', {
            'fields': ('is_featured', 'is_public')
        }),
        ('Statistiken', {
            'fields': ('file_size', 'download_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def file_extension(self, obj):
        return obj.file_extension or '-'
    file_extension.short_description = 'Format'
    
    def formatted_file_size(self, obj):
        return obj.formatted_file_size
    formatted_file_size.short_description = 'Dateigröße'


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['participant_number', 'first_name', 'last_name', 'event_title', 'completion_date', 'created_at']
    list_filter = ['completion_date', 'event_title', 'created_at']
    search_fields = ['first_name', 'last_name', 'participant_number', 'event_title']
    ordering = ['-completion_date', 'last_name', 'first_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Teilnehmerinformationen', {
            'fields': ('first_name', 'last_name', 'participant_number')
        }),
        ('Veranstaltungsinformationen', {
            'fields': ('event_title', 'completion_date')
        }),
        ('Zertifikat', {
            'fields': ('certificate_file',)
        }),
        ('Zeitstempel', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request)


# Admin site title and header customization
admin.site.site_header = "Lesezirkel Osnabrück Admin"
admin.site.site_title = "Lesezirkel Admin"
admin.site.index_title = "Verwaltungspanel"
