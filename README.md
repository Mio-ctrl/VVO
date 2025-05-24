# VVO Abfahrts-Sensor für Home Assistant

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)  
[![Home Assistant](https://img.shields.io/badge/home--assistant-supported-green)](https://www.home-assistant.io/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Übersicht

**VVO Abfahrts-Sensor** ist ein Custom Sensor für [Home Assistant](https://www.home-assistant.io/), der aktuelle Abfahrtszeiten des Verkehrsverbunds Oberelbe (VVO) über die offizielle VVO-Web-API abruft und anzeigt.

Er unterstützt mehrere Haltestellen, zeigt geplante und tatsächliche Abfahrtszeiten an und nutzt dabei die eindeutige Fahrt-ID (`DlId`), um Abfahrten präzise zu identifizieren.

---

## Features

- ✅ Abfrage mehrerer Haltestellen gleichzeitig  
- ✅ Anzeige von Linie, Richtung, Abfahrtszeit (geplant & real) und Gleis  
- ✅ Nutzung der offiziellen Fahrt-ID (`DlId`) für eindeutige Identifikation  
- ✅ Zeitangaben genau wie von der API bereitgestellt (keine Zeitzonenanpassung)  
- ✅ Fehlerbehandlung und Logging  
- ✅ Einfache Integration in Home Assistant

---

## Installation

1. Lege in deinem Home Assistant Verzeichnis unter `custom_components` einen neuen Ordner namens `vvo_departures` an.

2. Kopiere die Datei `sensor.py` in diesen Ordner.

3. Füge in deine `configuration.yaml` folgende Konfiguration ein:

```yaml
sensor:
  - platform: vvo_departures
    station_ids:
      - "12345"       # Beispiel-Haltestellen-ID, anpassen!
      - "67890"
    max_results: 10    # Optional, Standardwert: 10
