import pytesseract
from PIL import Image
import cv2
from pathlib import Path

# Configuration for pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this path if necessary

def preprocess_image(image_path):
    """
    Preprocess the image for better OCR results.
    """
    # Read image with OpenCV
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # Save processed image temporarily
    processed_path = image_path.parent / f"{image_path.stem}_processed.png"
    cv2.imwrite(str(processed_path), thresh)
    return processed_path

def process_invoice(image_path, output_dir):
    """
    Process the invoice image and save the OCR text in a .txt file.
    """
    # Preprocess image
    processed_path = preprocess_image(image_path)

    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(Image.open(processed_path))

    # Create a text file to save the OCR output
    output_file = output_dir / f"{image_path.stem}_output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    # Clean up temporary files
    processed_path.unlink()

    return output_file
