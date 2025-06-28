from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime, timezone
from utils.get_city import cities_coords, get_city_name_osm
import pandas as pd
import requests
from pymongo import MongoClient

from dateutil.relativedelta import relativedelta 
# Kết nối với MongoDB
client = MongoClient("mongodb://localhost:27017/") 
db = client["weather_db"]  
collection = db["air_quality_data"]  


current_date = datetime.now(timezone.utc).date()


start_date_utc = current_date - timedelta(days=7)
end_date_utc = current_date - timedelta(days=1) 

start_date_str = start_date_utc.strftime('%Y-%m-%d')
end_date_str = end_date_utc.strftime('%Y-%m-%d')

seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
collection.delete_many({"timestamp": {"$lt": seven_days_ago}})

def fetch_air_quality_data():

    all_air_quality_data = []

    for city in cities_coords:
        lat = city["lat"]
        lon = city["lon"]

        # Lấy tên thành phố từ OSM 
        city_name = get_city_name_osm(lat, lon)
        if city_name is None:
            city_name = city["name"]  # fallback

        air_quality_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        air_quality_params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date_str,
            "end_date": end_date_str,
            "hourly": "pm2_5,pm10,nitrogen_dioxide,ozone,sulphur_dioxide,carbon_monoxide",
            "timezone": "Asia/Ho_Chi_Minh"
        }

        air_quality_response = requests.get(air_quality_url, params=air_quality_params)

        if air_quality_response.status_code != 200:
            print(f"Error for {city_name}: {air_quality_response.status_code}")
            continue

        air_quality_data = air_quality_response.json()
        df_city_air_quality = pd.DataFrame(air_quality_data.get('hourly', {}))

        if not df_city_air_quality.empty:
            df_city_air_quality["city"] = city_name
            all_air_quality_data.append(df_city_air_quality)

    if all_air_quality_data:
        df_all_air_quality = pd.concat(all_air_quality_data, ignore_index=True)

        df_all_air_quality_clean = df_all_air_quality.dropna()
        # Chuyển đổi dữ liệu thành danh sách các từ điển (mỗi dòng là một tài liệu trong MongoDB)
        air_quality_records = df_all_air_quality_clean.to_dict(orient="records")

        # Lưu dữ liệu vào MongoDB
        collection.insert_many(air_quality_records)

        print("air quality data has been saved to MongoDB.")
    else:
        print("No air quality data available.")


