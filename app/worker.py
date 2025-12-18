import time
import json
from pathlib import Path
from pdf_extractor import extract_target_page

RESULT_DIR = Path("storage/results")

def process_pdf_job(job_id: str, pdf_path: str, phrase: str):
<<<<<<< HEAD
    # job start
    total_start = time.perf_counter()

    # pdf_start = time.perf_counter()
    result = extract_target_page(pdf_path, phrase)
    # pdf_duration = (time.perf_counter() - pdf_start) * 1000


    total_duration = (time.perf_counter() - total_start) * 1000
=======
    start = time.perf_counter()

    result = extract_target_page(pdf_path, phrase)

    duration = (time.perf_counter() - start) * 1000
>>>>>>> 2f0c3951e645b3df5c5c83faec8f330af8f86059

    with open(RESULT_DIR / f"{job_id}.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "job_id": job_id,
<<<<<<< HEAD
                "result": result,
                # "pdf_processing_time_ms": round(pdf_duration, 2),
                "total_processing_time_ms": round(total_duration, 2)
=======
                "job_processing_time_ms": round(duration, 2),
                "result": result
>>>>>>> 2f0c3951e645b3df5c5c83faec8f330af8f86059
            },
            f,
            ensure_ascii=False,
            indent=2
        )
<<<<<<< HEAD
    print(f"[INFO] Job {job_id} processed. Total time: {round(total_duration, 2)} ms")
=======
>>>>>>> 2f0c3951e645b3df5c5c83faec8f330af8f86059
