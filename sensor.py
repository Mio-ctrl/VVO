import logging
import requests
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

API_URL = "https://webapi.vvo-online.de/dm"

class VvoDepartureSensor(Entity):
    def __init__(self, station_id, name="VVO Abfahrten", max_results=10):
        self._station_id = station_id
        self._name = name
        self._max_results = max_results
        self._departures = []
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return f"{len(self._departures)} Abfahrten geladen"

    @property
    def extra_state_attributes(self):
        return {"departures": self._departures}

    def update(self):
        params = {
            "haltestelleId": self._station_id,
            "format": "json",
            "limit": self._max_results
        }
        try:
            response = requests.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Prüfen, ob Daten vorhanden sind
            departures_raw = data.get("departures", [])
            departures = []

            for entry in departures_raw:
                line = entry.get("line", {}).get("name", "")
                direction = entry.get("direction", "")
                departure_time = entry.get("departureTime", "")

                departures.append({
                    "line": line,
                    "direction": direction,
                    "departure_time": departure_time
                })

            self._departures = departures
            _LOGGER.debug(f"Abfahrten für {self._station_id}: {self._departures}")

        except Exception as e:
            _LOGGER.error(f"Fehler beim Abrufen der VVO Daten: {e}")
            self._departures = []
