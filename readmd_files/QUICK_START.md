# Quick Start Guide - Resume ATS Mobile App

## 🚀 Fast Setup (3 Steps)

<!--### Step 1: Install Flutter Dependencies
```powershell
cd "d:\project\ML PROJECTS\Resume App\mobile_app"
flutter pub get
```

### Step 2: Start Backend Server
```powershell
cd "d:\project\ML PROJECTS\Resume App\backend_api"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

### Step 3: Run Flutter App
```powershell
cd "d:\project\ML PROJECTS\Resume App\mobile_app"
flutter run
```

---

## 📱 What You Just Built

### Flutter Mobile App Features:
- ✅ Cross-platform (Android + iOS)
- ✅ Modern dark theme UI
- ✅ Resume upload (PDF/DOCX)
- ✅ ATS score calculation
- ✅ AI-powered resume guide (chat)
- ✅ Detailed feedback & recommendations

### FastAPI Backend:
- ✅ RESTful API endpoints
- ✅ Resume parsing
- ✅ ATS scoring
- ✅ RAG-based Q&A
- ✅ CORS enabled for mobile

---

## 🔧 Configuration

### Update API URL in Flutter App
Edit `mobile_app/lib/config/api_config.dart`:
```dart
static const String baseUrl = 'http://YOUR_IP:8000';
```

Find your IP:
```powershell
ipconfig
# Look for IPv4 Address
```

---

## 🎯 Next Steps

1. **Configure Firebase** (optional):
   ```powershell
   flutterfire configure
   ```

2. **Build APK**:
   ```powershell
   flutter build apk --release
   ```

3. **Deploy Backend**:
   - Railway: https://railway.app
   - Render: https://render.com

---

## 📖 Full Documentation
See `MOBILE_APP_README.md` for complete setup and deployment guide.
