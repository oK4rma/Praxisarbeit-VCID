# IFA VCID - Firmenfahrzeuge-App

## Inhaltsverzeichnis

• Auftrag

  • Warum dieses Projekt?
  
  • Ziel
  
  • Genauer Auftrag
  
  • Themeninhalte
  
• Erste SChritte

  • Voraussetzung
  
  • Installation
  
  • Genauer Auftrag
  
• Testen


## Auftrag

### Warum dieses Projekt?

Um Engpässe und Zeitverzögerungen bei der Nutzung der Firmenfahrzeuge zu vermeiden, wurde eine Webanwendung entwickelt, die es Mitarbeitern ermöglicht, Fahrzeuge zu prüfen, zu reservieren und Nutzungsinformationen zu verfolgen.

### Ziel
Diese Praxisarbeit zielt darauf ab, eine Webanwendung für die Nutzung der Firmenfahrzeuge zu entwickeln, die Benutzern ermöglicht, sich zu registrieren, Fahrzeuge zu prüfen, zu reservieren und Reservierungen zu stornieren, sowie eine Übersicht über die Fahrzeugnutzung zu erhalten. Die Anwendung wurde mit Flask, Python, Jinja2, Tailwind CSS und Gunicorn entwickelt, ist in einem Docker-Container gehostet und integriert eine PostgreSQL-Datenbank und NGINX für vollständige Containerisierung und Einsatzbereitschaft.

### Genauer Auftrag
Die Praxisarbeit zielt darauf ab, eine lauffähige Anwendung mit Flask und einer Datenbank zu entwickeln und eine kurze Dokumentation zur Bedienung bereitzustellen. Zudem umfasst sie eine nachvollziehbare Beschreibung der Softwarearchitektur, eine Cloud-basierte Bereitstellung der Anwendung sowie eine umfassende Dokumentation und Reflexion über die gewählten Technologien und Lösungsansätze, einschließlich potenzieller Herausforderungen im operativen Betrieb.

### Themeninhalt

• Datenbanken und Webentwicklung (DBWE)

• IT-Architektur (ITAR)

• Virtualisierung und Cloud Computing (VICC)

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
