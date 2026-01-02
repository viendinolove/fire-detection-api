# Fire & Smoke Detection API

AI model for detecting fire and smoke from images.

## Model Information
- Architecture: MobileNetV2 + Custom Head
- Classes: Fire, Neutral, Smoke
- Accuracy: 90-97%
- Framework: TensorFlow 2.15

## API Endpoints

### Health Check
```
GET /
```

### Predict
```
POST /predict
Content-Type: multipart/form-data
Body: image file
```

## Deployment

Deploy on Render.com:
1. Connect GitHub repository
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `gunicorn app:app`

## Usage
```python
import requests

url = "https://your-app.onrender.com/predict"
files = {'image': open('fire.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

## Author
Your Name
```

#### **File 5: .gitignore** (TẠO MỚI)

Tạo file `.gitignore`:
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Testing
test_images/
*.jpg
*.jpeg
*.png
!assets/*.png
```

## 2.3 Cấu trúc folder hoàn chỉnh:
```
fire-detection-api/                    ← Project folder
│
├── 📁 fire_smoke_detection_model/     ← Model (từ outputs/)
│   ├── saved_model.pb
│   ├── variables/
│   │   ├── variables.data-00000-of-00001
│   │   └── variables.index
│   └── assets/
│
├── 📄 app.py                          ← Flask API (file tôi tạo)
├── 📄 requirements.txt                ← Dependencies (file tôi tạo)
├── 📄 README.md                       ← Documentation (TẠO MỚI)
└── 📄 .gitignore                      ← Git ignore (TẠO MỚI)