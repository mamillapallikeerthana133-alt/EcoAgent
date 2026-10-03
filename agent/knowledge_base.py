# EcoAgent Knowledge Base
# Basic information about common electronic devices

KNOWLEDGE_BASE = {

    "laptop": {
        "common_problems": [
            "slow performance",
            "low storage",
            "battery problems",
            "broken screen",
            "overheating",
            "keyboard problems"
        ],

        "repair_options": [
            "Screen replacement",
            "Keyboard replacement",
            "Battery replacement",
            "Cleaning and servicing"
        ],

        "upgrade_options": [
            "Upgrade RAM",
            "Replace HDD with SSD",
            "Replace old battery"
        ],

        "reuse_options": [
            "Secondary computer",
            "Study device",
            "Media device",
            "Donation"
        ]
    },

    "smartphone": {
        "common_problems": [
            "slow performance",
            "broken screen",
            "battery problems",
            "charging problems",
            "storage problems"
        ],

        "repair_options": [
            "Screen replacement",
            "Battery replacement",
            "Charging port repair",
            "Speaker or camera repair"
        ],

        "upgrade_options": [
            "Battery replacement",
            "Storage cleanup"
        ],

        "reuse_options": [
            "Secondary phone",
            "Media device",
            "Camera device",
            "Donation"
        ]
    },

    "tablet": {
        "common_problems": [
            "slow performance",
            "battery problems",
            "broken screen",
            "charging problems"
        ],

        "repair_options": [
            "Screen replacement",
            "Battery replacement",
            "Charging port repair"
        ],

        "upgrade_options": [
            "Battery replacement",
            "Storage cleanup"
        ],

        "reuse_options": [
            "Reading device",
            "Media device",
            "Study device",
            "Donation"
        ]
    },

    "desktop": {
        "common_problems": [
            "slow performance",
            "low storage",
            "overheating",
            "power problems"
        ],

        "repair_options": [
            "Power supply replacement",
            "Cleaning and servicing",
            "Component replacement"
        ],

        "upgrade_options": [
            "Upgrade RAM",
            "Replace HDD with SSD",
            "Upgrade graphics card"
        ],

        "reuse_options": [
            "Study computer",
            "Home server",
            "Media computer",
            "Donation"
        ]
    },

    "battery": {
        "common_problems": [
            "swollen battery",
            "poor battery life",
            "leaking battery",
            "overheating"
        ],

        "repair_options": [
            "Battery replacement"
        ],

        "upgrade_options": [],

        "reuse_options": [],

        "disposal": [
            "Safe battery disposal",
            "Authorized e-waste recycling"
        ]
    },

    "tv": {
        "common_problems": [
            "display problems",
            "sound problems",
            "power problems",
            "remote problems"
        ],

        "repair_options": [
            "Display repair",
            "Power supply repair",
            "Speaker repair"
        ],

        "upgrade_options": [],

        "reuse_options": [
            "Secondary display",
            "Media device",
            "Donation"
        ]
    }
}


def get_device_info(device_type):
    """
    Return knowledge-base information for a device.
    """

    device_type = device_type.lower()

    return KNOWLEDGE_BASE.get(
        device_type,
        {
            "common_problems": [],
            "repair_options": [],
            "upgrade_options": [],
            "reuse_options": []
        }
    )