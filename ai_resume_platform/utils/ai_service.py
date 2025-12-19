import requests
import json
import os
from django.conf import settings

class AIService:
    """
    Service class to handle AI API calls
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
        self.base_url = 'https://openrouter.ai/api/v1/chat/completions'
        
    def analyze_resume_from_url(self, resume_url):
        """
        Analyze a resume from a Cloudinary URL and provide comprehensive feedback
        """
        prompt = f"""
Analyze the resume available at this public URL:

RESUME_URL: {resume_url}

IMPORTANT:
- The resume is a PDF.
- You must analyze content ONLY from this resume.
- Do NOT assume missing information.
- Be precise and professional.

Follow these definitions strictly:

STRENGTHS:
- Skills, technologies, or keywords repeated multiple times
- Clear achievements and impact
- Strong formatting, structure, grammar
- Role-relevant experience

WEAKNESSES:
- Content that exists but is:
  • Generic
  • Weakly worded
  • Outdated
  • Irrelevant to modern roles
  • Overused without impact

MISSING / IMPROVEMENTS:
- Important things NOT present:
  • Missing skills
  • Missing metrics
  • Missing industry keywords
  • Missing action verbs
  • Missing clarity or structure

Return your response in STRICT JSON format:

{{
  "ats_score": number (0-100),
  "summary": "short professional summary of the resume's overall impression",
  "strengths": [ "point 1", "point 2", "point 3", "point 4", "point 5" ],
  "weaknesses": [ "point 1", "point 2", "point 3", "point 4", "point 5" ],
  "missing_elements": [ "point 1", "point 2", "point 3", "point 4", "point 5" ],
  "best_programming_languages": [ "language 1", "language 2", "language 3" ],
  "industry_scores": {{
    "Software Development": number,
    "Data Science": number,
    "AI / ML": number,
    "IT / Support": number,
    "Management": number
  }},
  "suggestions": [ "suggestion 1", "suggestion 2", "suggestion 3" ]
}}

Do NOT include explanations.
Do NOT include markdown.
Return ONLY valid JSON.
        """
        
        return self._call_ai_api(prompt)
    
    def match_job_from_url(self, resume_url, job_details):
        """
        Match a resume from a Cloudinary URL against job details
        """
        # Format job information
        job_title = job_details.get('title', '')
        company = job_details.get('company', 'Not specified')
        job_level = job_details.get('level', 'Not specified')
        salary = job_details.get('salary', 'Not specified')
        job_description = job_details.get('description', '')
        
        prompt = f"""
You are an ATS Job Matching Engine.

Analyze the resume at this URL:

RESUME_URL: {resume_url}

Compare it with the following job:

Job Title: {job_title}
Company: {company}
Experience Level: {job_level}
Salary (if provided): {salary}
Job Description:
{job_description}

Rules:
- Do NOT rewrite the resume
- Do NOT assume skills not mentioned
- Match strictly based on resume content

Return STRICT JSON:

{{
  "match_percentage": number (0-100),
  "summary_overview": "short match summary",
  "strength_alignment": [ "point 1", "point 2", "point 3" ],
  "missing_skills": [ "skill 1", "skill 2", "skill 3", "skill 4" ],
  "final_verdict": "one-line hiring recommendation"
}}

Return ONLY JSON.
No markdown.
No explanations.
        """
        
        return self._call_ai_api(prompt)
    
    def analyze_resume(self, resume_text):
        """
        Analyze a resume and provide feedback
        """
        prompt = f"""
        Please analyze the following resume and provide detailed feedback:
        
        Resume Content:
        {resume_text}
        
        Please provide:
        1. An ATS compatibility score (0-100)
        2. Key strengths of the resume
        3. Areas for improvement
        4. Specific suggestions for enhancement
        
        Format your response as JSON with the following structure:
        {{
            "ats_score": 85,
            "strengths": ["strength1", "strength2"],
            "weaknesses": ["weakness1", "weakness2"],
            "suggestions": ["suggestion1", "suggestion2"]
        }}
        """
        
        return self._call_ai_api(prompt)
    
    def match_job(self, resume_text, job_description):
        """
        Match a resume against a job description
        """
        prompt = f"""
        Please match the following resume against the job description and provide detailed feedback:
        
        Resume Content:
        {resume_text}
        
        Job Description:
        {job_description}
        
        Please provide:
        1. A match score (0-100)
        2. Skills that match
        3. Skills that are missing
        4. Recommendations for improvement
        
        Format your response as JSON with the following structure:
        {{
            "match_score": 78,
            "matched_skills": ["skill1", "skill2"],
            "missing_skills": ["skill3", "skill4"],
            "recommendations": ["recommendation1", "recommendation2"]
        }}
        """
        
        return self._call_ai_api(prompt)
    
    def generate_resume(self, user_info, target_job, industry, experience_level):
        """
        Generate a resume based on user information and target job
        """
        prompt = f"""
        Please generate a professional resume based on the following information:
        
        User Information:
        Name: {user_info.get('name', '')}
        Email: {user_info.get('email', '')}
        Phone: {user_info.get('phone', '')}
        
        Target Job: {target_job}
        Industry: {industry}
        Experience Level: {experience_level}
        
        Please provide a complete resume in JSON format with the following structure:
        {{
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1 (555) 123-4567",
            "summary": "Professional summary...",
            "experience": [
                {{
                    "title": "Job Title",
                    "company": "Company Name",
                    "duration": "2020 - Present",
                    "description": "Job description..."
                }}
            ],
            "education": [
                {{
                    "degree": "Degree Name",
                    "school": "School Name",
                    "year": "2020"
                }}
            ],
            "skills": ["skill1", "skill2", "skill3"]
        }}
        """
        
        return self._call_ai_api(prompt)
    
    def plan_career_from_url(self, resume_url, user_inputs):
        """
        Provide skill development and learning plan based on resume and user inputs
        """
        career_goal = user_inputs.get('career_goal', '')
        timeframe = user_inputs.get('timeframe', '')
        preferred_industry = user_inputs.get('preferred_industry', '')
        current_skill_level = user_inputs.get('current_skill_level', '')
        learning_commitment = user_inputs.get('learning_commitment', '')
        target_outcome = user_inputs.get('target_outcome', '')
        
        prompt = f"""
You are a Career Mentor, Skill Strategist, and Personal Growth Coach.

Analyze the resume available at this URL:

RESUME_URL: {resume_url}

User Goal Details:
- Career Aim / Goal: {career_goal}
- Target Timeframe: {timeframe}
- Preferred Industry or Domain: {preferred_industry}
- Current Skill Level (Beginner / Intermediate / Advanced): {current_skill_level}
- Learning Commitment (hours per week): {learning_commitment}
- Target Outcome (role, skill mastery, startup, freelancing, higher studies, etc.): {target_outcome}

IMPORTANT RULES:
- ❌ Do NOT suggest job titles
- ❌ Do NOT suggest companies
- ❌ Do NOT suggest job switching
- ❌ Do NOT generate career roles

You must ONLY:
- Focus on **what the user should DO**
- Provide **skills, learning steps, habits, projects, certifications**
- Base everything strictly on resume content + user inputs
- Be realistic with timeframe
- Do NOT exaggerate abilities

---

OUTPUT FORMAT (STRICT JSON ONLY)

{{
  "goal_clarity": "Short explanation of how realistic the goal is based on resume",
  
  "skill_gap_analysis": [
    "Missing or weak skill 1",
    "Missing or weak skill 2",
    "Missing or weak skill 3"
  ],

  "learning_roadmap": [
    {{
      "phase": "Phase 1 (0–X months)",
      "focus": "Main focus area",
      "actions": [
        "Action 1",
        "Action 2",
        "Action 3"
      ]
    }},
    {{
      "phase": "Phase 2 (X–Y months)",
      "focus": "Main focus area",
      "actions": [
        "Action 1",
        "Action 2",
        "Action 3"
      ]
    }}
  ],

  "projects_to_build": [
    "Project idea 1",
    "Project idea 2",
    "Project idea 3"
  ],

  "daily_weekly_habits": [
    "Daily habit 1",
    "Weekly habit 2",
    "Practice routine"
  ],

  "recommended_certifications": [
    "Certification 1 (if useful)",
    "Certification 2 (optional)"
  ],

  "final_guidance": "Encouraging but practical closing advice"
}}

---

RESPONSE RULES
- Return ONLY valid JSON
- No markdown
- No explanations
- No job titles
- No company names
- No extra text
        """
        
        return self._call_ai_api(prompt)
    
    def match_job_from_url(self, resume_url, job_details):
        """
        Match a resume against a job description using URLs
        """
        job_title = job_details.get('title', '')
        company = job_details.get('company', 'Not specified')
        job_level = job_details.get('level', 'Not specified')
        salary = job_details.get('salary', 'Not specified')
        job_description = job_details.get('description', '')
        
        prompt = f"""
You are an ATS Job Matching Engine.

Analyze the resume at this URL:
RESUME_URL: {resume_url}

Compare it with the following job:
Job Title: {job_title}
Company: {company}
Experience Level: {job_level}
Salary (if provided): {salary}
Job Description: {job_description}

Rules:
- Do NOT rewrite the resume
- Do NOT assume skills not mentioned
- Match strictly based on resume content

Return STRICT JSON:
{{
  "match_percentage": number (0-100),
  "summary_overview": "short match summary",
  "strength_alignment": [ "point 1", "point 2", "point 3" ],
  "missing_skills": [ "skill 1", "skill 2", "skill 3", "skill 4" ],
  "final_verdict": "one-line hiring recommendation"
}}

Return ONLY JSON. No markdown. No explanations.
        """
        
        return self._call_ai_api(prompt)
    
    def _call_ai_api(self, prompt):
        """
        Internal method to call the AI API
        """
        if not self.api_key or self.api_key == 'your-openrouter-api-key':
            return {"error": "API key not configured. Please update your .env file with a valid OpenRouter API key."}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Resume Analyzer"
        }
        
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an expert career advisor and resume consultant. Always respond with valid JSON only, no markdown, no explanations."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
            "response_format": { "type": "json_object" }
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # Extract the content from the response
            content = result['choices'][0]['message']['content']
            
            # Try to parse as JSON
            try:
                parsed_data = json.loads(content)
                return parsed_data
            except json.JSONDecodeError:
                # If not JSON, return error with response preview
                return {"error": f"AI response was not valid JSON. Response preview: {content[:200]}..."}
                
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. The AI service took too long to respond."}
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except KeyError as e:
            return {"error": f"Unexpected API response format: {str(e)}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
    
    def generate_optimized_resume(self, resume_url, user_inputs):
        """
        Generate an optimized resume based on existing resume and user inputs
        """
        template_type = user_inputs.get('template_type', '')
        target_company = user_inputs.get('target_company', '')
        target_job_role = user_inputs.get('target_job_role', '')
        job_description = user_inputs.get('job_description', '')
        skills_to_highlight = user_inputs.get('skills_to_highlight', '')
        projects = user_inputs.get('projects', '')
        achievements = user_inputs.get('achievements', '')
        experience_level = user_inputs.get('experience_level', '')
        additional_notes = user_inputs.get('additional_notes', '')
        
        prompt = f"""
You are given an EXISTING resume available at this public URL:

RESUME_URL: {resume_url}

Your task is to:

1. Analyze the existing resume
2. Improve and rewrite it
3. Align it strictly with the provided Job Description
4. Structure it for a FINAL PDF resume using a named design template

--------------------------------------------------

USER INPUTS

--------------------------------------------------

Resume Design Template:
{template_type}

(Available templates:
Cosmic, Nebula, Lunar, Eclipse, Eon, Orion, Nova, Stellar, Quantum)

Target Company:
{target_company}

Target Job Role:
{target_job_role}

Job Description:
{job_description}

Skills to Emphasize:
{skills_to_highlight}

Projects:
{projects}

Achievements:
{achievements}

Experience Level:
{experience_level}

Additional Notes:
{additional_notes}

--------------------------------------------------

TEMPLATE DESIGN BEHAVIOR (IMPORTANT)

--------------------------------------------------

Each template affects ONLY visual structure, NOT content truth:

Cosmic → Modern, bold section headers, strong hierarchy  
Nebula → Creative but ATS-safe, soft emphasis, balanced spacing  
Lunar → Minimal, clean, recruiter-first  
Eclipse → Executive, sharp impact bullets  
Eon → Timeline-focused, growth-oriented  
Orion → Technical-heavy, skill-forward  
Nova → Fresh graduate / early career  
Stellar → Leadership & achievement-driven  
Quantum → Data & metrics-oriented  

You must:
- Keep content ATS-compliant
- Avoid tables or graphics that break ATS parsing
- Structure content so it can be rendered into PDF cleanly

--------------------------------------------------

STRICT CONTENT RULES (MANDATORY)

--------------------------------------------------

1. Use ONLY information from:
   - Existing resume
   - User-provided inputs
2. You MAY:
   - Rewrite bullets
   - Improve clarity
   - Add strong action verbs
   - Align wording with job description keywords
3. You MUST NOT:
   - Add fake companies or roles
   - Add fake experience
   - Add fake certifications
   - Invent metrics
4. Do NOT hallucinate achievements.
5. Ensure the resume is truthful, professional, and realistic.

--------------------------------------------------

WHAT YOU MUST DELIVER

--------------------------------------------------

- A fully updated resume aligned to the job description
- ATS-optimized wording and structure
- Template-aware organization
- Content that can be directly converted into a PDF
- FINAL output represents the completed resume

--------------------------------------------------

OUTPUT FORMAT (STRICT JSON ONLY)

--------------------------------------------------

{{
  "pdf_resume": {{
    "template_used": "{template_type}",

    "header": {{
      "name": "Use name from existing resume",
      "title": "Optimized professional title aligned with job role",
      "summary": "3–4 line ATS-optimized professional summary tailored to the job"
    }},

    "skills": [
      "Skill 1",
      "Skill 2",
      "Skill 3"
    ],

    "experience": [
      {{
        "company": "",
        "role": "",
        "duration": "",
        "bullets": [
          "Impact-focused bullet aligned with job description",
          "Action-oriented achievement",
          "Keyword-optimized responsibility"
        ]
      }}
    ],

    "projects": [
      {{
        "name": "",
        "description": "Result-oriented project description aligned to job needs"
      }}
    ],

    "education": [
      {{
        "degree": "",
        "institution": "",
        "year": ""
      }}
    ],

    "certifications": [
      "Only include if already present in original resume"
    ]
  }}
}}

--------------------------------------------------

FINAL CONSTRAINTS

--------------------------------------------------

- Return ONLY valid JSON
- No markdown
- No explanations
- No commentary
- No extra keys
- This output will be converted into a FINAL PDF resume

🔥 WHAT THIS ENABLES IN YOUR APP

✔ Resume is checked & improved automatically
✔ Resume is tailored per job description
✔ User selects Cosmic / Nebula / Lunar / Eclipse / Eon etc.
✔ Resume becomes PDF-only final output
✔ ATS-safe + visually distinctive
✔ Zero hallucination risk

🔧 FRONTEND → BACKEND FLOW

User selects template

User fills job details

Backend fetches resume URL

Prompt sent to AI

JSON parsed

Tailwind template renders layout

HTML → PDF

User downloads PDF
        """
        
        return self._call_ai_api(prompt)