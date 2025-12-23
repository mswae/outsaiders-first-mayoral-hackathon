def assign_typology(sorted_components, high_th=0.4, th=0.2):
    
    high_impact = []
    medium_impact = []
    low_impact = []

    for component, data in sorted_components.items():
        entry = {
            "component": component,
            "value": data["value"],
            "description": data.get("description", "")
        }

        if abs(data["value"]) >= high_th:
            high_impact.append(entry)
        elif abs(data["value"]) >= th:
            medium_impact.append(entry)
        else:
            low_impact.append(entry)

    typology = {
        "high": high_impact,
        "medium": medium_impact,
        "low": low_impact
    }

    return typology