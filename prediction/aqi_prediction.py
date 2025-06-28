import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
from pymongo import MongoClient
from data.air_quality_processing import calculate_all_AQIs, AQI_RANGES

# Kết nối với MongoDB
client = MongoClient("mongodb://localhost:27017/")   
db = client["weather_db"]
collection = db["air_quality_data"]  

# Mức độ chất lượng không khí từ AQI
def get_aqi_category(aqi_value):
    if aqi_value <= 200:
        return "Tốt"
    elif aqi_value <= 400:
        return "Trung bình"
    elif aqi_value <= 600:
        return "Kém"
    elif aqi_value <= 800:
        return "Xấu"
    elif aqi_value <= 1000:
        return "Rất xấu"
    elif aqi_value <= 1400:
        return "Nguy hại"
    else:
        return "Không xác định"

def predict_aqi():
    result = []  # Danh sách để lưu kết quả

    # Lấy tất cả dữ liệu từ MongoDB
    cursor = collection.find()  
    df_air_quality = pd.DataFrame(list(cursor))  

    df_air_quality['time'] = pd.to_datetime(df_air_quality['time'])

    cities = df_air_quality['city'].unique()

    for city in cities:

        city_data = df_air_quality[df_air_quality['city'] == city].copy()  # Sử dụng .copy() để tránh cảnh báo

        # Khởi tạo LabelEncoder
        label_encoder = LabelEncoder()

        # Mã hóa lại cột 'city' cho toàn bộ dữ liệu của thành phố 
        city_data.loc[:, 'city_encoded'] = label_encoder.fit_transform([city] * len(city_data))

        city_data.loc[:, 'AQI_PM2_5'] = calculate_all_AQIs(city_data, 'pm2_5', AQI_RANGES['pm2_5'])
        city_data.loc[:, 'AQI_PM10'] = calculate_all_AQIs(city_data, 'pm10', AQI_RANGES['pm10'])
        city_data.loc[:, 'AQI_NO2'] = calculate_all_AQIs(city_data, 'nitrogen_dioxide', AQI_RANGES['no2'])
        city_data.loc[:, 'AQI_O3'] = calculate_all_AQIs(city_data, 'ozone', AQI_RANGES['o3'])
        city_data.loc[:, 'AQI_SO2'] = calculate_all_AQIs(city_data, 'sulphur_dioxide', AQI_RANGES['so2'])
        city_data.loc[:, 'AQI_CO'] = calculate_all_AQIs(city_data, 'carbon_monoxide', AQI_RANGES['co'])

        # Loại bỏ các dòng có NaN
        city_data_cleaned = city_data.dropna(subset=['AQI_PM2_5', 'AQI_PM10', 'AQI_NO2', 'AQI_O3', 'AQI_SO2', 'AQI_CO'])

        average_data = city_data_cleaned[['AQI_PM2_5', 'AQI_PM10', 'AQI_NO2', 'AQI_O3', 'AQI_SO2', 'AQI_CO']].mean()

        input_data = pd.DataFrame([average_data], columns=['AQI_PM2_5', 'AQI_PM10', 'AQI_NO2', 'AQI_O3', 'AQI_SO2', 'AQI_CO'])

        try:
            model = joblib.load(f"models/air_quality/{city}_aqi_model.pkl")  # Tải mô hình 
            # Dự đoán trạng thái thời tiết cho ngày hôm nay
            aqi_prediction = model.predict(input_data)

            # Lấy mức độ AQI theo giá trị
            aqi_category = get_aqi_category(aqi_prediction[0])

            result.append([city, aqi_prediction[0], aqi_category])

        except FileNotFoundError:
            print(f"Không tìm thấy mô hình AQI cho {city}, vui lòng kiểm tra mô hình của thành phố này.")

    return result