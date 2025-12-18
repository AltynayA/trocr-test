from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException, Form, File
from pathlib import Path
import uuid
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pdf_extractor import extract_target_page

from worker import process_pdf_job

app = FastAPI()
@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{duration:.2f}"
    print(f"{request.method} {request.url.path} took {duration:.2f} ms")
    return response

UPLOAD_DIR = Path("storage/uploads")
RESULT_DIR = Path("storage/results")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

# loading the model to thread
executor = ThreadPoolExecutor(max_workers=2)

def run_in_executor(job_id: str, pdf_path: str, phrase: str):
    # wrapper to run OCR in separate thread
    executor.submit(process_pdf_job, job_id, pdf_path, phrase)
# upload pdf
@app.post("/upload-pdf")

async def upload_pdf(
    file: UploadFile = File(...),
    phrase: str = Form(...),
    # default argument
    background_tasks: BackgroundTasks = None,
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF only")

    job_id = str(uuid.uuid4())
    pdf_path = UPLOAD_DIR / f"{job_id}.pdf"

    # save uploaded PDF
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Run OCR in background (non blocking)
    background_tasks.add_task(
        process_pdf_job,
        job_id,
        str(pdf_path),
        phrase
    )

    return {
        "job_id": job_id,
        "status": "processing"
    }


# get by ID 
@app.get("/result/{job_id}")
def get_result(job_id: str):
    result_file = RESULT_DIR / f"{job_id}.json"
    

    if not result_file.exists():
        return {"status": "pending"}

    with open(result_file, "r", encoding="utf-8") as f:
        return json.load(f)