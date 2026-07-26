# YouTube Boost – Smart Recommendations

Browser-Erweiterung (Chrome/Edge, Manifest V3) für YouTube-Nutzer mit
Empfehlungsfilter, Watch-Time-Tracker, Playlist-Manager und einer dezenten,
CPM-basierten Werbefläche inkl. Admin-Dashboard.

## Funktionen

- **Empfehlungsfilter**: Blendet Videos nach Stichwort- oder Kanal-Blockliste
  aus der Startseite, den Suchergebnissen und der „Nächstes Video"-Leiste aus.
- **Watch-Time-Tracker**: Zeigt im Popup, wie viel Zeit heute, diese Woche
  und insgesamt mit YouTube-Videos verbracht wurde.
- **Playlist-Manager**: Eigene Playlists direkt im Popup anlegen und
  Videos von der aktuellen Watch-Seite hinzufügen.
- **Werbefläche**: Kleine, schließbare Sidebar-Karte auf YouTube-Seiten,
  max. 1–2 Einblendungen pro Sitzung (konfigurierbar).
- **Admin-Dashboard**: Anzeigen anlegen/bearbeiten/löschen, Impressionen,
  Klicks und geschätzte Einnahmen einsehen, CSV-Export.

Alle Daten (Watch-Time, Playlists, Anzeigen-Statistiken) werden ausschließlich
lokal im Browser über die `chrome.storage.local`-API gespeichert – es gibt
keine externen Server-Aufrufe und keine Abhängigkeiten von Drittanbieter-
Bibliotheken.

## Installation (Entwicklermodus / unverpackt laden)

Da die Erweiterung nicht im Chrome Web Store veröffentlicht ist, wird sie als
„entpackte Erweiterung" geladen:

1. **ZIP entpacken**: `youtube-boost-addon.zip` an einem festen Ort
   entpacken (z. B. `Dokumente/youtube-boost-addon`). Der Ordner sollte
   danach direkt `manifest.json` enthalten.
2. **Erweiterungsseite öffnen**:
   - Chrome: `chrome://extensions` in die Adresszeile eingeben
   - Edge: `edge://extensions` in die Adresszeile eingeben
3. **Entwicklermodus aktivieren**: Schalter oben rechts („Entwicklermodus" /
   „Developer mode") aktivieren.
4. **„Entpackt laden" / „Load unpacked"** klicken und den entpackten Ordner
   auswählen.
5. Die Erweiterung erscheint jetzt in der Symbolleiste. Ggf. über das
   Puzzle-Symbol anheften.
6. **YouTube öffnen** (youtube.com) – Empfehlungsfilter und Watch-Time-Tracker
   starten automatisch.

### Erste Schritte nach der Installation

1. Auf das Erweiterungssymbol klicken → Tab **„Filter"**.
2. Blockierte Stichwörter/Kanäle eintragen (kommagetrennt) und
   **Speichern** klicken.
3. Tab **„Watch-Time"** zeigt ab jetzt die getrackte Zeit.
4. Tab **„Playlists"** → Playlist anlegen, auf einem YouTube-Video das
   Popup öffnen und **„＋ Video"** klicken, um es hinzuzufügen.
5. Über **„Admin-Dashboard öffnen"** (unten im Popup) gelangst du zur
   Anzeigenverwaltung.

## Admin-Dashboard nutzen

1. Im Popup unten auf **„Admin-Dashboard öffnen"** klicken (öffnet die
   Options-Seite der Erweiterung).
2. **„+ Neue Anzeige"** klicken, Titel, Text, optionale Bild-URL, Ziel-Link
   und CPM eintragen, speichern.
3. Anzeigen können jederzeit **pausiert**, **bearbeitet** oder **gelöscht**
   werden.
4. Oben werden Gesamt-Impressionen, Gesamt-Klicks, durchschnittliche CTR und
   geschätzte Einnahmen (Impressionen ÷ 1000 × CPM) angezeigt.
5. **„CSV-Export"** lädt eine Tabelle mit allen Anzeigen-Kennzahlen herunter
   (z. B. für Reports an Werbekunden, siehe `business-docs/`).

## FAQ

**Die Erweiterung lässt sich nicht laden – „Manifest file is missing or
unreadable".**
→ Stelle sicher, dass du beim „Entpackt laden" den Ordner auswählst, der
direkt `manifest.json` enthält (nicht einen übergeordneten Ordner oder die
ZIP-Datei selbst).

**Nach einem Chrome-Update ist die Erweiterung deaktiviert.**
→ Bei „Entpackt geladenen" Erweiterungen kann Chrome nach Updates erneut
nachfragen. Unter `chrome://extensions` einfach wieder aktivieren.

**Die Werbe-Sidebar erscheint nicht.**
→ Prüfe im Popup unter „Filter", ob „Anzeigen im Sidebar anzeigen" aktiviert
ist, und ob im Admin-Dashboard mindestens eine **aktive** Anzeige existiert.

**Watch-Time zählt nicht hoch.**
→ Die Zeit wird nur gezählt, während ein Video tatsächlich läuft (nicht
pausiert) und der Tab im Vordergrund ist. Werte werden alle 15–30 Sekunden
gespeichert, nicht live pro Sekunde im Popup.

**Playlists sind nach einem Neustart des Browsers weg.**
→ Sollte nicht passieren, da `chrome.storage.local` browserübergreifend
persistent ist. Prüfe, ob im Inkognito-Modus gearbeitet wurde (dort ist die
Erweiterung standardmäßig deaktiviert) oder ob die Erweiterung zwischenzeitlich
entfernt und neu geladen wurde (das löscht den lokalen Speicher).

**Kann ich die Erweiterung im Chrome Web Store veröffentlichen?**
→ Ja, dafür ist ein Entwicklerkonto sowie zusätzlich eine
Datenschutzerklärung erforderlich (auch wenn keine Daten das Gerät
verlassen, verlangt der Store eine Erklärung zur Datennutzung). Die
Werbefunktion muss klar als „Anzeige" gekennzeichnet sein – dies ist im
aktuellen Design bereits über die Kennzeichnung „Anzeige" in der Sidebar
umgesetzt. Vor der Einreichung die aktuellen
[Chrome Web Store Program Policies](https://developer.chrome.com/docs/webstore/program-policies)
prüfen, insbesondere die Abschnitte zu Werbe-Anzeigen und Nutzerdaten.

**Werden Nutzerdaten irgendwohin übertragen?**
→ Nein. Alle Daten (Filtereinstellungen, Watch-Time, Playlists,
Anzeigen-Statistiken) bleiben lokal im Browser. Es gibt keinerlei
Netzwerk-Requests im Code der Erweiterung.

## Ordnerstruktur

```
youtube-boost-addon/
├── manifest.json
├── background.js        # Service Worker: zentrale Speicherlogik
├── content.js            # Läuft auf youtube.com: Filter, Tracker, Ad-Sidebar
├── content.css
├── icons/
├── popup/                 # Toolbar-Popup (Nutzer-Ansicht)
│   ├── popup.html
│   ├── popup.css
│   └── popup.js
└── dashboard/              # Admin-Dashboard (Anzeigenverwaltung)
    ├── dashboard.html
    ├── dashboard.css
    └── dashboard.js
```

## Business-Dokumente

Geschäftsplan, Verkaufs-E-Mails, Vertragsvorlage, Preisliste, Marketing-Plan
und Monetarisierungs-Strategie liegen im Ordner [`../business-docs`](../business-docs).
