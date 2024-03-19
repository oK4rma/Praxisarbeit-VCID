# Basisimage
FROM python:3.8-slim

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die aktuellen Verzeichnisinhalte in das Arbeitsverzeichnis im Container
COPY . /app

# Installieren Sie die benötigten Pakete aus der requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Installieren Sie Gunicorn
RUN pip install gunicorn

# Starten Sie die App mit Gunicorn. Passen Sie die Anzahl der Worker und Threads nach Bedarf an.
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "car:app"]
