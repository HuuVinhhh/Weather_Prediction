from data.weather_data import fetch_weather_data
from data.air_quality_data import fetch_air_quality_data
from prediction.weather_prediction import predict_weather
from prediction.tempurature_prediction import predict_tempurature
from prediction.aqi_prediction import predict_aqi
import pandas as pd

def main():

    temp_results = predict_tempurature()

    aqi_results = predict_aqi()

    weather_results = predict_weather()

    results_df = pd.DataFrame(columns=["THÀNH PHỐ", "AQI", "AQI CATEGORY", "WEATHER", "TEMPERATURE"])

    for result in aqi_results:
        results_df.loc[results_df.shape[0]] = [result[0], f"{result[1]:.2f}", result[2], "", ""]

    # Thêm kết quả dự đoán thời tiết vào DataFrame
    for i, result in enumerate(weather_results):
        if i < len(results_df): 
            results_df.loc[i, "WEATHER"] = result[1]

    # Thêm kết quả dự đoán nhiệt độ vào DataFrame
    for i, result in enumerate(temp_results):
        if i < len(results_df): 
            results_df.loc[i, "TEMPERATURE"] = f"{result[1]:.2f} °C / {result[2]:.2f} °C"

    # In kết quả ra bảng
    print(results_df.to_string(index=False)) 


if __name__ == "__main__":
    main()
