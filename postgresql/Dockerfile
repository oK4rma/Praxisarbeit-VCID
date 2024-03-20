# Verwendet das neueste offizielle PostgreSQL-Image als Basis.
FROM postgres:latest

# Kopiert die init-db.sql Datei in das Verzeichnis /docker-entrypoint-initdb.d/ im Container.
# PostgreSQL führt alle .sql-Dateien in diesem Verzeichnis automatisch beim ersten Start aus,
# um die Datenbank zu initialisieren.
COPY init-db.sql /docker-entrypoint-initdb.d/
