from fastapi import APIRouter, File, UploadFile
from schemas.job_schema import JobInput,JobProcessed
# from utils.extractData import extract_job_data
from utils.extractDataWithAI import extract_job_data
from services.job_service import save_job
from utils.job_scraper import extract_job_from_url
import traceback

router = APIRouter()

@router.post("/analyze-job-link")
async def analyze_job_link(url:str):
    try:
        scraped=await extract_job_from_url(url)

        extracted=extract_job_data(scraped["description"])

        job_record={
            "company":scraped["company"],
            "job_title":scraped["title"],
            "job_description":scraped["description"],
            "skills":extracted["skills"],
            "experience":extracted["experience"],
            "keywords":extracted["keywords"],
            "responsibilities":extracted["responsibilities"]
        }

        job_id=await save_job(job_record)
        print(job_id)

        return {"message":"Processed", 
                "job_id": job_id,
                "extracted":job_record}

    except Exception as e:
        return {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "trace": traceback.format_exc()
        }


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
async def upload_resume(file: UploadFile = File(...)):
    return {"filename": file.filename,
            "message":"resume uploaded successfully"}


@router.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@router.post("/compute-match")
async def compute_match():
    return {"massage":"resume match analyzed"}