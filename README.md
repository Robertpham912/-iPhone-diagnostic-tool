# Trạm chẩn đoán iPhone

Web app chẩn đoán sự cố iPhone (phần cứng + phần mềm), chạy backend Python (Flask)
kết hợp giao diện web dùng ngay trên trình duyệt (kể cả Safari trên chính iPhone).

## Chạy thử trên máy (Mac)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Server chạy tại `http://localhost:5050`. Mở bằng máy tính, hoặc để mở ngay trên
chính iPhone: cả hai thiết bị cần cùng mạng Wifi, sau đó mở
`http://<địa-chỉ-IP-máy-Mac>:5050` bằng Safari trên iPhone.

## Cấu trúc

```
app.py           Flask backend: phục vụ trang, API cây chẩn đoán, lưu lịch sử vào SQLite
rules.py         Toàn bộ cây luật chẩn đoán (hardware / software / nghi virus)
templates/       Giao diện HTML
static/          CSS + JS (chạy auto-test bằng Web API: pin, cảm ứng, mic/loa, camera, dung lượng, mạng)
```

## Giới hạn cần biết

Vì chạy trong trình duyệt, hệ thống **không thể**:
- Tự xoá app/profile, sửa cài đặt hệ thống, cập nhật iOS, hay "diệt virus" thật sự
  (iPhone về bản chất hiếm khi nhiễm virus dạng file thực thi như máy tính).
- Kết nối trực tiếp qua Bluetooth/USB để đọc dữ liệu từ iPhone — iOS không mở API
  này cho web vì lý do bảo mật.

Hệ thống **có thể**:
- Đọc một số dữ liệu qua Web API khi trình duyệt hỗ trợ (pin, dung lượng web,
  trạng thái mạng, test cảm ứng/camera/mic/loa trực tiếp).
- Dẫn dắt người dùng qua cây câu hỏi để đưa ra chẩn đoán và các bước xử lý cụ thể,
  giống một kỹ thuật viên hướng dẫn từ xa.

## Đẩy code lên GitHub

Repo đã được clone sẵn tại đây nhưng trống, nên bạn cần tự add/commit/push code này
lên `Robertpham912/-iPhone-diagnostic-tool` từ máy của bạn (không dán token vào chat
với bất kỳ ai, kể cả Claude — luôn thao tác token trực tiếp trong terminal của bạn):

```bash
git add .
git commit -m "Init: web app chan doan iPhone"
git push origin main
```
