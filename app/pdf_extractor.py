from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from pdf2image import convert_from_path
from pathlib import Path
from PIL import Image
import torch
import json
import re


# lazy model load (only after request)
processor = None
model = None

def load_model():
    global processor, model
    if processor is None or model is None:
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-printed", use_fast=False)
        model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-printed")
        model.eval()
    return processor, model

# normalization layer
def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-zа-я0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# extracting text from a single image 
def extract_text_from_image(image: Image.Image) -> str:
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    with torch.no_grad():
        generated_ids = model.generate(pixel_values)
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]


# converting pdf -> png
def pdf_to_images(pdf_path: str, out_dir: str = "train", dpi: int = 300):
    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    pages = convert_from_path(pdf_path, dpi=dpi)
    png_paths = []

    for i, page in enumerate(pages, start=1):
        png_file = out_dir_path / f"page_{i}.png"
        page.save(png_file, "PNG")
        png_paths.append(png_file)

    return png_paths

# extract page below the phrase
def extract_target_page(pdf_path: str, phrase: str, out_dir="train", dpi=300):
    png_files = pdf_to_images(pdf_path, out_dir, dpi)
    phrase_norm = normalize(phrase)

    for png_file in png_files:
        image = Image.open(png_file).convert("RGB")
        full_text = extract_text_from_image(image)
        # Split into lines (approximate by sentence / periods)
        lines = [l.strip() for l in full_text.split('\n') if l.strip()]
        # lines = [line.strip() for line in full_text.split('.') if line.strip()]
        # Find line containing phrase
        for idx, line in enumerate(lines):
            if phrase_norm in normalize(line):
                # Return PNG path and lines below heading
                return png_file, lines[idx + 1 :]
    return None, []



