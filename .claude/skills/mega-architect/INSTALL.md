# Installation: Mega-Architect Skill

## Voraussetzungen

- Claude Code (CLI, Desktop-App oder Web/Cowork) mit Skill-Unterstützung.
- Ein Git-Repository als Arbeitsverzeichnis (empfohlen, aber nicht zwingend).
- Kein zusätzliches Paket/Dependency nötig – der Skill besteht ausschließlich aus
  Markdown-Dateien.

## Schritt 1: Ordnerstruktur anlegen

Falls noch nicht vorhanden, im Projekt-Root:

```bash
mkdir -p .claude/skills/mega-architect/modules
```

## Schritt 2: Dateien ablegen

Kopiere alle folgenden Dateien in `.claude/skills/mega-architect/`:

```
SKILL.md
README.md
INSTALL.md
EXAMPLES.md
TROUBLESHOOTING.md
modules/01-meta-cognitive.md
modules/02-business-os.md
modules/03-agent-team.md
modules/04-workflow-integrations.md
modules/05-passive-income.md
modules/06-deployment-hosting.md
modules/07-training-onboarding.md
```

Wenn dieser Skill bereits Teil eines Repositories ist (z.B. via `git clone` oder als
Teil dieses Projekts), ist dieser Schritt bereits erledigt.

## Schritt 3: Skill von Claude Code erkennen lassen

Claude Code liest Skills automatisch aus `.claude/skills/<name>/SKILL.md`. Ein Neustart
der Session ist normalerweise **nicht** nötig – neue Skills werden beim nächsten
Prompt erkannt. Falls der Skill nicht in der Skill-Liste auftaucht:

1. Prüfe, dass `SKILL.md` ein gültiges YAML-Frontmatter mit `name:` und `description:`
   hat (siehe oberster Abschnitt der Datei).
2. Starte eine neue Claude-Code-Session/Chat, damit der Skill-Index neu aufgebaut wird.
3. Prüfe mit dem `ListSkills`-Werkzeug (falls verfügbar), ob `mega-architect` gelistet
   wird.

## Globale Installation (personenbezogen, projektübergreifend)

Zusätzlich zur projektgebundenen Installation (`.claude/skills/mega-architect/` im
Repo) kannst du den Skill **global** installieren, damit er in *jedem* Projekt zur
Verfügung steht, nicht nur in diesem Repo:

```bash
mkdir -p ~/.claude/skills
cp -r .claude/skills/mega-architect ~/.claude/skills/mega-architect
```

Für den zugehörigen Slash-Command global installieren:

```bash
mkdir -p ~/.claude/commands
cp .claude/commands/mega-architect.md ~/.claude/commands/mega-architect.md
```

Danach ist `/mega-architect <anfrage>` in jeder neuen Session unter deinem
Benutzerkonto verfügbar, unabhängig vom aktuellen Projekt.

**Wichtiger Unterschied lokal vs. Remote-Umgebung (Claude Code on the web / Cowork):**

- Läuft Claude Code **lokal auf deinem eigenen Rechner**, ist `~/.claude/` dein echtes,
  dauerhaftes Home-Verzeichnis – eine globale Installation dort bleibt über alle
  Projekte und Sessions hinweg erhalten.
- Läuft die Session dagegen in einer **isolierten Remote-Umgebung** (Cloud-Container),
  ist `~/.claude/` das Home-Verzeichnis *dieses Containers* – es lebt nur für die
  Dauer dieser Umgebung/Session. Wird der Container neu erstellt (z.B. neue Umgebung,
  langer Leerlauf), geht eine dort global installierte Kopie verloren.
- **Verlässliche Quelle bleibt immer die Repo-Version** unter
  `.claude/skills/mega-architect/` und `.claude/commands/mega-architect.md` – die ist
  committed, gepusht und wird bei jedem `git clone`/jeder neuen Session dieses Repos
  automatisch wieder verfügbar. Die globale Installation ist eine Bequemlichkeits-
  Kopie zusätzlich dazu, kein Ersatz.
- Wer den Skill wirklich dauerhaft global auf dem eigenen Rechner nutzen will: die
  beiden `cp`-Befehle oben einmalig auf der eigenen Maschine ausführen (nicht nur
  innerhalb einer Remote-Session).

## Schritt 4: Zustandsordner (optional, wird automatisch angelegt)

Der Skill schreibt seine Reports standardmäßig nach `.claude/mega-architect/state/`.
Du kannst diesen Ordner vorab anlegen und z.B. der `.gitignore` hinzufügen, falls die
Reports nicht versioniert werden sollen:

```bash
mkdir -p .claude/mega-architect/state
echo ".claude/mega-architect/state/" >> .gitignore
```

Falls die Reports (Lessons Learned, Changelogs, Business-Reports) hingegen versioniert
und im Team geteilt werden sollen, lass sie einfach getrackt – dazu einfach den obigen
`.gitignore`-Schritt weglassen.

## Schritt 5: Skill testen

Stelle eine typische Auslöse-Anfrage, z.B.:

```
Mach eine Pre-Mortem-Analyse für ein geplantes Deployment auf einen neuen Server.
```

Claude sollte daraufhin Modul 2 (Proactive Pre-Mortem) aus
`modules/01-meta-cognitive.md` anwenden und einen `PRE_MORTEM.md`-Bericht erzeugen.

## Deinstallation

Um den Skill zu entfernen, genügt es, den Ordner zu löschen:

```bash
rm -rf .claude/skills/mega-architect
```

Bereits erzeugte State-Dateien unter `.claude/mega-architect/state/` bleiben davon
unberührt und können separat gelöscht werden, falls gewünscht.

## Aktualisierung

Da der Skill nur aus Markdown-Dateien besteht, reicht es, die geänderten Dateien zu
überschreiben. Es gibt keine Build- oder Kompilierungsschritte.
