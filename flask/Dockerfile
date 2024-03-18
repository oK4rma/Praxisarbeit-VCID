# Basisimage
FROM python:3.8-slim

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die aktuellen Verzeichnisinhalte in das Arbeitsverzeichnis im Container
COPY . /app

# Installieren Sie die benötigten Pakete aus der requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# start app with: flask run --host=0.0.0.0
CMD ["flask", "run", "--host=0.0.0.0"]