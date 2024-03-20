import os
from dotenv import load_dotenv

# Bestimmt den absoluten Pfad des Verzeichnisses, in dem sich diese Datei befindet.
baseDir = os.path.abspath(os.path.dirname(__file__))
# Lädt Umgebungsvariablen aus einer .env-Datei im Basisverzeichnis.
load_dotenv(os.path.join(baseDir, ".env"))

 # Grundlegende Konfigurationsklasse für die Flask-Anwendung.
class Config(object):
    # Setzt den geheimen Schlüssel für die Anwendung.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "not_so_secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL")
    # Konfiguriert die Datenbankverbindung.
    or "sqlite:///" + os.path.join(baseDir, "app.db")
    # Deaktiviert die Signalverfolgung, um Overhead zu vermeiden.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Bestimmt, ob Logs in die Standardausgabe geschrieben werden sollen.
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT") or True
