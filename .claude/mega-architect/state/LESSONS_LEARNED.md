# Lessons Learned

## Aktive Regeln (aus wiederkehrenden Mustern)
- [2026-07-26] Vor jeder Deployment-/Security-relevanten Aussage `git ls-files` +
  `git check-ignore` aktiv prüfen, ob `.env`/`config.json`/ähnliche Dateien bereits
  getrackt sind, statt nur anzunehmen, dass sie lokal gehalten werden.

## Log

### 2026-07-26 – Task: Test-Lauf mega-architect Skill (Pre-Mortem für Cloud-Deployment)
- **Gut:** Bevor generisch über "Deployment-Risiken" geschrieben wurde, wurden zuerst
  `bot.py`, `README.md` und die Config-Dateien gelesen – dadurch sind die Risiken im
  `PRE_MORTEM.md` konkret und am echten Code verankert (z.B. fehlender Mod-Check bei
  `!rec`, OBS-WebSocket-Abhängigkeit von einem lokalen Host) statt generischer Floskeln.
- **Schlecht:** n/a für diesen Testlauf – Ergebnis war beim ersten Durchgang brauchbar.
- **Besser wäre gewesen:** Diese Prüfung war ursprünglich nur als Nachtrag geplant –
  richtig wäre, `git ls-files`/`git check-ignore` als festen ersten Schritt jeder
  Pre-Mortem-/Security-Analyse zu behandeln, nicht erst nachträglich.
- **Muster erkannt?** Ja – die nachträgliche Prüfung deckte sofort einen echten,
  kritischen Fund auf (`.env` und `config.json` sind im Git getrackt, inkl. eines wie
  echt aussehenden OAuth-Tokens). Daraus wurde eine aktive Regel oben abgeleitet.
