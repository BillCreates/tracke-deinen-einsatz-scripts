#!/usr/bin/env sh

# API-URL und API-Key hier eintragen.
API_URL='https://app.trackdeineneinsatz.de/api_einsatz.php'
API_TOKEN='sk_live_dein_generierter_schluessel_hier'

if [ "$#" -ne 1 ] || [ -z "$1" ]; then
  echo 'Fehler: Kein Einsatzstichwort uebergeben.' >&2
  exit 2
fi

if [ -z "$API_TOKEN" ]; then
  echo 'Fehler: API_TOKEN ist nicht gesetzt.' >&2
  exit 2
fi

PAYLOAD=$(python3 -c 'import json, sys; from datetime import datetime; print(json.dumps({"title": sys.argv[1], "alarm_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, ensure_ascii=False))' "$1") || exit 1
curl --fail --silent --show-error -X POST \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $API_TOKEN" \
  --data-binary "$PAYLOAD" \
  "$API_URL"
