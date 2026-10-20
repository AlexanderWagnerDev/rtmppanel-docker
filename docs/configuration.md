# Configuration / Konfiguration

Copy `.env.example` to `.env`, fill in the empty credentials, then run `docker compose config --quiet`.

| Variable | Meaning / Bedeutung | Default |
| --- | --- | --- |
| `LRTMP2_API_TOKEN` | Shared server and panel API token; 32–256 ASCII letters/digits, `-` or `_` | required |
| `SECRET_KEY` | Stable panel encryption/session secret; keep with panel database | required |
| `PANEL_PASSWORD` | Panel admin password / Admin-Passwort | required |
| `PANEL_USERNAME` | Panel admin username / Benutzername | admin |
| `REQUIRE_LOGIN` | Panel authentication / Anmeldung | True |
| `ALLOW_INSECURE_NO_LOGIN` | Required acknowledgement when disabling login / Freigabe ohne Anmeldung | 0 |
| `GUNICORN_WORKERS` | Worker processes; multiple workers require shared storage / Worker-Anzahl | 1 |
| `RATELIMIT_STORAGE_URI` | Session/rate-limit backend; use shared Redis for multiple workers | memory:// |
| `LRTMP2_API_URL` | Backend URL reached from the container, including custom port | http://host.docker.internal:8090 |
| `LRTMP2_STATS_URL` | Backend URL reached from the viewer's browser, including custom port | http://localhost:8090 |
| `LRTMP2_DOMAIN` | Public domain/IP used in stream URLs / Öffentliche Domain/IP | localhost |
| `RTMP_PORT` | Published RTMP port / Host-Port RTMP | 1935 |
| `RTMPPANEL_PORT` | Published panel port; internal panel stays on 8000 / Host-Port Panel | 8001 |
| `PANEL_LANG` | Interface language / Sprache | en |
| `TZ` | Container timezone / Zeitzone | UTC |
| `SESSION_COOKIE_SECURE` | Set True behind HTTPS / Bei HTTPS aktivieren | False |

Reuse the API token from the already-running backend. Generate only the encryption secret for a new panel using `openssl rand -hex 32`. Generate a new API token only when initializing a new backend and configure that same value on both sides. Choose a strong panel password. `.env` is local configuration and must not be committed. `LRTMP2_API_TOKEN` seeds a **new** server database; an existing database keeps its stored token. Use that token for the panel instead of generating another one. Keep `SECRET_KEY` unchanged when reusing the panel database, or stored stream keys cannot be decrypted.

Den vorhandenen Backend-API-Token übernehmen. Nur für ein neues Panel den Secret mit `openssl rand -hex 32` erzeugen; einen neuen API-Token nur bei der Initialisierung eines neuen Backends auf beiden Seiten identisch setzen. Ein starkes Passwort wählen. `.env` bleibt lokal. Eine bestehende Server-Datenbank behält ihren Token; diesen auch im Panel verwenden. Den `SECRET_KEY` bei bestehender Panel-Datenbank unverändert lassen, damit gespeicherte Stream-Keys entschlüsselt werden können.

## Storage and networking / Daten und Netzwerk

Compose uses project-prefixed named volumes for `/data`. Keep the project name stable (`docker compose -p NAME ...`) when updating. The shell installer uses volumes named `rtmp-server-data` and `rtmppanel-data` directly. Compose and the shell installer are separate deployment methods; do not run them over the same container names or switch without a data migration.

The server stack connects panel and backend through Docker DNS (`http://rtmp-server:8080`). The standalone panel uses `LRTMP2_API_URL` (default `http://host.docker.internal:8090`, Docker Engine 20.10+). For another host, set its reachable API URL. `localhost` inside the panel container refers to the panel itself.

Compose verwendet projektbezogene Volumes. Den Projektnamen bei Updates beibehalten. Shell-Installer und Compose sind getrennte Installationswege und verwenden unterschiedliche Volume-Namen; beim Wechsel Daten ausdrücklich migrieren. Im gemeinsamen Stack erreicht das Panel den Server über `rtmp-server:8080`; beim einzelnen Panel die vom Container erreichbare `LRTMP2_API_URL` setzen.

## Troubleshooting / Fehlerbehebung

- API errors: check `docker compose logs rtmp-server`, the API URL and shared token. Existing databases ignore a different token supplied through the environment.
- Panel refuses startup: configure a nonempty `SECRET_KEY`; verify `/data` is writable by the image's non-root user.
- Login: check `REQUIRE_LOGIN`, `PANEL_USERNAME`, `PANEL_PASSWORD` and HTTPS cookie settings.
- Existing host volume: back up first and make it writable for the image's `openrtmp` user. Do not make the database world-writable.
- Bei API-Fehlern URL, Token und Server-Logs prüfen; bei Login-Problemen Zugangsdaten und HTTPS-Cookies prüfen. Datenvolumes müssen für den Container-Benutzer schreibbar sein.

## Build from source / Selbst bauen

The application source is cloned from OpenRTMP during the image build. This branch retains its configured upstream revision:

```text
ARG PANEL_REPO=https://github.com/OpenRTMP/librtmp2-server-panel.git
ARG PANEL_REF=v0.1.10
```

From the cloned repository root:

```bash
docker build -t alexanderwagnerdev/rtmppanel:own .
```

Build arguments can override the repository/revision for local testing. The multi-platform publishing workflow remains manually dispatched; PR validation does not publish images. / Der Veröffentlichungs-Workflow bleibt manuell; PR-Prüfungen veröffentlichen keine Images.

## Standalone URLs and startup / URLs und Startkonfiguration

This standalone deployment does not publish or configure a backend API port. Set the full `LRTMP2_API_URL` for the existing server, for example `http://host.docker.internal:9190`. Set `LRTMP2_STATS_URL` independently, for example `https://stream.example.com` or `http://stream.example.com:9190`. Copied stats links use the latter; `host.docker.internal` is intended for container access and generally cannot be resolved by a remote viewer's browser. Replace the localhost example for remote viewers. RTMP_API_PORT is intentionally absent from this standalone template.

The default single Gunicorn worker works with `RATELIMIT_STORAGE_URI=memory://`. More workers require a shared session/rate-limit backend such as `redis://redis:6379/0` that you deploy separately; upstream rejects multiple workers with memory storage. Setting `REQUIRE_LOGIN=False` also requires `ALLOW_INSECURE_NO_LOGIN=1`; keep the acknowledgement at 0 unless deliberately disabling authentication. A nonempty panel password is still required by this Compose template.

Für einen eigenen Backend-Port die vollständige `LRTMP2_API_URL` ändern; eine separate Variable `RTMP_API_PORT` ist beim einzelnen Panel nicht vorgesehen. `LRTMP2_STATS_URL` muss für den Browser erreichbar sein und erhält die öffentliche Domain sowie gegebenenfalls den eigenen Port. Ein Worker funktioniert mit `memory://`; mehrere Worker benötigen ein gemeinsam genutztes Session-/Rate-Limit-Backend wie Redis. Zum bewussten Abschalten der Anmeldung zusätzlich zu `REQUIRE_LOGIN=False` auch `ALLOW_INSECURE_NO_LOGIN=1` setzen. Standardmäßig bleibt die Anmeldung aktiv.
