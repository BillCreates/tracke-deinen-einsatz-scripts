#!/usr/bin/env sh

# Bei Bedarf vollstaendigen Pfad zu python3 eintragen (der FE2-Dienst hat oft einen anderen PATH).
PYTHON='python3'

exec "$PYTHON" -X utf8 "$(dirname "$0")/FE2_URL_Aufruf.py" "$@"
