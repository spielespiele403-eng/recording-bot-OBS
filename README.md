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

Kopiere `.env.example` zu `.env` und ersetze den Token:

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

**Wichtig:** `.env` enthält dein Geheim-Token und wird von Git ignoriert (siehe `.gitignore`) — lade diese Datei nie in ein Repo oder öffentlich hoch. Falls du dieses Repo aus einer älteren Version geklont hast, in der `.env` mit einem echten Token committet war: **generiere den Token sofort neu**, der alte gilt als kompromittiert.

### 4. config.json anpassen

Kopiere `config.example.json` zu `config.json` und fülle deine Werte ein:

```json
{
  "software": {
    "host": "DEINE_OBS_IP",
    "port": 4455,
    "password": "DEIN_OBS_WEBSOCKET_PASSWORT"
  },
  "chat": {
    "username": "DEIN_TWITCH_USERNAME",
    "allowed_roles": ["broadcaster", "moderator"]
  }
}
```

`allowed_roles` legt fest, wer `!rec`/`!stoprec` nutzen darf. Der Broadcaster darf immer, unabhängig von dieser Liste.

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
  A: Ja. Nur Broadcaster und Moderatoren (konfigurierbar über `allowed_roles` in `config.json`) dürfen `!rec`/`!stoprec` nutzen.

**F: Mehrere Kanäle?**  
A: Nein. Eine Installation = ein Channel.

**F: Szenen wechseln?**  
  A: Nicht in dieser Version. Nur Recording.

**F: Sicherheit?**  
  A: OAuth Token nicht public machen (`.env` ist in `.gitignore` und wird nie committet). `config.json` lokal halten. Die IRC-Verbindung läuft verschlüsselt über TLS (Port 6697). Chat-Commands sind auf Broadcaster/Mods beschränkt, damit nicht jeder Zuschauer deine Aufnahme steuern kann.

## Support

Falls nix funktioniert:

1. Command Prompt im Bot-Ordner öffnen
2. `python bot.py` tippen
3. `!rec` im Chat testen
4. Fehler im Fenster anschauen

---

**Bot funktioniert. Einfach den Schritten folgen.**
