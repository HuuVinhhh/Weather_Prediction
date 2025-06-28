import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
from pymongo import MongoClient
from datetime import timedelta
from utils.weather_code_map import weather_code_mapping

# Kết nối với MongoDB
client = MongoClient("mongodb://localhost:27017/")  
db = client["weather_db"]  
collection = db["weather_data"] 

def predict_weather():
    result = []  

    cursor = collection.find()  
    df_weather = pd.DataFrame(list(cursor))  

    df_weather['time'] = pd.to_datetime(df_weather['time']) 

    label_encoder = LabelEncoder()
    df_weather['city_encoded'] = label_encoder.fit_transform(df_weather['city'])

    cities = df_weather['city'].unique()

    for city in cities:

        city_data = df_weather[df_weather['city'] == city]

        current_time = pd.to_datetime("now")

        average_data = city_data[['precipitation', 'cloudcover', 'windspeed_10m', 'relative_humidity_2m', 'pressure_msl', 'temperature_2m', 'city_encoded']].mean()

        input_data = pd.DataFrame([average_data], columns=['precipitation', 'cloudcover', 'windspeed_10m', 'relative_humidity_2m', 'pressure_msl', 'temperature_2m', 'city_encoded'])

        try:
            model = joblib.load(f"models/weather/{city}_weather_model.pkl")  # Tải mô hình 
            # Dự đoán trạng thái thời tiết cho ngày hôm nay
            weather_prediction = model.predict(input_data)

            # Áp dụng ánh xạ weather code
            weather_description = weather_code_mapping.get(weather_prediction[0], "Không xác định")
            
            result.append([city, weather_description])

        except FileNotFoundError:
            print(f"Không tìm thấy mô hình cho {city}, vui lòng kiểm tra mô hình của thành phố này.")

    return result