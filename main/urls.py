from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ueber-uns/', views.about, name='about'),
    path('veranstaltungen/', views.events, name='events'),
    path('veranstaltung/<int:pk>/', views.event_detail, name='event_detail'),
    path('nachrichten/', views.news, name='news'),
    path('nachricht/<int:pk>/', views.news_detail, name='news_detail'),
    path('galerie/', views.gallery, name='gallery'),
    path('herunterladen/', views.herunterladen, name='herunterladen'),
    path('dokument/<int:pk>/download/', views.document_download, name='document_download'),
    path('dokument/<int:pk>/', views.document_view, name='document_detail'),
    path('zertifikat-suche/', views.certificate_search, name='certificate_search'),
    path('zertifikat/<int:pk>/download/', views.certificate_download, name='certificate_download'),
    # Redirect old documents URL
    re_path(r'^dokumente/?$', RedirectView.as_view(pattern_name='herunterladen', permanent=True)),
    # Öffentlich sichtbare URL soll deutsch ("/kontakt/") olsun, name='contact' korunuyor.
    path('kontakt/', views.contact, name='contact'),
    # Eski /contact/ isteklerini kalıcı yönlendirelim (SEO + mevcut linkler)
    re_path(r'^contact/?$', RedirectView.as_view(pattern_name='contact', permanent=True)),
    path('impressum/', views.impressum, name='impressum'),
    path('datenschutz/', views.privacy, name='privacy'),
]