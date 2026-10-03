# ============================================================
# EcoAgent - Decision Engine
# ============================================================

from agent.knowledge_base import get_device_info


def make_decision(device_data):
    """
    Decide what should happen to the device:
    Repair, Upgrade, Reuse / Donate, Recycle, Safe Disposal,
    or Further Assessment.
    """

    # ========================================================
    # BASIC DEVICE INFORMATION
    # ========================================================

    device_type = device_data.get("device_type", "").lower()
    age = device_data.get("age", 0)
    power_status = device_data.get("power_status", "")
    physical_condition = device_data.get("physical_condition", "")
    problem = device_data.get("main_problem", "").lower().strip()
    ram = device_data.get("ram", "")
    storage = device_data.get("storage", "")
    battery_condition = device_data.get(
        "battery_condition",
        ""
    )


    # ========================================================
    # KNOWLEDGE BASE
    # ========================================================

    device_info = get_device_info(device_type)

    repair_options = device_info.get(
        "repair_options",
        []
    )

    upgrade_options = device_info.get(
        "upgrade_options",
        []
    )

    reuse_options = device_info.get(
        "reuse_options",
        []
    )


    # ========================================================
    # 1. SWOLLEN BATTERY / SAFETY CONDITION
    # ========================================================

    if battery_condition == "Swollen":

        return {
            "recommendation": "Safe Disposal",

            "reason":
                "The device has a swollen battery, "
                "which requires safe handling.",

            "actions": [
                "Stop using the device.",
                "Do not puncture or open the battery.",
                "Keep the device away from heat.",
                "Use an appropriate battery/e-waste disposal service."
            ]
        }


    # ========================================================
    # 2. DEVICE DOES NOT POWER ON + DAMAGED
    # ========================================================

    if (
        power_status == "No"
        and physical_condition == "Damaged"
    ):

        return {
            "recommendation": "Recycle",

            "reason":
                "The device does not power on and has "
                "significant physical damage.",

            "actions": [
                "Do not dispose of it in regular household waste.",
                "Back up or remove personal data if possible.",
                "Send the device to an authorized e-waste recycler."
            ]
        }


    # ========================================================
    # 3. REPAIRABLE PROBLEMS
    # ========================================================

    repair_keywords = [
        "broken screen",
        "cracked screen",
        "screen damage",
        "keyboard",
        "charging port",
        "charger",
        "speaker",
        "camera",
        "display",
        "screen",
        "power button",
        "button",
        "touch problem",
        "charging problem"
    ]

    repair_detected = any(
        word in problem
        for word in repair_keywords
    )


    # Also check device-specific knowledge base problems

    kb_repair_detected = any(
        problem in common_problem.lower()
        or common_problem.lower() in problem
        for common_problem in device_info.get(
            "common_problems",
            []
        )
    )


    if repair_detected:

        actions = [
            "Get the device inspected by a qualified technician.",
            "Compare repair cost with replacement cost.",
            "Repair the affected component if practical."
        ]

        # Add relevant knowledge-base repair options

        if repair_options:

            actions.append(
                "Possible repair options: "
                + ", ".join(repair_options[:3])
            )

        return {
            "recommendation": "Repair",

            "reason":
                "The reported problem may be repairable "
                "without replacing the entire device.",

            "actions": actions
        }


    # ========================================================
    # 4. LAPTOP / DESKTOP PERFORMANCE UPGRADE
    # ========================================================

    upgrade_keywords = [
        "slow",
        "slow performance",
        "lag",
        "takes long time",
        "freezing",
        "low storage",
        "performance problem",
        "hanging"
    ]


    performance_problem = any(
        word in problem
        for word in upgrade_keywords
    )


    if device_type in [
        "laptop",
        "desktop"
    ] and performance_problem:

        # RAM / HDD based upgrade

        if (
            ram in ["2 GB", "4 GB"]
            or storage == "HDD"
        ):

            actions = [
                "Consider upgrading RAM.",
                "Consider replacing an HDD with an SSD.",
                "Remove unnecessary software and files.",
                "Check the device's overall health."
            ]

            if upgrade_options:

                actions.append(
                    "Knowledge-base upgrade options: "
                    + ", ".join(upgrade_options[:3])
                )

            return {
                "recommendation": "Upgrade",

                "reason":
                    "The device is experiencing performance "
                    "problems and its hardware specifications "
                    "suggest that an upgrade may extend its useful life.",

                "actions": actions
            }


        # Performance problem but no obvious hardware limitation

        return {
            "recommendation": "Upgrade",

            "reason":
                "The device has a performance problem that "
                "may be improved through maintenance, storage "
                "optimization, or suitable hardware upgrades.",

            "actions": [
                "Remove unnecessary applications and files.",
                "Check storage health.",
                "Update the operating system and drivers.",
                "Check whether RAM or SSD upgrades are supported."
            ]
        }


    # ========================================================
    # 5. STORAGE PROBLEM
    # ========================================================

    if (
        "storage" in problem
        or "low storage" in problem
    ):

        if device_type in [
            "laptop",
            "desktop"
        ]:

            return {
                "recommendation": "Upgrade",

                "reason":
                    "The device has a storage-related "
                    "performance problem that may be improved "
                    "without replacing the entire device.",

                "actions": [
                    "Remove unnecessary files.",
                    "Move large files to external storage.",
                    "Consider upgrading the storage drive.",
                    "Consider an SSD upgrade if the device supports it."
                ]
            }


    # ========================================================
    # 6. BATTERY PROBLEM
    # ========================================================

    if (
        battery_condition == "Poor"
        or "battery problem" in problem
        or "poor battery" in problem
    ):

        if device_type != "battery":

            battery_repairs = [
                "Replace the old battery.",
                "Use an original or compatible replacement battery.",
                "Check the charging system."
            ]

            return {
                "recommendation": "Repair",

                "reason":
                    "The battery condition may be improved "
                    "through battery replacement or servicing.",

                "actions": battery_repairs
            }


    # ========================================================
    # 7. WORKING DEVICE → REUSE / DONATE
    # ========================================================

    no_major_problem = problem in [
        "",
        "none",
        "no major problem",
        "no problem",
        "working fine",
        "normal"
    ]


    if (
        power_status == "Yes"
        and physical_condition in [
            "Good",
            "Fair"
        ]
        and no_major_problem
    ):

        actions = [
            "Continue using the device.",
            "Consider using it as a secondary device.",
            "Donate it if it is no longer needed."
        ]

        if reuse_options:

            actions.append(
                "Possible reuse options: "
                + ", ".join(reuse_options[:3])
            )

        return {
            "recommendation": "Reuse / Donate",

            "reason":
                "The device is still working and does not "
                "have a major reported problem.",

            "actions": actions
        }


    # ========================================================
    # 8. OLD BUT WORKING DEVICE → REUSE / DONATE
    # ========================================================

    if (
        power_status == "Yes"
        and age >= 5
        and physical_condition in [
            "Good",
            "Fair"
        ]
    ):

        actions = [
            "Continue using it if it meets your needs.",
            "Consider donating it.",
            "Use it for basic or secondary tasks."
        ]

        if reuse_options:

            actions.append(
                "Possible reuse options: "
                + ", ".join(reuse_options[:3])
            )

        return {
            "recommendation": "Reuse / Donate",

            "reason":
                "Although the device is relatively old, "
                "it is still functioning and may have useful "
                "remaining life.",

            "actions": actions
        }


    # ========================================================
    # 9. BATTERY DEVICE
    # ========================================================

    if device_type == "battery":

        if battery_condition == "Swollen":

            return {
                "recommendation": "Safe Disposal",

                "reason":
                    "The battery may present a safety risk "
                    "and requires appropriate disposal.",

                "actions": [
                    "Stop using the battery.",
                    "Do not puncture or open it.",
                    "Use an authorized battery/e-waste disposal service."
                ]
            }


        if battery_condition in [
            "Poor",
            "Fair"
        ]:

            return {
                "recommendation": "Recycle",

                "reason":
                    "The battery has reduced condition and "
                    "should be handled through an appropriate "
                    "battery recycling channel.",

                "actions": [
                    "Do not place the battery in household waste.",
                    "Use an authorized battery recycling service."
                ]
            }


    # ========================================================
    # 10. GENERAL KNOWLEDGE-BASE MATCH
    # ========================================================

    if kb_repair_detected and repair_options:

        return {
            "recommendation": "Repair",

            "reason":
                "The reported problem matches a known "
                "device problem that may have repair options.",

            "actions": [
                "Get the device inspected by a qualified technician.",
                "Check the available repair options.",
                "Compare repair cost with replacement cost."
            ]
        }


    # ========================================================
    # 11. FINAL FALLBACK
    # ========================================================

    return {
        "recommendation": "Further Assessment",

        "reason":
            "The available information is not enough to "
            "determine the most suitable option.",

        "actions": [
            "Get the device professionally inspected.",
            "Check repair and upgrade possibilities.",
            "Compare the cost of extending its life with replacement."
        ]
    }