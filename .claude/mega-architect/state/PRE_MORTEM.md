# Pre-Mortem: Deployment von recording-bot-OBS auf einen neuen Cloud-Server
Datum: 2026-07-26
Modul: 2 (Proactive Pre-Mortem) – Test-Lauf des mega-architect Skills

## Annahme
Wir nehmen an, das Deployment auf einen neuen Cloud-Server ist gescheitert bzw. hat
zu einem ernsten Vorfall geführt. Warum?

## Risiken

### Technisch
| Risiko | Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|---|---|---|---|
| **KRITISCH – Secrets bereits in Git getrackt**: Verifiziert (`git ls-files`): sowohl `.env` als auch `config.json` sind aktuell im Repository getrackt, nicht nur lokal vorhanden. `.env` enthält einen wie ein echtes Twitch-OAuth-Token aussehenden Wert, `config.json` ein OBS-WebSocket-Passwort. Es existiert keine `.gitignore`. Ein Cloud-Deployment (z.B. via `git clone` auf dem Server oder CI/CD-Checkout) würde diese Secrets 1:1 mitausrollen und in der Versionshistorie für jeden Repo-Zugriff sichtbar lassen. | **bestätigt (kein Risiko, sondern Ist-Zustand)** | hoch (Account-/Session-Übernahme, wenn Repo geleakt/öffentlich wird) | Sofort vor jedem Deployment: (1) Token/Passwort rotieren – aktuell committete Werte als kompromittiert behandeln, (2) `.env` und `config.json` aus dem Git-Tracking entfernen (`git rm --cached`) und in `.gitignore` aufnehmen, (3) `config.json.example`/`.env.example` mit Platzhaltern committen, (4) bei Bedarf History-Rewrite prüfen (separate, bewusste Entscheidung mit dem User, da destruktiv). |
| **Architektur-Mismatch**: `bot.py` verbindet sich per `obsws_python.ReqClient` mit einer OBS-WebSocket-Instanz über `config.json` (`host`/`port`/`password`). OBS läuft typischerweise auf dem PC des Streamers, nicht im Cloud-Rechenzentrum. Ein Cloud-Server hat ohne VPN/Port-Forwarding keinen Netzwerkzugriff auf die lokale OBS-Instanz. | hoch | hoch (Kernfunktion fällt komplett aus) | Vor dem Deployment klären: Soll OBS auch remote/headless laufen, oder bleibt der Bot lokal und nur Zusatzdienste (z.B. zukünftige Web-Features) wandern in die Cloud? Falls echte Cloud-Steuerung gewünscht: OBS-WebSocket über gesichertes VPN (z.B. Wireguard) oder SSH-Tunnel exponieren, niemals Port 4455 offen ins Internet legen. |
| **Keine Autorisierung für Recording-Commands**: `!rec`/`!stoprec` sind laut `bot.py:101-106` für JEDEN Chat-Nutzer verfügbar (kein Mod-Check). README-FAQ bestätigt das explizit ("Nur Mods? Nein noch alle"). In der Cloud öffentlich erreichbar bedeutet: jeder Zuschauer kann Aufnahmen willkürlich starten/stoppen. | hoch | mittel (Kontrollverlust, Datenchaos, ggf. Trolling live on stream) | Vor Deployment Mod-/Broadcaster-Check ergänzen (Twitch-Badges aus IRC-Tags auswerten), bis dahin Deployment nur mit Hinweis an den User, dass dieses Risiko ungelöst bleibt. |
| **Keine Rekonnektion/Fehlerresilienz**: `IRC.loop()` hat keine Reconnect-Logik; bricht `sock.recv()` (z.B. Netzwerk-Hänger, wie er in Cloud-Umgebungen mit variabler Netzwerklatenz üblicher ist als lokal) mit einer nicht abgefangenen Exception ab, stirbt der Prozess. Kein Supervisor/Restart vorgesehen. | mittel | hoch (Bot bleibt nach einem Disconnect dauerhaft offline, ohne dass es jemand bemerkt) | Prozess-Supervisor einplanen (systemd-Service mit `Restart=always`, oder Docker mit Restart-Policy) + Monitoring/Alert bei Absturz (siehe Modul 28, Monitoring & Alerts). |
| **Secrets im Klartext**: OAuth-Token in `.env`, OBS-Passwort in `config.json` – beide unverschlüsselt. Auf einem geteilten/öffentlichen Cloud-Server steigt das Risiko eines Secret-Leaks (z.B. versehentlich committed, oder Server-Kompromittierung). | mittel | hoch (Account-Übernahme via Twitch-OAuth, wenn kompromittiert) | Vor Deployment: `.env`/`config.json` in `.gitignore` sicherstellen (aktuell nicht geprüft), Secrets über Cloud-Provider-Secret-Manager statt Datei einspielen, Token-Scopes minimal halten (nur `chat:read`, `chat:edit`). |
| **Kein TLS/Verschlüsselung auf IRC-Socket**: `IRC.connect()` nutzt Port 6667 (Klartext-IRC) statt der TLS-Variante (6697). In einer Cloud-Umgebung mit potenziell weniger vertrauenswürdigem Netzwerkpfad ist das ein zusätzliches Abhörrisiko für den OAuth-Token beim Verbindungsaufbau. | niedrig | mittel | Auf `irc.chat.twitch.tv:6697` mit TLS umstellen, bevor der Bot öffentlich/remote läuft. |

### Business
| Risiko | Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|---|---|---|---|
| **Live-Vorfall vor Publikum**: Da der Bot während eines laufenden Streams eingesetzt wird, führt jeder technische Ausfall (siehe oben) zu einem sichtbaren Vorfall vor der Community, nicht zu einem stillen Bug. | mittel | mittel-hoch (Vertrauensverlust bei Zuschauern, falls Aufnahmen verloren gehen) | Deployment auf Cloud zunächst nur in einer Testphase außerhalb eines Live-Streams validieren, nicht direkt im Live-Betrieb erstmalig testen. |
| **Ein-Channel-Beschränkung bleibt bestehen**: Laut README ist "Eine Installation = ein Channel" – ein Cloud-Deployment ändert daran nichts, könnte aber fälschlich als "jetzt Multi-Channel-fähig" verstanden werden. | niedrig | niedrig | Klar kommunizieren, dass das Cloud-Deployment die 1:1-Architektur nicht aufhebt, falls das nicht Teil dieses Tasks ist. |

### Zeit
| Risiko | Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|---|---|---|---|
| **Unterschätzter Netzwerk-Aufwand**: Die eigentliche Herausforderung ist nicht der Bot-Prozess selbst (leichtgewichtig, siehe README "Performance: ~50MB RAM, <1% CPU"), sondern die sichere Netzwerkanbindung an OBS. Das wird leicht unterschätzt, wenn man nur an "Bot in Cloud starten" denkt. | hoch | mittel (Deployment dauert deutlich länger als geplant) | Zeitschätzung getrennt für "Bot deployen" (kurz) und "sichere OBS-Konnektivität herstellen" (deutlich länger, ggf. VPN-Setup) ausweisen. |
| **DNS/Firewall-Wartezeiten**, falls der Server öffentlich per Domain erreichbar sein soll (z.B. für zukünftige Webhooks) – DNS-Propagation kann Stunden dauern. | niedrig | niedrig | Nicht am geplanten Launch-/Stream-Tag selbst einplanen, siehe Modul 27 (Domain & SSL). |

## Fazit
**Go mit Anpassungen.** Das reine Deployment des Bot-Prozesses in die Cloud ist technisch
trivial (geringer Ressourcenbedarf). Der eigentliche Blocker ist die Architektur-Annahme
"OBS läuft lokal neben dem Bot" – das muss vor dem Deployment explizit geklärt werden,
sonst startet der Bot in der Cloud und kann OBS nie erreichen. Zusätzlich sollte die
fehlende Zugriffskontrolle auf `!rec`/`!stoprec` behoben werden, bevor der Bot öffentlich
über einen Server läuft, der potenziell erreichbarer/langlebiger ist als ein lokaler PC.

**Keine der oben genannten Gegenmaßnahmen wurde automatisch umgesetzt** – dies ist eine
reine Risikoanalyse gemäß Modul 2. Eine tatsächliche Code-Änderung, ein echtes
Deployment oder ein Secret-Handling-Wechsel erfolgt erst nach Rücksprache mit dem User
(siehe `SKILL.md`, Anwendungsregel 6).
