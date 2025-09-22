import os, yaml

def get_config() -> dict:
    """
    Load planner config from ENV and ./config/rates.yaml.
    Always returns a dict: {'defaults': {...}, 'rates': {...}}
    """
    cfg = {
        "defaults": {
            "fuel_per_km": {"cab": 8.0, "suv": 9.5, "mini-truck": 10.5, "truck": 12.0},
            "distance_charge_per_km": {"cab": 8.0, "suv": 10.0, "mini-truck": 10.5, "truck": 12.0},
            "driver_per_day": {"cab": 800, "suv": 900, "mini-truck": 1200, "truck": 1500},
            "night_halt_per_night": 1000,
            "food_per_day": 400,
            "toll_per_100km": 100.0,
            "gst_rate": 0.18,
        },
        "rates": {}
    }

    # Optional YAML file (safe + tolerant)
    path = os.environ.get(
        "TPF_RATES_FILE",
        os.path.join("transport_company", "config", "rates.yaml")
    )
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                if isinstance(data, dict):
                    cfg["rates"].update(data)
        except Exception:
            # Ignore YAML errors; fall back to defaults
            pass

    # Optional ENV overrides
    if os.environ.get("TPF_TOLL_PER_100KM"):
        cfg["rates"]["toll_per_100km"] = float(os.environ["TPF_TOLL_PER_100KM"])
    if os.environ.get("TPF_GST_RATE"):
        cfg["rates"]["gst_rate"] = float(os.environ["TPF_GST_RATE"])

    return cfg   # <-- DO NOT FORGET THIS
