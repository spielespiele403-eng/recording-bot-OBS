# Teil 4 – Workflow-Integrationen

Diese 5 Module verankern den Mega-Skill im technischen Alltag: Git, CI/CD, Doku, Tests
und Security. Sie greifen auf Standard-Tools zurück (Bash/git, GitHub-MCP-Tools) statt
das Rad neu zu erfinden.

---

## 16. Git Integration

**Beschreibung**
Automatische Commits mit sinnvollen Messages, eine klare Branch-Strategie,
PR-Generierung und Changelog-Pflege.

**Anwendung**
1. Branch-Strategie (sofern das Repo keine eigene vorgibt – CLAUDE.md/README prüfen):
   `main` (stabil) / `develop` (Integration) / `feature/<kurzname>` (pro Aufgabe).
2. Commits: kleine, thematisch fokussierte Commits statt riesiger Sammel-Commits;
   Message beschreibt das WARUM, nicht nur das WAS (siehe Projekt-Konventionen im
   System-Prompt zu Git-Commits).
3. **Commits/Pushes nur nach expliziter User-Anfrage** – nie proaktiv committen, wenn
   nicht danach gefragt wurde (siehe Kernregeln der Session).
4. Pull-Request-Generierung: Titel kurz (<70 Zeichen), Body mit Summary + Testplan,
   existierendes PR-Template im Repo (`.github/pull_request_template.md` o.ä.) als
   Struktur übernehmen.
5. Changelog: bei nennenswerten Änderungen einen Eintrag in `CHANGELOG.md` nach
   [Keep a Changelog](https://keepachangelog.com/)-Konvention ergänzen (Added/Changed/
   Fixed/Removed).

**Output-Format** (`CHANGELOG.md`-Ausschnitt)
```markdown
## [Unreleased]
### Added
- Highlight-Detection-Modul für Auto-Clips.
### Fixed
- Rate-Limit-Bug im Discord-Cog.
```

**Beispiel**
> Feature-Branch `feature/highlight-clips`, 3 fokussierte Commits ("add ffmpeg peak
> detection", "add clip export", "add tests for clip export"), PR mit Testplan-Checkliste.

---

## 17. CI/CD Integration

**Beschreibung**
Generiert GitHub-Actions-Workflows, Dockerfiles, plant Deployment-Strategien und
überwacht den Build-Status.

**Anwendung**
1. Vorhandene CI prüfen (`.github/workflows/`), bevor etwas Neues angelegt wird –
   ergänzen statt duplizieren.
2. Minimaler, funktionierender Workflow zuerst (Lint + Test bei Push/PR), dann bei
   Bedarf erweitern (Build, Docker-Push, Deploy-Trigger).
3. Dockerfile nach Best Practices: schlankes Base-Image, Multi-Stage-Build wenn
   sinnvoll, kein Secrets im Image, `.dockerignore` pflegen.
4. Deployment-Strategie grob festhalten (z.B. "push zu main → Build → Deploy auf
   Staging automatisch, Produktion manuell bestätigt") – Produktions-Deploys laufen
   nie ohne explizite Freigabe automatisch.
5. Build-Status nach Push mit den GitHub-MCP-Tools (`actions_get`/`actions_list`)
   prüfen, wenn der User es verlangt oder eine PR-Überwachung aktiv ist.

**Output-Format** (`.github/workflows/ci.yml`, `Dockerfile`)
```yaml
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: pytest
```

**Beispiel**
> Für den Bot: CI führt `pytest` + `ruff check` bei jedem PR aus; Docker-Image wird nur
> bei Merge auf `main` gebaut und getaggt, Deploy bleibt manueller Schritt.

---

## 18. Documentation Module

**Beschreibung**
Generiert `README.md`, API-Dokumentation, User Guides und `CONTRIBUTING.md`.

**Anwendung**
1. Bestehende Doku nie kommentarlos überschreiben – ergänzen/aktualisieren, Struktur
   respektieren, wenn schon eine sinnvolle existiert.
2. README-Mindeststruktur: Was ist das Projekt, Installation, Nutzung/Quickstart,
   Konfiguration (Env-Vars), Beitrag leisten, Lizenz.
3. API-Doku direkt aus Code-Signaturen/Docstrings ableiten statt zu erfinden – bei
   Unklarheiten den Code lesen, nicht raten.
4. `CONTRIBUTING.md`: Setup-Schritte, Branch-/Commit-Konventionen (siehe Modul 16),
   Code-Style, wie PRs eingereicht werden.
5. Screenshots/Diagramme nur einfügen, wenn sie echten Mehrwert bringen (kein
   Deko-Auffüllen).

**Output-Format** (`README.md`-Grundgerüst)
```markdown
# <Projektname>

<Ein-Satz-Beschreibung>

## Installation
## Nutzung
## Konfiguration
## Contributing
## Lizenz
```

**Beispiel**
> Für den Recording-Bot: Abschnitt "Konfiguration" listet alle benötigten Discord-
> Bot-Permissions und Env-Vars (`DISCORD_TOKEN`, `WEBSOCKET_SECRET`, ...) tabellarisch.

---

## 19. Testing Module

**Beschreibung**
Generiert Unit-Tests, Integrationstests, plant E2E-Tests und führt Security-Scans durch
(Security-Scans im Detail siehe Modul 20).

**Anwendung**
1. Test-Framework des Projekts übernehmen (nicht ungefragt ein neues einführen).
2. Unit-Tests zuerst für Kernlogik ohne I/O (reine Funktionen), dann Integrationstests
   für Zusammenspiel (z.B. Bot-Command → DB), zuletzt E2E nur wenn es einen
   entsprechenden Rahmen gibt (z.B. Playwright bei Web-UI).
3. Edge Cases und Fehlerfälle testen, nicht nur den Happy Path.
4. Tests laufen lassen und Ergebnis zeigen, bevor der Task als fertig gemeldet wird –
   niemals ungetesteten Code als "fertig" ausgeben.
5. Bei UI-Änderungen zusätzlich real im Browser testen (siehe Session-Richtlinien),
   Test-Suiten ersetzen das nicht.

**Output-Format** (Kurzbericht nach Testlauf)
```
Tests: 24 passed, 0 failed (pytest, 3.2s)
Neue Tests: test_highlight_detection.py (Peak-Erkennung, leere Datei, korrupte Datei)
```

**Beispiel**
> Für die neue Highlight-Erkennung: Unit-Test mit synthetischem Audio-Peak,
> Integrationstest "Clip wird korrekt in Discord gepostet", Edge Case "Audiodatei ohne
> Peaks" (soll keinen Clip erzeugen, nicht crashen).

---

## 20. Security Module

**Beschreibung**
OWASP-Top-10-Scan, Dependency-Check, Secret-Scanning und Vulnerability-Reporting.

**Anwendung**
1. Vor jedem Deployment/PR mit sicherheitsrelevanten Änderungen (Auth, Datei-Uploads,
   DB-Queries, externe APIs) einen fokussierten Review gegen die OWASP-Top-10-Klassen
   durchführen (Injection, Broken Auth, Sensitive Data Exposure, SSRF, etc.).
2. Dependencies auf bekannte Schwachstellen prüfen (z.B. `pip-audit`, `npm audit`,
   oder GitHub-MCP-Tool `run_secret_scanning`/Dependabot-Hinweise, falls verfügbar).
3. Secret-Scanning: niemals Tokens/Keys/Passwörter im Klartext committen; vor jedem
   `git add`/Commit-Review prüfen, ob versehentlich Secrets enthalten sind (siehe
   Kernregeln zu sensiblen Dateien).
4. Befunde nach Schweregrad ordnen (kritisch/hoch/mittel/niedrig) mit konkretem
   Reproduktionsschritt und Fix-Vorschlag – keine vagen "könnte unsicher sein"-Aussagen
   ohne Beleg.
5. Kritische Findings sofort melden, nicht bis zum Report-Ende zurückhalten.

**Output-Format** (Security-Report, z.B. `SECURITY_REPORT.md`)
```markdown
# Security Report: <Scope>

| Schweregrad | Finding | Ort | Reproduktion | Fix-Vorschlag |
|---|---|---|---|---|
| Kritisch | ... | `bot.py:120` | ... | ... |

## Dependency-Check
| Paket | Version | Bekannte CVE | Empfehlung |
|---|---|---|---|

## Secret-Scan
Ergebnis: keine Secrets gefunden / X Funde (Details)
```

**Beispiel**
> Finding: WebSocket-Endpunkt akzeptiert Verbindungen ohne Auth-Token-Prüfung
> (`bot.py:87`) → kritisch, da beliebige Clients Recording-Daten abgreifen könnten.
> Fix: Token aus `.env` vor Verbindungsannahme validieren.
