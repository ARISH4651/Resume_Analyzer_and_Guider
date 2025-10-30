"""
Firebase Manager Module
Handles Firebase Storage operations for knowledge base PDFs
"""

import firebase_admin
from firebase_admin import credentials, storage
import os
from typing import List, Dict, Optional


class FirebaseManager:
    """Manage Firebase Storage operations"""
    
    def __init__(self, service_account_path: Optional[str] = None, service_account_dict: Optional[Dict] = None):
        """
        Initialize Firebase Manager
        
        Args:
            service_account_path: Path to service account JSON file (optional)
            service_account_dict: Service account credentials as dictionary (optional)
        """
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            if service_account_dict:
                cred = credentials.Certificate(service_account_dict)
            elif service_account_path:
                cred = credentials.Certificate(service_account_path)
            else:
                raise ValueError("Either service_account_path or service_account_dict must be provided")
            
            firebase_admin.initialize_app(cred, {
                'storageBucket': f"{service_account_dict.get('project_id', '')}.appspot.com" if service_account_dict else None
            })
        
        self.bucket = storage.bucket()
    
    def upload_pdf(self, local_path: str, storage_path: str) -> bool:
        """
        Upload PDF to Firebase Storage
        
        Args:
            local_path: Local file path
            storage_path: Path in Firebase Storage (e.g., 'knowledge_base/file.pdf')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            blob = self.bucket.blob(storage_path)
            blob.upload_from_filename(local_path)
            print(f"✅ Uploaded: {storage_path}")
            return True
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return False
    
    def download_pdf(self, storage_path: str, local_path: str) -> bool:
        """
        Download PDF from Firebase Storage
        
        Args:
            storage_path: Path in Firebase Storage
            local_path: Local destination path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            blob = self.bucket.blob(storage_path)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            blob.download_to_filename(local_path)
            print(f"✅ Downloaded: {storage_path}")
            return True
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def list_pdfs(self, prefix: str = "knowledge_base/") -> List[str]:
        """
        List all PDFs in Firebase Storage with given prefix
        
        Args:
            prefix: Folder prefix to search in
            
        Returns:
            List of file paths
        """
        try:
            blobs = self.bucket.list_blobs(prefix=prefix)
            pdf_files = [blob.name for blob in blobs if blob.name.endswith('.pdf')]
            return pdf_files
        except Exception as e:
            print(f"❌ List failed: {e}")
            return []
    
    def download_all_pdfs(self, storage_prefix: str = "knowledge_base/", local_dir: str = "./knowledge_base") -> int:
        """
        Download all PDFs from a folder in Firebase Storage
        
        Args:
            storage_prefix: Folder prefix in Firebase Storage
            local_dir: Local directory to save files
            
        Returns:
            Number of files downloaded
        """
        pdf_files = self.list_pdfs(storage_prefix)
        count = 0
        
        for file_path in pdf_files:
            filename = os.path.basename(file_path)
            local_path = os.path.join(local_dir, filename)
            
            if self.download_pdf(file_path, local_path):
                count += 1
        
        print(f"✅ Downloaded {count} PDF files")
        return count
    
    def delete_pdf(self, storage_path: str) -> bool:
        """
        Delete PDF from Firebase Storage
        
        Args:
            storage_path: Path in Firebase Storage
            
        Returns:
            True if successful, False otherwise
        """
        try:
            blob = self.bucket.blob(storage_path)
            blob.delete()
            print(f"✅ Deleted: {storage_path}")
            return True
        except Exception as e:
            print(f"❌ Delete failed: {e}")
            return False
