import requests
UA = {"User-Agent": "adk-transport-planner/1.0 (edu use)"}

def _geocode(city: str) -> dict:
  r = requests.get("https://nominatim.openstreetmap.org/search",
                   params={"q": city, "format": "json", "limit": 1},
                   headers=UA, timeout=20)
  r.raise_for_status()
  items = r.json()
  if not items: raise ValueError(f"Could not geocode: {city}")
  return {"lat": float(items[0]["lat"]), "lon": float(items[0]["lon"])}

def route_osrm(origin: str, destination: str) -> dict:
  """Driving route using OSRM. Returns {'distance_km', 'duration_hr'}."""
  o, d = _geocode(origin), _geocode(destination)
  url = f"http://router.project-osrm.org/route/v1/driving/{o['lon']},{o['lat']};{d['lon']},{d['lat']}"
  r = requests.get(url, params={"overview": "false"}, headers=UA, timeout=20)
  r.raise_for_status()
  route = r.json()["routes"][0]
  return {"distance_km": round(route["distance"]/1000.0, 1),
          "duration_hr": round(route["duration"]/3600.0, 2)}
