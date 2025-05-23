from homeassistant.helpers.discovery import async_load_platform

async def async_setup(hass, config):
    # Wir registrieren nur die Plattform "sensor"
    hass.async_create_task(
        async_load_platform(hass, "sensor", "vvo", {}, config)
    )
    return True
