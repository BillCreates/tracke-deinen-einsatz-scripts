# FE2: Einsatz per API anlegen

Die Logik steckt in `FE2_URL_Aufruf.py` (Python 3.6 oder neuer, nur Standardbibliothek, kein `curl`
nötig). `FE2_URL_Aufruf_Windows.bat` und `FE2_URL_Aufruf_Linux.sh` sind reine Wrapper, die das
Python-Skript mit allen übergebenen Argumenten starten.

Das von FE2 übergebene Stichwort (mehrere Argumente werden mit Leerzeichen zusammengefügt) wird als
JSON-Attribut `title` und die aktuelle Uhrzeit als `alarm_time` per POST an die `API_URL` aus der
`.env` gesendet.

## FE2 konfigurieren

1. `.env.example` nach `.env` kopieren und `API_URL` sowie den generierten Schlüssel bei
   `API_TOKEN` eintragen.
2. Wrapper, `FE2_URL_Aufruf.py` und `.env` gemeinsam innerhalb des FE2-Config-Ordners ablegen:
   - Windows: `C:\ProgramData\Alamos GmbH\FE2\Config\`
   - Linux: im Config-Ordner bzw. dessen Unterordner, Wrapper ausführbar machen mit
     `chmod +x FE2_URL_Aufruf_Linux.sh`
3. Im Plugin **Batch/Shell-Skripte** den vollständigen Dateipfad des Wrappers und die jeweilige
   Plattform wählen.
4. Als Alarmtext z.B. dies eintragen: `"&STICHW&"`

Das Skript sendet die Header `Content-Type: application/json` und `X-API-Key`. Bei HTTP-Fehlern
oder nicht erreichbarer API endet es mit einem Fehlerstatus, den FE2 erhält.

## Logs und Fehlersuche

- Logdatei: `logs/FE2_URL_Aufruf.log` neben dem Skript (rotierend: 512 KB pro Datei, 5 Sicherungen);
  dieselben Zeilen gehen an stderr.
- Protokolliert werden Aufrufargumente, Python-Version, `API_URL`, der gesendete Request sowie die
  Antwort bzw. der Fehler mit Traceback.
- Exit-Code: `0` Einsatz angelegt, `1` API- oder Netzwerkfehler, `2` Stichwort oder `.env` fehlt.
- Keine Logdatei: Entweder wurde Python nicht gefunden (Exit-Code 9009 bzw. 3 unter Windows, 127
  unter Linux; dann `PYTHON` im Wrapper auf den vollständigen Pfad setzen, der FE2-Dienst hat oft
  einen anderen PATH) oder das FE2-Dienstkonto darf im Ordner nicht schreiben (der Einsatz wird
  trotzdem angelegt, nur ohne Logdatei).
- Manuell testen (legt einen echten Einsatz an): `python FE2_URL_Aufruf.py "B1 Brand"`
