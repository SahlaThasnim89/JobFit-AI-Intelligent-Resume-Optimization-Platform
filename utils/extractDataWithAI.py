import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv() 

class JobData(BaseModel):
    job_title: str = Field(
        description="The job title or role being hired for."
    )
    required_skills: List[str] = Field(
        description="List of technical skills required for the job."
    )
    experience_years: Optional[str] = Field(
        description="Years of experience required. e.g. '3+ years'. "
                    "Return 'Not specified' if not mentioned."
    )
    responsibilities: List[str] = Field(
        description="Key responsibilities or duties of the role. "
                    "Maximum 8 items."
    )
    tech_stack: List[str] = Field(
        description="Technologies, frameworks, tools mentioned. "
                    "e.g. Python, React, AWS, Docker."
    )
    seniority_level: Optional[str] = Field(
        description="Seniority level: Junior, Mid, Senior, Lead, or Not specified."
    )


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_job_data(jd_text: str) -> dict:
    prompt = f"""Extract structured information from this job description.
Return ONLY a JSON object with these exact keys:
- company: The name of the hiring organization/company (e.g., look for context clues like 'About CompanyName').
- skills: list of required technical skills
- experience: years of experience required (string)
- keywords: important keywords from the JD
- responsibilities: list of key responsibilities (max 8)
- tech_stack: technologies and tools mentioned
- seniority_level: Junior/Mid/Senior/Lead/Not specified

Job Description:
{jd_text}

Return only the JSON object, no other text."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.1
    )

    text = response.choices[0].message.content
    clean = text.replace("```json", "").replace("```", "").strip()
    data = json.loads(clean)

    return {
        "company":           data.get("company", ""),
        "skills":           data.get("skills", []),
        "experience":       data.get("experience", "Not specified"),
        "keywords":         data.get("keywords", []),
        "responsibilities": data.get("responsibilities", []),
        "tech_stack":       data.get("tech_stack", []),
        "seniority_level":  data.get("seniority_level", "Not specified"),
    }


