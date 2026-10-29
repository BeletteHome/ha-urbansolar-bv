import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import selector
from homeassistant.const import UnitOfEnergy, UnitOfPower

from .const import (
    DOMAIN,
    CONF_SOLAR_POWER_SENSOR,
    CONF_TOTAL_POWER_CONSO_SENSOR,
)


def _validate_power_sensors(hass, user_input):
    errors = {}
    for input_key in (CONF_SOLAR_POWER_SENSOR, CONF_TOTAL_POWER_CONSO_SENSOR):
        state = hass.states.get(user_input[input_key])
        if (
            state is None
            or state.attributes.get("unit_of_measurement") != UnitOfPower.KILO_WATT
        ):
            errors[input_key] = "invalid_unit"
    return errors


class VirtualBatteryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for UrbanSolar Virtual Battery."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user input."""
        errors = {}

        if user_input is not None:
            errors = _validate_power_sensors(self.hass, user_input)

            self._log("Validation errors:", errors)

            if not errors:
                # Créer l'entrée sans await (car ce n'est pas une coroutine)
                entry = self.async_create_entry(title="UrbanSolar Battery", data=user_input)

                # Réinitialiser input_number.urban_energie_battery_out_hourly et in à 0
                for entity_id in [
                        "input_number.urban_energie_battery_out_hourly",
                        "input_number.urban_energie_battery_in_hourly",
                ]:
                        await self.hass.services.async_call(
                            "input_number",
                            "set_value",
                            {
                                "entity_id": entity_id,
                                "value": 0,
                            },
                            blocking=True,
                             )

                return entry


        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_SOLAR_POWER_SENSOR): selector({
                    "entity": {
                        "domain": "sensor",
                        "device_class": "power"
                    }
                }),
                vol.Required(CONF_TOTAL_POWER_CONSO_SENSOR): selector({
                    "entity": {
                        "domain": "sensor",
                        "device_class": "power"
                    }
                }),
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return VirtualBatteryOptionsFlowHandler(config_entry)

    @staticmethod
    def _log(message, *args):
        """Simple logger."""
        print(f"[VirtualBatteryConfigFlow] {message} {args}")


class VirtualBatteryOptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow for UrbanSolar Virtual Battery."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle the options form."""
        errors = {}
        current_config = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            errors = _validate_power_sensors(self.hass, user_input)
            if not errors:
                self._log("Options flow user input:", user_input)
                return self.async_create_entry(title="", data=user_input)

        self._log("Current config:", current_config)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_SOLAR_POWER_SENSOR,
                    default=current_config.get(CONF_SOLAR_POWER_SENSOR, "")
                ): selector({
                    "entity": {
                        "domain": "sensor",
                        "device_class": "power"
                    }
                }),
                vol.Required(
                    CONF_TOTAL_POWER_CONSO_SENSOR,
                    default=current_config.get(CONF_TOTAL_POWER_CONSO_SENSOR, "")
                ): selector({
                    "entity": {
                        "domain": "sensor",
                        "device_class": "power"
                    }
                }),
            }),
            errors=errors
        )

    def _log(self, message, *args):
        print(f"[VirtualBatteryOptionsFlowHandler] {message} {args}")