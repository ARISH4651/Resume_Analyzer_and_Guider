<!--# Resume ATS Analyzer & Guide Bot - Setup Guide

## Prerequisites

1. **Python 3.11+** installed
2. **Virtual environment** (recommended)
3. **Firebase account** with Storage enabled
4. **Groq API key** for LLM access

## Step-by-Step Setup

### 1. Clone or Download Project

```bash
cd "d:\project\ml projects\RAG"
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements_resume_ats.txt
```

**Note:** If you encounter numpy compatibility issues:
```powershell
pip uninstall numpy -y
pip install "numpy<2.0.0,>=1.22.4"
```

### 4. Set Up Firebase

#### A. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create new project or use existing one
3. Enable **Firebase Storage**

#### B. Create Service Account
1. Go to Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Download JSON file

#### C. Configure Streamlit Secrets
Create `.streamlit/secrets.toml`:

```toml
# Groq API
GROQ_API_KEY = "your-groq-api-key-here"

# Firebase Service Account
[firebase]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

### 5. Test Firebase Connection

```powershell
streamlit run test_firebase.py
```

You should see:
- ✅ Firebase initialized successfully!
- Project configuration details
- List of files in storage (if any)

### 6. Prepare Knowledge Base (Optional)

Create PDF documents with ATS guidance:
- `ats_basics.pdf` - How ATS systems work
- `keyword_guide.pdf` - Industry keywords
- `hr_perspective.pdf` - What recruiters look for
- `formatting_guide.pdf` - Best formatting practices
- `common_mistakes.pdf` - What to avoid
- `action_verbs.pdf` - Strong action words
- `quantification_guide.pdf` - How to show impact

Upload to Firebase Storage in `knowledge_base/` folder.

### 7. Run the Application

```powershell
streamlit run resume_ats_app.py
```

The app will open at `http://localhost:8501`

## Features

### 📊 Analyze Resume
- Upload PDF/DOCX resume
- Get ATS score (0-100)
- Detailed feedback on 7 categories
- Actionable improvement suggestions

### 💡 Resume Guide
- Ask questions about ATS optimization
- Get expert guidance from knowledge base
- Industry-specific keyword suggestions
- RAG-powered Q&A

## Troubleshooting

### Firebase 404 Error
If you see "bucket does not exist":
1. Check Firebase Console → Storage
2. Note exact bucket name (might end with `.firebasestorage.app`)
3. Update `firebase_utils.py` line 17 with correct bucket name

### Import Errors
```powershell
pip install --upgrade -r requirements_resume_ats.txt
```

### Numpy Version Conflicts
```powershell
pip install "numpy<2.0.0,>=1.22.4" --force-reinstall
```

### Missing Modules
```powershell
pip install PyPDF2 pdfplumber python-docx firebase-admin
```

## Project Structure

```
RAG/
├── resume_ats_app.py          # Main Streamlit app
├── resume_parser.py           # Resume parsing logic
├── ats_scorer.py             # ATS scoring algorithm
├── firebase_manager.py        # Firebase Storage operations
├── firebase_utils.py          # Streamlit-Firebase integration
├── rag_utility.py            # RAG pipeline
├── test_firebase.py          # Firebase connection test
├── requirements_resume_ats.txt
├── .streamlit/
│   └── secrets.toml          # API keys & credentials
└── knowledge_base/           # PDF documents (optional)
```

## Next Steps

1. ✅ Verify Firebase connection works
2. 📄 Upload knowledge base PDFs
3. 🧪 Test resume analysis with sample resume
4. 💬 Test Q&A with resume guidance questions
5. 🚀 Deploy (optional)

## Support

For issues:
1. Check all dependencies are installed
2. Verify Firebase credentials are correct
3. Ensure Groq API key is valid
4. Test each component separately

Happy resume optimization! 🎯
