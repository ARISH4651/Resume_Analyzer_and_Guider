# Firebase Setup for Resume ATS Bot

## Overview
<!--This guide walks you through setting up Firebase Storage for the Resume ATS knowledge base.

## Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"**
3. Enter project name (e.g., "resume-ats-bot")
4. (Optional) Enable Google Analytics
5. Click **"Create project"**

## Step 2: Enable Firebase Storage

1. In Firebase Console, click **"Storage"** in left sidebar
2. Click **"Get Started"**
3. Choose **"Start in production mode"** (we'll update rules later)
4. Select a storage location (e.g., us-central1)
5. Click **"Done"**

## Step 3: Update Storage Rules

1. Go to **Storage → Rules**
2. Replace default rules with:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /knowledge_base/{allPaths=**} {
      allow read: if true;  // Public read
      allow write: if request.auth != null;  // Auth required for write
    }
    match /{allPaths=**} {
      allow read, write: if request.auth != null;  // Auth for everything else
    }
  }
}
```

3. Click **"Publish"**

## Step 4: Create Service Account

1. Click **⚙️ (Settings)** → **"Project settings"**
2. Go to **"Service accounts"** tab
3. Click **"Generate new private key"**
4. Confirm and download JSON file
5. **Keep this file secure!** (contains sensitive credentials)

## Step 5: Configure Streamlit Secrets

1. Create folder: `.streamlit/` in your project
2. Create file: `.streamlit/secrets.toml`
3. Open the downloaded JSON file
4. Copy values to secrets.toml:

```toml
# Groq API Key
GROQ_API_KEY = "your-groq-api-key"

# Firebase Service Account
[firebase]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Multi-Line-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email"
universe_domain = "googleapis.com"
```

**Important:** Keep `\n` in the private_key value!

## Step 6: Get Your Bucket Name

1. In Firebase Console, go to **Storage**
2. Look at the top - you'll see your bucket name
3. It will be in one of these formats:
   - `your-project-id.appspot.com`
   - `your-project-id.firebasestorage.app`

4. If it's NOT `.appspot.com`, update `firebase_utils.py`:

```python
# Line 17
bucket_name = f"{project_id}.firebasestorage.app"  # Change if needed
```

## Step 7: Set Service Account Permissions

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to **IAM & Admin → IAM**
4. Find your service account email
5. Click **Edit (pencil icon)**
6. Add these roles:
   - **Storage Admin**
   - **Storage Object Admin**
7. Click **Save**

## Step 8: Test Connection

Run the test script:

```powershell
streamlit run test_firebase.py
```

Expected output:
```
✅ Firebase initialized successfully!
Project ID: your-project-id
Client Email: firebase-adminsdk@...
Found 0 PDF files (normal for new projects)
```

## Troubleshooting

### Error: "Bucket does not exist" (404)

**Solution 1:** Verify bucket name
```python
# In firebase_utils.py, line 17
bucket_name = f"{project_id}.firebasestorage.app"  # Try this format
```

**Solution 2:** Check Firebase Console
- Go to Storage
- Copy exact bucket name shown
- Update firebase_utils.py

### Error: "Permission denied" (403)

**Solution:** Add Storage Admin role
1. Google Cloud Console → IAM
2. Edit service account
3. Add "Storage Admin" role

### Error: "Invalid credentials"

**Solution:** Regenerate service account key
1. Firebase Console → Project Settings → Service Accounts
2. Generate new private key
3. Update secrets.toml with new values

### Error: Module import errors

```powershell
pip install firebase-admin google-cloud-storage
```

## Create Knowledge Base Folder

In Firebase Storage:

1. Click **"Upload file"** or **"Create folder"**
2. Create folder named: `knowledge_base`
3. Upload your PDF files:
   - ats_basics.pdf
   - keyword_guide.pdf
   - hr_perspective.pdf
   - formatting_guide.pdf
   - common_mistakes.pdf
   - action_verbs.pdf
   - quantification_guide.pdf

## Upload PDFs via Code (Optional)

Create `upload_pdfs.py`:

```python
from firebase_utils import init_firebase_from_secrets

firebase_manager = init_firebase_from_secrets()

# Upload single file
firebase_manager.upload_pdf(
    local_path="./pdfs/ats_basics.pdf",
    storage_path="knowledge_base/ats_basics.pdf"
)

# Upload multiple files
import os
pdf_dir = "./pdfs"
for filename in os.listdir(pdf_dir):
    if filename.endswith('.pdf'):
        firebase_manager.upload_pdf(
            local_path=os.path.join(pdf_dir, filename),
            storage_path=f"knowledge_base/{filename}"
        )
```

## Security Best Practices

1. ✅ **Never commit** secrets.toml to git
2. ✅ Add `.streamlit/secrets.toml` to `.gitignore`
3. ✅ Use environment-specific credentials
4. ✅ Rotate service account keys regularly
5. ✅ Limit service account permissions
6. ✅ Enable Firebase Storage Rules

## Next Steps

After Firebase is set up:

1. ✅ Test connection with `test_firebase.py`
2. 📄 Upload knowledge base PDFs
3. 🤖 Process PDFs into ChromaDB
4. 🚀 Run main app: `streamlit run resume_ats_app.py`

## Useful Links

- [Firebase Console](https://console.firebase.google.com/)
- [Firebase Storage Docs](https://firebase.google.com/docs/storage)
- [Service Account Docs](https://cloud.google.com/iam/docs/service-accounts)
- [Storage Security Rules](https://firebase.google.com/docs/storage/security)
