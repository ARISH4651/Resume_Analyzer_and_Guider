"""
ATS Scorer Module
Calculates ATS compatibility score for resumes
"""

from typing import Dict, List, Tuple
import re
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np


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
        
        # Initialize embeddings model for semantic scoring
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        except:
            self.embeddings = None
    
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
        
        # Calculate Semantic Score
        semantic_score = self.calculate_semantic_score(parsed_resume, job_description)
        
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
            'technical_ats_score': technical_ats_score,
            'semantic_score': semantic_score
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
    
    def calculate_semantic_score(self, resume: Dict, job_description: str = "") -> Dict:
        """
        Calculate Semantic Score - UNIQUE FEATURE
        
        Measures context & equivalence between resume and JD using LLM embeddings.
        Recognizes synonyms and inferred skills (e.g., "Used Pandas" matches "Data Analysis").
        Validates capability, not just word count.
        
        Args:
            resume: Parsed resume data
            job_description: Job description text
            
        Returns:
            Dictionary with semantic matching details
        """
        result = {
            'semantic_similarity_score': 0.0,
            'context_match_level': 'None',
            'inferred_skills': [],
            'synonym_matches': [],
            'capability_validation': 'Not Available'
        }
        
        if not job_description or not self.embeddings:
            result['capability_validation'] = 'No job description provided or embeddings unavailable'
            return result
        
        resume_text = resume.get('text', '')
        if not resume_text:
            return result
        
        try:
            # Split texts into manageable chunks (semantic sections)
            resume_chunks = self._extract_semantic_chunks(resume_text)
            jd_chunks = self._extract_semantic_chunks(job_description)
            
            # Generate embeddings
            resume_embeddings = [self.embeddings.embed_query(chunk) for chunk in resume_chunks]
            jd_embeddings = [self.embeddings.embed_query(chunk) for chunk in jd_chunks]
            
            # Calculate cosine similarity between all pairs
            similarities = []
            for r_emb in resume_embeddings:
                for jd_emb in jd_embeddings:
                    similarity = self._cosine_similarity(r_emb, jd_emb)
                    similarities.append(similarity)
            
            # Overall semantic similarity (average of top matches)
            if similarities:
                top_similarities = sorted(similarities, reverse=True)[:10]
                avg_similarity = np.mean(top_similarities)
                result['semantic_similarity_score'] = round(float(avg_similarity * 100), 2)
                
                # Context match level
                if avg_similarity >= 0.75:
                    result['context_match_level'] = 'High - Strong semantic alignment'
                elif avg_similarity >= 0.60:
                    result['context_match_level'] = 'Medium - Good contextual match'
                elif avg_similarity >= 0.45:
                    result['context_match_level'] = 'Low - Some relevance detected'
                else:
                    result['context_match_level'] = 'Very Low - Weak alignment'
            
            # Detect inferred skills and synonym matches
            result['inferred_skills'] = self._detect_inferred_skills(resume_text, job_description)
            result['synonym_matches'] = self._detect_synonym_matches(resume_text, job_description)
            
            # Capability validation
            if result['semantic_similarity_score'] >= 70:
                result['capability_validation'] = '✅ HIGH - Strong capability match, validates skills beyond keywords'
            elif result['semantic_similarity_score'] >= 50:
                result['capability_validation'] = '⚠️ MEDIUM - Moderate capability match, some relevant experience'
            else:
                result['capability_validation'] = '❌ LOW - Limited capability match, consider adding relevant experience'
                
        except Exception as e:
            result['capability_validation'] = f'Error calculating semantic score: {str(e)}'
        
        return result
    
    def _extract_semantic_chunks(self, text: str) -> List[str]:
        """Extract meaningful semantic chunks from text"""
        # Split by sentences or paragraphs
        chunks = []
        sentences = re.split(r'[.!?]\s+', text)
        
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < 500:  # Max chunk size
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [text[:500]]  # At least one chunk
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _detect_inferred_skills(self, resume_text: str, job_description: str) -> List[str]:
        """Detect inferred skills (e.g., 'pandas' implies 'data analysis')"""
        inferred = []
        resume_lower = resume_text.lower()
        jd_lower = job_description.lower()
        
        # Skill inference mappings
        skill_inferences = {
            'pandas': 'Data Analysis',
            'numpy': 'Numerical Computing',
            'scikit-learn': 'Machine Learning',
            'tensorflow': 'Deep Learning',
            'pytorch': 'Deep Learning',
            'sql': 'Database Management',
            'postgresql': 'Database Management',
            'docker': 'Containerization',
            'kubernetes': 'Container Orchestration',
            'aws': 'Cloud Computing',
            'azure': 'Cloud Computing',
            'git': 'Version Control',
            'jenkins': 'CI/CD',
            'react': 'Frontend Development',
            'node.js': 'Backend Development'
        }
        
        for tool, skill in skill_inferences.items():
            if tool in resume_lower and skill.lower() in jd_lower:
                inferred.append(f"'{tool.title()}' → infers '{skill}'")
        
        return inferred[:5]  # Top 5
    
    def _detect_synonym_matches(self, resume_text: str, job_description: str) -> List[str]:
        """Detect synonym matches between resume and JD"""
        matches = []
        resume_lower = resume_text.lower()
        jd_lower = job_description.lower()
        
        # Common synonym groups
        synonyms = {
            'leadership': ['led', 'managed', 'directed', 'supervised', 'headed'],
            'development': ['built', 'created', 'developed', 'engineered', 'designed'],
            'analysis': ['analyzed', 'evaluated', 'assessed', 'examined', 'studied'],
            'collaboration': ['collaborated', 'partnered', 'worked with', 'teamed', 'coordinated'],
            'improvement': ['improved', 'enhanced', 'optimized', 'streamlined', 'increased']
        }
        
        for concept, synonym_list in synonyms.items():
            if concept in jd_lower:
                found_synonyms = [syn for syn in synonym_list if syn in resume_lower]
                if found_synonyms:
                    matches.append(f"JD: '{concept}' ↔ Resume: '{found_synonyms[0]}'")
        
        return matches[:5]  # Top 5
    
    def calculate_pathfinder_analysis(self, resume: Dict, job_descriptions: List[str]) -> Dict:
        """
        Proactive Career Path Analysis (The "Pathfinder") - UNIQUE FEATURE
        
        Analyzes 3-5 job descriptions to identify:
        1. Common high-demand skills across all JDs
        2. Future-looking keywords
        3. Skill gaps in candidate's resume
        4. High-value synonyms to integrate
        
        Optimizes resume for the future career path, not just one job.
        
        Args:
            resume: Parsed resume data
            job_descriptions: List of 3-5 job description texts
            
        Returns:
            Dictionary with career path analysis
        """
        result = {
            'skill_gap_report': [],
            'high_value_synonyms': [],
            'common_keywords': [],
            'high_demand_skills': [],
            'future_looking_skills': [],
            'career_optimization_score': 0
        }
        
        if not job_descriptions or len(job_descriptions) < 3:
            result['error'] = 'Please provide at least 3 job descriptions for career path analysis'
            return result
        
        resume_text = resume.get('text', '').lower()
        
        try:
            # 1. AGGREGATE KEYWORDS ACROSS ALL JDs
            all_jd_keywords = []
            keyword_frequency = {}
            
            for jd in job_descriptions:
                jd_lower = jd.lower()
                # Extract meaningful keywords (filter common words)
                common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                               'of', 'with', 'by', 'from', 'will', 'be', 'is', 'are', 'have', 'has'}
                keywords = [word for word in re.findall(r'\b[a-z]{4,}\b', jd_lower) 
                           if word not in common_words]
                
                all_jd_keywords.extend(keywords)
                
                for keyword in set(keywords):
                    keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
            
            # 2. IDENTIFY COMMON HIGH-DEMAND KEYWORDS
            # Keywords appearing in at least 60% of JDs
            min_frequency = max(2, int(len(job_descriptions) * 0.6))
            common_keywords = [kw for kw, freq in keyword_frequency.items() 
                             if freq >= min_frequency]
            result['common_keywords'] = sorted(common_keywords, 
                                              key=lambda x: keyword_frequency[x], 
                                              reverse=True)[:15]
            
            # 3. IDENTIFY HIGH-DEMAND SKILLS (appear in multiple JDs)
            high_demand_skills = [kw for kw, freq in keyword_frequency.items() 
                                if freq >= len(job_descriptions) * 0.4]
            result['high_demand_skills'] = sorted(set(high_demand_skills), 
                                                 key=lambda x: keyword_frequency[x], 
                                                 reverse=True)[:10]
            
            # 4. IDENTIFY FUTURE-LOOKING SKILLS
            future_tech_keywords = {
                'ai', 'artificial intelligence', 'machine learning', 'deep learning',
                'kubernetes', 'cloud', 'microservices', 'devops', 'agile', 'scrum',
                'automation', 'cicd', 'containerization', 'serverless', 'blockchain',
                'data science', 'analytics', 'big data', 'distributed systems',
                'react', 'angular', 'vue', 'typescript', 'python', 'golang'
            }
            
            all_jd_text = ' '.join(job_descriptions).lower()
            future_skills_found = [skill for skill in future_tech_keywords 
                                  if skill in all_jd_text]
            result['future_looking_skills'] = future_skills_found[:10]
            
            # 5. SKILL GAP REPORT
            skill_gaps = []
            for keyword in result['common_keywords']:
                if keyword not in resume_text:
                    # Check if it's truly a skill/technology
                    if len(keyword) > 3 and keyword_frequency[keyword] >= min_frequency:
                        skill_gaps.append({
                            'skill': keyword,
                            'appears_in_jds': keyword_frequency[keyword],
                            'priority': 'HIGH' if keyword_frequency[keyword] >= len(job_descriptions) * 0.8 else 'MEDIUM'
                        })
            
            result['skill_gap_report'] = sorted(skill_gaps, 
                                               key=lambda x: x['appears_in_jds'], 
                                               reverse=True)[:10]
            
            # 6. HIGH-VALUE SYNONYM LIST
            high_value_synonyms = self._generate_high_value_synonyms(all_jd_text, resume_text)
            result['high_value_synonyms'] = high_value_synonyms
            
            # 7. CAREER OPTIMIZATION SCORE
            skills_in_resume = sum(1 for kw in result['high_demand_skills'] if kw in resume_text)
            total_high_demand = len(result['high_demand_skills'])
            
            if total_high_demand > 0:
                optimization_score = (skills_in_resume / total_high_demand) * 100
                result['career_optimization_score'] = round(optimization_score, 2)
            
            # Add recommendations
            if result['career_optimization_score'] >= 70:
                result['recommendation'] = '✅ Strong alignment with career path - well positioned for target roles'
            elif result['career_optimization_score'] >= 50:
                result['recommendation'] = '⚠️ Moderate alignment - add missing high-demand skills to strengthen position'
            else:
                result['recommendation'] = '❌ Low alignment - focus on acquiring and highlighting key skills from gap report'
                
        except Exception as e:
            result['error'] = f'Error in career path analysis: {str(e)}'
        
        return result
    
    def _generate_high_value_synonyms(self, aggregated_jds: str, resume_text: str) -> List[Dict]:
        """Generate high-impact synonyms to integrate into resume"""
        synonyms = []
        
        # High-value synonym mappings (JD terms → Resume-friendly alternatives)
        synonym_mappings = {
            'leadership': ['led teams', 'managed projects', 'directed initiatives', 'headed department'],
            'development': ['engineered solutions', 'built systems', 'created applications', 'developed platforms'],
            'collaboration': ['cross-functional teamwork', 'partnered with stakeholders', 'collaborated across teams'],
            'innovation': ['drove innovation', 'pioneered solutions', 'implemented cutting-edge', 'introduced novel approaches'],
            'optimization': ['streamlined processes', 'enhanced performance', 'improved efficiency', 'optimized workflows'],
            'scalability': ['scaled systems', 'architected scalable solutions', 'designed for growth'],
            'architecture': ['system design', 'solution architecture', 'technical architecture', 'platform design'],
            'agile': ['agile methodologies', 'scrum practices', 'iterative development', 'sprint planning'],
            'mentorship': ['mentored team members', 'coached developers', 'guided junior engineers'],
            'strategy': ['strategic planning', 'roadmap development', 'vision setting', 'strategic initiatives']
        }
        
        for concept, alternatives in synonym_mappings.items():
            if concept in aggregated_jds:
                # Check if concept or alternatives are missing from resume
                has_concept = concept in resume_text
                has_alternatives = any(alt.lower() in resume_text for alt in alternatives)
                
                if not has_concept and not has_alternatives:
                    synonyms.append({
                        'target_concept': concept.title(),
                        'recommended_phrases': alternatives[:3],
                        'impact': 'HIGH - appears frequently in target roles'
                    })
                elif has_concept and not has_alternatives:
                    synonyms.append({
                        'target_concept': concept.title(),
                        'recommended_phrases': alternatives[:2],
                        'impact': 'MEDIUM - use varied terminology to strengthen'
                    })
        
        return synonyms[:10]  # Top 10 high-value synonyms
