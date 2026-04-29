from pydantic import BaseModel

class JobInput(BaseModel):
    company:str
    job_title:str
    job_description:str


class JobProcessed(BaseModel):
    company:str
    job_title:str
    job_description:str
    skills:list[str]
    experience:str
    keywords:list[str]
    responsibilities:list[str]