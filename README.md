# Student Final Score Predictor

Ứng dụng dự đoán điểm cuối kỳ dựa trên điểm giữa kỳ của sinh viên bằng mô hình hồi quy tuyến tính.

## Giới thiệu

Project này xây dựng một chương trình dự báo điểm cuối kỳ dựa trên dữ liệu điểm giữa kỳ.  
Dữ liệu được lấy từ file Excel `TRAIN2.xlsx`, trong đó mỗi dòng biểu diễn điểm của một sinh viên.

Chương trình có giao diện đơn giản bằng Tkinter, cho phép người dùng nhập điểm giữa kỳ và nhận kết quả dự đoán điểm cuối kỳ tương ứng.

## Dataset

File dữ liệu sử dụng:

```text
TRAIN2.xlsx
```

Dataset gồm 2 cột chính:

```text
midterm
final
```

Trong đó:

- `midterm`: điểm giữa kỳ
- `final`: điểm cuối kỳ

Dữ liệu được làm sạch trước khi huấn luyện mô hình, bao gồm loại bỏ giá trị thiếu và chỉ giữ các điểm nằm trong khoảng từ 0 đến 10.

## Phương pháp dự báo

Chương trình sử dụng mô hình hồi quy tuyến tính một biến để mô tả mối quan hệ giữa điểm giữa kỳ và điểm cuối kỳ.

Công thức mô hình:

```text
final = a * midterm + b
```

Trong đó:

- `midterm` là biến đầu vào
- `final` là giá trị cần dự đoán
- `a` là hệ số góc của đường hồi quy
- `b` là hệ số chặn

Hai hệ số `a` và `b` được tính từ dữ liệu huấn luyện bằng phương pháp bình phương tối thiểu thông qua hàm `numpy.polyfit()`.

## Chức năng chính

Chương trình gồm các chức năng:

- Đọc dữ liệu từ file Excel
- Làm sạch dữ liệu điểm
- Huấn luyện mô hình hồi quy tuyến tính
- Hiển thị công thức dự báo
- Tính sai số MAE và hệ số R2
- Nhập điểm giữa kỳ để dự đoán điểm cuối kỳ
- Vẽ đồ thị dữ liệu thực tế và đường hồi quy

## Thư viện sử dụng

Project sử dụng các thư viện Python sau:

```text
numpy
pandas
matplotlib
tkinter
openpyxl
```

Trong đó:

- `numpy`: xử lý tính toán số học và huấn luyện hồi quy tuyến tính
- `pandas`: đọc và xử lý dữ liệu từ file Excel
- `matplotlib`: vẽ đồ thị dữ liệu và đường hồi quy
- `tkinter`: xây dựng giao diện người dùng
- `openpyxl`: hỗ trợ đọc file Excel `.xlsx`

## Cài đặt

Cài đặt các thư viện cần thiết bằng lệnh:

```bash
python -m pip install numpy pandas matplotlib openpyxl
```

## Cách chạy chương trình

Đảm bảo các file nằm cùng thư mục:

```text
student-final-score-predictor/
├── DuDoanDiemCK.py
├── TRAIN2.xlsx
└── README.md
```

Sau đó chạy chương trình bằng lệnh:

```bash
python DuDoanDiemCK.py
```

## Cách sử dụng

Sau khi chạy chương trình:

1. Nhập điểm giữa kỳ vào ô nhập liệu.
2. Bấm nút `Dự đoán`.
3. Chương trình sẽ hiển thị điểm cuối kỳ dự đoán.
4. Đồ thị sẽ cập nhật thêm điểm vừa nhập trên đường hồi quy.

## Kết quả

Chương trình hiển thị:

- Công thức hồi quy tuyến tính sau khi huấn luyện
- Số lượng mẫu dữ liệu
- Sai số MAE
- Hệ số R2
- Đồ thị thể hiện mối quan hệ giữa điểm giữa kỳ và điểm cuối kỳ

## Tác giả

Project được thực hiện cho bài tập dự đoán điểm cuối kỳ bằng mô hình hồi quy tuyến tính.
