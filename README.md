VVO Abfahrts-Sensor für Home Assistant



Projektbeschreibung
Dieser Custom Sensor für Home Assistant ermöglicht das Abfragen und Anzeigen von Abfahrtszeiten öffentlicher Verkehrsmittel des Verkehrsverbunds Oberelbe (VVO).
Der Sensor nutzt die offizielle VVO-Web-API, um für eine oder mehrere Haltestellen aktuelle Abfahrtsinformationen zu erhalten und als Sensorwerte in Home Assistant darzustellen.

Features
Abfrage mehrerer Haltestellen (Station IDs)

Anzeige der nächsten Abfahrten mit Linie, Richtung, Gleis, geplanter und tatsächlicher Abfahrtszeit

Verwendung der offiziellen eindeutigen Fahrt-ID (DlId) zur Identifikation

Zeitanzeige im originalen VVO-Format ohne Zeitzonenverschiebung

Robust gegen API-Fehler mit Fehler-Logging

Einfach in Home Assistant integrierbar

Installation
Lege im custom_components-Verzeichnis deines Home Assistant-Setups einen Ordner vvo_departures an.

Kopiere die Datei sensor.py aus diesem Repository in diesen Ordner.

Füge folgende Konfiguration in deine configuration.yaml ein:

yaml
Kopieren
Bearbeiten
sensor:
  - platform: vvo_departures
    station_ids:
      - "12345"       # Ersetze durch deine Haltestellen-IDs
      - "67890"
    max_results: 10   # Optional, Standard ist 10
Starte Home Assistant neu.

Konfiguration
Parameter	Typ	Beschreibung	Standardwert
station_ids	Liste[String]	Liste der Haltestellen-IDs, für die Abfahrten angezeigt werden sollen	—
max_results	Integer	Maximale Anzahl der angezeigten Abfahrten pro Station	10

Beispielhafte Sensorwerte
Nach der Einrichtung erstellt der Sensor für jede Haltestelle ein Entity mit folgendem Status und Attributen:

Status: Anzahl der verfügbaren Abfahrten (z.B. 5 Abfahrten)

Attribute:

station_id: ID der Haltestelle

departures: Liste der nächsten Abfahrten mit Details wie Linie, Richtung, Abfahrtszeit, geplant, Gleis, DlId und unique_id

Entwicklung & Struktur
setup_platform: Initialisiert Sensoren für jede Haltestelle

VvoDepartureSensor: Hauptklasse, die API abfragt und Daten verarbeitet

parse_ms_date: Hilfsfunktion zum Parsen der Zeitstempel aus der VVO-API

Bekannte Einschränkungen
Zeitangaben werden 1:1 von der API übernommen, ohne Umrechnung in lokale Zeitzonen

Keine Unterstützung für Ankunftszeiten (nur Abfahrten)

Synchroner API-Zugriff (kann in Zukunft asynchron umgesetzt werden)
