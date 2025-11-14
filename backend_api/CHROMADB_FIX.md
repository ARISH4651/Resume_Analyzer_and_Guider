# Fix for ChromaDB Version Incompatibility

## Quick Fix - Delete and Recreate Vector Database

The error occurs because ChromaDB 0.4.24 has a different schema than the existing database.

### Option 1: Delete Old Database (Recommended)
```powershell
# Backup old database
Move-Item "D:\project\ML PROJECTS\Resume App\doc_vectorstore" "D:\project\ML PROJECTS\Resume App\doc_vectorstore_backup"

# Recreate vector database
cd "D:\project\ML PROJECTS\Resume App"
python process_knowledge_base.py
```

### Option 2: Downgrade ChromaDB
```powershell
pip install chromadb==0.3.29
```

### Option 3: Upgrade ChromaDB
```powershell
pip install --upgrade chromadb
```

Choose Option 1 to fix immediately.
