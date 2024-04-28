from fastapi import FastAPI
from transformers import AutoProcessor, UdopForConditionalGeneration
from pydantic import BaseModel
from datasets import load_dataset
import pytesseract
from pdf2image import convert_from_bytes


processor = AutoProcessor.from_pretrained("microsoft/udop-large", apply_ocr=True)
model = UdopForConditionalGeneration.from_pretrained("microsoft/udop-large")

dataset = load_dataset("nielsr/funsd-layoutlmv3", split="train")
example = dataset[0]
image = example["image"]

path = r'C:\Users\Karl\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = path

class datainput(BaseModel):
    question: str
    image: str

app = FastAPI()

@app.post("/answer")
def make_answer(data: datainput):
    data = dict(data)
    image = convert_from_bytes(data['image'].encode('latin-1'), poppler_path=r'C:\Users\Karl\Code\poppler\poppler-24.02.0\Library\bin')[0]
    encoding = processor(image, data['question'], return_tensors="pt")
    predicted_ids = model.generate(**encoding)
    prediction = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return {'prediction': prediction}

