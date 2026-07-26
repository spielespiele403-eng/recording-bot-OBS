# Teil 5 – Passive Income Module

Diese 5 Module helfen, aus einem bestehenden Produkt/Repo wiederkehrende Einnahmen zu
entwickeln. Sie sind bewusst als **Planungs- und Analyse-Module** gestaltet – sie
bereiten Entscheidungen vor, treffen aber keine echten Finanz-/Vertragsentscheidungen
und lösen keine echten Zahlungen/Registrierungen aus.

---

## 21. Revenue Stream Generator

**Beschreibung**
Analysiert, welche Einnahmequellen für ein Produkt realistisch sind, erstellt je
Quelle einen Plan und priorisiert nach Aufwand/Ertrag.

**Anwendung**
1. Aus Produkt/Zielgruppe mögliche Einnahmequellen ableiten (z.B. Abo/SaaS, Einmalkauf,
   Affiliate, gesponserte Inhalte, Premium-Support, White-Label-Lizenzierung, API-Zugang).
2. Je Quelle: Aufwand (Setup + laufend), erwarteter Ertrag (grob, mit Annahmen),
   Abhängigkeiten (z.B. Nutzerzahl nötig, rechtliche Anforderungen).
3. Priorisieren nach Aufwand/Ertrag-Verhältnis, ähnlich Modul 10 (Financial), aber mit
   Fokus auf Diversifizierung statt Einzelplan.
4. Für Top-2-3 Quellen je einen kurzen Umsetzungsplan skizzieren.

**Output-Format** (`REVENUE_PLAN.md`)
```markdown
# Revenue Plan: <Produkt>

## Mögliche Einnahmequellen
| Quelle | Aufwand (Setup/laufend) | Ertragspotenzial | Abhängigkeiten | Priorität |
|---|---|---|---|---|

## Top-Quellen im Detail
### 1. <Quelle>
- Umsetzungsschritte: ...
- Benötigte Voraussetzungen: ...
```

**Beispiel**
> Für den Recording-Bot: Abo-Modell (Premium-Features wie längere Aufnahmen) als
> Hauptquelle, Affiliate-Links zu Streaming-Zubehör als Nebenquelle mit minimalem
> Zusatzaufwand.

---

## 22. Affiliate Marketing Module

**Beschreibung**
Findet passende Affiliate-Programme, unterstützt bei Tracking-Links und analysiert
Conversion-Daten, sofern vorhanden.

**Anwendung**
1. Passende Affiliate-Programme zur Zielgruppe recherchieren (falls Web-Zugriff
   verfügbar) oder anhand bekannter Branchen-Standards vorschlagen (z.B. Software-Tools,
   Hosting-Anbieter, Hardware bei Streaming-Zubehör).
2. Für jedes Programm: Provisionsmodell, Cookie-Laufzeit, Passung zur Zielgruppe
   festhalten – **niemals selbst bei einem Partnerprogramm anmelden oder echte
   Tracking-Links mit echten Account-IDs generieren**; nur die Struktur/Platzhalter
   vorbereiten, die der User dann mit seinen eigenen Zugangsdaten befüllt.
3. Placement-Empfehlungen geben (wo im Produkt/Content Links sinnvoll sind, ohne
   aufdringlich zu wirken).
4. Conversion-Analyse nur auf Basis echter, vom User bereitgestellter Daten – keine
   erfundenen Klickzahlen.

**Output-Format** (`AFFILIATE_REPORT.md`)
```markdown
# Affiliate Report

## Passende Programme
| Programm | Provision | Cookie-Laufzeit | Zielgruppen-Fit |
|---|---|---|---|

## Placement-Empfehlungen
- ...

## Conversion-Analyse (nur falls Daten vorliegen)
| Link/Placement | Klicks | Conversions | Rate |
|---|---|---|---|
```

**Beispiel**
> Für ein Streaming-Tool: Affiliate-Programme für Mikrofone/Capture-Karten passen zur
> Zielgruppe besser als generische Software-Affiliates.

---

## 23. Product Launch Module

**Beschreibung**
Plant einen strukturierten Launch (30-Tage-Plan), erstellt Checklisten und entwirft
Launch-Posts für Reddit, Twitter/X, LinkedIn.

**Anwendung**
1. Launch in 3 Phasen gliedern: **Vorbereitung** (Tag -30 bis -1), **Launch-Tag**,
   **Nachbereitung** (Tag +1 bis +30).
2. Checkliste je Phase: technisch (Deploy stabil, Monitoring an – siehe Modul 26/28),
   inhaltlich (Landingpage, Copy – siehe Modul 8), organisatorisch (Support bereit,
   Feedback-Kanal eingerichtet – siehe Modul 24).
3. Plattform-spezifische Post-Entwürfe liefern (Ton pro Plattform anpassen: Reddit
   community-nah und ehrlich über Eigeninteresse, Twitter/X kurz und bildstark,
   LinkedIn sachlicher mit Business-Winkel). Diese sind Entwürfe zur Freigabe durch
   den User – **niemals automatisch posten**, das ist eine öffentlich sichtbare
   Aktion und bedarf expliziter Bestätigung.
4. Nach dem Launch: Verbindung zu Modul 1 (Retrospektive) und Modul 24 (Feedback)
   herstellen.

**Output-Format** (`LAUNCH_PLAN.md`)
```markdown
# Launch Plan: <Produkt>

## Phase 1: Vorbereitung (Tag -30 bis -1)
- [ ] ...

## Phase 2: Launch-Tag
- [ ] ...

## Phase 3: Nachbereitung (Tag +1 bis +30)
- [ ] ...

## Launch-Post-Entwürfe
### Reddit (r/<subreddit>)
...
### Twitter/X
...
### LinkedIn
...
```

**Beispiel**
> Launch-Tag-Checkliste: Monitoring aktiv (Modul 28), Support-Discord-Kanal offen,
> Reddit-Post erst nach manueller Freigabe durch den User veröffentlicht.

---

## 24. Customer Feedback Module

**Beschreibung**
Sammelt Feedback von Nutzern, analysiert Bewertungen und identifiziert
Verbesserungspotenziale.

**Anwendung**
1. Feedback-Quellen festlegen (In-App-Umfrage, Discord-Kanal, Reviews, Support-Tickets)
   – nur auswerten, was tatsächlich vorliegt, nichts unterstellen.
2. Feedback kategorisieren: Bug, Feature-Wunsch, UX-Reibung, Lob.
3. Muster erkennen (gleiche Beschwerde von mehreren Nutzern = hohe Priorität) statt
   auf Einzelmeinungen überzureagieren.
4. Verbindung zu Modul 13 (CPO/Backlog) herstellen: konkrete Verbesserungen als
   User-Story-Kandidaten markieren.

**Output-Format** (`FEEDBACK_REPORT.md`)
```markdown
# Feedback Report: <Zeitraum>

## Zusammenfassung
Anzahl Rückmeldungen: X | Quelle(n): ...

## Kategorisiert
| Kategorie | Anzahl | Beispiel-Zitat | Priorität |
|---|---|---|---|

## Erkannte Muster
- ...

## Empfohlene Maßnahmen (→ Backlog)
- ...
```

**Beispiel**
> 4 von 12 Rückmeldungen bemängeln lange Verarbeitungszeit bei langen Aufnahmen →
> hohe Priorität, Kandidat für nächsten Sprint (Modul 13).

---

## 25. Growth Module

**Beschreibung**
Plant Wachstumsstrategien, analysiert Kanäle (SEO, Social, Email, Referral) und
entwickelt Growth-Hacking-Ideen.

**Anwendung**
1. Aktuelle Kanäle und deren grobe Wirksamkeit auflisten (soweit Daten vorliegen,
   sonst als unvalidierte Hypothese kennzeichnen).
2. Für jeden relevanten Kanal (SEO, Social, Email, Referral/Empfehlungsprogramm,
   Community) eine konkrete, umsetzbare Maßnahme vorschlagen statt genereller Tipps.
3. Growth-Hacking-Ideen sammeln, aber auf ethische/plattformkonforme Taktiken
   beschränken (kein Spam, keine gefälschten Bewertungen/Bots, keine Täuschung – siehe
   Sicherheitsrichtlinien: keine Massen-Zielgruppen-Angriffe oder Detection-Evasion).
4. Ideen nach erwartetem Hebel und Umsetzungsaufwand sortieren.

**Output-Format** (`GROWTH_PLAN.md`)
```markdown
# Growth Plan: <Produkt>

## Kanal-Analyse
| Kanal | Aktueller Stand | Wirksamkeit | Maßnahme |
|---|---|---|---|

## Growth-Ideen (priorisiert)
| Idee | Hebel | Aufwand | Ethisch/plattformkonform geprüft |
|---|---|---|---|
```

**Beispiel**
> Referral-Idee: bestehende Nutzer erhalten einen Monat gratis Premium, wenn ein
> geworbener Nutzer zahlender Kunde wird – einfach umzusetzen, kein Graubereich.
