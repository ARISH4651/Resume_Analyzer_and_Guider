"""
FastAPI Backend for Resume ATS Mobile App
Uses existing modules from parent directory to avoid reinstalling heavy dependencies
"""
import sys
import os

# Add parent directory to path to use existing installed modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Check if venv from parent exists and use it
parent_venv = os.path.join(parent_dir, 'venv')
if os.path.exists(parent_venv):
    print(f"Using virtual environment from: {parent_venv}")
    # Add parent venv to path
    site_packages = os.path.join(parent_venv, 'Lib', 'site-packages')
    if os.path.exists(site_packages):
        sys.path.insert(0, site_packages)

# Now import and run the FastAPI app
from main import app

if __name__ == "__main__":
    import uvicorn
    print("Starting Resume ATS API Server...")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
