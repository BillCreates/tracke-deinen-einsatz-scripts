@echo off
setlocal

rem API-URL und API-Key hier eintragen.
set "API_URL=https://app.trackdeineneinsatz.de/api_einsatz.php"
set "API_TOKEN=sk_live_dein_generierter_schluessel_hier"

if "%~1"=="" (
  echo Fehler: Kein Einsatzstichwort uebergeben.
  exit /b 2
)

if "%API_TOKEN%"=="" (
  echo Fehler: API_TOKEN ist nicht gesetzt.
  exit /b 2
)

powershell.exe -NoProfile -Command "$body = @{ title = $args[0] } | ConvertTo-Json -Compress; & curl.exe --fail --silent --show-error -X POST -H 'Content-Type: application/json' -H ('X-API-Key: ' + $env:API_TOKEN) --data-binary $body $env:API_URL; exit $LASTEXITCODE" -- "%~1"
exit /b %ERRORLEVEL%
