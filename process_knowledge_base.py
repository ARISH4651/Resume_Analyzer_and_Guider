"""
Process Knowledge Base
Downloads PDFs from Firebase and processes them into ChromaDB
"""

from firebase_utils import init_firebase_from_secrets
from rag_utility import process_document_to_chroma_db
import os
import tempfile

def process_knowledge_base():
    """
    Download PDFs from Firebase and process into ChromaDB vector store
    """
    # Initialize Firebase
    print("🔥 Initializing Firebase...")
    firebase_manager = init_firebase_from_secrets()
    
    # List available PDFs
    print("📄 Fetching PDF list...")
    pdf_files = firebase_manager.list_pdfs("knowledge_base/")
    
    if not pdf_files:
        print("❌ No PDF files found in Firebase Storage")
        return
    
    print(f"✅ Found {len(pdf_files)} PDF files")
    print("-" * 50)
    
    # Create temporary directory for downloads
    with tempfile.TemporaryDirectory() as temp_dir:
        processed_count = 0
        
        for pdf_path in pdf_files:
            filename = os.path.basename(pdf_path)
            local_path = os.path.join(temp_dir, filename)
            
            print(f"\n📥 Processing: {filename}")
            
            # Download from Firebase
            if firebase_manager.download_pdf(pdf_path, local_path):
                # Process into ChromaDB
                print(f"🔄 Adding to vector store...")
                try:
                    process_document_to_chroma_db(local_path)
                    processed_count += 1
                    print(f"✅ {filename} processed successfully")
                except Exception as e:
                    print(f"❌ Error processing {filename}: {e}")
            else:
                print(f"❌ Failed to download {filename}")
    
    print("-" * 50)
    print(f"🎉 Completed! Processed {processed_count}/{len(pdf_files)} documents")
    print("📊 Knowledge base is ready for Q&A!")


if __name__ == "__main__":
    print("⚠️  Run this with Streamlit:")
    print("   streamlit run process_knowledge_base.py")
    
    # Uncomment below if running with streamlit
    # process_knowledge_base()
