"""
Upload PDFs to Firebase Storage
Helper script to batch upload knowledge base documents
"""

from firebase_utils import init_firebase_from_secrets
import os

def upload_knowledge_base_pdfs(local_dir: str = "./knowledge_base"):
    """
    Upload all PDFs from local directory to Firebase Storage
    
    Args:
        local_dir: Local directory containing PDF files
    """
    # Initialize Firebase
    firebase_manager = init_firebase_from_secrets()
    
    # Check if directory exists
    if not os.path.exists(local_dir):
        print(f"❌ Directory not found: {local_dir}")
        return
    
    # Get all PDF files
    pdf_files = [f for f in os.listdir(local_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"❌ No PDF files found in {local_dir}")
        return
    
    print(f"📄 Found {len(pdf_files)} PDF files")
    print("-" * 50)
    
    # Upload each file
    success_count = 0
    for pdf_file in pdf_files:
        local_path = os.path.join(local_dir, pdf_file)
        storage_path = f"knowledge_base/{pdf_file}"
        
        print(f"Uploading: {pdf_file}...")
        if firebase_manager.upload_pdf(local_path, storage_path):
            success_count += 1
    
    print("-" * 50)
    print(f"✅ Successfully uploaded {success_count}/{len(pdf_files)} files")


if __name__ == "__main__":
    # Note: This requires Streamlit to run for accessing secrets
    print("⚠️  Run this with Streamlit:")
    print("   streamlit run upload_to_firebase.py")
    
    # Uncomment below if running with streamlit
    # upload_knowledge_base_pdfs()
