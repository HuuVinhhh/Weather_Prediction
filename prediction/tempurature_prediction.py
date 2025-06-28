import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from pymongo import MongoClient
from datetime import timedelta

# Kết nối với MongoDB
client = MongoClient("mongodb://localhost:27017/") 
db = client["weather_db"]  
collection = db["weather_data"]  

def predict_tempurature():
    result = []  

    # Lấy tất cả dữ liệu từ MongoDB
    cursor = collection.find() 
    df_weather = pd.DataFrame(list(cursor))  

    df_weather['time'] = pd.to_datetime(df_weather['time'])

    label_encoder = LabelEncoder()
    df_weather['city_encoded'] = label_encoder.fit_transform(df_weather['city'])

    cities = df_weather['city'].unique()

    for city in cities:

        city_data = df_weather[df_weather['city'] == city]

        average_data = city_data[['cloudcover', 'windspeed_10m', 'relative_humidity_2m', 'pressure_msl']].mean()

        average_data['city_encoded'] = label_encoder.transform([city])[0]

        input_data = pd.DataFrame([average_data], columns=['cloudcover', 'windspeed_10m', 'relative_humidity_2m', 'pressure_msl', 'city_encoded'])

        model_directory = '/home/huuvinhh/Documents/Semester_3_2024-2025/Big_Data_Integration_and_Analysis/weather_prediction/models/tempurature'  # Cập nhật với đường dẫn thực tế tới thư mục models/temperature

        # Xây dựng tên tệp mô hình cho nhiệt độ cao nhất và thấp nhất
        model_max_filename = f"{city}_max_temperature_model.pkl"
        model_min_filename = f"{city}_min_temperature_model.pkl"

        # Xây dựng đường dẫn đầy đủ tới các tệp mô hình
        model_max_filepath = os.path.join(model_directory, model_max_filename)
        model_min_filepath = os.path.join(model_directory, model_min_filename)

        try:
            # Tải mô hình 
            model_max = joblib.load(model_max_filepath)  
            model_min = joblib.load(model_min_filepath)  

            # Dự đoán 
            max_temperature = model_max.predict(input_data)[0]
            min_temperature = model_min.predict(input_data)[0]

            # Lưu kết quả vào danh sách
            result.append([city, min_temperature, max_temperature])

        except FileNotFoundError:
            print(f"Không tìm thấy mô hình cho {city}, vui lòng kiểm tra mô hình của thành phố này.")

    return result