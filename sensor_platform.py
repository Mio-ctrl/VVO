import logging
from homeassistant.helpers.entity import Entity
from .sensor import VvoDepartureSensor

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    # Beispiel: Stationen aus Config oder fest in Code
    station_ids = config.get("station_ids", ["12345", "67890"])
    max_results = config.get("max_results", 10)

    sensors = []
    for station_id in station_ids:
        sensors.append(VvoDepartureSensor(station_id, name=f"VVO Abfahrten {station_id}", max_results=max_results))

    async_add_entities(sensors, True)
