# Mega-Architect: Meta-Cognitive Architect & Business OS

Ein Claude-Code-Skill, der aus einem reinen Coding-Assistenten ein
**selbst-lernendes, sich selbst verbesserndes, proaktives und orchestrierendes System**
macht – von der ersten Idee bis zum wiederkehrenden Umsatz.

## Warum dieser Skill existiert

Standard-Claude-Code ist exzellent darin, einzelne Aufgaben zu lösen. Was fehlt, ist
die Klammer darüber: Lernt es aus Fehlern? Denkt es Risiken vorher durch? Wählt es
bewusst, wie viel Kontext eine Aufgabe braucht? Denkt es über Code hinaus – Markt,
Produkt, Marketing, Finanzen, Deployment?

Mega-Architect beantwortet all das mit **30 konkreten, dokumentierten Modulen** in
**7 Kategorien**, jeweils mit klarem Anwendungsfall, Output-Format und Beispiel – kein
vages Prinzip, sondern nachvollziehbare Arbeitsanweisungen.

## Die 7 Kategorien im Überblick

1. **Meta-Cognitive Architect** – Selbstreflexion, Pre-Mortem, Skill-Orchestrierung,
   Context Budgeting, Self-Improvement.
2. **Business OS** – Opportunity Discovery, Produktentwicklung, Marketing & Sales,
   Analytics, Finanzen.
3. **Agent-Team** – CEO, CTO, CPO, CMO, CFO als delegierbare Rollen.
4. **Workflow-Integrationen** – Git, CI/CD, Dokumentation, Testing, Security.
5. **Passive Income** – Revenue Streams, Affiliate Marketing, Product Launch, Feedback,
   Growth.
6. **Deployment & Hosting** – Cloud, Domain/SSL, Monitoring.
7. **Training & Onboarding** – User Onboarding, Team Training.

Details, Anwendung, Output-Format und Beispiel zu jedem der 30 Module stehen in den
Dateien unter `modules/`. Die Haupt-Logik und Trigger-Bedingungen stehen in `SKILL.md`.

## Ordnerstruktur

```
.claude/skills/mega-architect/
├── SKILL.md                          # Haupt-Skill (Frontmatter + Meta-Loop + Quick-Reference)
├── README.md                         # dieses Dokument
├── INSTALL.md                        # Installationsanleitung
├── EXAMPLES.md                       # 5 konkrete Anwendungsbeispiele
├── TROUBLESHOOTING.md                # häufige Probleme & Lösungen
└── modules/
    ├── 01-meta-cognitive.md          # Module 1-5
    ├── 02-business-os.md             # Module 6-10
    ├── 03-agent-team.md              # Module 11-15
    ├── 04-workflow-integrations.md   # Module 16-20
    ├── 05-passive-income.md          # Module 21-25
    ├── 06-deployment-hosting.md      # Module 26-28
    └── 07-training-onboarding.md     # Module 29-30
```

Zur Laufzeit legt der Skill zusätzlich `.claude/mega-architect/state/` im Projekt-Root
an – dort landen alle generierten Reports (`LESSONS_LEARNED.md`, `PRE_MORTEM.md`,
`OPPORTUNITY_REPORT.md` usw.).

## Kurz-Nutzung

Der Skill triggert automatisch bei strategischen/unternehmerischen/mehrstufigen
Anfragen (siehe `description` in `SKILL.md`). Du kannst ihn auch explizit ansprechen:

```
/mega-architect Baue mir ein Konzept für ein Highlight-Clip-Feature, von der
Marktanalyse bis zum Launch-Plan.
```

Für Installation siehe `INSTALL.md`, für konkrete Beispiele siehe `EXAMPLES.md`, bei
Problemen siehe `TROUBLESHOOTING.md`.

## Design-Prinzipien

- **Kein Modul autorisiert riskante/irreversible Aktionen** (echte Deploys,
  Domain-Käufe, Social-Media-Posts, Geldausgaben) – sie planen und bereiten vor, der
  User bestätigt und führt aus.
- **Kein erfundenes Zahlenmaterial.** Wo echte Daten fehlen, wird das als Annahme
  gekennzeichnet statt Scheingenauigkeit vorzutäuschen.
- **Lean by default.** Nur die tatsächlich benötigten Module/Sub-Skills werden
  geladen (siehe Modul 4, Context Budgeting).
- **Alles ist dokumentiert.** Jede Entscheidung, jeder Lernschritt, jede
  Selbstverbesserung wird in einer nachvollziehbaren Markdown-Datei protokolliert.
