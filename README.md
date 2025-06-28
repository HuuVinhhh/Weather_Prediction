# Dự án Dự báo Thời tiết
Dự án này sử dụng dữ liệu thời tiết và chất lượng không khí để dự báo thời tiết trong tương lai, trong đó bao gồm 3 mô hình dự đoán:

1. **Dự đoán trạng thái thời tiết**: Dự báo các trạng thái thời tiết (mưa, nắng, mây,...).
2. **Dự đoán nhiệt độ**: Dự báo nhiệt độ trong một khoảng thời gian cụ thể.
3. **Dự đoán chất lượng không khí (AQI)**: Dự báo chỉ số chất lượng không khí (Air Quality Index) dựa trên các yếu tố môi trường.

Dưới đây là hướng dẫn cài đặt và sử dụng dự án.

## 1. Clone Dự án từ GitHub

```bash
git clone https://github.com/HuuVinhhh/Weather_Prediction.git
cd Weather_Prediction
```

## 2. Cài đặt MongoDB

Để lưu trữ dữ liệu về thời tiết và chất lượng không khí, bạn cần cài đặt MongoDB và tạo cơ sở dữ liệu.

### 2.1. Tải và cài đặt MongoDB

Tải MongoDB tại [MongoDB Official Website](https://www.mongodb.com/try/download/community) và làm theo hướng dẫn cài đặt cho hệ điều hành của bạn.

### 2.2. Tạo Database và Collections

1. Mở terminal và khởi động MongoDB:

   ```bash
   mongod
   ```

2. Mở terminal mới và kết nối với MongoDB:

   ```bash
   mongo
   ```

3. Tạo database và collections:

   ```javascript
   use weather_db
   db.createCollection('weather_data')
   db.createCollection('air_quality_data')
   ```

### 2.3. Kết nối MongoDB trong Dự án

Dự án sẽ tự động kết nối với MongoDB khi bạn chạy mã nguồn. Đảm bảo rằng MongoDB đang chạy trên cổng mặc định (27017).

## 3. Cài Đặt Môi Trường Ảo

1. Cài đặt môi trường ảo:

   ```bash
   python3 -m venv .venv
   ```

2. Kích hoạt môi trường ảo:

   - Trên macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

   - Trên Windows:
     ```bash
     .venv\Scripts\activate
     ```

## 4. Cài Đặt Các Thư Viện Cần Thiết

```bash
pip install -r requirements.txt
```

## 5. Chạy Dự Án

Sau khi đã cài đặt tất cả các phụ thuộc và chuẩn bị cơ sở dữ liệu MongoDB, bạn có thể chạy dự án bằng cách:

```bash
python main.py
```

Dự án sẽ kết nối với MongoDB và bắt đầu thực hiện các tác vụ dự báo thời tiết.

## 6. Lưu Ý

- Đảm bảo rằng MongoDB đang chạy trên cổng mặc định (27017) để dự án có thể kết nối đúng.
- Nếu có bất kỳ vấn đề nào khi cài đặt hoặc sử dụng dự án, vui lòng tham khảo tài liệu chính thức của MongoDB hoặc các thư viện Python sử dụng trong dự án.