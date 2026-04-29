import re

SKILL_SET=[
    "python", "java","docker","kubernetes","aws","sql","fastapi","react"
]

def extract_job_data(text:str):
    text_lower=text.lower()

    # Extract skills
    skills=[skill for skill in SKILL_SET if skill in text_lower]

    # Extract experience
    exp_match=re.search(r"\d+\+?\s*(years|yrs)",text_lower)
    experience=exp_match.group(0) if exp_match else "Not specified"

    # keywords (basic)
    words=re.findall(r"\b[a-zA-Z]+\b",text_lower)
    keywords=list(set(words))[:30]

    # Responsibilities (very basic split)
    responsibilities=[line.strip() for line in text.split("\n") if len(line.strip())>20][:10]

    return{
        "skills":skills,
        "experience":experience,
        "keywords":keywords,
        "responsibilities":responsibilities
    }