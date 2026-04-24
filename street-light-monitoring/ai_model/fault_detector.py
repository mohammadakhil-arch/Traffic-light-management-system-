def detect_fault(row):
    voltage = row["voltage"]
    current = row["current"]
    temperature = row["temperature"]
    status = row["status"]

    # Highest priority: Light OFF
    if voltage == 0 or status == "OFF":
        return "Light OFF"

    # Cable break: voltage present but no current
    if voltage > 200 and current == 0:
        return "Cable Breakage"

    # Current leakage
    if current > 1.5:
        return "Current Leakage"

    # Overheating
    if temperature > 70:
        return "Overheating"

    return "Normal"

def fault_severity(fault):
    if fault == "Light OFF":
        return "HIGH"
    if fault in ["Current Leakage", "Overheating"]:
        return "Medium"
    return "Low"
