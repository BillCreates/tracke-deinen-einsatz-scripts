@echo off
setlocal

rem Bei Bedarf vollstaendigen Pfad zu python.exe eintragen (der FE2-Dienst hat oft einen anderen PATH).
set "PYTHON=python"

rem -X utf8: Ausgabe sonst in der Codepage (cp1252); Emoji im Stichwort wuerden das Logging stoeren.
"%PYTHON%" -X utf8 "%~dp0FE2_URL_Aufruf.py" %*
exit /b %ERRORLEVEL%
