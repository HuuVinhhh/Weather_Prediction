from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime, timezone
from utils.get_city import cities_coords, get_city_name_osm
import pandas as pd
import requests
from pymongo import MongoClient

# Kết nối với MongoDB
client = MongoClient("mongodb://localhost:27017/") 
db = client["weather_db"] 
collection = db["weather_data"] 

current_date = datetime.now(timezone.utc).date()

start_date_utc = current_date - timedelta(days=7)
end_date_utc = current_date - timedelta(days=1) 

start_date_str = start_date_utc.strftime('%Y-%m-%d')
end_date_str = end_date_utc.strftime('%Y-%m-%d')

seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
collection.delete_many({"timestamp": {"$lt": seven_days_ago}})

def fetch_weather_data():

    all_weather_data = []

    for city in cities_coords:
        lat = city["lat"]
        lon = city["lon"]

        # Lấy tên thành phố từ OSM 
        city_name = get_city_name_osm(lat, lon)
        if city_name is None:
            city_name = city["name"]  # fallback

        weather_url = "https://archive-api.open-meteo.com/v1/archive"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date_str,
            "end_date": end_date_str,
            "hourly": "temperature_2m,precipitation,windspeed_10m,winddirection_10m,cloudcover,pressure_msl,relative_humidity_2m,weathercode",
            "temperature_unit": "celsius",
            "windspeed_unit": "kmh",
            "precipitation_unit": "mm",
            "timezone": "Asia/Ho_Chi_Minh"
        }

        weather_response = requests.get(weather_url, params=weather_params)
        if weather_response.status_code != 200:
            print(f"Error fetching weather for {city_name}: {weather_response.status_code}")
            continue

        weather_data = weather_response.json()
        df_city_weather = pd.DataFrame(weather_data.get('hourly', {}))

        if not df_city_weather.empty:
            df_city_weather["city"] = city_name
            all_weather_data.append(df_city_weather)


    if all_weather_data:
        df_all = pd.concat(all_weather_data, ignore_index=True)

        # Loại bỏ các dòng có dữ liệu NaN
        df_all_weather_clean = df_all.dropna()

        # Chuyển đổi dữ liệu thành danh sách các từ điển (mỗi dòng là một tài liệu trong MongoDB)
        weather_records = df_all_weather_clean.to_dict(orient="records")

        # Lưu dữ liệu vào MongoDB
        collection.insert_many(weather_records)

        print("Weather data has been saved to MongoDB.")
    else:
        print("No weather data available.")
