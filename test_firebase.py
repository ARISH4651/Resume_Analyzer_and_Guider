"""
Test Firebase Connection
Quick script to verify Firebase is set up correctly
"""

import streamlit as st
from firebase_utils import init_firebase_from_secrets

st.set_page_config(page_title="Firebase Connection Test", page_icon="🔥")

st.title("🔥 Firebase Connection Test")

try:
    # Initialize Firebase
    firebase_manager = init_firebase_from_secrets()
    st.success("✅ Firebase initialized successfully!")
    
    # Display Firebase config
    firebase_creds = dict(st.secrets["firebase"])
    st.write("### Firebase Configuration")
    st.write(f"**Project ID:** {firebase_creds.get('project_id', 'N/A')}")
    st.write(f"**Client Email:** {firebase_creds.get('client_email', 'N/A')}")
    st.write(f"**Bucket Name:** {firebase_creds.get('project_id', 'N/A')}.appspot.com")
    
    # Try to list files
    st.write("### Storage Files")
    with st.spinner("Fetching files from Firebase Storage..."):
        files = firebase_manager.list_pdfs()
        
        if files:
            st.success(f"Found {len(files)} PDF files:")
            for file in files:
                st.write(f"- {file}")
        else:
            st.info("No PDF files found in storage (this is normal for new projects)")
    
except Exception as e:
    st.error(f"❌ Firebase connection failed!")
    st.write("**Error Details:**")
    st.code(str(e))
    st.write("**Troubleshooting Steps:**")
    st.write("1. Check if `.streamlit/secrets.toml` exists")
    st.write("2. Verify all Firebase credentials are correctly set")
    st.write("3. Ensure Firebase Storage is enabled in Firebase Console")
    st.write("4. Check if service account has proper permissions")
