cities_coords = [
    {"name": "Thành phố Hồ Chí Minh", "lat": 10.7769, "lon": 106.7009},
    {"name": "Hà Nội", "lat": 21.0285, "lon": 105.8542},
    {"name": "Đà Nẵng", "lat": 16.0471, "lon": 108.2068},
    {"name": "Phú Quốc", "lat": 10.2899, "lon": 103.9840},
    {"name": "Nha Trang", "lat": 12.2451, "lon": 109.1943},
    {"name": "Hội An", "lat": 15.8801, "lon": 108.3380},
    {"name": "Đà Lạt", "lat": 11.9404, "lon": 108.4583},
    {"name": "Phan Thiết", "lat": 10.9333, "lon": 108.1000},
    {"name": "Huế", "lat": 16.4637, "lon": 107.5909},
    {"name": "Hai Phong", "lat": 20.8449, "lon": 106.6881}
]

import requests
from datetime import datetime, timedelta
import pandas as pd

def get_city_name_osm(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "addressdetails": 1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            address = data.get("address", {})
            return address.get("city") or address.get("town") or address.get("country") or None
    except Exception as e:
        print(f"Error fetching city name: {e}")
    return None
