from sqlalchemy import Column,Integer,String,Text,JSON
from db.session import engine
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class Job(Base):
    __tablename__="jobs"

    id=Column(Integer,primary_key=True, index=True)
    company=Column(String)
    job_title=Column(String)
    job_description=Column(Text)
    skills=Column(JSON)
    experience=Column(String)
    keywords=Column(JSON)
    responsibilities=Column(JSON)





