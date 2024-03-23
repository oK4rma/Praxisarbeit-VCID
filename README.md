# IFA VCID - Firmenfahrzeuge-App

Themeninhalt
• Datenbanken und Webentwicklung (DBWE)
• IT-Architektur (ITAR)
• Virtualisierung und Cloud Computing (VICC)

## Warum dieses Projekt?

Im Rahmen dieser qualifikationsrelevanten Praxisarbeit soll das Erlernte in einen praktischen Kontext zur Anwendung kommen.

### Genauer Arbeitsauftrag

Ihre praktische Arbeit soll die folgenden Ergebnisse erzielen: Eine voll funktionsfähige Anwendung mit Flask und einer Datenbank erstellen. Eine prägnante Dokumentation zur Nutzung der Anwendung bereitstellen. Eine klare Beschreibung der Softwarearchitektur liefern, insbesondere wenn diese von den im Lehrplan behandelten Technologien und Verfahren abweicht. Eine geeignete Cloud-Plattform für die Bereitstellung der Anwendung wählen und dokumentieren, einschließlich der Gründe für die Auswahl sowie der damit verbundenen Vor- und Nachteile. Eine Reflexion über die Skalierbarkeit, Hochverfügbarkeit, Portierung und potenzielle Herausforderungen im operativen Betrieb der Anwendung durchführen.

## Erste Schritte

### Voraussetzungen

Sie sollten eine virtuelle Maschine mit Ubuntu Linux haben.

### Installation

Bitte befolgen Sie diese Schritte, damit alles funktioniert:

1. **Git installieren:**

  ```bash
   sudo apt install -y git
   ```

2. **Das Repository klonen:**

   ```bash
   git clone https://github.com/oK4rma/Praxisarbeit_VCID_Steiner_Tobyas.git
   ```

3. **Navigieren Sie zum Verzeichnis:**

   ```bash
   cd Praxisarbeit_VCID_Steiner_Tobyas
   ```

4. **Anwedung starten**

   ```bash
   docker compose up --build
   ```
  Dadurch werden nun alle Anforderungen aus der „requirements.txt“ installiert und die Anwendung mit NGINX und GUNICORN gestartet

5. **Anwendung starten**

   Da die Anwendung vollständig in Containern verpackt ist, kann die Linux-Maschine beim Hosten einfach geschlossen werden. Die Anwendung läuft weiterhin im Hintergrund.

6. **Anwendung stoppen**

    Mit der Tastenkombination „STRG“ + „C“ kann die Anwendung gestoppt werden.
 

## Testen

Dazu muss die Datei „boot.sh“ gestartet werden. Dadurch wird eine Testumgebung erstellt, alle Anforderungen installiert und die drei automatisierten Tests ausgeführt. Wenn diese erfolgreich durchgeführt wurden, können auch die manuellen Tests durchgeführt werden.

```bash
./boot.sh
```
