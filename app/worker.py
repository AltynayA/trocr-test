

from pdf_extractor import extract_target_page
from pathlib import Path
import torch
import json

RESULT_DIR = Path("storage/results")
RESULT_DIR.mkdir(parents=True, exist_ok=True)

def process_pdf_job(job_id: str, pdf_path: str, phrase: str):

    try:
        torch.set_num_threads(1)

        result = extract_target_page(
            pdf_path=pdf_path,
            phrase=phrase
        )

        output_path = RESULT_DIR / f"{job_id}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({
                "job_id": job_id,
                "status": "completed",
                "data": result
            }, f, ensure_ascii=False, indent=2)

    except Exception as e:
        error_path = RESULT_DIR / f"{job_id}.json"
        with open(error_path, "w", encoding="utf-8") as f:
            json.dump({
                "job_id": job_id,
                "status": "error",
                "error": str(e)
            }, f, indent=2)
