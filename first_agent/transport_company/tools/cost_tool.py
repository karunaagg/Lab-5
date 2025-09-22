from transport_company.tools.config_tool import get_config

def _pick(mapping: dict, vehicle: str, fallback: float) -> float:
    return float(mapping.get(vehicle, fallback))

def estimate_cost(distance_km: float, days: int, vehicle: str = "cab", purpose: str = "tourism") -> dict:
    """Estimate INR cost using config-driven rates. total includes GST."""
    if distance_km <= 0 or days < 1:
        raise ValueError("Invalid distance/days.")

    cfg = get_config()
    rates = {**cfg["defaults"], **cfg.get("rates", {})}

    fuel = _pick(rates["fuel_per_km"], vehicle, 8.0) * distance_km
    distance_charge = _pick(rates["distance_charge_per_km"], vehicle, 8.0) * distance_km
    tolls = float(rates.get("toll_per_100km", 100.0)) * (distance_km / 100.0)
    driver = _pick(rates["driver_per_day"], vehicle, 800.0) * days
    night_halt = (rates["night_halt_per_night"] if days > 1 else 0) * max(days - 1, 0)
    food = rates["food_per_day"] * days
    misc = 0.05 * (fuel + distance_charge + tolls + driver + night_halt + food)

    pre_gst_total = fuel + distance_charge + tolls + driver + night_halt + food + misc
    gst_rate = float(rates.get("gst_rate", 0.18))
    gst = pre_gst_total * gst_rate
    total = pre_gst_total + gst  # <-- total now includes GST

    return {k: round(v, 2) for k, v in {
        "fuel": fuel,
        "distance_charge": distance_charge,
        "tolls": tolls,
        "driver": driver,
        "night_halt": night_halt,
        "food": food,
        "misc": misc,
        "gst": gst,                      # <--- NEW
        "total_pre_gst": pre_gst_total,  # <--- helpful for transparency
        "total": total                   # <--- GST-inclusive
    }.items()}
