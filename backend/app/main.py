from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.utils.ocr_utils import process_invoice

app = FastAPI()

# Directories for uploads, outputs, and templates
UPLOAD_DIR = Path("./app/static/uploads")
OUTPUT_DIR = Path("./app/static/outputs")
TEMPLATES_DIR = Path("./app/templates")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Render the file upload form."""
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload/")
async def upload_invoice(file: UploadFile = File(...)):
    """Handle file upload and process OCR."""
    # Save the uploaded image
    if not file.filename.lower().endswith(("png", "jpg", "jpeg")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG, JPG, JPEG allowed.")
    
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Process the invoice
    try:
        text_file = process_invoice(file_path, OUTPUT_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    # Return the text file path
    return FileResponse(path=text_file, media_type="text/plain", filename=text_file.name)
