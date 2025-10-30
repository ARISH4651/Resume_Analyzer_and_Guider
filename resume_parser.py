"""
Resume Parser Module
Extracts and parses content from PDF and DOCX resume files
"""

import re
from typing import Dict, List
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from docx import Document
except ImportError:
    Document = None


class ResumeParser:
    """Parse resume content from PDF/DOCX files"""
    
    def __init__(self):
        self.action_verbs = [
            'achieved', 'improved', 'developed', 'created', 'managed', 'led',
            'designed', 'implemented', 'built', 'increased', 'decreased',
            'launched', 'established', 'streamlined', 'optimized', 'resolved',
            'delivered', 'executed', 'coordinated', 'initiated', 'transformed'
        ]
    
    def parse_resume(self, file_path: str) -> Dict:
        """
        Parse resume file and extract structured information
        
        Args:
            file_path: Path to resume file (PDF or DOCX)
            
        Returns:
            Dictionary containing parsed resume information
        """
        # Extract text
        text = self.extract_text(file_path)
        
        if not text:
            return {'error': 'Could not extract text from resume'}
        
        # Parse sections
        parsed_data = {
            'text': text,
            'word_count': len(text.split()),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'sections': self.extract_sections(text),
            'action_verb_count': self.count_action_verbs(text),
            'has_quantifiable_results': self.has_quantifiable_results(text)
        }
        
        return parsed_data
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX file"""
        if file_path.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return self.extract_text_from_docx(file_path)
        return ""
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using pdfplumber or PyPDF2"""
        text = ""
        
        # Try pdfplumber first (better extraction)
        if pdfplumber:
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                return text
            except Exception as e:
                print(f"pdfplumber error: {e}")
        
        # Fallback to PyPDF2
        if PyPDF2:
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                return text
            except Exception as e:
                print(f"PyPDF2 error: {e}")
        
        return text
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        if not Document:
            return ""
        
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            return ""
    
    def extract_email(self, text: str) -> str:
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else ""
    
    def extract_phone(self, text: str) -> List[str]:
        """Extract phone numbers from text"""
        # Pattern for various phone formats
        phone_patterns = [
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 123-456-7890
            r'\b\(\d{3}\)\s?\d{3}[-.\s]?\d{4}\b',   # (123) 456-7890
            r'\b\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'  # +1 123-456-7890
        ]
        
        phones = []
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            phones.extend(matches)
        
        return list(set(phones))  # Remove duplicates
    
    def extract_sections(self, text: str) -> Dict[str, bool]:
        """Detect common resume sections"""
        text_lower = text.lower()
        
        sections = {
            'experience': any(keyword in text_lower for keyword in [
                'experience', 'work history', 'employment', 'professional experience'
            ]),
            'education': any(keyword in text_lower for keyword in [
                'education', 'academic', 'degree', 'university', 'college'
            ]),
            'skills': any(keyword in text_lower for keyword in [
                'skills', 'technical skills', 'competencies', 'expertise'
            ]),
            'summary': any(keyword in text_lower for keyword in [
                'summary', 'profile', 'objective', 'about'
            ]),
            'projects': 'project' in text_lower,
            'certifications': any(keyword in text_lower for keyword in [
                'certification', 'certificate', 'credential'
            ])
        }
        
        return sections
    
    def count_action_verbs(self, text: str) -> int:
        """Count action verbs in resume"""
        text_lower = text.lower()
        count = sum(1 for verb in self.action_verbs if verb in text_lower)
        return count
    
    def has_quantifiable_results(self, text: str) -> bool:
        """Check if resume contains quantifiable achievements"""
        # Look for percentages, numbers with units, etc.
        patterns = [
            r'\d+%',  # Percentages
            r'\$\d+',  # Dollar amounts
            r'\d+\s*(million|thousand|billion|k)',  # Large numbers
            r'increased by \d+',
            r'decreased by \d+',
            r'saved \$?\d+',
            r'grew by \d+',
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
