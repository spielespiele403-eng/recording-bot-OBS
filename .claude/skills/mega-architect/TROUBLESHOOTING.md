# Troubleshooting: Mega-Architect Skill

## Der Skill triggert nicht / Claude ignoriert ihn

**Mögliche Ursachen:**
- Die Anfrage ist zu simpel/isoliert (z.B. ein Ein-Zeilen-Fix) – das ist **beabsichtigt**,
  siehe `SKILL.md`: "Sprich diesen Skill NICHT für triviale Ein-Zeilen-Fixes an."
- Der Skill-Ordner ist nicht am erwarteten Pfad (`.claude/skills/mega-architect/SKILL.md`).
- Das YAML-Frontmatter in `SKILL.md` ist fehlerhaft (z.B. fehlende Anführungszeichen,
  falsche Einrückung).

**Lösung:**
1. Pfad prüfen: `ls .claude/skills/mega-architect/SKILL.md`.
2. Frontmatter validieren (muss mit `---` beginnen/enden, `name:` und `description:`
   enthalten).
3. Skill explizit ansprechen: `Nutze den mega-architect Skill für: ...`
4. Neue Session starten, falls der Skill kürzlich hinzugefügt wurde.

## Zu viele Module werden geladen / Kontext läuft schnell voll

**Ursache:** Modul 4 (Context Budgeting) wurde nicht befolgt – z.B. wurde für eine
einfache Aufgabe "Full-Context" statt "Lean-Context" gewählt.

**Lösung:**
- Explizit einschränken: "Nutze nur Modul X, nicht das ganze Agent-Team."
- In `LESSONS_LEARNED.md` als Muster vermerken, wenn das wiederholt passiert – Modul 5
  (Self-Improvement Engine) soll das künftig automatisch vermeiden.
- Bei sehr großen Projekten: State-Dateien (`ORCHESTRATION_LOG.md` etc.) regelmäßig
  kürzen/archivieren, damit sie selbst nicht zum Kontext-Ballast werden.

## Reports/State-Dateien werden überschrieben statt ergänzt

**Ursache:** Ein Modul, das eigentlich ein Log ist (`LESSONS_LEARNED.md`,
`SKILL_CHANGELOG.md`, `ORCHESTRATION_LOG.md`), wurde versehentlich komplett neu
geschrieben statt am Ende ergänzt.

**Lösung:**
- Vor dem Schreiben immer kurz die bestehende Datei lesen/anhängen (siehe Hinweis in
  `SKILL.md`, Abschnitt "Zustandsdateien").
- Falls es doch passiert ist: `git diff`/`git log -p` nutzen, um den vorherigen Inhalt
  wiederherzustellen, dann den neuen Eintrag anhängen statt ersetzen.

## Agent-Team-Module (CEO/CTO/CPO/CMO/CFO) erzeugen widersprüchliche Ergebnisse

**Das ist kein Bug, sondern beabsichtigt** – siehe Modul 11 (CEO Agent): Konflikte
zwischen Rollen (z.B. CTO-Zeitschätzung vs. CFO-Budget) sollen explizit benannt werden,
nicht versteckt. Der CEO-Agent soll die Optionen aufzeigen, nicht künstlich glätten.

**Wenn die Zusammenfassung fehlt:** explizit anfragen: "Fass die Ergebnisse der Rollen
als CEO zusammen und zeig mir Konflikte."

## Ein Modul schlägt eine riskante Aktion vor (Deploy, Domain-Kauf, Post veröffentlichen)

**Das ist beabsichtigt begrenzt:** Alle Module in Kategorie 5 (Passive Income) und 6
(Deployment & Hosting) planen nur – sie führen nichts automatisch aus. Wenn Claude
dennoch eine solche Aktion ohne Rückfrage ausführen will, weise explizit auf `SKILL.md`
Regel 6 hin ("Destruktive/riskante Aktionen laufen NIE automatisch") und bitte um
Bestätigungsschritt.

## Business-Reports enthalten offensichtlich erfundene Zahlen

**Ursache:** Ohne Web-/Datenzugriff kann Claude reale Marktdaten nicht recherchieren.

**Lösung:**
- Prüfen, ob Zahlen explizit als "Annahme" gekennzeichnet sind (das ist vorgeschrieben,
  siehe `modules/02-business-os.md`, Einleitung).
- Falls nicht: Claude bitten, alle unbelegten Zahlen als Annahme zu kennzeichnen oder
  durch eine Bandbreite/Methodik-Beschreibung zu ersetzen.
- Bei Bedarf echte Datenquellen (eigene Analytics, CSV-Exporte) bereitstellen, damit
  Modul 9 (Analytics) mit echten Daten arbeiten kann.

## Neue Sub-Skills/Module werden ungefragt angelegt

**Ursache:** Modul 5 (Self-Improvement Engine) sollte strukturelle Änderungen (neue
Dateien/Module) nur *vorschlagen*, nicht automatisch umsetzen.

**Lösung:** Falls doch automatisch umgesetzt, das als Regelverstoß zurückmelden – Claude
soll strukturelle Änderungen künftig erst in `SKILL_CHANGELOG.md` als Vorschlag
festhalten und auf Bestätigung warten.

## Der Skill kollidiert mit einem anderen installierten Skill (z.B. `skill-creator`,
`review`, `run`)

**Lösung:** Kein Konflikt zu erwarten, da Mega-Architect andere Skills referenziert
(Modul 3, Dynamic Skill Orchestration), aber nicht überschreibt. Falls Claude
unsicher ist, welcher Skill führen soll, explizit sagen: "Nutze zuerst
`mega-architect`, um zu orchestrieren, welche anderen Skills sinnvoll sind."

## Ich will die generierten State-Dateien nicht im Git-Repo haben

Siehe `INSTALL.md`, Schritt 4 – füge `.claude/mega-architect/state/` zur `.gitignore`
hinzu.
