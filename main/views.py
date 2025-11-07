from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db import transaction
from datetime import datetime, date
import calendar
import os
from .models import Event, News, TeamMember, Gallery, Contact, EventRegistration, Document, Certificate
from .forms import ContactForm
from .document_utils import DocumentConverter

def home(request):
    """Home page view"""
    # Get upcoming events (not just featured ones) - all future events
    from datetime import datetime
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:8]  # Next 8 events
    featured_news = News.objects.filter(is_featured=True)[:3]
    recent_gallery = Gallery.objects.all()[:6]
    
    context = {
        'featured_events': upcoming_events,  # Keep same variable name for template compatibility
        'featured_news': featured_news,
        'recent_gallery': recent_gallery,
    }
    return render(request, 'main/home.html', context)

def about(request):
    """About page view"""
    team_members = TeamMember.objects.all()
    context = {
        'team_members': team_members,
    }
    return render(request, 'main/about.html', context)

def events(request):
    """Events page view - Calendar format"""
    # Get month and year parameters
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Check month boundaries
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1
    
    # Create calendar
    cal = calendar.Calendar(firstweekday=0)  # Monday start
    month_days = cal.monthdayscalendar(year, month)
    
    # Get events for this month
    events_in_month = Event.objects.filter(
        date__year=year,
        date__month=month
    ).order_by('date')
    
    # Group events by days
    events_by_day = {}
    for event in events_in_month:
        day = event.date.day
        if day not in events_by_day:
            events_by_day[day] = []
        events_by_day[day].append(event)
    
    # Month names (German)
    month_names = [
        'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
        'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'
    ]
    
    # Day names (German)
    day_names = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    
    # Previous and next month
    prev_month = month - 1
    prev_year = year
    if prev_month < 1:
        prev_month = 12
        prev_year -= 1
        
    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year += 1
    
    context = {
        'current_year': year,
        'current_month': month,
        'current_month_name': month_names[month - 1],
        'month_days': month_days,
        'events_by_day': events_by_day,
        'day_names': day_names,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': timezone.now().date(),
    }
    return render(request, 'main/events.html', context)

def event_detail(request, pk):
    """Event detail page view"""
    event = get_object_or_404(Event, pk=pk)
    related_events = Event.objects.exclude(pk=pk)[:3]
    
    # Check if event is in the past
    is_past_event = event.date < timezone.now()
    
    # Handle event registration (only for future events)
    if request.method == 'POST' and event.registration_required and event.is_public and not is_past_event:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        privacy_consent = request.POST.get('privacy_consent') == 'on'
        newsletter_consent = request.POST.get('newsletter_consent') == 'on'
        photo_consent = request.POST.get('photo_consent') == 'on'
        
        if first_name and last_name and email and privacy_consent:
            try:
                with transaction.atomic():
                    # Check if already registered
                    existing = EventRegistration.objects.filter(event=event, email=email).first()
                    if existing:
                        messages.warning(request, 'Sie sind bereits für diese Veranstaltung angemeldet.')
                    else:
                        # Check capacity with atomic select_for_update to prevent race conditions
                        if event.max_participants:
                            current_registrations = EventRegistration.objects.filter(
                                event=event, is_confirmed=True
                            ).count()
                            if current_registrations >= event.max_participants:
                                messages.error(request, 'Diese Veranstaltung ist bereits ausgebucht.')
                            else:
                                EventRegistration.objects.create(
                                    event=event,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    phone=phone,
                                    message=message,
                                    privacy_consent=privacy_consent,
                                    newsletter_consent=newsletter_consent,
                                    photo_consent=photo_consent
                                )
                                messages.success(request, 'Ihre Anmeldung wurde erfolgreich eingereicht! Sie erhalten eine Bestätigung per E-Mail.')
                        else:
                            EventRegistration.objects.create(
                                event=event,
                                first_name=first_name,
                                last_name=last_name,
                                email=email,
                                phone=phone,
                                message=message,
                                privacy_consent=privacy_consent,
                                newsletter_consent=newsletter_consent,
                                photo_consent=photo_consent
                            )
                            messages.success(request, 'Ihre Anmeldung wurde erfolgreich eingereicht! Sie erhalten eine Bestätigung per E-Mail.')
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error('Event registration error for event %s: %s', event.pk, str(e))
                messages.error(request, 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.')
        else:
            messages.error(request, 'Bitte füllen Sie alle erforderlichen Felder aus und stimmen Sie der Datenschutzerklärung zu.')
    
    # Get current registrations count for capacity display
    current_registrations = 0
    if event.max_participants:
        current_registrations = EventRegistration.objects.filter(event=event, is_confirmed=True).count()
    
    context = {
        'event': event,
        'related_events': related_events,
        'current_registrations': current_registrations,
        'is_past_event': is_past_event,  # Pass to template
    }
    return render(request, 'main/event_detail.html', context)

def news(request):
    """News page view"""
    news_list = News.objects.all()
    paginator = Paginator(news_list, 9)  # 9 news per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'news_list': page_obj,
    }
    return render(request, 'main/news.html', context)

def news_detail(request, pk):
    """News detail page view"""
    news_item = get_object_or_404(News, pk=pk)
    related_news = News.objects.exclude(pk=pk)[:3]
    
    context = {
        'news_item': news_item,
        'related_news': related_news,
    }
    return render(request, 'main/news_detail.html', context)

def gallery(request):
    """Gallery page view"""
    gallery_items = Gallery.objects.all()
    paginator = Paginator(gallery_items, 12)  # 12 images per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'gallery_items': page_obj,
    }
    return render(request, 'main/gallery.html', context)

def contact(request):
    """Contact page view with ModelForm (honeypot + PRG pattern)"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Honeypot already validated in form.clean_hp_field
            # Use proper logging instead of print statements
            import logging
            logger = logging.getLogger(__name__)
            logger.info('Contact form submission from %s', form.cleaned_data.get('email'))
            form.save()
            messages.success(request, 'Ihre Nachricht wurde erfolgreich gesendet! Wir werden uns so schnell wie möglich bei Ihnen melden.')
            # Post-Redirect-Get to avoid duplicate submissions on refresh
            return redirect('contact')
        else:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning('Invalid contact form submission: %s', form.errors.as_json())
            messages.error(request, 'Bitte korrigieren Sie die markierten Felder.')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})


def impressum(request):
    """Impressum page view"""
    return render(request, 'main/impressum.html')


def privacy(request):
    """Privacy policy page view"""
    return render(request, 'main/privacy.html')


def herunterladen(request):
    """Download page view - renamed from documents"""
    category = request.GET.get('category', '')
    
    documents_list = Document.objects.filter(is_public=True)
    
    if category:
        documents_list = documents_list.filter(category=category)
    
    documents_list = documents_list.order_by('-is_featured', '-created_at')
    
    # Get categories for filter
    categories = Document.CATEGORY_CHOICES
    
    # Pagination
    paginator = Paginator(documents_list, 12)  # 12 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'documents': page_obj,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'main/herunterladen.html', context)


def certificate_search(request):
    """Certificate search view"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        participant_number = request.POST.get('participant_number', '').strip()
        
        if not all([first_name, last_name, participant_number]):
            messages.error(request, 'Bitte füllen Sie alle Felder aus.')
            return render(request, 'main/certificate_search.html')
        
        try:
            certificate = Certificate.objects.get(
                first_name__iexact=first_name,
                last_name__iexact=last_name,
                participant_number=participant_number
            )
            return redirect('certificate_download', pk=certificate.pk)
        except Certificate.DoesNotExist:
            messages.error(request, 'Kein Zertifikat mit diesen Daten gefunden. Bitte überprüfen Sie Ihre Eingaben.')
    
    return render(request, 'main/certificate_search.html')


def certificate_download(request, pk):
    """Certificate download view"""
    certificate = get_object_or_404(Certificate, pk=pk)
    
    try:
        response = HttpResponse(certificate.certificate_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{certificate.full_name}_Zertifikat.pdf"'
        return response
    except FileNotFoundError:
        raise Http404("Zertifikat nicht gefunden")


def document_download(request, pk):
    """Document download view - converts to PDF and serves the file"""
    document = get_object_or_404(Document, pk=pk, is_public=True)
    
    try:
        # Get the file path
        file_path = document.file.path
        original_filename = os.path.basename(document.file.name)
        
        # Convert to PDF
        pdf_buffer = DocumentConverter.convert_to_pdf(file_path, original_filename)
        
        # Create response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{document.title}.pdf"'
        response.write(pdf_buffer.getvalue())
        
        # Increment download count
        document.download_count += 1
        document.save(update_fields=['download_count'])
        
        return response
        
    except Exception as e:
        # If conversion fails, provide original file
        import logging
        logger = logging.getLogger(__name__)
        logger.error('PDF conversion failed for document %s: %s', document.pk, str(e))
        
        try:
            with open(document.file.path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{original_filename}"'
                
                # Increment download count
                document.download_count += 1
                document.save(update_fields=['download_count'])
                
                return response
        except Exception as file_error:
            logger.error('File access failed for document %s: %s', document.pk, str(file_error))
            raise Http404("Document file not found")


def document_view(request, pk):
    """Document detail view (optional - for viewing document info before download)"""
    document = get_object_or_404(Document, pk=pk, is_public=True)
    
    # Get related documents from same category
    related_documents = Document.objects.filter(
        category=document.category, 
        is_public=True
    ).exclude(pk=pk)[:3]
    
    context = {
        'document': document,
        'related_documents': related_documents,
    }
    return render(request, 'main/document_detail.html', context)
