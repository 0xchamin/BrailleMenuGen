from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import json

# Model ID for a smaller model suitable for Spaces
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
FALLBACK_MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"

# Initialize with None - will be loaded on first use
tokenizer = None
text_generation_pipeline = None

def get_text_pipeline():
    """
    Initialize or return the text generation pipeline.
    Uses smaller models that work well on Spaces.
    """
    global tokenizer, text_generation_pipeline
    
    if text_generation_pipeline is None:
        try:
            # Try to load primary model
            tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
            
            # Use 8-bit quantization to reduce memory usage
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID, 
                device_map="auto",
                torch_dtype=torch.float16,
                load_in_8bit=True
            )
            
            # Create the pipeline
            text_generation_pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=1024,
                do_sample=True,
                temperature=0.3,
                top_p=0.95,
                repetition_penalty=1.15
            )
            
        except Exception as e:
            print(f"Error loading primary model: {str(e)}")
            print(f"Falling back to {FALLBACK_MODEL_ID}")
            
            try:
                # Fall back to Mistral model which is more widely available
                tokenizer = AutoTokenizer.from_pretrained(FALLBACK_MODEL_ID)
                model = AutoModelForCausalLM.from_pretrained(
                    FALLBACK_MODEL_ID,
                    device_map="auto",
                    torch_dtype=torch.float16,
                    load_in_8bit=True
                )
                
                text_generation_pipeline = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_new_tokens=1024,
                    do_sample=True,
                    temperature=0.3,
                    top_p=0.95,
                    repetition_penalty=1.15
                )
            except Exception as e2:
                print(f"Error loading fallback model: {str(e2)}")
                return None
    
    return text_generation_pipeline

def process_menu_text(raw_text):
    """
    Process raw OCR text using LLM to improve structure and readability.
    
    Args:
        raw_text: Raw text extracted from menu image
        
    Returns:
        Processed and structured menu text
    """
    # Get the pipeline
    pipeline = get_text_pipeline()
    
    if pipeline is None:
        # Fallback to simple processing if model not available
        return {
            'structured_text': raw_text,
            'menu_sections': [],
            'success': False,
            'error': "LLM model not available"
        }
    
    # Construct prompt for the LLM
    prompt = f"""<|system|>
You are an AI assistant that helps structure menu text from OCR.
Your task is to clean up the text, correct obvious OCR errors, and structure it properly.
Identify menu sections, items, and prices.
Format your response as JSON with menu sections, items, and prices.
<|user|>
Here is the raw text extracted from a menu image:

{raw_text}

Please clean and structure this menu text. Format your response as JSON with the following structure:
{{
    "menu_sections": [
        {{
            "section_name": "Section name (e.g., Appetizers, Main Course, etc.)",
            "items": [
                {{
                    "name": "Item name",
                    "description": "Item description if available",
                    "price": "Price if available"
                }}
            ]
        }}
    ]
}}
<|assistant|>
"""
    
    try:
        # Generate response from LLM
        response = pipeline(prompt, return_full_text=False)[0]['generated_text']
        
        # Extract JSON from response
        response_text = response.strip()
        
        # Find JSON in the response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            menu_data = json.loads(json_str)
            
            # Reconstruct structured text
            structured_text = ""
            for section in menu_data.get('menu_sections', []):
                structured_text += f"{section.get('section_name', 'Menu Items')}\n"
                structured_text += "-" * len(section.get('section_name', 'Menu Items')) + "\n\n"
                
                for item in section.get('items', []):
                    structured_text += f"{item.get('name', '')}"
                    if item.get('price'):
                        structured_text += f" - {item.get('price')}"
                    structured_text += "\n"
                    
                    if item.get('description'):
                        structured_text += f"  {item.get('description')}\n"
                    
                    structured_text += "\n"
                
                structured_text += "\n"
            
            return {
                'structured_text': structured_text,
                'menu_data': menu_data,
                'success': True
            }
        else:
            # Fallback to simple processing
            return {
                'structured_text': raw_text,
                'menu_sections': [],
                'success': False,
                'error': "Failed to parse LLM response as JSON"
            }
            
    except Exception as e:
        return {
            'structured_text': raw_text,
            'menu_sections': [],
            'success': False,
            'error': str(e)
        }
