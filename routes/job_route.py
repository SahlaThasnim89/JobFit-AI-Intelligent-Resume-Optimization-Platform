from fastapi import APIRouter
from schemas.job_schema import JobInput,JobProcessed
from utils.extractData import extract_job_data
from services.job_service import save_job

router = APIRouter()

@router.post("/analyze-job-link")
async def analyze_job_link(url:str):
    



@router.post("/analyze-job")
async def analyze_job(data:JobInput):

    extracted=extract_job_data(data.job_description)

    job_record={
        "company":data.company,
        "job_title":data.job_title,
        "job_description":data.job_description,
        "skills":extracted["skills"],
        "experience":extracted["experience"],
        "keywords":extracted["keywords"],
        "responsibilities":extracted["responsibilities"]
    }

    job_id=await save_job(job_record)

    return {"message":"Processed", 
            "job_id": job_id,
            "extracted":job_record}


@router.post("/upload-resume")
async def upload_resume(file):
    return {"message":"resume uploaded successfully"}


@router.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@router.post("/compute-match")
async def compute_match():
    return {"massage":"resume match analyzed"}