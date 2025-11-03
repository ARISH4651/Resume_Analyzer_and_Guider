import os
import streamlit as st
from resume_parser import ResumeParser
from ats_scorer import ATSScorer
from rag_utility import answer_question
import tempfile

# Set working directory
working_dir = os.getcwd()

# Cache heavy model loading
@st.cache_resource
def get_parser():
    # Placeholder for actual model loading
    # Replace with your actual initialization logic if needed
    try:
        return ResumeParser()
    except Exception as e:
        st.error(f"Error initializing ResumeParser: {e}")
        return None

@st.cache_resource
def get_scorer():
    # Placeholder for actual model loading
    # Replace with your actual initialization logic if needed
    try:
        return ATSScorer()
    except Exception as e:
        st.error(f"Error initializing ATSScorer: {e}")
        return None

# Load models
parser = get_parser()
scorer = get_scorer()

# Apply minimal CSS for clean UI
st.markdown("""
<style>


[data-testid="column"]:nth-child(1) section[data-testid="stFileUploader"] label:hover {
    background-color: #3d3d3d !important;
}

/* --- Rest of your CSS (mostly unchanged) --- */

.welcome-title {
    font-size: 1.8rem !important;
}
.feature-card {
    padding: 1rem;
    height: auto;
    min-height: 200px;
}
.chat-input-container {
    max-width: 100%;
}
.stTextInput > div > div > input {
    padding: 12px 40px 12px 20px;
    font-size: 14px;
}
.user-message, .assistant-message {
    padding: 0.75rem;
    font-size: 14px;
}
.stButton > button {
    padding: 0.4rem 1rem;
    font-size: 14px;
}
@media (max-width: 480px) {
    .stApp {
        padding: 0 0.25rem;
    }
    h1 {
        font-size: 1.25rem !important;
        margin-bottom: 0.5rem;
    }
    .welcome-title {
        font-size: 1.5rem !important;
        margin-bottom: 1rem;
    }
    .feature-card {
        padding: 0.75rem;
        margin-bottom: 0.75rem;
    }
    .stTextInput > div > div > input {
        padding: 10px 35px 10px 15px;
        font-size: 13px;
        border-radius: 20px;
    }
    .user-message, .assistant-message {
        padding: 0.5rem;
        font-size: 13px;
    }
    [data-testid="column"]:last-child .stButton > button {
        width: 32px;
        height: 32px;
        font-size: 16px;
    }
}
/* Chat message styling */
.user-message {
    background-color: #2d2d2d;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}
.assistant-message {
    background-color: #1e1e1e;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}
/* Input box styling - ChatGPT style */
.stTextInput > div > div > input {
    background-color: black;
    border: 1px solid white;
    border-radius: 26px;
    padding: 14px 50px 14px 50px;
    color: white;
    font-size: 15px;
    transition: all 0.2s ease;
}
.stTextInput > div > div > input:focus {
    border: 1px solid white;
    outline: none;
    box-shadow: none;
}
.stTextInput > div > div > input::placeholder {
    color: #8e8ea0;
}
/* Button styling */
.stButton > button {
    background-color: transparent;
    border: 1px solid #3d3d3d;
    border-radius: 10px;
    color: white;
    padding: 0.5rem 1.5rem;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background-color: #2d2d2d;
    border-color: #5d5d5d;
}
/* Chat input wrapper styling */
.chat-input-container {
    position: relative;
    max-width: 800px;
    margin: 0 auto;
}
/* Plus button on left */
.plus-button {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: #8e8ea0;
    font-size: 20px;
    cursor: pointer;
    z-index: 10;
}
/* Send button on right - circular */
[data-testid="column"]:last-child .stButton > button {
    background-color: #2d2d2d;
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}
/* Upload button on left - circular */
[data-testid="column"]:nth-child(1) .stButton > button { 
    display: none !important; 
}


[data-testid="column"]:nth-child(1) .stButton > button:hover,
[data-testid="column"]:last-child .stButton > button:hover {
    background-color: #3d3d3d;
}

/* Welcome message styling */
.welcome-container {
    text-align: center;
    padding: 2rem 0 1rem 0;
}
.welcome-title {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}
/* Top navigation buttons */
.top-nav-buttons {
    position: absolute;
    top: 1rem;
    left: 1rem;
    display: flex;
    gap: 0.5rem;
}
/* Feature card styling */
.feature-card {
    background-color: #1e1e1e;
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #3d3d3d;
    margin-bottom: 1rem;
    height: 280px;
}
.feature-card h3 {
    margin-top: 0;
    margin-bottom: 1rem;
}
.feature-card ul {
    margin-bottom: 0;
}
/* Hide column dividers and gaps */
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    gap: 0rem;
}
[data-testid="column"] {
    border: none !important;
    box-shadow: none !important;
    background: none !important;
}
/* Remove column gaps */
[data-testid="column"]::before,
[data-testid="column"]::after {
    display: none !important;
}
/* Hide any scroll indicators */
::-webkit-scrollbar {
    display: none !important;
}
* {
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}
</style>
""",
unsafe_allow_html=True)
# Initialize session state
if 'mode' not in st.session_state:
    st.session_state.mode = 'home'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'analyzed_resume' not in st.session_state:
    st.session_state.analyzed_resume = None

# Title (hidden by CSS, but used for browser tab)
if st.session_state.mode != 'home':
    # Mode selection buttons at top
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button(" Home ", use_container_width=True):
            st.session_state.mode = 'home'
            st.rerun()
    with col2:
        if st.button(" Analyze Resume", use_container_width=True):
            st.session_state.mode = 'analyze'
            st.rerun()
    with col3:
        if st.button(" Resume Guide", use_container_width=True):
            st.session_state.mode = 'guide'
            st.rerun()
    with col4:
        if st.button(" Enhance Resume", use_container_width=True):
            st.session_state.mode = 'enhance'
            st.rerun()

# ==================== HOME MODE ====================
if st.session_state.mode == 'home':
    # Welcome section - centered like ChatGPT
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-title">What would you like to do today?</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature cards in row layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Analyze Resume card
        st.markdown("""
        <div class="feature-card">
            <h3> Analyze Resume</h3>
            <p>Upload your resume and get:</p>
            <ul>
                <li>ATS Score (0-100)</li>
                <li>Detailed feedback on each section</li>
                <li>Improvement suggestions</li>
                <li>Keyword analysis</li>
                <li>Format compatibility check</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Button below card
        if st.button("Analyze Resume", key="analyze_btn", use_container_width=True, type="primary"):
            st.session_state.mode = 'analyze'
            st.rerun()
    
    with col2:
        # Resume Guide card
        st.markdown("""
        <div class="feature-card">
            <h3>Resume Guide</h3>
            <p>Get expert guidance on:</p>
            <ul>
                <li>Creating ATS-friendly resumes</li>
                <li>Industry-specific keywords</li>
                <li>HR perspective insights</li>
                <li>Common mistakes to avoid</li>
                <li>Formatting best practices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Button below card
        if st.button(" Resume Guide", key="guide_btn", use_container_width=True, type="primary"):
            st.session_state.mode = 'guide'
            st.rerun()

# ==================== ANALYZE MODE ====================
elif st.session_state.mode == 'analyze':
    st.header(" Resume ATS Analyzer")
    
    # Optional job description
    with st.expander(" Add Job Description (Optional - for better keyword matching)"):
        job_description = st.text_area(
            "Paste the job description here",
            height=150,
            placeholder="Paste the job posting you're applying for to get better keyword matching..."
        )
    
    # Upload section at bottom with text box style
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Store uploaded file in session state
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    
    # Simple file uploader
    uploaded_resume = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=['pdf', 'docx'],
        key="resume_upload"
    )
    
    # Analyze button
    analyze_clicked = st.button("Analyze Resume", type="primary")
    
    if uploaded_resume and analyze_clicked:
        with st.spinner("Analyzing your resume..."):
            # Save uploaded file temporarily
            # Check if parser and scorer are successfully initialized
            if parser is None or scorer is None:
                st.error("Analysis failed: Resume parser or ATS scorer could not be initialized.")
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_resume.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_resume.getbuffer())
                    tmp_path = tmp_file.name
                
                try:
                    # Parse resume
                    parsed = parser.parse_resume(tmp_path)
                    
                    if 'error' in parsed:
                        st.error(parsed['error'])
                    else:
                        # Calculate ATS score
                        jd = job_description if 'job_description' in locals() else ""
                        ats_result = scorer.calculate_ats_score(parsed, jd)
                        
                        # Store in session
                        st.session_state.analyzed_resume = {
                            'parsed': parsed,
                            'ats_result': ats_result
                        }
                        
                        # Display results
                        st.success(" Analysis Complete!...")
                        
                        # Score display
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.metric(
                                label="ATS Score",
                                value=f"{ats_result['total_score']}/100",
                                delta=f"{ats_result['grade']}"
                            )
                            
                            # Progress bar
                            st.progress(ats_result['total_score'] / 100)
                        
                        st.markdown("---")
                        
                        # Detailed feedback
                        st.subheader("Detailed Analysis..")
                        
                        for category, details in ats_result['detailed_feedback'].items():
                            with st.expander(f"{category} - {details['score']}/{details['max']} points"):
                                for feedback in details['feedback']:
                                    if '✓' in feedback:
                                        st.success(feedback)
                                    elif '⚠' in feedback:
                                        st.warning(feedback)
                                    else:
                                        st.error(feedback)
                        
                        st.markdown("---")
                        
                        # Key insights
                        st.subheader(" Key Insights...")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Contact Information:**")
                            st.write(f"- Email: {parsed.get('email', 'Not found')}")
                            st.write(f"- Phone: {', '.join(parsed.get('phone', [])) or 'Not found'}")
                        
                        with col2:
                            st.write("**Content Metrics:**")
                            st.write(f"- Word Count: {parsed.get('word_count', 0)}")
                            st.write(f"- Action Verbs: {parsed.get('action_verb_count', 0)}")
                            st.write(f"- Quantifiable Results: {'Yes' if parsed.get('has_quantifiable_results') else 'No'}")
                        
                        # Recommendations
                        st.markdown("---")
                        st.subheader(" Recommendations...")
                        
                        recommendations = []
                        if ats_result['total_score'] < 70:
                            recommendations.append("🔴 **Critical**: Your resume needs significant improvements to pass ATS screening.")
                        if not parsed.get('email'):
                            recommendations.append("Add a professional email address")
                        if not parsed.get('has_quantifiable_results'):
                            recommendations.append("Add quantifiable achievements (e.g., 'Increased sales by 25%')")
                        if parsed.get('action_verb_count', 0) < 5:
                            recommendations.append(" Use more action verbs (achieved, improved, developed, etc.)")
                        
                        if recommendations:
                            for rec in recommendations:
                                st.warning(rec)
                        else:
                            st.success("Great job! Your resume is well-optimized for ATS!")
                        
                        # Enhance Resume button - always show
                        st.markdown("---")
                        if st.button("🚀 Enhance Resume", type="primary"):
                            st.session_state.mode = 'enhance'
                            st.rerun()
                        
                finally:
                    # Cleanup temp file
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)

# ==================== GUIDE MODE ====================
elif st.session_state.mode == 'guide':
    
    # If no chat history, show welcome message
    if not st.session_state.chat_history:
        st.markdown("""
            <div class="welcome-container">
                <div class="welcome-title">Where should we begin?</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Suggested questions in centered layout
        st.markdown("<br>", unsafe_allow_html=True)
        
        quick_questions = [
            "What is ATS and why is it important?",
            "What keywords should I include for a software engineer role?",
            "How should I format my experience section?",
            "What are common ATS mistakes?",
        ]
        
        for question in quick_questions:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(question, use_container_width=True):
                    st.session_state.chat_history.append({'role': 'user', 'content': question})
                    # Add check for utility function
                    if 'answer_question' in globals():
                        answer = answer_question(question)
                    else:
                        answer = "Error: RAG utility not available."
                        
                    st.session_state.chat_history.append({'role': 'assistant', 'content': answer})
                    st.rerun()
    
    else:
        # Display chat history
        for message in st.session_session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>AI Guide:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input at bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([8, 0.5])
    with col1:
        user_question = st.text_input(
            "",
            key=f"guide_input_{len(st.session_state.chat_history)}",
            placeholder="Ask anything",
            label_visibility="collapsed"
        )
    with col2:
        send_clicked = st.button("↑", key=f"send_{len(st.session_state.chat_history)}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if (send_clicked or user_question) and user_question.strip():
        # Add user question
        st.session_state.chat_history.append({'role': 'user', 'content': user_question})
        
        with st.spinner(""):
            # Get answer from RAG system
            if 'answer_question' in globals():
                answer = answer_question(user_question)
            else:
                answer = "Error: RAG utility not available."
            
            # Add AI response
            st.session_state.chat_history.append({'role': 'assistant', 'content': answer})
        
        st.rerun()

# ==================== ENHANCE MODE ====================
elif st.session_state.mode == 'enhance':
    st.header("🚀 Enhance Your Resume")
    
    # Check if we have analyzed resume data
    if not st.session_state.analyzed_resume:
        st.warning("Please analyze your resume first before enhancing it.")
        if st.button("Go to Analyze"):
            st.session_state.mode = 'analyze'
            st.rerun()
    else:
        ats_result = st.session_state.analyzed_resume['ats_result']
        parsed = st.session_state.analyzed_resume['parsed']
        
        # Show current score
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.metric(
                label="Current ATS Score",
                value=f"{ats_result['total_score']}/100",
                delta=f"{ats_result['grade']}"
            )
        
        st.markdown("---")
        
        # Enhancement sections
        st.subheader("📝 Resume Enhancement Guide")
        st.write("Fix the following issues to improve your ATS score:")
        
        # Collect all issues that need fixing
        issues_to_fix = []
        
        # Check each category for issues
        for category, details in ats_result['detailed_feedback'].items():
            for feedback in details['feedback']:
                if '✗' in feedback or '⚠' in feedback:
                    issues_to_fix.append({
                        'category': category,
                        'issue': feedback,
                        'severity': 'critical' if '✗' in feedback else 'warning'
                    })
        
        if not issues_to_fix:
            st.success("Your resume is already well-optimized!")
        else:
            # Group issues by severity
            critical_issues = [i for i in issues_to_fix if i['severity'] == 'critical']
            warning_issues = [i for i in issues_to_fix if i['severity'] == 'warning']
            
            # Display critical issues
            if critical_issues:
                st.error("### 🔴 Critical Issues (Fix these first)")
                for idx, issue in enumerate(critical_issues, 1):
                    with st.expander(f"{idx}. {issue['category']}", expanded=True):
                        st.write(issue['issue'])
                        st.text_area(
                            "How will you fix this?",
                            key=f"fix_critical_{idx}",
                            placeholder="Enter your corrected text or describe how you'll fix this issue...",
                            height=100
                        )
            
            # Display warning issues
            if warning_issues:
                st.warning("### ⚠️ Improvements Recommended")
                for idx, issue in enumerate(warning_issues, 1):
                    with st.expander(f"{idx}. {issue['category']}"):
                        st.write(issue['issue'])
                        st.text_area(
                            "How will you improve this?",
                            key=f"fix_warning_{idx}",
                            placeholder="Enter your improved text...",
                            height=100
                        )
        
        st.markdown("---")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Analysis", use_container_width=True):
                st.session_state.mode = 'analyze'
                st.rerun()
        with col2:
            if st.button("✅ Mark as Complete", type="primary", use_container_width=True):
                st.success("Great! Make sure to update your resume with these improvements.")
                st.balloons()
                st.info("Tip: Re-analyze your resume after making changes to see your improved score!")