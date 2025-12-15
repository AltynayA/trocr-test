from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException, Form, File
from pathlib import Path
import uuid
import json
from pdf_extractor import extract_target_page

from worker import process_pdf_job

app = FastAPI()


UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# upload pdf
@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile,
    phrase: str = Form(...),
    # default argument
    background_tasks: BackgroundTasks = None,


):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF only")

    job_id = str(uuid.uuid4())
    pdf_path = UPLOAD_DIR / f"{job_id}.pdf"

    # Save uploaded PDF
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Run OCR in background
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
    result_file = Path("storage/results") / f"{job_id}.json"
    if not result_file.exists():
        return {"status": "pending"}
    import json
    with open(result_file, "r", encoding="utf-8") as f:
        return json.load(f)