# Anwendungsbeispiele: Mega-Architect Skill

Fünf konkrete, durchgängige Beispiele – jeweils mit Anfrage, ausgelösten Modulen und
erwartetem Ergebnis. Alle Beispiele beziehen sich exemplarisch auf dieses Repository
(einen Discord-Recording-Bot mit OBS-Integration), lassen sich aber auf jedes Projekt
übertragen.

---

## Beispiel 1: Neues Feature von der Idee bis zum Launch

**Anfrage:**
> "Ich will ein Auto-Highlight-Clip-Feature für unseren Bot. Führ mich von der
> Marktanalyse bis zum Launch-Plan."

**Ausgelöste Module (in dieser Reihenfolge, dokumentiert in `ORCHESTRATION_LOG.md`):**
1. Modul 3 (Dynamic Skill Orchestration) plant die Reihenfolge.
2. Modul 6 (Opportunity Discovery) → `OPPORTUNITY_REPORT.md`
3. Modul 7 (Product Development) → PRD + `PRODUCT_ROADMAP.md`
4. Modul 2 (Pre-Mortem) vor der technischen Umsetzung → `PRE_MORTEM.md`
5. Modul 12 (CTO Agent) für Architektur-Entscheidung (FFmpeg-Heuristik vs. Cloud-ML)
6. Modul 19 (Testing) + Modul 20 (Security) parallel zur Implementierung
7. Modul 8 (Marketing & Sales) → `MARKETING_PLAN.md`
8. Modul 23 (Product Launch) → `LAUNCH_PLAN.md`
9. Modul 1 (Retrospektive) nach Abschluss → Eintrag in `LESSONS_LEARNED.md`

**Ergebnis:** Ein vollständiger Ordner an Reports unter
`.claude/mega-architect/state/`, plus tatsächlicher Code für das Feature inkl. Tests.

---

## Beispiel 2: Schnelle Risiko-Analyse vor einem Deployment

**Anfrage:**
> "Bevor wir den Bot auf einen neuen Server deployen: was könnte schiefgehen?"

**Ausgelöste Module:**
- Modul 2 (Proactive Pre-Mortem) – Fokus auf Technisch/Business/Zeit-Risiken rund um
  das Deployment.
- Optional Modul 26 (Cloud Deployment) für die konkrete Infrastruktur-Planung, falls
  noch keine Konfiguration existiert.

**Ergebnis:** `PRE_MORTEM.md` mit konkreten Risiken wie "falsches Discord-Token in
`.env`", "DNS-Propagation dauert länger als erwartet", plus Gegenmaßnahmen. Kein
automatisches Deployment – das bleibt manueller, bestätigter Schritt.

---

## Beispiel 3: Virtuelles C-Level-Team für eine strategische Frage

**Anfrage:**
> "Spiel CEO für dieses Projekt: Sollen wir aus dem Bot ein SaaS mit Abo-Modell
> machen?"

**Ausgelöste Module:**
- Modul 11 (CEO Agent) zerlegt die Frage in Teilziele.
- Parallel delegiert an: Modul 12 (CTO – technische Machbarkeit als SaaS), Modul 15
  (CFO – Break-even/Pricing, greift auf Modul 10 zurück), Modul 14 (CMO –
  Zielgruppen-Fit, greift auf Modul 6 zurück).
- CEO fasst zusammen, benennt Konflikte (z.B. CTO sieht 6 Wochen Aufwand, CFO sieht
  Budget nur für 3 Wochen Entwicklung).

**Ergebnis:** Eine CEO-Zusammenfassung im Chat mit klarer Empfehlung ("Go mit
reduziertem MVP-Scope") plus Detail-Reports der einzelnen Rollen.

---

## Beispiel 4: Passives Einkommen aus einem bestehenden Projekt

**Anfrage:**
> "Wie kann ich mit diesem Bot passives Einkommen generieren?"

**Ausgelöste Module:**
- Modul 21 (Revenue Stream Generator) → `REVENUE_PLAN.md` mit priorisierten Optionen
  (Abo-Modell, Affiliate, White-Label).
- Modul 22 (Affiliate Marketing) für die Nebenquelle → `AFFILIATE_REPORT.md`
  (Programm-Vorschläge, keine echte Anmeldung).
- Modul 10 (Financial Module) für Break-even-Rechnung des Abo-Modells.
- Modul 25 (Growth Module) für Kanäle, um zahlende Nutzer zu gewinnen.

**Ergebnis:** Ein priorisierter, umsetzbarer Plan mit realistischen Zahlen/Annahmen
statt vager Versprechen – inklusive Hinweis, dass echte Anmeldungen/Zahlungen beim
User liegen.

---

## Beispiel 5: CI/CD, Tests und Security für ein bestehendes Repo einrichten

**Anfrage:**
> "Richte für dieses Repo eine vollständige CI/CD-Pipeline mit Tests und
> Security-Checks ein."

**Ausgelöste Module:**
1. Modul 3 (Orchestrierung) plant: erst Testing, dann Security, dann CI/CD, dann Docs.
2. Modul 19 (Testing Module) – Unit-/Integrationstests für Kernlogik ergänzen, falls
   noch nicht vorhanden.
3. Modul 20 (Security Module) – OWASP-Check, Dependency-Check, Secret-Scan.
4. Modul 17 (CI/CD Integration) – GitHub-Actions-Workflow + ggf. Dockerfile.
5. Modul 18 (Documentation Module) – README/CONTRIBUTING aktualisieren, damit neue
   Contributor die Pipeline verstehen.
6. Modul 16 (Git Integration) – fokussierte Commits, PR mit Testplan (nur nach
   expliziter Aufforderung tatsächlich gepusht).

**Ergebnis:** `.github/workflows/ci.yml`, ggf. `Dockerfile`, aktualisierte Tests,
Security-Report, aktualisierte Doku – als PR zur Review, nicht automatisch gemerged.
