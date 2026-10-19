@echo off
setlocal

rem API-URL und API-Key hier eintragen.
set "API_URL=https://app.trackdeineneinsatz.de/api_einsatz.php"
set "API_TOKEN=sk_live_dein_generierter_schluessel_hier"

rem %* nicht direkt vergleichen: Anfuehrungszeichen/Sonderzeichen wuerden die if-Zeile zerlegen.
set "HAS_TITLE="
for %%A in (%*) do if not "%%~A"=="" set "HAS_TITLE=1"
if not defined HAS_TITLE (
  echo Fehler: Kein Einsatzstichwort uebergeben.
  exit /b 2
)

if "%API_TOKEN%"=="" (
  echo Fehler: API_TOKEN ist nicht gesetzt.
  exit /b 2
)

rem -X utf8: Python gibt sonst in die Codepage (cp1252) aus und scheitert bei Emoji.
python -X utf8 -c "import json, sys; from datetime import datetime; print(json.dumps({'title': ' '.join(sys.argv[1:]), 'alarm_time': datetime.now().strftime('%%Y-%%m-%%d %%H:%%M:%%S')}, ensure_ascii=False))" %* | curl.exe --fail --silent --show-error -X POST -H "Content-Type: application/json" -H "X-API-Key: %API_TOKEN%" --data-binary @- "%API_URL%"
exit /b %ERRORLEVEL%
