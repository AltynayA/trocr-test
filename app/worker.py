
from pdf_extractor import extract_target_page

from pathlib import Path
import json

RESULT_DIR = Path("storage/results")
RESULT_DIR.mkdir(parents=True, exist_ok=True)

def process_pdf_job(job_id: str, pdf_path: str, phrase: str):
    target_png, lines_below = extract_target_page(pdf_path, phrase)
    results = {
        "job_id": job_id,
        "target_page": str(target_png) if target_png else None,
        "lines_below_heading": lines_below
    }

    output_path = RESULT_DIR / f"{job_id}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
