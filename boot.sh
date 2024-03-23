#!/bin/bash

# Setzen Sie das erwartete Verzeichnis für das Skript
EXPECTED_DIR="/flask"

# Aktuelles Verzeichnis prüfen und wechseln falls notwendig
if [ "$(pwd)" != "$EXPECTED_DIR" ]; then
    echo "Wechsele zum erwarteten Verzeichnis..."
    cd "$EXPECTED_DIR" || exit 1
fi

# Prüfen ob .env existiert
if [ ! -f .env ]; then
    echo "Die .env Datei existiert nicht."
    exit 1
fi

# Backup der .env-Datei erstellen
cp .env .env_backup 

# Erstelle Testumgebung
echo "Erstelle Testumgebung..."
pytest --setup-show tests

# Installiere erforderliche Pakete
echo "Installiere erforderliche Pakete..."
pip install -r requirements.txt

# Führe Tests aus
echo "Führe Tests aus..."
pytest tests

# Prüfen ob Tests erfolgreich waren
if [ $? -ne 0 ]; then
    echo "Tests fehlgeschlagen. Abbruch."
    exit 1
fi

# Images neu erstellen
docker compose down --rmi all
docker compose up -d --build

# Lösche alle nicht verwendeten Docker-Images
echo "Lösche alle nicht verwendeten Docker-Images..."
docker image prune -a --force
