def validate_final_json(obj: dict) -> bool:
    """Validate the final JSON shape. Raise ValueError if invalid."""
    req_top = {"spec","routing","pois","cost","itinerary","notes"}
    missing = req_top - set(obj.keys())
    if missing:
        raise ValueError(f"Missing keys: {sorted(missing)}")

    spec = obj["spec"]; routing = obj["routing"]; cost = obj["cost"]
    if not isinstance(spec.get("days", None), int) or spec["days"] < 1:
        raise ValueError("spec.days must be int >= 1")
    if float(routing.get("distance_km", 0)) <= 0:
        raise ValueError("routing.distance_km must be > 0")

    parts = ["fuel","distance_charge","tolls","driver","night_halt","food","misc","gst","total_pre_gst","total"]
    for p in parts:
        if p not in cost:
            raise ValueError(f"cost missing {p}")

    # Check pre-GST math
    subtotal = sum(float(cost[k]) for k in ["fuel","distance_charge","tolls","driver","night_halt","food","misc"])
    if abs(float(cost["total_pre_gst"]) - subtotal) > max(200.0, 0.05 * subtotal):
        raise ValueError("cost.total_pre_gst not close to sum of pre-GST parts")

    # Check GST and final total
    expected_total = float(cost["total_pre_gst"]) + float(cost["gst"])
    if abs(float(cost["total"]) - expected_total) > max(200.0, 0.02 * expected_total):
        raise ValueError("cost.total not close to total_pre_gst + gst")

    return True
