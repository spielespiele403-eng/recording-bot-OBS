# phone-agent-saas

KI-Telefon-/Chat-Agent + Terminbuchung für lokale Dienstleister (Handwerker,
Zahnarztpraxen, Kfz-Werkstätten, etc.) — branchenübergreifend konfigurierbar,
kein Code pro Kunde/Branche nötig.

Zwei Kernpfade:
1. **Angenommener Anruf** → Vapi-Voice-Agent beantwortet Fragen (Öffnungszeiten,
   Leistungen, FAQ) und bucht Termine live über Cal.com.
2. **Verpasster Anruf** → automatische SMS-Rückmeldung (Twilio) mit
   Buchungslink.

## Stack

- Node.js + TypeScript, Express
- [Vapi](https://vapi.ai) als Voice-AI-Plattform (Telefonie + STT/TTS/LLM)
- [Cal.com](https://cal.com) API für Verfügbarkeit/Buchung
- [Twilio](https://twilio.com) für die Missed-Call-Recovery-SMS
- SQLite + Prisma ORM (trivial auf Postgres umstellbar über `DATABASE_URL`)

## Voraussetzungen (musst du selbst einrichten)

- **Vapi**-Account + API-Key ([dashboard.vapi.ai](https://dashboard.vapi.ai))
- **Twilio**-Account + Account SID, Auth Token, SMS-fähige Telefonnummer
- **Cal.com**-Account (Cloud oder self-hosted) + API-Key + mindestens ein
  Event Type pro angebotener Leistung
- Eine öffentlich erreichbare HTTPS-URL für Webhooks (lokal z.B. via
  [ngrok](https://ngrok.com), in Produktion deine eigene Domain) — Vapi,
  Twilio und Cal.com müssen diesen Server erreichen können.

## Setup

```bash
npm install
cp .env.example .env   # dann echte Werte eintragen
npx prisma migrate dev
npx prisma db seed     # legt eine Demo-Business "demo-handwerker" an
npm run typecheck
npm run build
```

Lokal starten (mit ngrok in einem zweiten Terminal, `PUBLIC_BASE_URL` auf die
ngrok-URL setzen):

```bash
npm run dev
```

`GET /health` sollte `{"ok":true}` liefern, `GET /api/businesses` die
konfigurierte(n) Business(es).

## Eine Business live schalten (Onboarding)

Die Demo-Business ist zunächst nur ein DB-Eintrag mit Platzhaltern
(`vapiAssistantId: "PENDING_PROVISIONING"`). Um sie wirklich anrufbar zu
machen:

1. In `prisma/seed.ts` (oder per eigenem Skript) die echten Werte eintragen:
   `calcomApiKey`, `calcomUsername`, `services[].calcomEventTypeId`,
   `twilioSmsFromNumber` (deine echte Twilio-Nummer), `escalationPhoneNumber`.
2. Provisionierung ausführen:
   ```bash
   npm run provision -- demo-handwerker
   ```
   Das Skript legt den Vapi-Assistant an (bzw. aktualisiert ihn), importiert
   die Twilio-Nummer in Vapi und speichert die IDs in der `Business`-Zeile.
3. In der Twilio-Konsole für die importierte Nummer den **Status Callback**
   auf `<PUBLIC_BASE_URL>/webhooks/twilio/call-status` setzen (für die
   Missed-Call-Recovery).

## Konfigurationsgetrieben statt Branchen-fest

Jede `Business`-Zeile trägt Branche, Öffnungszeiten, Services, FAQ und
Eskalationsnummer — der Assistant-Prompt und die Tool-Antworten werden daraus
generiert (`src/businesses/business.service.ts`). Eine neue Branche/Kunde
bedeutet einen neuen DB-Eintrag + `npm run provision`, keine Code-Änderung.

## Bewusst nicht enthalten (v1)

Kein Admin-Dashboard-UI (Config nur via `prisma/seed.ts` bzw. REST unter
`/api/businesses`), kein Multi-Tenant-Login/Auth, kein Billing, kein
Self-Serve-Signup, keine Erinnerungs-/No-Show-Follow-ups, keine
Verschlüsselung der gespeicherten Cal.com-API-Keys (Hardening-Punkt für
später), keine Analytics-UI (nur `GET /api/calls?businessId=` wäre der
nächste Schritt).

## Sicherheitshinweis zu Abhängigkeiten

`@vapi-ai/server-sdk` ist bewusst exakt auf `1.2.0` (ohne `^`) gepinnt, da die
Versionen `1.2.1` und `1.2.2` zum Zeitpunkt der Erstellung dieses Projekts als
kompromittiert (Malware im Install-Script) markiert waren. Vor einem Update
dieser Abhängigkeit unbedingt `npm view @vapi-ai/server-sdk@<version> deprecated`
prüfen.
