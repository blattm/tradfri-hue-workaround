# Settings per model id. Every model has a "default", and may have complete
# overrides keyed by software version for firmwares that behave differently.
# An override replaces the default outright, it is not merged into it.
SETTINGS_BY_MODELID = {
    "TRADFRI bulb E14 WS candle 470l": {
        "default": {
            "color": True,
            "brightness": False,
            "freezes": True,
        },
    },
    "TRADFRI bulb E14 WS globe 470lm": {
        "default": {
            "color": True,
            "brightness": False,
            "freezes": True,
        },
    },
    "TRADFRI bulb E14 CWS globe 806l": {
        "default": {
            "color": False,
            "brightness": True,
            "freezes": True,
        },
    },
    "TRADFRI bulb E27 CWS globe 806l": {
        "default": {
            "color": False,
            "brightness": False,
            "freezes": True,
        },
        # Only this firmware drops the color command when the brightness changes too
        "1.0.44": {
            "color": True,
            "brightness": True,
            "freezes": True,
        },
    },
    "TRADFRIbulbE27WSglobeclear806lm": {
        "default": {
            "color": False,
            "brightness": True,
            "freezes": False,
        },
    },
}


def get_settings(model_id, swversion):
    '''Settings for a light, or None if the model is not in the table'''
    model = SETTINGS_BY_MODELID.get(model_id)
    if model is None:
        return None
    return model.get(swversion, model.get("default"))
