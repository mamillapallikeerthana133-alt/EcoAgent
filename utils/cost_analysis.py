def calculate_cost_analysis(device_data, recommendation):
    """
    Estimate repair/upgrade cost and compare it
    with a typical replacement cost.
    """

    device_type = device_data.get("device_type", "")
    problem = device_data.get("main_problem", "").lower()

    # Typical approximate replacement costs in INR
    replacement_costs = {
        "Laptop": 40000,
        "Smartphone": 20000,
        "Tablet": 15000,
        "Desktop": 45000,
        "TV": 30000,
        "Battery": 3000,
        "Other": 20000
    }

    replacement_cost = replacement_costs.get(
        device_type,
        20000
    )

    # Estimate repair / upgrade cost
    if recommendation == "Upgrade":

        if "slow" in problem or "performance" in problem:
            repair_cost = 6000
        else:
            repair_cost = 5000

    elif recommendation == "Repair":

        if "screen" in problem or "display" in problem:
            repair_cost = 7000
        elif "battery" in problem:
            repair_cost = 3000
        elif "charging" in problem:
            repair_cost = 2500
        else:
            repair_cost = 4000

    elif recommendation == "Reuse / Donate":

        repair_cost = 0

    else:

        repair_cost = 0

    # Compare costs
    if repair_cost == 0:

        saving = replacement_cost

    else:

        saving = replacement_cost - repair_cost

    # Generate explanation
    if recommendation in ["Repair", "Upgrade"]:

        if repair_cost < replacement_cost:

            comparison = (
                "Extending the life of the current device "
                "may cost substantially less than replacing it."
            )

        else:

            comparison = (
                "The estimated repair cost is relatively high "
                "compared with replacement."
            )

    elif recommendation == "Reuse / Donate":

        comparison = (
            "The device can continue providing value "
            "without immediate replacement."
        )

    else:

        comparison = (
            "Cost comparison is not the primary consideration "
            "because safety or recycling is required."
        )

    return {
        "estimated_repair_cost": repair_cost,
        "estimated_replacement_cost": replacement_cost,
        "estimated_saving": max(saving, 0),
        "comparison": comparison
    }