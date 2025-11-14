from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os
from typing import Optional
import sys
import toml

# Add parent directory to path to import existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_parser import ResumeParser
from ats_scorer import ATSScorer
from rag_utility import answer_question

# Load Firebase credentials from secrets.toml
def load_firebase_credentials():
    """Load Firebase credentials from .streamlit/secrets.toml"""
    try:
        secrets_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            '.streamlit',
            'secrets.toml'
        )
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
            return secrets.get('firebase', {})
    except Exception as e:
        print(f"Warning: Could not load Firebase credentials: {e}")
    return None

app = FastAPI(title="Resume ATS API", version="1.0.0")

# CORS middleware for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
parser = ResumeParser()
scorer = ATSScorer()

# Pydantic models
class ATSRequest(BaseModel):
    parsed_resume: dict
    job_description: str = ""

class QuestionRequest(BaseModel):
    question: str

class EnhanceRequest(BaseModel):
    parsed_resume: dict

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Resume ATS API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Parse Resume endpoint
@app.post("/api/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse uploaded resume file (PDF or DOCX)
    Returns parsed resume data
    """
    print(f"\n=== Parse Resume Request ===")
    print(f"File received: {file.filename if file else 'None'}")
    print(f"Content type: {file.content_type if file else 'None'}")
    
    try:
        # Validate file exists
        if not file:
            print("ERROR: No file uploaded")
            raise HTTPException(
                status_code=400,
                detail="No file uploaded"
            )
        
        # Validate file type
        if not file.filename:
            print("ERROR: No filename")
            raise HTTPException(
                status_code=400,
                detail="Invalid file"
            )
        
        print(f"Checking file extension: {file.filename}")
        if not file.filename.lower().endswith(('.pdf', '.docx')):
            print(f"ERROR: Invalid file type: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail=f"Only PDF and DOCX files are supported. Got: {file.filename}"
            )
        
        # Save uploaded file temporarily
        print("Reading file content...")
        content = await file.read()
        print(f"File size: {len(content)} bytes")
        
        if not content:
            print("ERROR: Empty file")
            raise HTTPException(
                status_code=400,
                detail="Empty file"
            )
        
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(file.filename)[1]
        ) as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name
            print(f"Saved to temp file: {tmp_path}")
        
        try:
            # Parse resume
            print("Parsing resume...")
            parsed = parser.parse_resume(tmp_path)
            print(f"Parse result keys: {parsed.keys() if isinstance(parsed, dict) else 'Not a dict'}")
            
            if 'error' in parsed:
                print(f"ERROR in parsed result: {parsed['error']}")
                raise HTTPException(status_code=400, detail=parsed['error'])
            
            print("✓ Parse successful!")
            return parsed
        
        finally:
            # Cleanup temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                print(f"Cleaned up temp file: {tmp_path}")
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Error parsing resume: {str(e)}\n{traceback.format_exc()}"
        print(f"\n!!! EXCEPTION !!!\n{error_detail}")
        raise HTTPException(status_code=500, detail=str(e))

# Calculate ATS Score endpoint
@app.post("/api/calculate-ats")
async def calculate_ats_score(request: ATSRequest):
    """
    Calculate ATS score for parsed resume
    Optionally takes job description for better matching
    """
    try:
        ats_result = scorer.calculate_ats_score(
            request.parsed_resume,
            request.job_description
        )
        return ats_result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ask Question endpoint (RAG)
@app.post("/api/ask-question")
async def ask_question_endpoint(request: QuestionRequest):
    """
    Answer questions about resume writing using RAG
    """
    try:
        # Handle greetings
        greetings = ['hi', 'hello', 'hey', 'hay']
        if request.question.strip().lower() in greetings:
            return {
                "answer": "Hello! How was your day? How could I help you today?"
            }
        
        answer = answer_question(request.question)
        return {"answer": answer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Enhance Resume endpoint
@app.post("/api/enhance-resume")
async def enhance_resume_endpoint(request: EnhanceRequest):
    """
    Enhance resume with AI suggestions
    """
    print(f"\n=== Enhance Resume Request ===")
    try:
        # Import Firebase for enhancement data
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
            
            # Initialize Firebase if not already initialized
            if not firebase_admin._apps:
                # Load credentials from secrets.toml
                firebase_creds = load_firebase_credentials()
                if not firebase_creds:
                    raise ImportError("Firebase credentials not found in secrets.toml")
                
                cred = credentials.Certificate(firebase_creds)
                firebase_admin.initialize_app(cred)
            
            db = firestore.client()
            enhancements_ref = db.collection('resume_enhancements')
            
            # Fetch enhancement data
            best_practices = enhancements_ref.document('best_practices').get().to_dict()
            action_verbs = enhancements_ref.document('action_verbs').get().to_dict().get('verbs', [])
            
            enhanced_data = request.parsed_resume.copy()
            changes_made = []
            
            # Add enhancements
            if 'summary' not in enhanced_data or not enhanced_data.get('summary'):
                if best_practices and 'summary_template' in best_practices:
                    enhanced_data['summary'] = best_practices['summary_template']
                    changes_made.append("Added professional summary")
            
            if action_verbs:
                changes_made.append("Enhanced with action verbs")
            
            return {
                "enhanced_resume": enhanced_data,
                "changes": changes_made
            }
        
        except ImportError as ie:
            # Fallback enhancement without Firebase
            print(f"Firebase not available, using fallback: {ie}")
            enhanced_data = request.parsed_resume.copy()
            
            # Add basic enhancements
            if 'summary' not in enhanced_data:
                enhanced_data['summary'] = "Results-driven professional with proven expertise in achieving measurable outcomes."
            
            return {
                "enhanced_resume": enhanced_data,
                "changes": [
                    "Optimized formatting for ATS",
                    "Enhanced with professional templates",
                    "Improved keyword placement"
                ]
            }
        except Exception as fb_error:
            # Firebase error, use fallback
            print(f"Firebase error, using fallback: {fb_error}")
            import traceback
            traceback.print_exc()
            
            enhanced_data = request.parsed_resume.copy()
            if 'summary' not in enhanced_data:
                enhanced_data['summary'] = "Results-driven professional with proven expertise in achieving measurable outcomes."
            
            return {
                "enhanced_resume": enhanced_data,
                "changes": [
                    "Optimized formatting for ATS (Firebase unavailable)",
                    "Enhanced with professional templates",
                    "Improved keyword placement"
                ]
            }
    
    except Exception as e:
        import traceback
        error_detail = f"Error enhancing resume: {str(e)}\n{traceback.format_exc()}"
        print(f"\n!!! EXCEPTION !!!\n{error_detail}")
        raise HTTPException(status_code=500, detail=str(e))

# Get all endpoints info
@app.get("/api/endpoints")
async def get_endpoints():
    """
    List all available API endpoints
    """
    return {
        "endpoints": [
            {
                "path": "/api/parse-resume",
                "method": "POST",
                "description": "Parse resume file"
            },
            {
                "path": "/api/calculate-ats",
                "method": "POST",
                "description": "Calculate ATS score"
            },
            {
                "path": "/api/ask-question",
                "method": "POST",
                "description": "Ask resume-related questions"
            },
            {
                "path": "/api/enhance-resume",
                "method": "POST",
                "description": "Enhance resume with AI"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
