import re
import os
import numpy as np
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import easyocr


reader = easyocr.Reader(["en"], gpu=False)


def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def extract_numbers(text: str):
    return re.findall(r"\d+(?:\.\d+)?", text)


def pdf_to_images(pdf_path: str, out_dir="pages", dpi=150):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pages = convert_from_path(pdf_path, dpi=dpi)
    paths = []

    for i, page in enumerate(pages, start=1):
        p = out_dir / f"page_{i}.png"
        page.save(p, "PNG")
        paths.append(p)

    return paths


def extract_table_numbers(pdf_path: str, header_phrase: str, dpi=150):
    header_norm = normalize(header_phrase)
    pages = pdf_to_images(pdf_path, dpi=dpi)

    for page_path in pages:
        with Image.open(page_path) as img:
            img = img.convert("L")
            w, h = img.size
            if w > 1200:
                img = img.resize((1200, int(h * 1200 / w)))
            img_np = np.array(img)

        # OCR с bbox
        results = reader.readtext(img_np, detail=1)

        header_y = None

        # 1️⃣ ищем заголовок
        for bbox, text, conf in results:
            if header_norm in normalize(text):
                header_y = min(p[1] for p in bbox)
                break

        if header_y is None:
            continue

        # 2️⃣ всё что ниже заголовка
        table_text = []
        numbers = []

        for bbox, text, conf in results:
            y = min(p[1] for p in bbox)
            if y > header_y + 10:  # небольшой отступ
                table_text.append(text)
                numbers.extend(extract_numbers(text))

        return {
            "page": str(page_path),
            "numbers": numbers,
            "raw_rows": table_text
        }

    return {
        "page": None,
        "numbers": [],
        "raw_rows": []
    }
