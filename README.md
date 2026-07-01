# RTMPPanel 🎥

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/alexanderwagnerdev/rtmppanel)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

A Docker wrapper for the web-based control panel for [librtmp2-server](https://github.com/OpenRTMP/librtmp2-server). The application source is not stored in this repository. It is cloned from [OpenRTMP/librtmp2-server-panel](https://github.com/OpenRTMP/librtmp2-server-panel) during the Docker build.

## ✨ Features

- 📺 **Stream Management** - Create, view, and delete RTMP streams
- 🔗 **Easy URL Access** - Publish, play, and stats URLs with one-click copy functionality
- 📊 **Live Statistics** - View bitrate, resolution, codec, and uptime stats from librtmp2-server
- 🔐 **Optional Authentication** - Configurable admin login via environment variables
- ⚙️ **REST API Integration** - Communicates with librtmp2-server's HTTP API
- 🐳 **Docker Ready** - Easy deployment with Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Running librtmp2-server instance
- librtmp2-server API token

### Installation with Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/AlexanderWagnerDev/rtmppanel-docker.git
cd rtmppanel-docker
```

2. Edit `docker-compose.yml` and configure your environment variables:
```yaml
environment:
  REQUIRE_LOGIN: "True"             # Enable/disable authentication
  USERNAME: "admin"                 # Admin username
  PASSWORD: "supersecret"           # Admin password
  SECRET_KEY: "generate-a-stable-random-secret"  # Stable Flask/encryption secret
  LRTMP2_API_URL: "http://librtmp2-server:8080"  # librtmp2-server API URL
  LRTMP2_API_TOKEN: "your_api_token" # librtmp2-server API token
  LRTMP2_DOMAIN: "streaming.example.com" # Public RTMP host/IP
```

Generate a strong `SECRET_KEY` with:
```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

3. Build and start the container:
```bash
docker compose up -d --build
```

4. Access the panel at `http://localhost:8000`

### Installation with Docker Run

For manual deployment:

```bash
docker run -d \
  --name rtmppanel \
  -e REQUIRE_LOGIN=True \
  -e USERNAME=admin \
  -e PASSWORD=supersecret \
  -e SECRET_KEY=generate-a-stable-random-secret \
  -e LRTMP2_API_URL=http://librtmp2-server:8080 \
  -e LRTMP2_API_TOKEN=your_api_token \
  -e LRTMP2_DOMAIN=localhost \
  -e LANG=en \
  -e TZ=Europe/Vienna \
  -e LRTMP2_RTMP_PORT=1935 \
  -e LRTMP2_APP=live \
  -e PANEL_DB_PATH=/data/panel.db \
  -v rtmppanel-data:/data \
  -p 8000:8000/tcp \
  alexanderwagnerdev/rtmppanel:latest
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LRTMP2_API_URL` | librtmp2-server API endpoint | - | Yes |
| `LRTMP2_API_TOKEN` | librtmp2-server API token | - | Yes |
| `LRTMP2_DOMAIN` | Domain or IP for public RTMP URLs | `localhost` | Yes |
| `LRTMP2_RTMP_PORT` | RTMP listener port | `1935` | No |
| `LRTMP2_APP` | Default RTMP app name | `live` | No |
| `REQUIRE_LOGIN` | Enable authentication (`True`/`False`) | `False` | No |
| `USERNAME` | Admin username | `admin` | If login enabled |
| `PASSWORD` | Admin password | - | If login enabled |
| `SECRET_KEY` | Stable Flask session/encryption secret for stored stream keys | - | Yes |
| `PANEL_DB_PATH` | SQLite database path for stored stream keys | `/data/panel.db` | No |
| `SESSION_COOKIE_SECURE` | Use secure cookies when served over HTTPS | `False` | No |
| `LANG` | Interface language | `en` | No |
| `TZ` | Timezone | `UTC` | No |

Important: Keep `SECRET_KEY` stable. The panel uses it to encrypt locally stored stream keys, so changing it can make already stored keys unreadable.

### Example Configuration

Minimal setup with authentication:
```yaml
environment:
  REQUIRE_LOGIN: "True"
  USERNAME: "admin"
  PASSWORD: "supersecret"
  SECRET_KEY: "generate-a-stable-random-secret"
  LRTMP2_API_URL: "http://librtmp2-server:8080"
  LRTMP2_API_TOKEN: "mytoken123"
  LRTMP2_DOMAIN: "streaming.example.com"
```

## 🔧 Troubleshooting

### Cannot connect to librtmp2-server
- Verify `LRTMP2_API_URL` is correct and reachable from the container
- Check if `LRTMP2_API_TOKEN` matches the token from librtmp2-server
- Ensure librtmp2-server is running and the HTTP API is enabled

### Login not working
- Verify `REQUIRE_LOGIN` is set to `True`
- Check `USERNAME`, `PASSWORD`, and `SECRET_KEY`
- Clear browser cache and cookies

### Stored stream keys cannot be read after restart
- Make sure the same `SECRET_KEY` is used after every container restart
- Keep the `/data` volume mounted so `PANEL_DB_PATH=/data/panel.db` persists

### View container logs
```bash
docker compose logs -f rtmppanel
```

## 📝 License

This Docker wrapper is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For questions, issues, or feature requests:
- Open an [issue on GitHub](https://github.com/AlexanderWagnerDev/rtmppanel-docker/issues)
- Check existing issues for solutions

## 🔗 Related Projects

- [librtmp2-server-panel](https://github.com/OpenRTMP/librtmp2-server-panel) - The upstream panel source cloned during Docker build
- [librtmp2-server](https://github.com/OpenRTMP/librtmp2-server) - The RTMP server this panel manages

---

# RTMPPanel 🎥

*[Deutsche Version]*

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/alexanderwagnerdev/rtmppanel)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Ein Docker-Wrapper für das webbasierte Control Panel von [librtmp2-server](https://github.com/OpenRTMP/librtmp2-server). Der App-Sourcecode liegt nicht in diesem Repository. Er wird beim Docker-Build aus [OpenRTMP/librtmp2-server-panel](https://github.com/OpenRTMP/librtmp2-server-panel) geklont.

## ✨ Features

- 📺 **Stream-Verwaltung** - RTMP-Streams erstellen, anzeigen und löschen
- 🔗 **Einfacher URL-Zugriff** - Publish-, Play- und Stats-URLs mit Ein-Klick-Kopierfunktion
- 📊 **Live-Statistiken** - Bitrate, Auflösung, Codec und Uptime von librtmp2-server anzeigen
- 🔐 **Optionale Authentifizierung** - Konfigurierbarer Admin-Login per Umgebungsvariablen
- ⚙️ **REST-API-Integration** - Kommunikation mit der HTTP-API von librtmp2-server
- 🐳 **Docker-Ready** - Einfaches Deployment mit Docker Compose

## 🚀 Schnellstart

### Voraussetzungen

- Docker und Docker Compose installiert
- Laufende librtmp2-server Instanz
- librtmp2-server API-Token

### Installation mit Docker Compose (Empfohlen)

1. Repository klonen:
```bash
git clone https://github.com/AlexanderWagnerDev/rtmppanel-docker.git
cd rtmppanel-docker
```

2. `docker-compose.yml` bearbeiten und Umgebungsvariablen konfigurieren:
```yaml
environment:
  REQUIRE_LOGIN: "True"             # Authentifizierung aktivieren/deaktivieren
  USERNAME: "admin"                 # Admin-Benutzername
  PASSWORD: "supersecret"           # Admin-Passwort
  SECRET_KEY: "generate-a-stable-random-secret"  # Stabiles Flask/Verschlüsselungs-Secret
  LRTMP2_API_URL: "http://librtmp2-server:8080"  # librtmp2-server API-URL
  LRTMP2_API_TOKEN: "your_api_token" # librtmp2-server API-Token
  LRTMP2_DOMAIN: "streaming.example.com" # Öffentliche RTMP Domain/IP
```

Starkes `SECRET_KEY` erzeugen:
```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

3. Container bauen und starten:
```bash
docker compose up -d --build
```

4. Panel unter `http://localhost:8000` aufrufen

### Installation mit Docker Run

Für manuelles Deployment:

```bash
docker run -d \
  --name rtmppanel \
  -e REQUIRE_LOGIN=True \
  -e USERNAME=admin \
  -e PASSWORD=supersecret \
  -e SECRET_KEY=generate-a-stable-random-secret \
  -e LRTMP2_API_URL=http://librtmp2-server:8080 \
  -e LRTMP2_API_TOKEN=your_api_token \
  -e LRTMP2_DOMAIN=localhost \
  -e LANG=de \
  -e TZ=Europe/Vienna \
  -e LRTMP2_RTMP_PORT=1935 \
  -e LRTMP2_APP=live \
  -e PANEL_DB_PATH=/data/panel.db \
  -v rtmppanel-data:/data \
  -p 8000:8000/tcp \
  alexanderwagnerdev/rtmppanel:latest
```

## ⚙️ Konfiguration

### Umgebungsvariablen

| Variable | Beschreibung | Standard | Erforderlich |
|----------|--------------|----------|--------------|
| `LRTMP2_API_URL` | librtmp2-server API-Endpunkt | - | Ja |
| `LRTMP2_API_TOKEN` | librtmp2-server API-Token | - | Ja |
| `LRTMP2_DOMAIN` | Domain oder IP für öffentliche RTMP-URLs | `localhost` | Ja |
| `LRTMP2_RTMP_PORT` | RTMP Listener-Port | `1935` | Nein |
| `LRTMP2_APP` | Standard-RTMP-App-Name | `live` | Nein |
| `REQUIRE_LOGIN` | Authentifizierung aktivieren (`True`/`False`) | `False` | Nein |
| `USERNAME` | Admin-Benutzername | `admin` | Bei Login |
| `PASSWORD` | Admin-Passwort | - | Bei Login |
| `SECRET_KEY` | Stabiles Flask Session-/Verschlüsselungs-Secret für gespeicherte Stream-Keys | - | Ja |
| `PANEL_DB_PATH` | SQLite-Datenbankpfad für gespeicherte Stream-Keys | `/data/panel.db` | Nein |
| `SESSION_COOKIE_SECURE` | Sichere Cookies verwenden, wenn HTTPS genutzt wird | `False` | Nein |
| `LANG` | Sprache der Oberfläche | `en` | Nein |
| `TZ` | Zeitzone | `UTC` | Nein |

Wichtig: `SECRET_KEY` muss stabil bleiben. Das Panel verschlüsselt lokal gespeicherte Stream-Keys damit. Wenn du es änderst, können bereits gespeicherte Keys unlesbar werden.

### Beispiel-Konfiguration

Minimale Einrichtung mit Authentifizierung:
```yaml
environment:
  REQUIRE_LOGIN: "True"
  USERNAME: "admin"
  PASSWORD: "supersecret"
  SECRET_KEY: "generate-a-stable-random-secret"
  LRTMP2_API_URL: "http://librtmp2-server:8080"
  LRTMP2_API_TOKEN: "mytoken123"
  LRTMP2_DOMAIN: "streaming.example.com"
```

## 🔧 Fehlerbehebung

### Verbindung zu librtmp2-server nicht möglich
- Überprüfe, ob `LRTMP2_API_URL` korrekt ist und vom Container aus erreichbar
- Prüfe, ob `LRTMP2_API_TOKEN` mit dem Token von librtmp2-server übereinstimmt
- Stelle sicher, dass librtmp2-server läuft und die HTTP-API aktiviert ist

### Login funktioniert nicht
- Überprüfe, ob `REQUIRE_LOGIN` auf `True` gesetzt ist
- Prüfe `USERNAME`, `PASSWORD` und `SECRET_KEY`
- Lösche Browser-Cache und Cookies

### Gespeicherte Stream-Keys sind nach Neustart nicht lesbar
- Stelle sicher, dass nach jedem Container-Neustart dasselbe `SECRET_KEY` verwendet wird
- Lass das `/data` Volume gemountet, damit `PANEL_DB_PATH=/data/panel.db` bestehen bleibt

### Container-Logs anzeigen
```bash
docker compose logs -f rtmppanel
```

## 📝 Lizenz

Dieser Docker-Wrapper ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

## 🤝 Support

Für Fragen, Probleme oder Feature-Requests:
- Öffne ein [Issue auf GitHub](https://github.com/AlexanderWagnerDev/rtmppanel-docker/issues)
- Prüfe bestehende Issues für Lösungen

## 🔗 Verwandte Projekte

- [librtmp2-server-panel](https://github.com/OpenRTMP/librtmp2-server-panel) - Der Upstream-Panel-Sourcecode, der beim Docker-Build geklont wird
- [librtmp2-server](https://github.com/OpenRTMP/librtmp2-server) - Der RTMP-Server, den dieses Panel verwaltet
