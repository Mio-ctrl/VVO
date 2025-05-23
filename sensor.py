import logging
import requests
from datetime import datetime
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEFAULT_MAX_RESULTS = 10

def setup_platform(hass, config, add_entities, discovery_info=None):
    station_ids = config.get("station_ids", [])
    max_results = config.get("max_results", DEFAULT_MAX_RESULTS)

    sensors = []
    for station_id in station_ids:
        sensors.append(VvoDepartureSensor(station_id, max_results))

    add_entities(sensors, True)

class VvoDepartureSensor(Entity):
    def __init__(self, station_id, max_results=DEFAULT_MAX_RESULTS):
        self._station_id = station_id
        self._max_results = max_results
        self._name = f"Abfahrten {station_id}"
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        url = "https://webapi.vvo-online.de/dm"
        payload = {
            "stopid": self._station_id,
            "limit": self._max_results,
            "isarrival": False
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            departures = []

            for journey in data.get("Departures", []):
                planned_time = journey["ScheduledTime"]
                estimated_time = journey.get("RealTime", planned_time)

                dep = {
                    "line": journey.get("LineName", ""),
                    "direction": journey.get("Direction", ""),
                    "departure_time": self._format_time(estimated_time),
                    "scheduled_time": self._format_time(planned_time),
                    "platform": journey.get("Platform", "")
                }
                departures.append(dep)

            self._state = f"{len(departures)} Abfahrten"
            self._attributes = {
                "station_id": self._station_id,
                "departures": departures
            }

        except Exception as e:
            _LOGGER.error(f"[VVO] Fehler beim Abrufen der Abfahrten für {self._station_id}: {e}")
            self._state = "Fehler"
            self._attributes = {}

    def _format_time(self, timestring):
        try:
            # Format: "/Date(1716578880000+0200)/"
            timestamp = int(timestring.split("(")[1].split("+")[0]) / 1000
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%H:%M")
        except Exception as e:
            _LOGGER.warning(f"Fehler beim Formatieren der Zeit: {timestring} – {e}")
            return "?"
