# Teil 2 – Business OS Module

Diese 5 Module decken den Weg von der Marktidee bis zum belastbaren Finanzplan ab.
Sie liefern Reports, keine Marketing-Floskeln – jede Aussage sollte, wo möglich, mit
einer nachvollziehbaren Annahme oder Quelle unterlegt sein. Wenn echte Marktdaten nicht
recherchierbar sind (z.B. kein Internetzugriff verfügbar), das explizit als Annahme
kennzeichnen statt Zahlen zu erfinden.

---

## 6. Opportunity Discovery Module

**Beschreibung**
Scannt Märkte nach unbesetzten Nischen, analysiert Konkurrenzprodukte und bewertet
Marktgröße/Umsatzpotenzial.

**Anwendung**
1. Ausgangspunkt klären: Branche, Zielgruppe, oder existierendes Produkt/Repo als Basis?
2. Wenn Web-Recherche verfügbar ist (`WebSearch`/`WebFetch`): 3-5 existierende
   Wettbewerber recherchieren, deren Positionierung, Preismodell und offensichtliche
   Schwächen (Reviews, fehlende Features, schlechtes UX) zusammenfassen.
3. Lücken identifizieren: Was fragen Nutzer in Foren/Reviews, das keiner der
   Wettbewerber gut löst?
4. Marktgröße grob schätzen (Top-Down: Gesamtmarkt × realistischer Anteil; oder
   Bottom-Up: Zielgruppe × Zahlungsbereitschaft) – Annahmen immer offenlegen.
5. Nischen nach Aufwand/Ertrag/Wettbewerbsintensität priorisieren.

**Output-Format** (`OPPORTUNITY_REPORT.md`)
```markdown
# Opportunity Report: <Thema>

## Analysierte Wettbewerber
| Produkt | Positionierung | Preis | Stärken | Schwächen/Lücke |
|---|---|---|---|---|

## Identifizierte Nischen
1. **<Nische>** – Beschreibung, Zielgruppe, warum unbesetzt.

## Marktgrößen-Schätzung
- Methode: Top-Down / Bottom-Up
- Annahmen: ...
- Geschätztes Umsatzpotenzial: ... (mit Bandbreite, keine Scheingenauigkeit)

## Priorisierung
| Nische | Aufwand | Ertragspotenzial | Wettbewerb | Score |
|---|---|---|---|---|

## Empfehlung
Top-1 Nische + Begründung in 2-3 Sätzen.
```

**Beispiel**
> Für einen bestehenden Discord-Recording-Bot: Nische "Auto-Highlight-Clips für
> Streamer" – Wettbewerber bieten manuelles Schneiden, aber keine automatische
> KI-Highlight-Erkennung im Preissegment unter 15€/Monat.

---

## 7. Product Development Module

**Beschreibung**
Generiert PRDs (Product Requirements Documents), MVP-Spezifikationen und
Feature-Roadmaps mit Meilensteinen.

**Anwendung**
1. Aus Opportunity/Vision die Kernfunktion (Value Proposition) in einem Satz formulieren.
2. PRD-Grundstruktur füllen: Problem, Zielgruppe, Lösung, Nicht-Ziele (explizit, um
   Scope Creep zu vermeiden), Erfolgskriterien.
3. MVP definieren: das kleinstmögliche Set an Features, das die Kernfunktion beweist –
   klar trennen von "Nice-to-have später".
4. Roadmap in Meilensteine gliedern (z.B. MVP → Beta → v1.0 → Wachstum), mit groben
   Zeithorizonten statt Fixdaten, sofern keine harten Deadlines vorgegeben sind.

**Output-Format** (`PRODUCT_ROADMAP.md`, PRD als Abschnitt darin oder separat)
```markdown
# PRD: <Produktname>

## Problem
## Zielgruppe
## Lösung / Value Proposition (1 Satz)
## Nicht-Ziele

# Product Roadmap

## Meilenstein 1: MVP
- Feature A (must-have)
- Feature B (must-have)
- Erfolgskriterium: ...

## Meilenstein 2: Beta
- ...

## Meilenstein 3: v1.0
- ...

## Später / Backlog (nicht priorisiert)
- ...
```

**Beispiel**
> MVP für ein Highlight-Clip-Feature: nur "erkenne Lautstärke-Peaks + erstelle 30s-Clip".
> Nicht-Ziel für MVP: automatisches Posten auf Social Media (kommt in Meilenstein 2).

---

## 8. Marketing & Sales Module

**Beschreibung**
Erstellt Go-to-Market-Strategien, Marketing-Kopien für Landingpages und
Social-Media-Kampagnenpläne.

**Anwendung**
1. Zielgruppe und Haupt-Painpoint aus PRD/Opportunity-Report übernehmen.
2. Go-to-Market-Kanäle auswählen (z.B. Content/SEO, Community/Discord, Paid Ads,
   Partnerschaften) und je Kanal eine grobe Taktik + erwarteten Aufwand nennen.
3. Landingpage-Copy entwerfen: Headline, Subheadline, 3 Kernvorteile, Call-to-Action,
   Social Proof-Platzhalter.
4. Social-Media-Kampagne grob planen (Plattform, Frequenz, Content-Typen) – konkrete
   Post-Texte optional als Beispiele liefern, keine Massen-Content-Fabrik ungefragt.

**Output-Format** (`MARKETING_PLAN.md`)
```markdown
# Marketing Plan: <Produkt>

## Zielgruppe & Painpoint

## Go-to-Market-Kanäle
| Kanal | Taktik | Erwarteter Aufwand | Priorität |
|---|---|---|---|

## Landingpage-Copy
- Headline: ...
- Subheadline: ...
- 3 Kernvorteile: ...
- CTA: ...

## Social-Media-Plan
| Plattform | Frequenz | Content-Typ | Beispiel-Post |
|---|---|---|---|
```

**Beispiel**
> Kanal-Priorität für ein Nischen-Tool: zuerst Community (Discord-Server, Reddit-
> Nischen-Subreddits), da niedrige Kosten und hohe Zielgruppen-Passung; Paid Ads erst
> nach validierter Conversion.

---

## 9. Analytics & Metrics Module

**Beschreibung**
Definiert und trackt KPIs, analysiert Nutzerverhalten (soweit Daten vorliegen) und
erstellt Reports/Dashboards.

**Anwendung**
1. Passende KPIs je nach Produktphase wählen (z.B. MVP: Activation-Rate; Wachstum:
   Retention, MRR-Wachstum, Churn).
2. Wenn echte Daten vorliegen (Logs, DB, Analytics-Tool): auswerten und
   zusammenfassen. Wenn keine Daten vorliegen: KPI-Definitionen + Tracking-Plan
   liefern (was soll künftig gemessen werden, mit welchem Tool/Event-Schema), statt
   Zahlen zu erfinden.
3. Auffälligkeiten/Trends klar von Spekulation trennen ("Daten zeigen X" vs.
   "Hypothese: könnte an Y liegen").
4. Bei Bedarf ein einfaches Dashboard als Artifact (HTML) vorschlagen/erstellen.

**Output-Format** (`ANALYTICS_REPORT.md`)
```markdown
# Analytics Report: <Zeitraum/Produkt>

## Getrackte KPIs
| KPI | Definition | Aktueller Wert | Trend | Zielwert |
|---|---|---|---|---|

## Erkenntnisse (datenbasiert)
## Hypothesen (nicht datenbasiert, zur Prüfung)
## Fehlendes Tracking (Empfehlung für Instrumentierung)
```

**Beispiel**
> Für den Bot: KPI "Recordings pro aktivem Server/Woche". Kein Analytics-Tool
> vorhanden → Empfehlung: einfaches Event-Logging in eine SQLite-Tabelle statt
> spekulativer Nutzerzahlen.

---

## 10. Financial Module

**Beschreibung**
Berechnet Break-even-Punkte, plant Pricing-Strategien und analysiert Umsatzquellen.

**Anwendung**
1. Fixkosten (Hosting, Tools, ggf. Personal) und variable Kosten pro Nutzer erfassen.
2. Pricing-Modell vorschlagen (Freemium, Abo-Stufen, Einmalzahlung, Usage-based) mit
   Vergleich zu 2-3 Wettbewerbspreisen, falls aus Modul 6 bekannt.
3. Break-even berechnen: `Fixkosten / (Preis pro Kunde − variable Kosten pro Kunde)`
   = benötigte Kundenzahl. Rechnung transparent zeigen, keine Blackbox-Zahl.
4. Umsatzquellen auflisten und nach Wahrscheinlichkeit/Beitrag gewichten (siehe auch
   Modul 21, Revenue Stream Generator, für die strategische Tiefenanalyse).

**Output-Format** (`FINANCIAL_PLAN.md`)
```markdown
# Financial Plan: <Produkt>

## Kostenstruktur
| Posten | Fix/Variabel | Betrag/Monat |
|---|---|---|

## Pricing-Strategie
| Stufe | Preis | Enthalten | Vergleich Wettbewerb |
|---|---|---|---|

## Break-even-Berechnung
Formel + eingesetzte Werte + Ergebnis (benötigte zahlende Kunden/Monat)

## Umsatzquellen
| Quelle | Anteil (geschätzt) | Risiko |
|---|---|---|
```

**Beispiel**
> Fixkosten 40€/Monat Hosting, Preis 9€/Monat, variable Kosten 1€/Kunde (API-Calls)
> → Break-even bei 40 / (9−1) = 5 zahlenden Kunden.
