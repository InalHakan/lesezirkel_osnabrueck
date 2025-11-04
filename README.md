# Lesezirkel Osnabrück e.V. - Website

Ein Django-basiertes Content Management System für den Lesezirkel Osnabrück e.V.

## Über das Projekt

Diese Website wurde entwickelt, um die Aktivitäten des Lesezirkels Osnabrück e.V. zu präsentieren und zu verwalten. Das System ermöglicht die Verwaltung von Veranstaltungen, Nachrichten, Dokumenten und Mitgliedern.

## Funktionen

- 📅 **Veranstaltungsmanagement**: Erstellen und verwalten von Lesungen, Diskussionsrunden und literarischen Events
- 📰 **Nachrichtensystem**: Aktuelle Informationen und Ankündigungen
- 👥 **Mitgliederverwaltung**: Registration und Verwaltung von Vereinsmitgliedern
- 📚 **Dokumentenverwaltung**: Upload und Verwaltung von Vereinsdokumenten
- 🖼️ **Galerie**: Fotogalerie von Veranstaltungen
- 📝 **Kontaktformular**: Direkte Kommunikation mit dem Verein
- 🌐 **Mehrsprachigkeit**: Unterstützung für Deutsch, Englisch und Türkisch

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
git clone [repository-url]
cd Lesezirkel_Osna
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
- `documents/` - Vereinsdokumente
- `team/` - Teamfotos

## Deployment

### Mit Gunicorn und Nginx

1. Gunicorn Service installieren:
```bash
sudo cp gunicorn-lesezirkel.service /etc/systemd/system/
sudo systemctl enable gunicorn-lesezirkel
sudo systemctl start gunicorn-lesezirkel
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

## Beitrag

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue für Verbesserungsvorschläge.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

## Kontakt

Lesezirkel Osnabrück e.V.
- Email: info@lesezirkel-osnabrueck.de
- Website: https://lesezirkel-osnabrueck.de

## Danksagungen

- Django Framework Team
- Bootstrap Team
- Alle Mitwirkenden des Vereins

---

Erstellt für Lesezirkel Osnabrück e.V. - Förderung der Literatur und Gemeinschaft