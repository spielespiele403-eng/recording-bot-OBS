# Teil 1 – Meta-Cognitive Architect (Kern-Skill)

Diese 5 Module bilden das "Gehirn" des Mega-Skills: Sie sorgen dafür, dass Claude Code
aus Erfahrung lernt, Risiken vorhersieht, sich selbst orchestriert, Kontext bewusst
einsetzt und sich selbst verbessert.

---

## 1. Self-Reflection & Learning Loop

**Beschreibung**
Nach jedem abgeschlossenen Task (nicht nach jedem einzelnen Tool-Call!) führt Claude
eine kurze automatische Retrospektive durch und speichert die Erkenntnisse dauerhaft.

**Anwendung**
1. Task abschließen wie gewohnt.
2. Kurz reflektieren:
   - **Was war gut?** (Ansatz, Reihenfolge, Tool-Wahl, die funktioniert hat)
   - **Was war schlecht?** (Umwege, falsche Annahmen, unnötige Rückfragen, Fehler)
   - **Was hätte besser sein können?** (konkreter, umsetzbarer Verbesserungsvorschlag)
3. Vor dem Schreiben neuer Learnings: bestehende `LESSONS_LEARNED.md` kurz überfliegen
   (letzte 20-30 Zeilen reichen), um Wiederholungen zu vermeiden und Muster zu erkennen.
4. Eintrag am Ende von `.claude/mega-architect/state/LESSONS_LEARNED.md` anhängen
   (niemals überschreiben).
5. **Muster-Erkennung**: Wenn derselbe Fehlertyp zum 2. oder 3. Mal auftaucht, das
   explizit als "Wiederkehrendes Muster" markieren und in einem eigenen Abschnitt
   "Aktive Regeln" oben in der Datei zusammenfassen (diese Regeln liest Claude künftig
   VOR ähnlichen Tasks, siehe Schritt 6).
6. **Anwendung auf künftige Tasks**: Bei einem neuen, ähnlichen Task zuerst die "Aktiven
   Regeln" aus `LESSONS_LEARNED.md` lesen und aktiv befolgen, bevor der Task beginnt.

**Output-Format** (`LESSONS_LEARNED.md`)
```markdown
# Lessons Learned

## Aktive Regeln (aus wiederkehrenden Mustern)
- [2026-07-20] Immer `.env.example` aktualisieren, wenn neue Env-Var eingeführt wird.
- [2026-07-22] Vor DB-Migrationen zuerst lokal testen, nie direkt gegen Remote.

## Log

### 2026-07-26 – Task: <Kurzbeschreibung>
- **Gut:** <...>
- **Schlecht:** <...>
- **Besser wäre gewesen:** <...>
- **Muster erkannt?** ja/nein – <Beschreibung>
```

**Beispiel**
> Task: "Füge Rate-Limiting zum Discord-Bot hinzu."
> Retro: Gut war die Nutzung von `discord.py`'s eingebautem Cooldown. Schlecht war,
> dass zunächst ein eigenes Rate-Limiting gebaut wurde, obwohl die Library das schon
> kann – Zeit verschwendet. Besser: vor Custom-Code immer kurz prüfen, ob das Framework
> es nativ anbietet. → Wird als aktive Regel gespeichert.

---

## 2. Proactive Pre-Mortem

**Beschreibung**
Vor jedem komplexen, teuren oder schwer umkehrbaren Task simuliert Claude im Voraus ein
Scheitern ("Stell dir vor, dieser Task ist in 3 Monaten grandios gescheitert – warum?")
und leitet daraus Gegenmaßnahmen ab.

**Wann anwenden**: neue Architektur, Produkt-Launch, Deployment in Produktion,
Preis-/Business-Entscheidung, Migration, alles mit hohem Blast-Radius. NICHT für
Routine-Fixes.

**Anwendung**
1. Task kurz zusammenfassen.
2. Risiken in 3 Kategorien sammeln:
   - **Technisch** (Bugs, Skalierung, Sicherheitslücken, Datenverlust, Abhängigkeiten)
   - **Business** (keine Nachfrage, falsche Zielgruppe, Konkurrenz, rechtliche Risiken)
   - **Zeit** (Scope Creep, Unterschätzung, Blocker durch Dritte, Deadline-Druck)
3. Jedes Risiko bewerten: Wahrscheinlichkeit (niedrig/mittel/hoch) × Auswirkung
   (niedrig/mittel/hoch).
4. Für jedes Risiko mit mittlerer/hoher Kombination eine konkrete vorbeugende Maßnahme
   vorschlagen.
5. Bericht schreiben, dann erst mit der eigentlichen Umsetzung beginnen.

**Output-Format** (`PRE_MORTEM.md`)
```markdown
# Pre-Mortem: <Task-Name>
Datum: <YYYY-MM-DD>

## Annahme
Wir nehmen an, dieser Task ist gescheitert. Warum?

## Risiken

### Technisch
| Risiko | Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|---|---|---|---|
| ... | mittel | hoch | ... |

### Business
| Risiko | Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|---|---|---|---|

### Zeit
| Risiko | Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|---|---|---|---|

## Fazit
Go / Go mit Anpassungen / No-Go, plus Begründung in 1-2 Sätzen.
```

**Beispiel**
> Task: "Deploy des Bots auf einen neuen Cloud-Server."
> Technisch: Discord-Token könnte falsch konfiguriert sein → vorher `.env` gegen
> `.env.example` prüfen. Business: n/a. Zeit: DNS-Propagation kann Stunden dauern →
> das vorher einplanen, nicht am Launch-Tag selbst.

---

## 3. Dynamic Skill Orchestration

**Beschreibung**
Erkennt automatisch, welche (Sub-)Skills, Module und Agenten für eine Aufgabe relevant
sind, bringt sie in eine sinnvolle Reihenfolge und dokumentiert diese Entscheidung.

**Anwendung**
1. Aufgabe in Teilziele zerlegen.
2. Für jedes Teilziel prüfen: Gibt es ein passendes Modul aus diesem Mega-Skill
   (`modules/*.md`) oder einen anderen installierten Skill (`ListSkills`/`SearchSkills`),
   der das abdeckt?
3. Reihenfolge festlegen nach Abhängigkeiten, z.B.:
   `Opportunity Discovery → Product Development → frontend-design → webapp-testing →
   Security Module → CI/CD Integration → Cloud Deployment`
4. Parallelisierbare Schritte identifizieren (z.B. Marketing-Plan und
   Security-Scan können parallel laufen, wenn sie sich nicht gegenseitig blockieren) –
   ggf. via `Agent`-Tool parallel starten.
5. Reihenfolge + Begründung in `ORCHESTRATION_LOG.md` festhalten, BEVOR die Ausführung
   beginnt.
6. Nach Abschluss: kurz vermerken, ob die geplante Reihenfolge tatsächlich passte oder
   angepasst werden musste (Input für Modul 1 und 5).

**Output-Format** (`ORCHESTRATION_LOG.md`)
```markdown
## 2026-07-26 – Orchestrierung für: <Task>

**Erkannte Teilziele:** A, B, C

**Gewählte Reihenfolge:**
1. Modul/Skill X – warum zuerst
2. Modul/Skill Y – Abhängigkeit von X
3. Modul/Skill Z – parallel zu Y möglich

**Abweichung während Ausführung:** <keine / Beschreibung>
```

**Beispiel**
> "Baue eine Landingpage, teste sie, und deploye sie."
> Reihenfolge: `frontend-design` → `webapp-testing` → `Security Module` (Modul 20,
> parallel zu Tests möglich) → `CI/CD Integration` (Modul 17) → `Cloud Deployment`
> (Modul 26).

---

## 4. Context Budgeting & Token Optimization

**Beschreibung**
Überwacht den Kontext-/Token-Verbrauch während der Session und trifft bewusste
Entscheidungen darüber, wie viel Kontext für eine Aufgabe geladen werden sollte.

**Anwendung**
1. Vor Beginn: Task-Komplexität grob einschätzen:
   - **Lean-Context** (Standard): nur SKILL.md + genau die 1-2 benötigten Sub-Skill-
     Dateien laden. Für einfache/klar abgegrenzte Tasks (ein Feature, ein Bugfix, ein
     Report).
   - **Full-Context**: mehrere Sub-Skills + Agent-Team laden. Nur für wirklich
     bereichsübergreifende Aufgaben (kompletter Produkt-Launch, Multi-Domain-Strategie).
2. Während der Arbeit: keine Dateien "auf Vorrat" lesen. Große Dateien gezielt mit
   Offset/Limit lesen statt komplett, wenn nur ein Ausschnitt gebraucht wird.
3. Wenn absehbar ist, dass der Task viele Zwischenergebnisse produziert (z.B. viele
   Suchergebnisse, lange Logs), diese in einer Subagent-Delegation kapseln (siehe
   `Agent`-Tool), statt sie in den Hauptkontext zu ziehen.
4. Wenn die Konversation lang wird und Kompression droht: wichtige Zwischenstände
   proaktiv in State-Dateien sichern (nicht nur im Chat-Gedächtnis halten), damit nach
   einer Zusammenfassung nichts verloren geht.
5. Nach Abschluss des Tasks: kurzer Token-Kosten-Hinweis an den User (grobe Einschätzung:
   niedrig/mittel/hoch, plus was den Verbrauch dominiert hat).

**Output-Format** (kein separates File – kurzer Hinweis im Chat nach Taskabschluss)
```
Kontext-Bericht: Lean-Context genutzt (SKILL.md + 04-workflow-integrations.md).
Hauptkosten: 3× vollständiges Lesen von bot.py (~600 Zeilen). Für Folge-Tasks an
dieser Datei: gezielt mit Grep statt Volltext lesen.
```

**Beispiel**
> Ein einfacher Typo-Fix in `README.md` lädt NICHT das gesamte Agent-Team-Modul,
> sondern höchstens `modules/04-workflow-integrations.md` (Documentation-Abschnitt).

---

## 5. Self-Improvement Engine

**Beschreibung**
Analysiert wiederholt die eigene Performance dieses Skills und schlägt konkrete
Verbesserungen für den Skill selbst vor – bis hin zu neuen Sub-Skills, wenn ein
wiederkehrender Bedarf erkannt wird.

**Anwendung**
1. In regelmäßigen Abständen (z.B. wenn der User explizit danach fragt, oder nachdem
   `LESSONS_LEARNED.md` mehrere neue "Aktive Regeln" gesammelt hat) eine Selbstanalyse
   durchführen:
   - Welche Module wurden häufig genutzt? Welche nie?
   - Gab es wiederkehrende Reibungspunkte (aus `ORCHESTRATION_LOG.md` /
     `LESSONS_LEARNED.md`)?
   - Fehlt ein Modul für einen wiederkehrenden Bedarf?
2. Konkrete Verbesserungsvorschläge formulieren (z.B. "Modul X sollte Schritt Y
   standardmäßig einschließen", "neues Modul für Z wäre sinnvoll").
3. Änderungen NICHT automatisch und unangekündigt an den Skill-Dateien vornehmen, wenn
   sie strukturell sind (neue Datei, neues Modul) – dem User vorschlagen und bei Zustimmung
   umsetzen. Kleine, klar risikofreie Klarstellungen (Tippfehler, Formatierung) dürfen
   direkt gemacht werden.
4. Jede tatsächliche Änderung am Skill in `SKILL_CHANGELOG.md` protokollieren, inklusive
   Begründung ("Warum wurde das geändert").

**Output-Format** (`SKILL_CHANGELOG.md`)
```markdown
## 2026-07-26

- **Geändert:** `modules/04-workflow-integrations.md` – Security-Scan jetzt Standard
  vor jedem Deployment.
- **Warum:** Dreimal in Folge wurde ein Security-Scan vergessen (siehe
  LESSONS_LEARNED.md, Einträge vom 07-15, 07-18, 07-24).

## Vorschläge (noch nicht umgesetzt, warten auf User-Bestätigung)
- Neues Modul "Localization" vorschlagen, da 3 Tasks Übersetzungsbedarf hatten.
```

**Beispiel**
> Nach 5 Business-OS-Durchläufen fällt auf, dass immer ein Pricing-Vergleich mit
> Konkurrenten gemacht wurde, der aktuell nicht explizit in Modul 10 (Financial)
> vorgesehen ist → Vorschlag: Abschnitt "Wettbewerbs-Pricing" zu Modul 10 hinzufügen.
