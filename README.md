# RTMPPanel 🎥

[![Docker Hub](https://img.shields.io/docker/pulls/alexanderwagnerdev/rtmppanel?style=flat-square)](https://hub.docker.com/r/alexanderwagnerdev/rtmppanel)
[![License](https://img.shields.io/github/license/AlexanderWagnerDev/rtmppanel-docker?style=flat-square)](LICENSE)

Docker wrapper for the web control panel from OpenRTMP/librtmp2-server-panel.

Branch: **main** · Server image: `alexanderwagnerdev/rtmp-server:latest` · Panel image: `alexanderwagnerdev/rtmppanel:latest`.

## ✨ Features

- OpenRTMP HTTP API, stream management and live statistics
- RTMPPanel with configurable authentication
- Persistent SQLite data and a stable panel encryption secret
- Docker Hub/GHCR images and Docker Compose deployment

## 🚀 Quick Start

The [stream-relay-installer](https://github.com/AlexanderWagnerDev/stream-relay-installer/tree/main) offers guided setup and service management. Docker Engine 20.10+ and Docker Compose v2 are required for the examples. A running OpenRTMP backend and its API token are required.

### Docker Compose

```bash
git clone --branch main https://github.com/AlexanderWagnerDev/rtmppanel-docker.git
cd rtmppanel-docker
cp .env.example .env
# Edit .env: API token, stable SECRET_KEY, password and public domain.
# Reuse the running backend's API token; do not generate a panel-only token.
# Generate SECRET_KEY for a NEW panel only: openssl rand -hex 32
docker compose config --quiet
docker compose up -d
```

Panel: `http://localhost:8001`. Set `LRTMP2_API_URL` to your running backend as reached from the container, and `LRTMP2_STATS_URL` to its browser-reachable base URL (including any custom port).

## 📖 Usage

Create streams in RTMPPanel and copy the provided publish, playback and statistics URLs. Publishing and playback keys may differ. The default application is `live`; freely chosen nginx `/publish/key` URLs do not create streams.

```bash
docker compose ps
docker compose logs -f rtmppanel
```

## 🔌 Ports

| Service | Host | Container | Protocol |
| --- | --- | --- | --- |
| RTMP | 1935 | 1935 | TCP |
| RTMP API | 8090 | 8080 | TCP |
| RTMPPanel | 8001 | 8000 | TCP |

Only the panel port is published by this standalone Compose file; backend ports belong to the separately deployed server.

## ⚙️ Configuration and storage

See [configuration](docs/configuration.md) for all environment settings, networking, storage and troubleshooting, and [migration](docs/migration.md) for the nginx transition. Copy `.env.example`, reuse the backend token, configure the panel credentials, and keep `.env` and volume backups private. The panel `SECRET_KEY` must stay unchanged across updates.

## 🔄 Updates

```bash
docker compose pull
docker compose up -d
```

Retain the same Compose project name, `.env` and named volumes. Do not combine a Compose deployment with a shell-installer deployment using the same names/ports. `docker compose down -v` deletes stored data.

## 📦 Built With / Related Projects

- [OpenRTMP/librtmp2-server](https://github.com/OpenRTMP/librtmp2-server)
- [OpenRTMP/librtmp2-server-panel](https://github.com/OpenRTMP/librtmp2-server-panel)
- [RTMP server Docker](https://github.com/AlexanderWagnerDev/rtmp-server-docker)
- [RTMPPanel Docker](https://github.com/AlexanderWagnerDev/rtmppanel-docker)
- [SRTLA server Docker](https://github.com/AlexanderWagnerDev/srtla-server-docker)
- [SLSPanel Docker](https://github.com/AlexanderWagnerDev/slspanel-docker)

## 📄 License

See [LICENSE](LICENSE). Upstream components retain their respective licenses.

---

# RTMPPanel 🎥 (Deutsch)

Branch **main**: OpenRTMP-Server mit RTMPPanel, persistenten Daten und konfigurierbarer Anmeldung. Die Struktur folgt SRTLA-Server und SLSPanel: Compose-Datei, Umgebungsbeispiel, Konfiguration, Fehlerbehebung und Projektlinks.

## 🚀 Schnellstart

Den oben gezeigten Branch klonen, `.env.example` nach `.env` kopieren und API-Token, festen `SECRET_KEY`, Passwort und öffentliche Domain eintragen. Den vorhandenen API-Token des laufenden Backends übernehmen. Nur für ein neues Panel den `SECRET_KEY` mit `openssl rand -hex 32` erzeugen; bei bestehender Panel-Datenbank dessen bisherigen Secret behalten. Danach `docker compose config --quiet` und `docker compose up -d` ausführen.

Das einzelne Panel benötigt einen laufenden OpenRTMP-Server. Dessen vom Container erreichbare `LRTMP2_API_URL` und vorhandenen Token in `.env` eintragen. Für kopierte Statistik-Links die im Browser erreichbare `LRTMP2_STATS_URL` einschließlich eines eigenen Ports setzen.

## 📖 Verwendung und Konfiguration

Das Panel läuft standardmäßig auf Port **8001**, die RTMP-API auf **8090**, RTMP auf **1935**. Streams im Panel anlegen und die dort angezeigten Sende-, Wiedergabe- und Statistik-URLs verwenden. Sende- und Wiedergabe-Keys können verschieden sein.

[Konfiguration und Fehlerbehebung](docs/configuration.md) · [Migration von nginx](docs/migration.md)

Bei Updates `.env`, denselben Compose-Projektnamen, Datenvolumes und den festen `SECRET_KEY` behalten. `docker compose down -v` löscht Daten. Den interaktiven Installer und Compose als getrennte Installationswege behandeln; beim Wechsel Daten ausdrücklich migrieren.

## 📄 Lizenz

Details siehe [LICENSE](LICENSE).
