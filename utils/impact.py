# ============================================================
# EcoAgent - Environmental Impact Calculator
# ============================================================

DEVICE_WEIGHTS = {
    "Laptop": 2.0,
    "Smartphone": 0.2,
    "Tablet": 0.5,
    "Battery": 0.5,
    "TV": 8.0,
    "Desktop": 7.0,
    "Other": 2.0
}


def calculate_impact(device_data, recommendation):

    device_type = device_data.get("device_type", "Other")
    age = device_data.get("age", 0)

    # Device weight
    device_weight = DEVICE_WEIGHTS.get(
        device_type,
        2.0
    )

    # Additional useful life
    if recommendation == "Upgrade":
        useful_life = "1–3 years"

    elif recommendation == "Repair":
        useful_life = "1–3 years"

    elif recommendation == "Reuse / Donate":
        useful_life = "2–4 years"

    elif recommendation == "Further Assessment":
        useful_life = "Up to 1 year"

    elif recommendation == "Recycle":
        useful_life = "End of useful life"

    elif recommendation == "Safe Disposal":
        useful_life = "End of useful life"

    else:
        useful_life = "1–2 years"

    return {
        "device_weight": device_weight,
        "useful_life": useful_life,
        "recommendation": recommendation,
        "device_age": age
    }