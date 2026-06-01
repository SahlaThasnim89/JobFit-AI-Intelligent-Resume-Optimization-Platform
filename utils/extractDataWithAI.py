import os
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional

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


client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def extract_job_data(jd_text: str) -> JobData:
    """
    Extract structured data from a job description using Gemini.
    
    Args:
        jd_text: raw job description text
    
    Returns:
        JobData object with all extracted fields
    """
    prompt = f"""
    Extract structured information from the following job description.
    Be precise and only extract what is explicitly mentioned.
    
    Job Description:
    {jd_text}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": JobData,
        },
    )

    job_data= JobData.model_validate_json(response.text)
    return {
        "skills":           job_data.required_skills,
        "experience":       job_data.experience_years or "Not specified",
        "keywords":         job_data.keywords,
        "responsibilities": job_data.responsibilities,
        "tech_stack":       job_data.tech_stack,
        "seniority_level":  job_data.seniority_level or "Not specified",
    }

# ── Test it ───────────────────────────────────────────────────
if __name__ == "__main__":
    sample_jd = """
    Senior Python Developer — Bengaluru (Hybrid)
    
    We are looking for a Senior Python Developer with 4+ years of experience
    to join our growing team.
    
    Requirements:
    - Strong proficiency in Python and FastAPI
    - Experience with PostgreSQL and Redis
    - Knowledge of Docker and Kubernetes
    - Familiarity with AWS services (EC2, S3, Lambda)
    - Experience with React is a plus
    
    Responsibilities:
    - Design and build scalable REST APIs
    - Collaborate with frontend team on integration
    - Write unit and integration tests
    - Participate in code reviews
    - Deploy and monitor services on AWS
    
    Nice to have: experience with Kafka or RabbitMQ
    """
    
    result = extract_job_data(sample_jd)
    print(result)
