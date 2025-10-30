"""
Firebase Utilities for Streamlit
Helper functions to initialize Firebase from Streamlit secrets
"""

import streamlit as st
from firebase_manager import FirebaseManager


def init_firebase_from_secrets():
    """
    Initialize Firebase using credentials from Streamlit secrets
    
    Returns:
        FirebaseManager instance
    """
    # Get Firebase credentials from secrets
    firebase_creds = dict(st.secrets["firebase"])
    
    # Extract project_id to construct bucket name
    project_id = firebase_creds.get("project_id", "")
    bucket_name = f"{project_id}.appspot.com"
    
    # Initialize Firebase Manager
    firebase_manager = FirebaseManager(service_account_dict=firebase_creds)
    
    return firebase_manager


def check_firebase_connection():
    """
    Test Firebase connection
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        firebase_manager = init_firebase_from_secrets()
        
        # Try to list files (this will fail if connection is bad)
        files = firebase_manager.list_pdfs()
        
        return True, f"✅ Firebase connected! Found {len(files)} PDF files."
    except Exception as e:
        return False, f"❌ Firebase connection failed: {str(e)}"
