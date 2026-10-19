# FE2: Einsatz per API anlegen

Trage in beiden Skripten den generierten Schlüssel bei `API_TOKEN` ein. 
Das von FE2 übergebene Stichwort (mehrere Argumente werden mit Leerzeichen zusammengefügt) wird als JSON-Attribut `title` und die aktuelle Uhrzeit als `alarm_time` per POST an
`https://app.trackdeineneinsatz.de/api_einsatz.php` gesendet.

## FE2 konfigurieren

1. Lege die passende Datei innerhalb des FE2-Config-Ordners ab:
   - Windows: `C:\ProgramData\Alamos GmbH\FE2\Config\FE2_URL_Aufruf_Windows.bat`
   - Linux: im Config-Ordner bzw. dessen Unterordner, ausführbar machen mit
     `chmod +x FE2_URL_Aufruf_Linux.sh`
2. Im Plugin **Batch/Shell-Skripte** den vollständigen Dateipfad und die jeweilige
   Plattform wählen.
3. Als Alarmtext exakt dies eintragen: `"&STICHW&"`

Die Skripte senden die Header `Content-Type: application/json` und `X-API-Key`.
Bei HTTP-Fehlern oder nicht erreichbarer API liefern sie einen Fehlerstatus an
FE2 zurück. Linux benötigt `curl` und `python3`; Windows PowerShell und `curl.exe`.
