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
            }
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
