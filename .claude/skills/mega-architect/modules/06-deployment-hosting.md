# Teil 6 – Deployment & Hosting Module

Diese 3 Module planen und dokumentieren die Infrastruktur. **Sie führen keine echten
Cloud-Ressourcen-Erstellungen, Domain-Käufe oder Produktions-Deployments ohne
ausdrückliche User-Bestätigung durch** – Infrastruktur-Änderungen sind schwer
umkehrbar und wirken sich auf reale Kosten/Erreichbarkeit aus (siehe Kernregeln zu
riskanten Aktionen).

---

## 26. Cloud Deployment

**Beschreibung**
Erstellt Konfigurationen für AWS/Azure/GCP, Kubernetes-Manifeste und Terraform-Skripte.

**Anwendung**
1. Zuerst den einfachsten passenden Ansatz wählen (z.B. Single-VM oder
   Managed-Container-Dienst) statt reflexhaft Kubernetes vorzuschlagen, wenn die
   Last das nicht rechtfertigt – Komplexität soll dem tatsächlichen Bedarf entsprechen.
2. Konfigurationsdateien (Terraform/K8s-Manifeste) als Code liefern, aber **nicht
   automatisch `apply`/`deploy` ausführen** – das obliegt dem User oder einem
   CI/CD-Schritt mit expliziter Freigabe (siehe Modul 17).
3. Secrets/Zugangsdaten nie in Klartext in Konfigurationsdateien – auf Secret-Manager/
   Env-Vars verweisen.
4. Kosten-Implikationen der gewählten Architektur kurz benennen (grobe Größenordnung).
5. Rollback-Strategie mitdenken (z.B. Blue-Green, vorherige Version taggen).

**Output-Format** (`DEPLOYMENT_GUIDE.md`)
```markdown
# Deployment Guide: <Projekt>

## Gewählte Architektur
<Beschreibung + Begründung, warum diese Komplexitätsstufe>

## Ressourcen
- ...

## Konfigurationsdateien
- `infra/main.tf` (Terraform) / `k8s/deployment.yaml`

## Kosten (grobe Schätzung)
## Rollback-Strategie
## Manuelle Freigabeschritte (was NICHT automatisiert läuft)
```

**Beispiel**
> Für den Discord-Bot: eine einzelne Container-Instanz (z.B. Fly.io/Render) reicht,
> Kubernetes wäre für die aktuelle Last unnötige Komplexität.

---

## 27. Domain & SSL

**Beschreibung**
Unterstützt bei Domain-Registrierung, SSL-Zertifikaten und DNS-Konfiguration.

**Anwendung**
1. Domain-Registrierung selbst **nicht durchführen** (echter Kauf/echte Zahlung) –
   nur Namensvorschläge und Registrar-Vergleichskriterien liefern (Preis, Datenschutz-
   Whois, Verlängerungskonditionen).
2. DNS-Einträge als klare Anleitung/Tabelle liefern (A/AAAA/CNAME/TXT), die der User
   selbst im Registrar-/DNS-Panel einträgt.
3. SSL: Let's-Encrypt/automatisches Zertifikat empfehlen (z.B. via Caddy/Certbot/
   Managed-Platform), Konfigurationsschritte liefern, aber keine echten Zertifikate im
   Namen des Users beantragen ohne dessen Ausführung.
4. Auf Ablaufüberwachung hinweisen (Auto-Renewal aktivieren, sonst Reminder setzen).

**Output-Format** (`DOMAIN_SETUP.md`)
```markdown
# Domain & SSL Setup: <Projekt>

## Domain-Vorschläge
| Domain | Verfügbarkeit (zu prüfen) | Registrar-Empfehlung |
|---|---|---|

## DNS-Einträge
| Typ | Name | Wert | TTL |
|---|---|---|---|

## SSL-Konfiguration
Methode: Let's Encrypt via <Tool>
Schritte: ...

## Ablauf-Überwachung
Auto-Renewal: ja/nein – Empfehlung
```

**Beispiel**
> A-Record `@` → Server-IP, CNAME `www` → `@`, SSL via Caddy automatisch mit
> Auto-Renewal – User führt DNS-Eintragung selbst im Registrar-Panel aus.

---

## 28. Monitoring & Alerts

**Beschreibung**
Definiert Logging-Strategie, Alerting (z.B. Slack/Email) und Dashboard-Erstellung
(z.B. Grafana).

**Anwendung**
1. Logging-Level und -Struktur festlegen (strukturierte Logs bevorzugt, keine Secrets
   in Logs).
2. Kritische Alerts definieren (z.B. Bot offline, Fehlerquote über Schwellenwert,
   Speicher/Disk knapp) – Alert-Müdigkeit vermeiden, nur auf wirklich actionable
   Ereignisse alarmieren.
3. Alert-Kanäle (Slack/Email/Push) konfigurieren – Zugangsdaten/Webhooks bleiben beim
   User, nicht im Klartext in Reports.
4. Dashboard-Grundgerüst vorschlagen (z.B. Grafana-Panels: Uptime, Fehlerquote,
   aktive Recordings) – Aufbau, keine erfundenen Live-Daten.

**Output-Format** (`MONITORING_PLAN.md`)
```markdown
# Monitoring Plan: <Projekt>

## Logging
Level: ... | Format: ... | Aufbewahrung: ...

## Alerts
| Ereignis | Schwellenwert | Kanal | Priorität |
|---|---|---|---|

## Dashboard-Panels
- Uptime
- Fehlerquote
- <projektspezifische Metrik>
```

**Beispiel**
> Alert: "Bot nicht erreichbar >2 Minuten" → Slack-Webhook, Priorität hoch. Kein Alert
> für einzelne, erwartbare Rate-Limit-Warnungen (vermeidet Alert-Spam).
