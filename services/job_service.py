from models.job_model import Job
from db.session import AsyncSessionLocal

async def save_job(job_record):
    async with AsyncSessionLocal() as session:
        new_job=Job(**job_record)

        session.add(new_job)
        await session.commit()
        await session.refresh(new_job)

        return new_job.id

