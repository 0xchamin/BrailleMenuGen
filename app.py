import gradio as gr
import numpy as np
from PIL import Image
import io
import base64

# Import our custom modules
from utils.image_preprocessing import preprocess_image
from models.document_ai import extract_text_and_layout
from models.text_processor import process_menu_text
from models.braille_translator import text_to_braille, get_braille_metadata
from utils.pdf_generator import create_braille_pdf, create_braille_pdf_with_comparison


def generate_pdf(original_text, braille_text, title, comparison=False):
    """Generate a PDF file with Braille content."""
    try:
        if comparison:
            pdf_buffer = create_braille_pdf_with_comparison(original_text, braille_text, title)
        else:
            pdf_buffer = create_braille_pdf(original_text, braille_text, title)
        
        return pdf_buffer
    except Exception as e:
        print(f"Error in generate_pdf: {str(e)}")
        raise

# Function to create a download link for a PDF
def generate_pdf1(original_text, braille_text, title, comparison=False):
    """Generate a PDF file with Braille content."""
    if comparison:
        pdf_buffer = create_braille_pdf_with_comparison(original_text, braille_text, title)
    else:
        pdf_buffer = create_braille_pdf(original_text, braille_text, title)
    
    return pdf_buffer

def process_image_v2(image, use_llm, use_context):
    """Process the uploaded image and generate results."""
    if image is None:
        return "Please upload an image first.", "", "", None
    
    # Convert to PIL Image if needed
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    
    # Preprocess the image
    preprocessed_img = preprocess_image(image)
    
    # Extract text using document AI
    try:
        result = extract_text_and_layout(preprocessed_img)
        
        if not result.get('words', []):
            return "No text was extracted from the image.", "", "", None
        
        raw_text = ' '.join(result['words'])
        
        # Process text with LLM if enabled
        if use_llm:
            processed_result = process_menu_text(raw_text)
            
            if processed_result['success']:
                processed_text = processed_result['structured_text']
            else:
                processed_text = raw_text
        else:
            processed_text = raw_text
        
        # Translate to Braille
        braille_result = text_to_braille(processed_text, use_context=use_context)
        
        if not braille_result['success']:
            return processed_text, "", "Braille translation failed.", None
        
        braille_text = braille_result['formatted_braille']
        
        # Generate metadata
        metadata = get_braille_metadata(processed_text)
        metadata_text = f"Translation contains {metadata['word_count']} words, {metadata['character_count']} characters, {metadata['line_count']} lines."
        
        # Store both Unicode and ASCII versions for later use
        state_data = {
            'original_text': processed_text,
            'braille_text': braille_text,
            'ascii_braille': braille_result.get('formatted_ascii', '')
        }
        
        # Return results
        return processed_text, braille_text, metadata_text, state_data
    
    except Exception as e:
        return f"Error processing image: {str(e)}", "", "", None


def process_image(image, use_llm, use_context):
    """Process the uploaded image and generate results."""
    if image is None:
        return "Please upload an image first.", "", "", None
    
    # Convert to PIL Image if needed
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    
    # Preprocess the image
    preprocessed_img = preprocess_image(image)
    
    # Extract text using document AI
    try:
        result = extract_text_and_layout(preprocessed_img)
        
        if not result.get('words', []):
            return "No text was extracted from the image.", "", "", None
        
        raw_text = ' '.join(result['words'])
        
        # Process text with LLM if enabled
        if use_llm:
            processed_result = process_menu_text(raw_text)
            
            if processed_result['success']:
                processed_text = processed_result['structured_text']
            else:
                processed_text = raw_text
        else:
            processed_text = raw_text
        
        # Translate to Braille
        braille_result = text_to_braille(processed_text, use_context=use_context)
        
        if not braille_result['success']:
            return processed_text, "", "Braille translation failed.", None
        
        braille_text = braille_result['formatted_braille']
        
        # Generate metadata
        metadata = get_braille_metadata(processed_text)
        metadata_text = f"Translation contains {metadata['word_count']} words, {metadata['character_count']} characters, {metadata['line_count']} lines."
        
        # Return results
        return processed_text, braille_text, metadata_text, (processed_text, braille_text)
    
    except Exception as e:
        return f"Error processing image: {str(e)}", "", "", None


def create_pdf_v2(state, pdf_title, pdf_type):
    """Create a PDF file for download."""
    if state is None:
        return None
    
    # Extract data from state
    try:
        original_text = state['original_text']
        ascii_braille = state['ascii_braille']
        
        # If ASCII version is not available, use the Unicode version
        if not ascii_braille:
            ascii_braille = state['braille_text']
    except:
        # Fallback for backward compatibility
        if isinstance(state, tuple) and len(state) == 2:
            original_text, braille_text = state
            ascii_braille = braille_text
        else:
            return None
    
    comparison = (pdf_type == "Side-by-Side Comparison")
    
    try:
        pdf_buffer = generate_pdf(original_text, ascii_braille, pdf_title, comparison)
        
        # Create a temporary file to save the PDF
        temp_file_path = f"/tmp/{pdf_title.replace(' ', '_').lower()}.pdf"
        
        # Write the buffer to a file
        with open(temp_file_path, "wb") as f:
            f.write(pdf_buffer.getvalue())
        
        return temp_file_path
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None

def create_pdf(state, pdf_title, pdf_type):
    """Create a PDF file for download."""
    if state is None:
        return None
    
    # Extract data from state
    try:
        original_text = state['original_text']
        braille_text = state['braille_text']  # Use Unicode Braille text
    except:
        # Fallback for backward compatibility
        if isinstance(state, tuple) and len(state) == 2:
            original_text, braille_text = state
        else:
            return None
    
    comparison = (pdf_type == "Side-by-Side Comparison")
    
    try:
        pdf_buffer = generate_pdf(original_text, braille_text, pdf_title, comparison)
        
        # Create a temporary file to save the PDF
        temp_file_path = f"/tmp/{pdf_title.replace(' ', '_').lower()}.pdf"
        
        # Write the buffer to a file
        with open(temp_file_path, "wb") as f:
            f.write(pdf_buffer.getvalue())
        
        return temp_file_path
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None

def create_pdf_v1_working(state, pdf_title, pdf_type):
    """Create a PDF file for download."""
    if state is None or len(state) != 2:
        return None
    
    original_text, braille_text = state
    
    # Get ASCII representation for PDF
    try:
        braille_result = text_to_braille(original_text, use_context=False)
        ascii_braille = braille_result.get('formatted_ascii', braille_text)
    except:
        ascii_braille = braille_text
    
    comparison = (pdf_type == "Side-by-Side Comparison")
    
    try:
        pdf_buffer = generate_pdf(original_text, ascii_braille, pdf_title, comparison)
        
        # Create a temporary file to save the PDF
        temp_file_path = f"/tmp/{pdf_title.replace(' ', '_').lower()}.pdf"
        
        # Write the buffer to a file
        with open(temp_file_path, "wb") as f:
            f.write(pdf_buffer.getvalue())
        
        return temp_file_path
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None

def create_pdf2(state, pdf_title, pdf_type):
    """Create a PDF file for download."""
    if state is None or len(state) != 2:
        return None
    
    original_text, braille_text = state
    comparison = (pdf_type == "Side-by-Side Comparison")
    
    try:
        pdf_buffer = generate_pdf(original_text, braille_text, pdf_title, comparison)
        
        # Create a temporary file to save the PDF
        temp_file_path = f"/tmp/{pdf_title.replace(' ', '_').lower()}.pdf"
        
        # Write the buffer to a file
        with open(temp_file_path, "wb") as f:
            f.write(pdf_buffer.getvalue())
        
        return temp_file_path
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None


def create_pdf1(state, pdf_title, pdf_type):
    """Create a PDF file for download."""
    if state is None or len(state) != 2:
        return None
    
    original_text, braille_text = state
    comparison = (pdf_type == "Side-by-Side Comparison")
    
    pdf_buffer = generate_pdf(original_text, braille_text, pdf_title, comparison)
    
    # Return the file for download
    return pdf_buffer

# Create the Gradio interface
with gr.Blocks(title="English Menu to Braille Menu Converter") as demo:
    gr.Markdown("# English Menu to Braille Menu")
    gr.Markdown("Upload a menu image to convert it to Braille text")
    
    with gr.Row():
        with gr.Column(scale=1):
            # Input components
            image_input = gr.Image(type="pil", label="Upload Menu Image")
            
            with gr.Row():
                use_llm = gr.Checkbox(label="Use AI for text processing", value=True)
                use_context = gr.Checkbox(label="Use AI for context enhancement", value=True)
            
            process_button = gr.Button("Process Menu")
        
        with gr.Column(scale=2):
            # Output components
            processed_text = gr.Textbox(label="Processed Text", lines=8)
            braille_output = gr.Textbox(label="Braille Translation", lines=10)
            metadata_output = gr.Markdown()
            
            # Hidden state for PDF generation
            state = gr.State()
            
            # PDF download section
            with gr.Group():
                gr.Markdown("### Download Options")
                pdf_title = gr.Textbox(label="PDF Title", value="Menu in Braille")
                pdf_type = gr.Radio(
                    ["Sequential (Text then Braille)", "Side-by-Side Comparison"],
                    label="PDF Format",
                    value="Sequential (Text then Braille)"
                )
                pdf_button = gr.Button("Generate PDF")
                pdf_output = gr.File(label="Download PDF")
    
    # Set up event handlers
    process_button.click(
        process_image,
        inputs=[image_input, use_llm, use_context],
        outputs=[processed_text, braille_output, metadata_output, state]
    )
    
    pdf_button.click(
        create_pdf,
        inputs=[state, pdf_title, pdf_type],
        outputs=[pdf_output]
    )
    
    # Add examples
    gr.Examples(
        examples=["assets/sample_menus/menu1.jpg", "assets/sample_menus/menu2.jpg"],
        inputs=image_input
    )
    
    # Add about section
    with gr.Accordion("About", open=False):
        gr.Markdown("""
        This application converts menu images to Braille text using AI technologies:
        
        - Document AI for text extraction
        - LLMs for text processing and enhancement
        - Braille translation with formatting
        - PDF generation for download
        
        Created as a demonstration of AI-powered accessibility tools.
        """)

# Launch the app
if __name__ == "__main__":
    demo.launch()
