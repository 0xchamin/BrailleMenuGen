from transformers import pipeline
import re

# English to Braille mapping (Grade 1 Braille) #
BRAILLE_MAP = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
    '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑', '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊',
    '.': '⠲', ',': '⠂', ';': '⠆', ':': '⠒', '!': '⠖', '?': '⠦', '"': '⠦', "'": '⠄', '(': '⠐⠣', ')': '⠐⠜',
    '-': '⠤', '/': '⠌', '+': '⠬', '=': '⠐⠶', '*': '⠐⠔', '&': '⠯', '%': '⠐⠏', '#': '⠼', '@': '⠐⠁',
    '$': '⠐⠎', '€': '⠐⠑', '£': '⠐⠇', '¥': '⠐⠽', '₹': '⠐⠗',
    ' ': '⠀'
}

# Initialize the summarization pipeline for context understanding
summarizer = None

def get_summarizer():
    """Get or initialize the summarization model."""
    global summarizer
    if summarizer is None:
        try:
            # Use a small, efficient model for summarization
            summarizer = pipeline(
                "summarization", 
                model="facebook/bart-large-cnn",
                max_length=100,
                min_length=30,
                truncation=True
            )
        except Exception as e:
            print(f"Error loading summarizer: {str(e)}")
    return summarizer

def text_to_grade1_braille(text):
    """
    Convert text to Grade 1 Braille.
    
    Args:
        text: Text to convert
        
    Returns:
        Braille text
    """
    braille_text = ""
    for char in text.lower():
        if char in BRAILLE_MAP:
            braille_text += BRAILLE_MAP[char]
        else:
            # For characters not in our map, just keep the original
            braille_text += char
    
    return braille_text


def text_to_braille(text, use_context=True):
    """
    Convert text to Braille, with optional context enhancement.
    
    Args:
        text: Text to convert to Braille
        use_context: Whether to use AI to enhance context understanding
        
    Returns:
        Dictionary with Braille text and metadata
    """
    try:
        # Basic Braille translation
        braille_text = text_to_grade1_braille(text)
        
        # Create an ASCII representation for PDF
        ascii_braille = unicode_braille_to_ascii(braille_text)
        
        # If context enhancement is enabled
        context_summary = None
        if use_context and len(text) > 200:  # Only for longer texts
            summarizer = get_summarizer()
            if summarizer:
                try:
                    # Generate a summary to understand context
                    summary_result = summarizer(text)
                    if summary_result and len(summary_result) > 0:
                        context_summary = summary_result[0]['summary_text']
                except Exception as e:
                    print(f"Summarization error: {str(e)}")
        
        # Format the Braille text for better readability
        formatted_braille = format_braille_text(braille_text)
        formatted_ascii = format_braille_text(ascii_braille)
        
        return {
            'braille_text': braille_text,
            'formatted_braille': formatted_braille,
            'ascii_braille': ascii_braille,
            'formatted_ascii': formatted_ascii,
            'context_summary': context_summary,
            'success': True
        }
    except Exception as e:
        return {
            'braille_text': '',
            'error': str(e),
            'success': False
        }

def unicode_braille_to_ascii(braille_text):
    """
    Convert Unicode Braille to ASCII representation.
    
    Args:
        braille_text: Text with Unicode Braille characters
        
    Returns:
        ASCII representation of Braille
    """
    # Map each Braille character to a descriptive ASCII representation
    result = ""
    for char in braille_text:
        if char in BRAILLE_MAP.values():
            # For Braille characters, use a letter representation
            for letter, braille in BRAILLE_MAP.items():
                if braille == char and len(letter) == 1:
                    result += f"[{letter.upper()}]"
                    break
            else:
                result += "[?]"
        else:
            # For non-Braille characters, keep them as is
            result += char
    
    return result

def text_to_braille1(text, use_context=True):
    """
    Convert text to Braille, with optional context enhancement.
    
    Args:
        text: Text to convert to Braille
        use_context: Whether to use AI to enhance context understanding
        
    Returns:
        Dictionary with Braille text and metadata
    """
    try:
        # Basic Braille translation
        braille_text = text_to_grade1_braille(text)
        
        # If context enhancement is enabled
        context_summary = None
        if use_context and len(text) > 200:  # Only for longer texts
            summarizer = get_summarizer()
            if summarizer:
                try:
                    # Generate a summary to understand context
                    summary_result = summarizer(text)
                    if summary_result and len(summary_result) > 0:
                        context_summary = summary_result[0]['summary_text']
                except Exception as e:
                    print(f"Summarization error: {str(e)}")
        
        # Format the Braille text for better readability
        formatted_braille = format_braille_text(braille_text)
        
        return {
            'braille_text': braille_text,
            'formatted_braille': formatted_braille,
            'context_summary': context_summary,
            'success': True
        }
    except Exception as e:
        return {
            'braille_text': '',
            'error': str(e),
            'success': False
        }

def format_braille_text(braille_text, line_length=32):
    """
    Format Braille text for better readability.
    
    Args:
        braille_text: Raw Braille text
        line_length: Maximum characters per line
        
    Returns:
        Formatted Braille text
    """
    # Split text by existing newlines first
    paragraphs = braille_text.split('\n')
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        # Skip empty paragraphs
        if not paragraph.strip():
            formatted_paragraphs.append('')
            continue
            
        # Word wrap to line_length
        words = paragraph.split(' ')
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            # If adding this word exceeds line length, start a new line
            if current_length + len(word) + (1 if current_length > 0 else 0) > line_length:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                if current_length > 0:
                    current_length += 1  # Space
                current_line.append(word)
                current_length += len(word)
                
        # Add the last line if not empty
        if current_line:
            lines.append(' '.join(current_line))
            
        formatted_paragraphs.append('\n'.join(lines))
    
    # Join paragraphs with double newlines
    return '\n\n'.join(formatted_paragraphs)

def get_braille_metadata(text):
    """
    Get metadata about the Braille translation.
    
    Args:
        text: Original text
        
    Returns:
        Dictionary with metadata
    """
    word_count = len(re.findall(r'\b\w+\b', text))
    character_count = len(text)
    line_count = len(text.split('\n'))
    
    return {
        'word_count': word_count,
        'character_count': character_count,
        'line_count': line_count
    }
