import logging
from datetime import timedelta
import requests

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "VVO Departure"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required("station_id"): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

SCAN_INTERVAL = timedelta(minutes=1)  # alle 1 Minute aktualisieren

def setup_platform(hass, config, add_entities, discovery_info=None):
    station_id = config.get("station_id")
    name = config.get(CONF_NAME)

    add_entities([VvoDepartureSensor(station_id, name)], True)

class VvoDepartureSensor(Entity):
    def __init__(self, station_id, name):
        self._station_id = station_id
        self._name = name
        self._state = None
        self._departures = []

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        # Zum Beispiel: Anzahl der Abfahrten
        if self._departures:
            return len(self._departures)
        return "unbekannt"

    @property
    def extra_state_attributes(self):
        # Hier können wir die Abfahrten detailliert ablegen
        return {
            "departures": self._departures
        }

    def update(self):
        _LOGGER.debug(f"Rufe Abfahrten für Station {self._station_id} ab...")
        # Hier holst du die echten Daten von der API (Dummy hier)
        try:
            # Beispiel-Request (muss auf VVO-API angepasst werden)
            url = f"https://example-vvo-api/station/{self._station_id}/departures"
            # response = requests.get(url)
            # data = response.json()

            # Dummy Daten als Beispiel
            data = [
                {"line": "4", "direction": "Weinböhla", "departure_time": "23:01"},
                {"line": "3", "direction": "Striesen", "departure_time": "23:05"},
            ]
            self._departures = data
        except Exception as e:
            _LOGGER.error(f"Fehler beim Abrufen der VVO Daten: {e}")
            self._departures = []
