def text_to_unicode_braille(braille_text):
    """
    Convert Braille dots notation to Unicode Braille symbols.
    
    Args:
        braille_text: Braille text in dots notation
        
    Returns:
        Text with Unicode Braille symbols
    """
    # Mapping from Braille dots to Unicode Braille patterns
    # Unicode Braille patterns start at U+2800 (⠀)
    unicode_base = 0x2800
    
    # Convert each Braille character to its Unicode equivalent
    unicode_braille = ""
    for char in braille_text:
        # Check if the character is a standard Braille pattern
        if char in "⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿":
            unicode_braille += char
        else:
            # For non-Braille characters, keep them as is
            unicode_braille += char
    
    return unicode_braille

def create_braille_html(braille_text):
    """
    Create HTML to display Braille with proper styling.
    
    Args:
        braille_text: Braille text (either in dots or Unicode)
        
    Returns:
        HTML string for displaying Braille
    """
    # Convert to Unicode Braille if not already
    unicode_braille = text_to_unicode_braille(braille_text)
    
    # Replace newlines with <br> tags before using in f-string
    formatted_text = unicode_braille.replace('\n', '<br>')
    
    # Create HTML with proper styling
    html = f"""
    <div style="font-family: 'Courier New', monospace; font-size: 20px; line-height: 1.5; 
                background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        {formatted_text}
    </div>
    """
    
    return html


def create_braille_comparison(text, braille_text):
    """
    Create a side-by-side comparison of text and its Braille representation.
    
    Args:
        text: Original text
        braille_text: Braille translation
        
    Returns:
        HTML string for displaying the comparison
    """
    # Convert to Unicode Braille
    unicode_braille = text_to_unicode_braille(braille_text)
    
    # Split into lines
    text_lines = text.split('\n')
    braille_lines = unicode_braille.split('\n')
    
    # Ensure both lists have the same length
    max_lines = max(len(text_lines), len(braille_lines))
    text_lines = text_lines + [''] * (max_lines - len(text_lines))
    braille_lines = braille_lines + [''] * (max_lines - len(braille_lines))
    
    # Create HTML table for comparison
    html = """
    <style>
        .braille-table {
            width: 100%;
            border-collapse: collapse;
        }
        .braille-table td {
            padding: 8px;
            vertical-align: top;
            border-bottom: 1px solid #ddd;
        }
        .braille-text {
            font-family: 'Courier New', monospace;
            font-size: 20px;
            background-color: #f5f5f5;
        }
        .original-text {
            font-family: Arial, sans-serif;
        }
    </style>
    <table class="braille-table">
        <tr>
            <th>Original Text</th>
            <th>Braille Representation</th>
        </tr>
    """
    
    for i in range(max_lines):
        html += f"""
        <tr>
            <td class="original-text">{text_lines[i]}</td>
            <td class="braille-text">{braille_lines[i]}</td>
        </tr>
        """
    
    html += "</table>"
    
    return html
