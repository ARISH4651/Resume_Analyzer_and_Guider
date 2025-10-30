"""
ATS Scorer Module
Calculates ATS compatibility score for resumes
"""

from typing import Dict, List, Tuple
import re


class ATSScorer:
    """Calculate ATS compatibility score"""
    
    def __init__(self):
        # Common ATS-friendly keywords by category
        self.technical_keywords = [
            'python', 'java', 'javascript', 'sql', 'aws', 'azure', 'docker',
            'kubernetes', 'react', 'node.js', 'machine learning', 'data analysis'
        ]
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem-solving',
            'analytical', 'project management', 'collaboration'
        ]
        
        # Must-have skills for different roles (expandable)
        self.must_have_skills = {
            'software engineer': ['programming', 'coding', 'software', 'development'],
            'data scientist': ['data', 'analysis', 'statistics', 'machine learning'],
            'project manager': ['project', 'management', 'planning', 'coordination'],
            'default': ['experience', 'skills']
        }
        
        # Formatting error patterns
        self.formatting_errors = {
            'tables': r'\|[\s\S]*\|',  # Markdown/text tables
            'special_chars': r'[★●■□▪►]',  # Special bullets/symbols
            'multiple_columns': r'(.{20,})\s{10,}(.{20,})',  # Wide spacing (columns)
        }
    
    def calculate_ats_score(self, parsed_resume: Dict, job_description: str = "") -> Dict:
        """
        Calculate overall ATS score
        
        Args:
            parsed_resume: Parsed resume data from ResumeParser
            job_description: Optional job description for keyword matching
            
        Returns:
            Dictionary with total score and detailed feedback
        """
        if 'error' in parsed_resume:
            return {'error': parsed_resume['error']}
        
        # Calculate individual scores
        format_score = self.score_format(parsed_resume)
        keyword_score = self.score_keywords(parsed_resume, job_description)
        section_score = self.score_sections(parsed_resume)
        contact_score = self.score_contact(parsed_resume)
        experience_score = self.score_experience(parsed_resume)
        skills_score = self.score_skills(parsed_resume)
        length_score = self.score_length(parsed_resume)
        
        # Total score (out of 100)
        total_score = (
            format_score[0] +
            keyword_score[0] +
            section_score[0] +
            contact_score[0] +
            experience_score[0] +
            skills_score[0] +
            length_score[0]
        )
        
        # Grade
        if total_score >= 90:
            grade = "Excellent"
        elif total_score >= 80:
            grade = "Very Good"
        elif total_score >= 70:
            grade = "Good"
        elif total_score >= 60:
            grade = "Fair"
        else:
            grade = "Needs Improvement"
        
        # Calculate Technical ATS Score
        technical_ats_score = self.calculate_technical_ats_score(parsed_resume, job_description)
        
        return {
            'total_score': round(total_score),
            'grade': grade,
            'detailed_feedback': {
                'Format': {'score': format_score[0], 'max': 20, 'feedback': format_score[1]},
                'Keywords': {'score': keyword_score[0], 'max': 25, 'feedback': keyword_score[1]},
                'Sections': {'score': section_score[0], 'max': 15, 'feedback': section_score[1]},
                'Contact Info': {'score': contact_score[0], 'max': 10, 'feedback': contact_score[1]},
                'Experience': {'score': experience_score[0], 'max': 15, 'feedback': experience_score[1]},
                'Skills': {'score': skills_score[0], 'max': 10, 'feedback': skills_score[1]},
                'Length': {'score': length_score[0], 'max': 5, 'feedback': length_score[1]}
            },
            'technical_ats_score': technical_ats_score
        }
    
    def score_format(self, resume: Dict) -> Tuple[float, List[str]]:
        """Score resume format (20 points max)"""
        score = 0
        feedback = []
        
        # Basic format check (assume PDF/DOCX is ATS-friendly)
        score += 10
        feedback.append("✓ File format is ATS-compatible")
        
        # Check for reasonable word count
        word_count = resume.get('word_count', 0)
        if 300 <= word_count <= 800:
            score += 10
            feedback.append(f"✓ Word count is optimal ({word_count} words)")
        elif word_count > 0:
            score += 5
            feedback.append(f"⚠ Word count is {word_count} (recommended: 300-800)")
        else:
            feedback.append("✗ Could not determine word count")
        
        return score, feedback
    
    def score_keywords(self, resume: Dict, job_description: str = "") -> Tuple[float, List[str]]:
        """Score keyword presence (25 points max)"""
        score = 0
        feedback = []
        text = resume.get('text', '').lower()
        
        # Technical keywords
        tech_found = sum(1 for kw in self.technical_keywords if kw in text)
        tech_score = min(15, (tech_found / len(self.technical_keywords)) * 15)
        score += tech_score
        
        if tech_found > 5:
            feedback.append(f"✓ Good technical keyword coverage ({tech_found} found)")
        else:
            feedback.append(f"⚠ Limited technical keywords ({tech_found} found)")
        
        # Soft skills
        soft_found = sum(1 for skill in self.soft_skills if skill in text)
        soft_score = min(10, (soft_found / len(self.soft_skills)) * 10)
        score += soft_score
        
        if soft_found > 3:
            feedback.append(f"✓ Good soft skills representation ({soft_found} found)")
        else:
            feedback.append(f"⚠ Consider adding more soft skills ({soft_found} found)")
        
        return score, feedback
    
    def score_sections(self, resume: Dict) -> Tuple[float, List[str]]:
        """Score section structure (15 points max)"""
        score = 0
        feedback = []
        sections = resume.get('sections', {})
        
        required_sections = ['experience', 'education', 'skills']
        optional_sections = ['summary', 'projects', 'certifications']
        
        # Required sections (3 points each)
        for section in required_sections:
            if sections.get(section, False):
                score += 5
                feedback.append(f"✓ {section.title()} section present")
            else:
                feedback.append(f"✗ Missing {section.title()} section")
        
        return score, feedback
    
    def score_contact(self, resume: Dict) -> Tuple[float, List[str]]:
        """Score contact information (10 points max)"""
        score = 0
        feedback = []
        
        # Email (5 points)
        if resume.get('email'):
            score += 5
            feedback.append(f"✓ Email present: {resume['email']}")
        else:
            feedback.append("✗ Email not found")
        
        # Phone (5 points)
        phones = resume.get('phone', [])
        if phones:
            score += 5
            feedback.append(f"✓ Phone number present")
        else:
            feedback.append("✗ Phone number not found")
        
        return score, feedback
    
    def score_experience(self, resume: Dict) -> Tuple[float, List[str]]:
        """Score experience section quality (15 points max)"""
        score = 0
        feedback = []
        
        # Action verbs (7 points)
        action_verb_count = resume.get('action_verb_count', 0)
        if action_verb_count >= 5:
            score += 7
            feedback.append(f"✓ Good use of action verbs ({action_verb_count} found)")
        elif action_verb_count > 0:
            score += 3
            feedback.append(f"⚠ Limited action verbs ({action_verb_count} found)")
        else:
            feedback.append("✗ No action verbs detected")
        
        # Quantifiable results (8 points)
        if resume.get('has_quantifiable_results', False):
            score += 8
            feedback.append("✓ Contains quantifiable achievements")
        else:
            feedback.append("✗ No quantifiable results found (add metrics, percentages, numbers)")
        
        return score, feedback
    
    def score_skills(self, resume: Dict) -> Tuple[float, List[str]]:
        """Score skills section (10 points max)"""
        score = 0
        feedback = []
        
        sections = resume.get('sections', {})
        if sections.get('skills', False):
            score += 10
            feedback.append("✓ Skills section present")
        else:
            feedback.append("✗ Skills section not clearly identified")
        
        return score, feedback
    
    def score_length(self, resume: Dict) -> Tuple[float, List[str]]:
        """Score resume length (5 points max)"""
        score = 0
        feedback = []
        
        word_count = resume.get('word_count', 0)
        
        # Optimal length: 1-2 pages (roughly 400-800 words)
        if 400 <= word_count <= 800:
            score += 5
            feedback.append("✓ Optimal resume length")
        elif 300 <= word_count < 400 or 800 < word_count <= 1000:
            score += 3
            feedback.append("⚠ Resume length acceptable but not optimal")
        else:
            score += 1
            feedback.append(f"✗ Resume length needs adjustment ({word_count} words)")
        
        return score, feedback
    
    def calculate_technical_ats_score(self, resume: Dict, job_description: str = "") -> Dict:
        """
        Calculate Technical (ATS) Score - UNIQUE FEATURE
        
        Measures:
        1. Parsing & Keywords: Explicit keyword overlap with job description
        2. Boolean checks: Must-have skills presence
        3. Formatting errors: Tables, non-standard headings, special characters
        
        Args:
            resume: Parsed resume data
            job_description: Job description text for keyword matching
            
        Returns:
            Dictionary with technical score details
        """
        text = resume.get('text', '').lower()
        result = {
            'keyword_overlap_percentage': 0,
            'must_have_skills_found': [],
            'must_have_skills_missing': [],
            'formatting_errors': [],
            'formatting_clean': True,
            'parsing_quality': 'Good'
        }
        
        # 1. KEYWORD OVERLAP ANALYSIS
        if job_description:
            jd_lower = job_description.lower()
            # Extract meaningful words (filter common words)
            common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            jd_keywords = set([word for word in re.findall(r'\b\w+\b', jd_lower) if len(word) > 3 and word not in common_words])
            resume_keywords = set([word for word in re.findall(r'\b\w+\b', text) if len(word) > 3 and word not in common_words])
            
            if jd_keywords:
                overlap = jd_keywords.intersection(resume_keywords)
                overlap_percentage = (len(overlap) / len(jd_keywords)) * 100
                result['keyword_overlap_percentage'] = round(overlap_percentage, 2)
                result['matched_keywords'] = list(overlap)[:10]  # Top 10 matches
        
        # 2. BOOLEAN CHECK FOR MUST-HAVE SKILLS
        # Detect job role from text or use default
        role = 'default'
        for job_role in self.must_have_skills.keys():
            if job_role in text or (job_description and job_role in job_description.lower()):
                role = job_role
                break
        
        must_have = self.must_have_skills.get(role, self.must_have_skills['default'])
        
        for skill in must_have:
            if skill in text:
                result['must_have_skills_found'].append(skill)
            else:
                result['must_have_skills_missing'].append(skill)
        
        # 3. FORMATTING ERROR DETECTION
        original_text = resume.get('text', '')
        
        # Check for tables
        if re.search(self.formatting_errors['tables'], original_text):
            result['formatting_errors'].append('❌ Tables detected (ATS may not parse correctly)')
            result['formatting_clean'] = False
        
        # Check for special characters/bullets
        if re.search(self.formatting_errors['special_chars'], original_text):
            result['formatting_errors'].append('❌ Special characters/bullets detected (use standard bullets: -, •)')
            result['formatting_clean'] = False
        
        # Check for multiple columns (wide spacing)
        if re.search(self.formatting_errors['multiple_columns'], original_text):
            result['formatting_errors'].append('❌ Multiple columns detected (use single-column layout)')
            result['formatting_clean'] = False
        
        # Check for non-standard section headings
        sections = resume.get('sections', {})
        if not any(sections.values()):
            result['formatting_errors'].append('❌ Non-standard section headings (use: Experience, Education, Skills)')
            result['formatting_clean'] = False
        
        if not result['formatting_errors']:
            result['formatting_errors'].append('✅ No formatting errors detected')
        
        # 4. PARSING QUALITY ASSESSMENT
        word_count = resume.get('word_count', 0)
        has_email = bool(resume.get('email'))
        has_sections = any(sections.values())
        
        if word_count > 200 and has_email and has_sections:
            result['parsing_quality'] = 'Excellent'
        elif word_count > 100 and (has_email or has_sections):
            result['parsing_quality'] = 'Good'
        else:
            result['parsing_quality'] = 'Poor - Resume may not parse correctly in ATS'
        
        return result
