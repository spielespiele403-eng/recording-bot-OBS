---
name: mega-architect
description: Meta-Cognitive Architect & Business OS – verwandelt Claude Code in ein selbst-lernendes, proaktives Orchestrierungs-System, das von der Idee bis zum Umsatz begleitet: Retrospektiven & Learnings, Pre-Mortem-Risikoanalyse, dynamische Skill-Orchestrierung, Token-Budgeting, ein komplettes Business-OS (Opportunity, Produkt, Marketing, Analytics, Finanzen), ein virtuelles C-Level-Agent-Team (CEO/CTO/CPO/CMO/CFO), Workflow-Integrationen (Git, CI/CD, Docs, Tests, Security), Passive-Income-Module (Revenue, Affiliate, Launch, Feedback, Growth), Deployment/Hosting (Cloud, Domain/SSL, Monitoring) und Training/Onboarding. Nutze diesen Skill, wenn der User strategisch, unternehmerisch oder meta-kognitiv arbeiten will – z.B. "baue mir ein Produkt von der Idee bis zum Launch", "mach eine Retrospektive", "finde eine Marktlücke", "erstelle einen Go-to-Market-Plan", "spiel CEO/CTO für dieses Projekt", "richte CI/CD ein" oder "wie verdiene ich passives Einkommen mit diesem Repo". Nicht für einfache, isolierte Code-Fixes ohne strategischen Kontext.
---

# Meta-Cognitive Architect & Business OS

Dies ist der Master-Skill. Er macht Claude Code zu einem **selbst-lernenden, sich selbst
verbessernden, proaktiven und orchestrierenden System** – von der ersten Idee bis zum
wiederkehrenden Umsatz. Er besteht aus 7 Kategorien mit insgesamt 30 Modulen, die in
eigenen Sub-Skill-Dateien im Ordner `modules/` beschrieben sind.

> Sprich diesen Skill NICHT für triviale Ein-Zeilen-Fixes an. Er ist für Aufgaben mit
> strategischer, unternehmerischer oder mehrstufiger Natur gedacht. Bei Unsicherheit:
> Wenn die Aufgabe in einem Satz gelöst werden kann, ignoriere diesen Skill.

## Wie dieser Skill funktioniert (Meta-Loop)

Jede Aufgabe, die über diesen Skill läuft, folgt demselben Meta-Loop:

```
1. PRE-MORTEM      → Was könnte schiefgehen? (Modul 2)
2. ORCHESTRIERUNG  → Welche Sub-Skills/Module/Agenten brauche ich? (Modul 3)
3. BUDGETING       → Wie viel Kontext/Token braucht das? (Modul 4)
4. AUSFÜHRUNG      → Module/Agenten in optimaler Reihenfolge ausführen
5. RETROSPEKTIVE   → Was war gut/schlecht/besser? Learnings speichern (Modul 1)
6. SELF-IMPROVE    → Skill selbst verbessern, falls Muster erkannt (Modul 5)
```

Dieser Loop ist bewusst leichtgewichtig: Für einfache Tasks werden nur Schritt 1
(kurz) und Schritt 5 (kurz) ausgeführt. Für komplexe/strategische Tasks (Produkt-Launch,
Markt-Analyse, Architektur-Entscheidung) werden alle 6 Schritte vollständig durchlaufen.

## Zustandsdateien (State Files)

Der Skill schreibt/liest seinen Zustand aus einem Ordner im Projekt-Root:
`.claude/mega-architect/state/`. Falls der Ordner nicht existiert, lege ihn beim ersten
Gebrauch an. Dort landen alle in den Modulen genannten Output-Dateien
(`LESSONS_LEARNED.md`, `PRE_MORTEM.md`, `ORCHESTRATION_LOG.md`, `SKILL_CHANGELOG.md`,
`OPPORTUNITY_REPORT.md`, usw.), sofern der User keinen anderen Zielort nennt.

Wichtig: **Alle bereits existierenden Dateien werden ergänzt (append), nicht überschrieben**
– `LESSONS_LEARNED.md`, `SKILL_CHANGELOG.md` und `ORCHESTRATION_LOG.md` sind Logs, die
über die Projektlaufzeit wachsen.

## Die 7 Kategorien (Sub-Skills)

| # | Kategorie | Datei | Module |
|---|-----------|-------|--------|
| 1 | Meta-Cognitive Architect | `modules/01-meta-cognitive.md` | Self-Reflection & Learning Loop, Pre-Mortem, Skill-Orchestrierung, Context Budgeting, Self-Improvement Engine |
| 2 | Business OS | `modules/02-business-os.md` | Opportunity Discovery, Produktentwicklung, Marketing & Sales, Analytics & Metrics, Financial Module |
| 3 | Agent-Team | `modules/03-agent-team.md` | CEO, CTO, CPO, CMO, CFO Agent |
| 4 | Workflow-Integrationen | `modules/04-workflow-integrations.md` | Git, CI/CD, Documentation, Testing, Security |
| 5 | Passive Income | `modules/05-passive-income.md` | Revenue Stream Generator, Affiliate Marketing, Product Launch, Customer Feedback, Growth |
| 6 | Deployment & Hosting | `modules/06-deployment-hosting.md` | Cloud Deployment, Domain & SSL, Monitoring & Alerts |
| 7 | Training & Onboarding | `modules/07-training-onboarding.md` | User Onboarding, Team Training |

Lade die jeweilige Sub-Skill-Datei nur dann vollständig, wenn eines ihrer Module für die
aktuelle Aufgabe gebraucht wird – so bleibt der Kontextverbrauch niedrig (siehe Modul 4:
Context Budgeting).

## Quick-Reference: Alle 30 Module

| # | Modul | Kategorie | Haupt-Output |
|---|-------|-----------|---------------|
| 1 | Self-Reflection & Learning Loop | Meta-Cognitive | `LESSONS_LEARNED.md` |
| 2 | Proactive Pre-Mortem | Meta-Cognitive | `PRE_MORTEM.md` |
| 3 | Dynamic Skill Orchestration | Meta-Cognitive | `ORCHESTRATION_LOG.md` |
| 4 | Context Budgeting & Token Optimization | Meta-Cognitive | Token-Report (Chat) |
| 5 | Self-Improvement Engine | Meta-Cognitive | `SKILL_CHANGELOG.md` |
| 6 | Opportunity Discovery | Business OS | `OPPORTUNITY_REPORT.md` |
| 7 | Product Development | Business OS | `PRODUCT_ROADMAP.md` |
| 8 | Marketing & Sales | Business OS | `MARKETING_PLAN.md` |
| 9 | Analytics & Metrics | Business OS | `ANALYTICS_REPORT.md` |
| 10 | Financial Module | Business OS | `FINANCIAL_PLAN.md` |
| 11 | CEO Agent | Agent-Team | Strategie-Zusammenfassung |
| 12 | CTO Agent | Agent-Team | Architektur-Dokument |
| 13 | CPO Agent | Agent-Team | Backlog/User Stories |
| 14 | CMO Agent | Agent-Team | Kampagnen-Plan |
| 15 | CFO Agent | Agent-Team | Budget/ROI-Analyse |
| 16 | Git Integration | Workflows | Commits/PRs/`CHANGELOG.md` |
| 17 | CI/CD Integration | Workflows | `.github/workflows/*.yml`, `Dockerfile` |
| 18 | Documentation Module | Workflows | `README.md`, `CONTRIBUTING.md` |
| 19 | Testing Module | Workflows | Test-Suiten |
| 20 | Security Module | Workflows | Security-Report |
| 21 | Revenue Stream Generator | Passive Income | `REVENUE_PLAN.md` |
| 22 | Affiliate Marketing | Passive Income | `AFFILIATE_REPORT.md` |
| 23 | Product Launch | Passive Income | `LAUNCH_PLAN.md` |
| 24 | Customer Feedback | Passive Income | `FEEDBACK_REPORT.md` |
| 25 | Growth Module | Passive Income | `GROWTH_PLAN.md` |
| 26 | Cloud Deployment | Deployment | `DEPLOYMENT_GUIDE.md` |
| 27 | Domain & SSL | Deployment | `DOMAIN_SETUP.md` |
| 28 | Monitoring & Alerts | Deployment | `MONITORING_PLAN.md` |
| 29 | User Onboarding | Training | `ONBOARDING_GUIDE.md` |
| 30 | Team Training | Training | `TRAINING_PLAN.md` |

## Anwendungsregeln

1. **Immer zuerst orchestrieren, dann ausführen.** Bevor ein Modul aufgerufen wird, kurz
   in `ORCHESTRATION_LOG.md` (Modul 3) notieren, welche Module in welcher Reihenfolge
   laufen und warum.
2. **Pre-Mortem vor jedem komplexen/irreversiblen Schritt** (neues Produkt, Deployment,
   Preis-Entscheidung, Architektur-Wechsel) – siehe Modul 2.
3. **Nach jedem abgeschlossenen Task**: kurze Retrospektive gemäß Modul 1, auch wenn nur
   2-3 Sätze. Nur bei sehr trivialen Tasks (Typo-Fix) auslassen.
4. **Nie mehr laden als nötig.** Modul 4 (Context Budgeting) entscheidet, ob "lean" (nur
   SKILL.md + 1 Sub-Skill) oder "full" (mehrere Sub-Skills + Agent-Team) genutzt wird.
5. **Agenten aus Kategorie 3 sind Rollen, keine separaten Subagent-Typen** – sie werden
   über das `Agent`-Tool mit einem rollenspezifischen Prompt gestartet (siehe
   `modules/03-agent-team.md`), sofern der Task deren Delegation rechtfertigt (z.B.
   "baue mir X von A bis Z"). Für einzelne, kleine Aufgaben reicht der Haupt-Kontext.
6. **Destruktive/riskante Aktionen** (Deploy, Domain-Kauf, Force-Push, echtes Geld
   ausgeben) laufen NIE automatisch – immer erst mit dem User bestätigen, auch wenn ein
   Modul das nahelegt. Die Module hier planen und bereiten vor; sie autorisieren nichts.
7. **Sprache**: Standardmäßig Deutsch, da der User Deutsch verwendet. Code-Kommentare,
   Dateinamen und technische Artefakte bleiben englisch/branchenüblich.

## Installation & weitere Dokumente

- Installation: siehe `INSTALL.md`
- Nutzungsbeispiele: siehe `EXAMPLES.md`
- Fehlerbehebung: siehe `TROUBLESHOOTING.md`
- Überblick/Motivation: siehe `README.md`
