
import re
import numpy as np
from pathlib import Path
import easyocr
from pdf2image import convert_from_path
import os
from PIL import Image


# global reader
reader = easyocr.Reader(["ru"], gpu=False)

# Normalization
def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-zа-я0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# PDF -> images
def pdf_to_images(pdf_path: str, out_dir="pages", dpi=150):
    os.makedirs(out_dir, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=dpi)

    png_files = []
    for i, page in enumerate(pages):
        png_path = Path(out_dir) / f"page_{i + 1}.png"
        page.save(png_path, "PNG")
        png_files.append(png_path)

    return png_files


# Extract target page and text below phrase
def extract_target_page(pdf_path: str, phrase: str, out_dir="pages", dpi=150):
    phrase_norm = normalize(phrase)
<<<<<<< HEAD
    # reader = easyocr.Reader(['ru, 'kz])
=======
>>>>>>> 2f0c3951e645b3df5c5c83faec8f330af8f86059
    png_files = pdf_to_images(pdf_path, out_dir, dpi)

    for png_file in png_files:
        with Image.open(png_file) as img:
            img = img.convert("L")
            w, h = img.size
            if w > 1024:
                img = img.resize((1024, int(h * 1024 / w)))
            img_np = np.array(img)

            lines = reader.readtext(img_np, detail=0)

        norm_lines = [normalize(l) for l in lines if l.strip()]

        for i, line in enumerate(norm_lines):
            if phrase_norm in line:
                return [{
                    "page": str(png_file),
                    "text_below_phrase": " ".join(norm_lines[i + 1:])
                }]

    return []

