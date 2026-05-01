# 🖐️ Hand Tracking 2D + 3D (MediaPipe + OpenCV + PyOpenGL)

## 📌 Giới thiệu

Project này sử dụng **MediaPipe** để nhận diện bàn tay theo thời gian thực từ webcam, kết hợp:

* 🟢 OpenCV → hiển thị tracking 2D
* 🔵 PyOpenGL → hiển thị mô hình tay 3D
* 🟡 PyQt5 → giao diện người dùng

👉 Kết quả:

* Theo dõi bàn tay realtime
* Hiển thị landmark 2D + 3D
* Có smoothing giúp chuyển động mượt hơn

---

## 🎥 Demo



---

## 📁 Cấu trúc project

```
.
├── model/
│   └── hand_landmarker.task
├── config.py
├── draw.py
├── draw3D.py
├── handtracking.py
├── Tracker.py
├── ui.py
├── main.py
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Cài đặt

### 1. Clone repo

```bash
git clone https://github.com/your-username/your-repo.git
```

### 2. Tạo môi trường ảo (khuyến nghị)
- Python version: `Python 3.14.4`

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Cài thư viện

```bash
pip install -r requirements.txt
```

---

## ▶️ Chạy chương trình

```bash
python main.py
```

---

## 🎮 Cách hoạt động

### 1. Tracking

* Sử dụng MediaPipe Hand Landmarker
* Nhận diện tối đa `NUM_HANDS`

### 2. Smoothing

* Giảm rung tay bằng:

  * `SMOOTHING`
  * `THRESHOLD`

### 3. Hiển thị

* 2D: vẽ điểm + khớp tay trên camera
* 3D: dựng mô hình tay bằng OpenGL

---

## 🔧 Cấu hình

Trong `config.py`:

```python
MODEL_PATH = "model/hand_landmarker.task"
NUM_HANDS = 1
CAMERA_ID = 0

SMOOTHING = 0.3
THRESHOLD = 0.01
```
