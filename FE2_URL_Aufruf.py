"""Legt aus einem FE2-Alarm per API einen Einsatz bei Track Deinen Einsatz an.

Aufruf: python FE2_URL_Aufruf.py <Einsatzstichwort...>
API_URL und API_TOKEN stehen in der .env neben diesem Skript.
Exit-Code: 0 = Einsatz angelegt, 1 = API-/Netzwerkfehler, 2 = Stichwort oder Konfiguration fehlt.
"""
import http.client
import json
import logging
import logging.handlers
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
LOG_FILE = BASE_DIR / "logs" / "FE2_URL_Aufruf.log"
TIMEOUT_SECONDS = 30

log = logging.getLogger("fe2")


def setup_logging():
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(levelname)-7s [%(process)d] %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    log.addHandler(console)

    try:
        LOG_FILE.parent.mkdir(exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=512 * 1024, backupCount=5, encoding="utf-8")
    except OSError as exc:
        log.warning(f"Logdatei {LOG_FILE} nicht beschreibbar: {exc}")
        return
    
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)


def load_env(path):
    values = {}

    # utf-8-sig: Windows-Editoren speichern die .env gern mit BOM.
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        value = value.strip()

        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]

        values[key.strip()] = value
    return values


def post_json(parts, headers, payload):
    # http.client statt urllib: urllib schreibt Header-Namen um (X-API-Key -> X-Api-Key).
    connection_class = http.client.HTTPSConnection if parts.scheme == "https" else http.client.HTTPConnection
    connection = connection_class(parts.hostname, parts.port, timeout=TIMEOUT_SECONDS)

    try:
        target = urllib.parse.urlunsplit(("", "", parts.path or "/", parts.query, ""))
        connection.request("POST", target, payload.encode("utf-8"), headers)
        response = connection.getresponse()
        body = response.read().decode("utf-8", "replace")[:2000]
        return response.status, response.reason, response.getheader("Location"), body
    finally:
        connection.close()


def main(args):
    log.info(f"Start: argv={sys.argv!r}")
    log.debug(f"Python {sys.version.split()[0]} ({sys.executable}) auf {sys.platform}")

    title = " ".join(args)

    if not title.strip():
        log.error("Kein Einsatzstichwort uebergeben.")
        return 2

    if not ENV_FILE.is_file():
        log.error(f".env nicht gefunden: {ENV_FILE}")
        return 2
    
    config = load_env(ENV_FILE)
    log.debug(f"Schluessel in .env: {sorted(config)}")
    url = config.get("API_URL", "")
    token = config.get("API_TOKEN", "")
    missing = [name for name, value in (("API_URL", url), ("API_TOKEN", token)) if not value]

    if missing:
        log.error(f"In {ENV_FILE} fehlt: {', '.join(missing)}")
        return 2
    
    parts = urllib.parse.urlsplit(url)

    if parts.scheme not in ("http", "https") or not parts.hostname:
        log.error(f"API_URL ungueltig (erwartet http(s)://host/pfad): {url}")
        return 2
    
    log.info(f"API_URL={url}")

    payload = json.dumps({"title": title, "alarm_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, ensure_ascii=False)
    headers = {"Content-Type": "application/json", "X-API-Key": token, "User-Agent": "FE2_URL_Aufruf"}

    log.info(f"Sende POST: {payload}")
    log.debug(f"Request-Header: {sorted(headers)}")

    started = time.monotonic()
    try:
        status, reason, location, body = post_json(parts, headers, payload)
    except Exception:
        log.exception(f"Anfrage an {url} fehlgeschlagen")
        return 1
    elapsed_ms = (time.monotonic() - started) * 1000

    if 200 <= status < 300:
        log.info(f"Antwort: HTTP {status} {reason} ({elapsed_ms:.0f} ms): {body}")
        return 0
    
    log.error(f"Fehlerantwort: HTTP {status} {reason} ({elapsed_ms:.0f} ms): {body}")

    if location:
        log.error(f"Weiterleitung nach {location} - API_URL in .env pruefen")
    return 1


if __name__ == "__main__":
    setup_logging()

    try:
        exit_code = main(sys.argv[1:])
    except Exception:
        log.exception("Abbruch durch unerwarteten Fehler")
        exit_code = 1
    
    log.info(f"Ende mit Exit-Code {exit_code}")
    sys.exit(exit_code)
