# worker.py
import time
import json
from pathlib import Path
from pdf_extractor import extract_target_page

RESULT_DIR = Path("storage/results")

def process_pdf_job(job_id: str, pdf_path: str, phrase: str):
    start = time.perf_counter()

    result = extract_target_page(pdf_path, phrase)

    duration = (time.perf_counter() - start) * 1000

    with open(RESULT_DIR / f"{job_id}.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "job_id": job_id,
                "processing_time_ms": round(duration, 2),
                "result": result
            },
            f,
            ensure_ascii=False,
            indent=2
        )
