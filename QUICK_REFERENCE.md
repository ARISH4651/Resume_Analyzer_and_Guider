# Resume ATS Bot - Quick Reference

<!--## Installation
```powershell
pip install -r requirements_resume_ats.txt
```

## Run Application
```powershell
streamlit run resume_ats_app.py
```

## Test Firebase
```powershell
streamlit run test_firebase.py
```

## Key Files

| File | Purpose |
|------|---------|
| `resume_ats_app.py` | Main application UI |
| `resume_parser.py` | Extract text from resumes |
| `ats_scorer.py` | Calculate ATS compatibility |
| `firebase_manager.py` | Firebase Storage ops |
| `firebase_utils.py` | Streamlit-Firebase bridge |
| `rag_utility.py` | RAG Q&A system |

## ATS Scoring Breakdown (100 points)

| Category | Points | What's Checked |
|----------|--------|----------------|
| **Format** | 20 | File type, word count |
| **Keywords** | 25 | Technical & soft skills |
| **Sections** | 15 | Experience, Education, Skills |
| **Contact** | 10 | Email, phone present |
| **Experience** | 15 | Action verbs, metrics |
| **Skills** | 10 | Skills section clarity |
| **Length** | 5 | 400-800 words optimal |

## Score Grades

- **90-100**: Excellent
- **80-89**: Very Good
- **70-79**: Good
- **60-69**: Fair
- **<60**: Needs Improvement

## Common Commands

### Install specific package
```powershell
pip install PyPDF2
```

### Fix numpy issues
```powershell
pip install "numpy<2.0.0,>=1.22.4"
```

### Activate venv
```powershell
.\venv\Scripts\Activate
```

### Deactivate venv
```powershell
deactivate
```

## Firebase Quick Setup

1. **Create project** at [Firebase Console](https://console.firebase.google.com/)
2. **Enable Storage**
3. **Generate service account key**
4. **Add to** `.streamlit/secrets.toml`
5. **Test** with `streamlit run test_firebase.py`

## Secrets Template

`.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-key-here"

[firebase]
type = "service_account"
project_id = "your-project-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk@your-project.iam.gserviceaccount.com"
# ... other fields
```

## Quick Tips

✅ **DO:**
- Use PDF or DOCX format
- Include email and phone
- Use action verbs
- Add quantifiable results
- Keep 400-800 words
- Have clear sections

❌ **DON'T:**
- Use tables or columns
- Add images/graphics
- Use fancy fonts
- Exceed 2 pages
- Forget contact info
- Skip skills section

## Suggested Questions (Resume Guide)

- "What is ATS and why is it important?"
- "What keywords should I include for [role]?"
- "How should I format my experience section?"
- "What are common ATS mistakes?"
- "Best action verbs for [industry]?"

## Support

🔍 Check logs if app crashes
🔥 Test Firebase connection first
📦 Reinstall packages if import errors
🔑 Verify API keys in secrets.toml
