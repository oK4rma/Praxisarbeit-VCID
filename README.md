# IFA VCID - Firmenfahrzeuge-App

Themeninhalt
• Datenbanken und Webentwicklung (DBWE)
• IT-Architektur (ITAR)
• Virtualisierung und Cloud Computing (VICC)

## Warum dieses Projekt?

Im Rahmen dieser qualifikationsrelevanten Praxisarbeit soll das Erlernte in einen praktischen Kontext zur Anwendung kommen.

### Genauer Arbeitsauftrag

Ihre praktische Arbeit soll folgende Ergebnisse liefern:
• Eine ausführbare Anwendung mit Flask und einer Datenbank
• Eine kurze Dokumentation zur Verwendung der Anwendung
• Eine verständliche Beschreibung der Architektur der Software, insbesondere wenn diese aus dem
   Technologien und Verfahren weichen von der Lehre ab.
• Eine Plattform, auf der die Anwendung in der Cloud bereitgestellt wird
• Dokumentation der ausgewählten Plattform(en), Technologie(n), Architektur und Lösungsansätze
   Darüber hinaus wird darüber nachgedacht, warum dies gewählt wurde und welche Vorteile und potenziellen Risiken es mit sich bringt
   bringt.
• Reflexion über Skalierbarkeit, Hochverfügbarkeit, Portierung und mögliche Herausforderungen
   operativer Betrieb.

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
