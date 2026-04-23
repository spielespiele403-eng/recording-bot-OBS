# OBS Recording Bot - Twitch Chat Integration

Steuere deine OBS Aufnahmen direkt aus dem Twitch Chat.

## Was der Bot macht

Mit einfachen Chat-Commands kontrollierst du deine OBS-Aufnahmen:

```
!rec        → Aufnahme starten
!stoprec    → Aufnahme stoppen
```

Der Bot verbindet sich automatisch mit deiner OBS und deinem Twitch-Kanal.

## Voraussetzungen

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **OBS Studio** mit aktivem WebSocket Server
- **Twitch OAuth Token** ([Generator](https://twitchtokengenerator.com/))

## Installation

### 1. Python installieren

1. [python.org/downloads](https://www.python.org/downloads/) aufrufen
2. Python 3.9+ downloaden und starten
3. **WICHTIG:** Häkchen bei "Add Python to PATH"
4. "Install Now"

Prüfung in Command Prompt:
```
python --version
```

### 2. Bot-Dateien

Erstelle einen Ordner und lege folgende Dateien rein:

```
dein-bot-ordner/
├── START.bat
├── bot.py
├── .env
└── config.json
```

### 3. .env konfigurieren

Öffne `.env` mit Editor und ersetze den Token:

```
TWITCH_BOT_OAUTH=DEIN_TOKEN_HIER
```

Token holen:
1. [twitchtokengenerator.com](https://twitchtokengenerator.com/)
2. Dein Account
3. Permissions: "chat:read", "chat:edit"
4. Generieren
5. In `.env` eintragen

Speichern (Ctrl+S)

### 4. config.json anpassen

Öffne `config.json` und fülle deine Werte ein:

```json
{
  "software": {
    "host": "DEINE_OBS_IP",
    "port": 4455,
    "password": "DEIN_OBS_WEBSOCKET_PASSWORT"
  },
  "chat": {
    "username": "DEIN_TWITCH_USERNAME"
  }
}
```

**Wie du deine OBS-Daten findest:**

1. OBS öffnen
2. Werkzeuge → WebSocket Server Einstellungen
3. Dort findest du:
   - Server-IP (Geschätzt) → host
   - Serverport → port (meist 4455)
   - Serverpasswort → password

### 5. OBS WebSocket Setup

Das ist wichtig!

1. OBS öffnen
2. Werkzeuge → WebSocket Server Einstellungen
3. **Häkchen setzen bei:** "WebSocket-Server aktivieren"
4. **JA Häkchen bei:** "Authentifizierung aktivieren" (!)
5. OK

### 6. Bot starten

Doppelklick auf `START.bat`

Du solltest sehen:
```
[OBS] Connected
[IRC] Connected
[BOT] Ready
```

**Fertig!** 🚀

## Nutzung

Schreib im Twitch Chat:

```
!rec
```

Bot antwortet: "Recording started"

OBS nimmt auf.

Zum Stoppen:
```
!stoprec
```

## Troubleshooting

### "[OBS] Failed: Connection refused"

- OBS läuft?
- WebSocket Server aktiv? (Werkzeuge → WebSocket Server Einstellungen)
- IP und Port korrekt in config.json?
- Passwort korrekt?

### "Command funktioniert nicht"

- Bot läuft noch? (Fenster offen?)
- Im richtigen Twitch Channel?
- `!rec` klein geschrieben?

### Bot startet nicht

- Python installiert? (`python --version` in cmd)
- Alle 4 Dateien im gleichen Ordner?
- START.bat doppelklicken

### Bot-Fenster schließt sofort

Rechtsklick auf START.bat → "Als Administrator ausführen"

## Dateien

| Datei | Zweck |
|-------|-------|
| `START.bat` | Bot starten |
| `bot.py` | Bot Code |
| `.env` | Twitch Token (geheim!) |
| `config.json` | OBS Einstellungen |

## Performance

- RAM: ~50MB
- CPU: <1%
- Uptime: 24/7 stabil

Bot kann Tage laufen ohne Probleme.

## FAQ

**F: Nur Mods dürfen Commands?**  
  A: Nein noch alle, aber wird alles gemacht .

**F: Mehrere Kanäle?**  
A: Nein. Eine Installation = ein Channel.

**F: Szenen wechseln?**  
  A: Nicht in dieser Version. Nur Recording.

**F: Sicherheit?**  
  A: OAuth Token nicht public machen. config.json lokal halten.

## Support

Falls nix funktioniert:

1. Command Prompt im Bot-Ordner öffnen
2. `python bot.py` tippen
3. `!rec` im Chat testen
4. Fehler im Fenster anschauen

---

**Bot funktioniert. Einfach den Schritten folgen.**
