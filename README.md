# Lesezirkel Osnabrück

Eine Full-Stack-Webanwendung zur Verwaltung eines Lesezirkels in Osnabrück. Die Anwendung ermöglicht die Verwaltung von Büchern und die Organisation von Leseterminen.

## Technologien

### Backend
- Node.js mit Express
- MongoDB mit Mongoose
- RESTful API
- CORS-Unterstützung
- Rate Limiting (100 Anfragen pro 15 Minuten)

### Frontend
- React
- React Router für Navigation
- Axios für API-Kommunikation
- Responsives Design

## Projektstruktur

```
lesezirkel_osnabrueck/
├── backend/                 # Backend-Anwendung
│   ├── src/
│   │   ├── config/         # Datenbankkonfiguration
│   │   ├── controllers/    # Request-Handler
│   │   ├── models/         # MongoDB-Modelle
│   │   ├── routes/         # API-Routen
│   │   └── server.js       # Hauptserver-Datei
│   └── package.json
├── frontend/                # Frontend-Anwendung
│   ├── src/
│   │   ├── components/     # React-Komponenten
│   │   ├── pages/          # Seiten-Komponenten
│   │   ├── services/       # API-Services
│   │   └── App.js          # Haupt-React-Komponente
│   └── package.json
└── README.md
```

## Installation

### Voraussetzungen
- Node.js (v14 oder höher)
- MongoDB (lokal oder MongoDB Atlas)
- npm oder yarn

### Backend einrichten

1. Navigieren Sie zum Backend-Verzeichnis:
```bash
cd backend
```

2. Installieren Sie die Abhängigkeiten:
```bash
npm install
```

3. Erstellen Sie eine `.env` Datei basierend auf `.env.example`:
```bash
cp .env.example .env
```

4. Passen Sie die Umgebungsvariablen in `.env` an:
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/lesezirkel
NODE_ENV=development
```

5. Starten Sie den Backend-Server:
```bash
# Entwicklungsmodus mit automatischem Neustart
npm run dev

# Produktionsmodus
npm start
```

Der Backend-Server läuft nun auf `http://localhost:5000`

### Frontend einrichten

1. Öffnen Sie ein neues Terminal und navigieren Sie zum Frontend-Verzeichnis:
```bash
cd frontend
```

2. Installieren Sie die Abhängigkeiten:
```bash
npm install
```

3. Erstellen Sie eine `.env` Datei basierend auf `.env.example`:
```bash
cp .env.example .env
```

4. Starten Sie die Frontend-Anwendung:
```bash
npm start
```

Die Frontend-Anwendung läuft nun auf `http://localhost:3000`

## API-Endpunkte

### Bücher
- `GET /api/books` - Alle Bücher abrufen
- `GET /api/books/:id` - Ein Buch nach ID abrufen
- `POST /api/books` - Neues Buch erstellen
- `PUT /api/books/:id` - Buch aktualisieren
- `DELETE /api/books/:id` - Buch löschen

### Lesetermine
- `GET /api/sessions` - Alle Lesetermine abrufen
- `GET /api/sessions/:id` - Einen Lesetermin nach ID abrufen
- `POST /api/sessions` - Neuen Lesetermin erstellen
- `PUT /api/sessions/:id` - Lesetermin aktualisieren
- `DELETE /api/sessions/:id` - Lesetermin löschen

### Health Check
- `GET /api/health` - Server-Status prüfen

## Funktionen

### Bücherverwaltung
- Bücher hinzufügen mit Titel, Autor, ISBN, Beschreibung und Veröffentlichungsjahr
- Bücher bearbeiten und löschen
- Status-Tracking (Verfügbar, Lesen, Abgeschlossen)
- Übersichtliche Darstellung aller Bücher

### Lesetermin-Verwaltung
- Lesetermine planen mit Datum und Ort
- Teilnehmerlisten pflegen
- Notizen zu Diskussionen hinzufügen
- Verknüpfung mit Büchern

## Verwendung

1. Starten Sie sowohl Backend als auch Frontend (siehe Installationsanleitung)
2. Öffnen Sie `http://localhost:3000` in Ihrem Browser
3. Navigieren Sie zu "Bücher", um Bücher zu verwalten
4. Navigieren Sie zu "Lesetermine", um Lesetermine zu organisieren

## Entwicklung

### Backend-Entwicklung
```bash
cd backend
npm run dev  # Startet mit nodemon für automatischen Neustart
```

### Frontend-Entwicklung
```bash
cd frontend
npm start  # Startet mit Hot Reload
```

## Docker-Deployment

Die Anwendung kann einfach mit Docker Compose bereitgestellt werden:

```bash
# Alle Services starten (MongoDB, Backend, Frontend)
docker-compose up -d

# Services stoppen
docker-compose down

# Services neu bauen
docker-compose up -d --build
```

Nach dem Start ist die Anwendung unter folgenden URLs erreichbar:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5000/api`
- MongoDB: `localhost:27017`

## Sicherheit

Die Anwendung implementiert folgende Sicherheitsmaßnahmen:
- **Rate Limiting**: API-Anfragen sind auf 100 Anfragen pro 15 Minuten pro IP-Adresse beschränkt
- **CORS**: Cross-Origin Resource Sharing ist aktiviert für Frontend-Integration
- **Fehlerbehandlung**: Alle Fehler werden ordnungsgemäß behandelt und geloggt

## Lizenz

ISC

## Autor

Lesezirkel Osnabrück