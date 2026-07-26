# Teil 7 – Training & Onboarding Module

Diese 2 Module sorgen dafür, dass sowohl Endnutzer als auch das eigene Team das
Produkt tatsächlich nutzen und weiterentwickeln können.

---

## 29. User Onboarding

**Beschreibung**
Erstellt einen Onboarding-Flow, Tutorials und eine FAQ für Endnutzer.

**Anwendung**
1. Den kürzesten Weg zum "Aha-Moment" definieren (erste erfolgreiche Nutzung des
   Kernfeatures) – Onboarding so kurz wie möglich halten, nicht jede Funktion vorab
   erklären.
2. Onboarding-Flow in Schritte gliedern (z.B. Bot einladen → Berechtigung erteilen →
   ersten Befehl ausführen → Ergebnis sehen).
3. Tutorial-Inhalte (Text/Schritt-für-Schritt, ggf. Screenshots-Platzhalter) für die
   wichtigsten 2-3 Use-Cases erstellen, nicht für jede Randfunktion.
4. FAQ aus echten wiederkehrenden Fragen ableiten (Support-Tickets, Discord, siehe
   Modul 24 Feedback) statt erfundener Fragen.

**Output-Format** (`ONBOARDING_GUIDE.md`)
```markdown
# Onboarding Guide: <Produkt>

## Onboarding-Flow
1. Schritt – Ziel: ...
2. Schritt – Ziel: ...

## Tutorials
### <Use-Case 1>
...

## FAQ
**F: ...**
A: ...
```

**Beispiel**
> Onboarding-Flow für den Bot: `/invite` → Bot bekommt Sprachkanal-Berechtigung →
> `/record start` → Nutzer sieht sofort Bestätigung + Speicherort des Mitschnitts.

---

## 30. Team Training

**Beschreibung**
Erstellt Trainingsmaterialien, plant Workshops und baut eine Knowledge-Base für das
eigene (Entwicklungs-)Team auf.

**Anwendung**
1. Zielgruppe des Trainings klären (neue Entwickler, Support-Team, Stakeholder) – Inhalt
   und Tiefe entsprechend anpassen.
2. Trainingsmaterial aus vorhandener Doku ableiten (README, `CONTRIBUTING.md`,
   `LESSONS_LEARNED.md`), nicht parallel neu erfinden – Redundanz vermeiden, stattdessen
   verlinken.
3. Workshop-Struktur vorschlagen (Dauer, Agenda, Hands-on-Übung) statt reiner Theorie.
4. Knowledge-Base als lebendes Dokument behandeln, das bei neuen Erkenntnissen
   (insbesondere aus Modul 1, Self-Reflection) ergänzt wird.

**Output-Format** (`TRAINING_PLAN.md`)
```markdown
# Training Plan: <Zielgruppe>

## Lernziele
## Trainingsmaterial (verlinkt auf bestehende Docs)
## Workshop-Agenda
| Zeit | Thema | Format |
|---|---|---|

## Knowledge-Base-Struktur
- Verweis auf: README.md, CONTRIBUTING.md, LESSONS_LEARNED.md
```

**Beispiel**
> Onboarding-Workshop für neue Mitwirkende: 60 Minuten – 15 Min Architektur-Überblick
> (aus CTO-Doku, Modul 12), 15 Min Branch-/Commit-Konventionen (Modul 16), 30 Min
> Hands-on: ersten kleinen Bugfix selbst umsetzen.
