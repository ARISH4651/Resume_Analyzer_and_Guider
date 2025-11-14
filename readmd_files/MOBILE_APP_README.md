# Resume ATS Mobile App

<!--AI-powered Resume ATS Analyzer mobile application built with **Flutter** and **FastAPI**.

## 📱 Tech Stack

### Frontend (Mobile)
- **Flutter** - Cross-platform mobile framework
- **Riverpod** - State management
- **Dio** - HTTP client for API calls
- **Firebase** - Authentication & Cloud Storage

### Backend (API)
- **FastAPI** - Modern Python web framework
- **LangChain** - LLM orchestration
- **Groq** - LLM provider
- **ChromaDB** - Vector database for RAG

---

## 🚀 Project Structure

```
Resume App/
├── mobile_app/                 # Flutter mobile application
│   ├── lib/
│   │   ├── main.dart
│   │   ├── config/
│   │   │   ├── theme.dart
│   │   │   └── api_config.dart
│   │   ├── screens/
│   │   │   ├── splash_screen.dart
│   │   │   ├── home_screen.dart
│   │   │   ├── analyze_screen.dart
│   │   │   ├── guide_screen.dart
│   │   │   └── result_screen.dart
│   │   ├── services/
│   │   │   └── api_service.dart
│   │   └── models/
│   │       ├── ats_result.dart
│   │       └── chat_message.dart
│   └── pubspec.yaml
│
├── backend_api/                # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
│
├── resume_parser.py           # Existing resume parsing logic
├── ats_scorer.py              # Existing ATS scoring logic
├── rag_utility.py             # Existing RAG utility
└── firebase_utils.py          # Existing Firebase utilities
```

---

## 🛠️ Setup Instructions

### Prerequisites
- **Flutter SDK** (3.0 or higher)
- **Python** (3.8 or higher)
- **Node.js** (for Firebase CLI)
- **Android Studio** / **Xcode** (for mobile development)

---

## 📱 Mobile App Setup (Flutter)

### 1. Navigate to mobile_app directory
```powershell
cd "d:\project\ML PROJECTS\Resume App\mobile_app"
```

### 2. Install Flutter dependencies
```powershell
flutter pub get
```

### 3. Configure Firebase

#### Install Firebase CLI
```powershell
npm install -g firebase-tools
```

#### Login to Firebase
```powershell
firebase login
```

#### Configure Firebase for Flutter
```powershell
dart pub global activate flutterfire_cli
flutterfire configure
```

This will:
- Create Firebase project (or select existing)
- Generate `firebase_options.dart` with your credentials
- Configure iOS and Android apps

### 4. Update API Base URL

Edit `lib/config/api_config.dart`:
```dart
static const String baseUrl = 'http://YOUR_IP:8000';
```

**Note:** Use your computer's local IP (not localhost) for testing on physical devices.

To find your IP:
```powershell
ipconfig
# Look for IPv4 Address under your active network
```

### 5. Run the Flutter app

#### On Android Emulator:
```powershell
flutter run
```

#### On Physical Device:
```powershell
flutter devices  # List available devices
flutter run -d DEVICE_ID
```

---

## 🔧 Backend API Setup (FastAPI)

### 1. Navigate to backend_api directory
```powershell
cd "d:\project\ML PROJECTS\Resume App\backend_api"
```

### 2. Create virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` file:
```powershell
cp .env.example .env
```

Edit `.env`:
```env
GROQ_API_KEY=your_actual_groq_api_key
FIREBASE_CREDENTIALS_PATH=../firebase-credentials.json
```

### 5. Run the FastAPI server
```powershell
python main.py
```

Or with uvicorn directly:
```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs`

---

## 🔌 API Endpoints

### Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/parse-resume` | POST | Parse resume file (PDF/DOCX) |
| `/api/calculate-ats` | POST | Calculate ATS score |
| `/api/ask-question` | POST | Ask resume-related questions (RAG) |
| `/api/enhance-resume` | POST | Enhance resume with AI |

### Example API Requests

#### Parse Resume
```bash
curl -X POST "http://localhost:8000/api/parse-resume" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

#### Calculate ATS Score
```bash
curl -X POST "http://localhost:8000/api/calculate-ats" \
  -H "Content-Type: application/json" \
  -d '{
    "parsed_resume": {...},
    "job_description": "..."
  }'
```

#### Ask Question
```bash
curl -X POST "http://localhost:8000/api/ask-question" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is ATS?"}'
```

---

## 📦 Building for Production

### Android APK
```powershell
flutter build apk --release
```

Output: `build/app/outputs/flutter-apk/app-release.apk`

### Android App Bundle (for Play Store)
```powershell
flutter build appbundle --release
```

Output: `build/app/outputs/bundle/release/app-release.aab`

### iOS (requires Mac)
```bash
flutter build ios --release
```

---

## 🚀 Deployment

### Backend Deployment Options

#### 1. Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway init
railway up
```

#### 2. Render
- Connect GitHub repo
- Set build command: `pip install -r requirements.txt`
- Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### 3. AWS EC2 / DigitalOcean
```bash
# Install nginx
sudo apt install nginx

# Install supervisor
sudo apt install supervisor

# Configure supervisor for FastAPI
# See deployment docs
```

### Update Flutter App with Production API

Edit `lib/config/api_config.dart`:
```dart
static const String baseUrl = 'https://your-api-domain.com';
```

---

## 🧪 Testing

### Test Backend API
```powershell
# From backend_api directory
pytest tests/
```

### Test Flutter App
```powershell
# From mobile_app directory
flutter test
```

---

## 📱 Features

### ✅ Implemented Features
- **Splash Screen** with animated logo
- **Home Screen** with feature cards
- **Resume Analysis**
  - Upload PDF/DOCX files
  - Calculate ATS score (0-100)
  - Detailed feedback by category
  - Visual score representation
- **Resume Guide (RAG)**
  - AI-powered Q&A
  - Quick question suggestions
  - Chat interface
- **Dark Theme** (ChatGPT-style UI)

### 🔜 Upcoming Features
- Resume Enhancement with AI suggestions
- Export enhanced resume as PDF
- Firebase Authentication
- Save analysis history
- Compare multiple resumes
- Industry-specific templates

---

## 🐛 Troubleshooting

### Flutter Issues

**Problem:** `flutter pub get` fails
```powershell
flutter clean
flutter pub get
```

**Problem:** Can't connect to API from device
- Make sure backend is running
- Use your computer's local IP (not localhost)
- Check firewall settings

**Problem:** Firebase not configured
```powershell
flutterfire configure
```

### Backend Issues

**Problem:** Import errors
```powershell
# Make sure you're in backend_api directory
cd backend_api
python main.py
```

**Problem:** CORS errors
- Check CORS middleware in `main.py`
- Update `allow_origins` if needed

---

## 📝 Environment Variables

### Backend (.env)
```env
GROQ_API_KEY=your_groq_api_key
FIREBASE_CREDENTIALS_PATH=path_to_firebase_creds.json
HOST=0.0.0.0
PORT=8000
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**ARISH4651**
- GitHub: [@ARISH4651](https://github.com/ARISH4651)
- Repository: [CHAT_WITH_DOCS](https://github.com/ARISH4651/CHAT_WITH_DOCS)

---

## 🙏 Acknowledgments

- **Flutter Team** - Amazing cross-platform framework
- **FastAPI** - Modern Python web framework
- **LangChain** - LLM orchestration
- **Groq** - Fast LLM inference
- **Firebase** - Backend services

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check API documentation at `http://localhost:8000/docs`

---

**Happy Coding! 🚀**
