import torch
from transformers import LayoutLMv2Processor, LayoutLMv2ForSequenceClassification
from PIL import Image
import numpy as np
import pytesseract

# Initialize the model and processor with caching
processor = None
model = None

def get_document_ai_models():
    """Get or initialize document AI models with proper caching."""
    global processor, model
    if processor is None:
        processor = LayoutLMv2Processor.from_pretrained("microsoft/layoutlmv2-base-uncased")
    if model is None:
        model = LayoutLMv2ForSequenceClassification.from_pretrained("microsoft/layoutlmv2-base-uncased")
    return processor, model

def extract_text_with_tesseract(image):
    """Extract text using Tesseract OCR."""
    if isinstance(image, np.ndarray):
        pil_image = Image.fromarray(image).convert("RGB")
    else:
        pil_image = image.convert("RGB")
    
    # Use pytesseract for OCR
    text = pytesseract.image_to_string(pil_image)
    
    # Get word boxes for structure
    boxes = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT)
    
    # Extract words and their positions
    words = []
    word_boxes = []
    
    for i in range(len(boxes['text'])):
        if boxes['text'][i].strip() != '':
            words.append(boxes['text'][i])
            x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
            word_boxes.append([x, y, x + w, y + h])
    
    return words, word_boxes

def extract_text_and_layout(image):
    """
    Extract text and layout information using OCR and LayoutLMv2.
    
    Args:
        image: PIL Image object
        
    Returns:
        Dictionary with extracted text and layout information
    """
    # Convert numpy array to PIL Image if needed
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image).convert("RGB")
    
    # Extract text using Tesseract
    words, boxes = extract_text_with_tesseract(image)
    
    # If no words were found, return empty result
    if not words:
        return {
            'words': [],
            'boxes': [],
            'success': False
        }
    
    return {
        'words': words,
        'boxes': boxes,
        'success': True
    }
