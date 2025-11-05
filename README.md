# Lesezirkel der Friedensstadt Osnabrück e.V. - Website

Ein Django-basiertes Content Management System für den Lesezirkel der Friedensstadt Osnabrück e.V.

## Über das Projekt

Diese Website wurde entwickelt, um die Aktivitäten des Lesezirkels der Friedensstadt Osnabrück e.V. zu präsentieren und zu verwalten. Das System ermöglicht die Verwaltung von Veranstaltungen, Nachrichten, Dokumenten und Zertifikaten.

## Funktionen

- 📅 **Veranstaltungsmanagement**: Erstellen und verwalten von Bildungsveranstaltungen und Dialogrunden
- 📰 **Nachrichtensystem**: Aktuelle Informationen und Ankündigungen
- 👥 **Mitgliederverwaltung**: Registration und Verwaltung von Vereinsmitgliedern
- 📚 **Dokumentenverwaltung**: Upload und Verwaltung von Vereinsdokumenten mit Kategorien
- 🏆 **Zertifikatssystem**: Download-System für Teilnahmezertifikate
- 🖼️ **Galerie**: Fotogalerie von Veranstaltungen
- 📝 **Kontaktformular**: Direkte Kommunikation mit dem Verein
- 🌐 **Mehrsprachigkeit**: Unterstützung für Deutsch, Englisch und Türkisch

## Design Features

- **Modern Hero Section**: Mit Logo-Reflexionseffekt und Live-Etkinlik-Vorschau
- **Responsive Design**: Optimiert für alle Geräte
- **Glassmorphism Effects**: Moderne transparente Designelemente
- **Blue/Navy Color Scheme**: Passend zum Vereinslogo
- **Accessibility**: Barrierefreie Navigation und Inhalte

## Technische Details

- **Framework**: Django 5.2.6
- **Datenbank**: SQLite (entwicklung) / PostgreSQL (produktion)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Deployment**: Gunicorn + Nginx

## Installation

### Voraussetzungen

- Python 3.8+
- pip
- Virtual Environment (empfohlen)

### Lokale Entwicklung

1. Repository klonen:
```bash
git clone https://github.com/InalHakan/lesezirkel_osnabrueck.git
cd lesezirkel_osnabrueck
```

2. Virtual Environment erstellen und aktivieren:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

4. Datenbank migrieren:
```bash
python manage.py migrate
```

5. Superuser erstellen (optional):
```bash
python manage.py createsuperuser
```

6. Entwicklungsserver starten:
```bash
python manage.py runserver
```

Die Website ist dann unter `http://127.0.0.1:8000/` erreichbar.

## Konfiguration

### Umgebungsvariablen

Für die Produktionsumgebung sollten folgende Umgebungsvariablen gesetzt werden:

```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@localhost/database
```

### Media Files

Medien-Uploads werden im `media/` Ordner gespeichert:
- `events/` - Veranstaltungsbilder
- `news/` - Nachrichtenbilder
- `gallery/` - Galeriebilder
- `documents/` - Vereinsdokumente (Kategorien: Formulare, Broschüren, Berichte, Zertifikate)
- `team/` - Teamfotos

## Zertifikatssystem

Das System enthält ein innovatives Zertifikatssystem:
- Teilnehmer können über Vorname, Nachname und Teilnehmernummer ihre Zertifikate suchen
- Automatischer Download bei erfolgreicher Suche
- Verwaltung über Django Admin Interface

## Deployment

### Mit Gunicorn und Nginx

1. Gunicorn Service installieren:
```bash
sudo cp gunicorn-kulturbrucke.service /etc/systemd/system/
sudo systemctl enable gunicorn-kulturbrucke
sudo systemctl start gunicorn-kulturbrucke
```

2. Nginx konfigurieren:
```bash
sudo cp nginx.conf.example /etc/nginx/sites-available/lesezirkel-osnabrueck
sudo ln -s /etc/nginx/sites-available/lesezirkel-osnabrueck /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

## Entwicklung

### Tests ausführen

```bash
python manage.py test
```

### Admin Interface

Das Admin Interface ist unter `/admin/` erreichbar. Erstellen Sie einen Superuser für den Zugang.

### Code Style

Das Projekt folgt den Django-Konventionen und PEP 8 Standards.

## Mission & Vision

**Mission**: Der Lesezirkel der Friedensstadt Osnabrück e.V. setzt sich für eine offene, demokratische und vielfältige Gesellschaft ein. Durch Bildung, interkulturellen Dialog und ehrenamtliches Engagement schaffen wir Räume für Begegnung, Austausch und persönliche Weiterentwicklung.

**Vision**: Eine lebendige und engagierte Gemeinschaft in Osnabrück, in der Bildung, Dialog und Zusammenhalt das Fundament des Miteinanders bilden.

## Beitrag

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue für Verbesserungsvorschläge.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

## Kontakt

Lesezirkel der Friedensstadt Osnabrück e.V.
- Email: info@lz-os.de
- Adresse: Großhandelsring 1, 49084 Osnabrück
- Telefon: +49 (0) 15560 66 92 55
- Bürozeiten: Dienstag & Donnerstag, 15:00 - 17:00 Uhr

## Danksagungen

- Django Framework Team
- Bootstrap Team
- Alle Mitwirkenden des Vereins
- EU-Förderung

---

Erstellt für Lesezirkel der Friedensstadt Osnabrück e.V. - Förderung von Bildung, Dialog und Gemeinschaft
