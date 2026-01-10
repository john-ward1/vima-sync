import requests
import time

_cache = {}

def reverse_geocode(lat: float, lon: float) -> str | None:
    key = f"{round(lat, 3)},{round(lon, 3)}"
    if key in _cache:
        return _cache[key]

    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "zoom": 10  # city / region level
    }
    headers = {"User-Agent": "vima-sync"}

    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()

    location = r.json().get("display_name")
    _cache[key] = location

    time.sleep(1)  # be polite
    return location
