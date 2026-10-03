def check_safety(device_data):
    """
    Check whether the device has any dangerous condition.
    """

    battery_condition = device_data.get("battery_condition", "")
    main_problem = device_data.get("main_problem", "").lower()
    physical_condition = device_data.get("physical_condition", "")

    # Swollen battery
    if battery_condition == "Swollen":
        return {
            "is_safe": False,
            "reason": "The device has a swollen battery.",
            "action": "Stop using the device and seek safe battery/e-waste disposal guidance."
        }

    # Dangerous battery-related descriptions
    dangerous_words = [
        "swollen",
        "bulging",
        "leaking battery",
        "battery leaking",
        "burning",
        "smoke",
        "sparking",
        "overheating"
    ]

    for word in dangerous_words:
        if word in main_problem:
            return {
                "is_safe": False,
                "reason": f"Possible safety issue detected: {word}.",
                "action": "Stop using the device and seek appropriate safety or e-waste disposal guidance."
            }

    # Severe physical damage
    if physical_condition == "Damaged" and any(
        word in main_problem
        for word in ["burn", "smoke", "spark", "fire"]
    ):
        return {
            "is_safe": False,
            "reason": "The device may have a serious physical/electrical safety issue.",
            "action": "Do not continue using the device. Seek appropriate professional or e-waste safety guidance."
        }

    # No obvious safety issue
    return {
        "is_safe": True,
        "reason": "No immediate safety issue was detected from the provided information.",
        "action": "The device can proceed to normal assessment."
    }