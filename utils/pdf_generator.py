import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

# Try to register a font that supports Braille Unicode characters
try:
    # Check for common Braille fonts
    font_paths = [
        "DejaVuSans.ttf",  # Common on Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Arial Unicode.ttf",  # Mac
        "C:\\Windows\\Fonts\\arial.ttf"  # Windows
    ]
    
    font_registered = False
    for font_path in font_paths:
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('BrailleFont', font_path))
            font_registered = True
            break
    
    if not font_registered:
        # Use default font if none of the above are found
        print("No suitable font found for Braille. Using default font.")
except Exception as e:
    print(f"Error registering font: {str(e)}")

def create_braille_pdf(original_text, braille_text, title="Menu in Braille"):
    """
    Create a PDF file with original text and its Braille translation.
    
    Args:
        original_text: Original text content
        braille_text: Braille translation
        title: PDF title
        
    Returns:
        BytesIO object containing the PDF
    """
    try:
        # Create a BytesIO object to store the PDF
        buffer = io.BytesIO()
        
        # Register a Unicode font that supports Braille
        pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Create a custom style for Braille text with Unicode support
        braille_style = ParagraphStyle(
            'Braille',
            parent=normal_style,
            fontName='DejaVu',  # Use DejaVu font which supports Unicode Braille
            fontSize=14,
            leading=18,
            spaceAfter=12
        )
        
        # Create the content
        content = []
        
        # Add title
        content.append(Paragraph(title, title_style))
        content.append(Spacer(1, 12))
        
        # Add original text section
        content.append(Paragraph("Original Text", heading_style))
        content.append(Spacer(1, 6))
        
        # Split original text by lines and add each as a paragraph
        for line in original_text.split('\n'):
            if line.strip():
                content.append(Paragraph(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), normal_style))
            else:
                content.append(Spacer(1, 12))
        
        content.append(Spacer(1, 24))
        
        # Add Braille section
        content.append(Paragraph("Braille Translation", heading_style))
        content.append(Spacer(1, 6))
        
        # Split Braille text by lines and add each as a paragraph
        for line in braille_text.split('\n'):
            if line.strip():
                content.append(Paragraph(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), braille_style))
            else:
                content.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(content)
        
        # Reset buffer position to the beginning
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error in create_braille_pdf: {str(e)}")
        # Create a simple PDF with error message
        simple_buffer = io.BytesIO()
        doc = SimpleDocTemplate(simple_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        content = [Paragraph(f"Error creating PDF: {str(e)}", styles['Normal'])]
        doc.build(content)
        simple_buffer.seek(0)
        return simple_buffer


def create_braille_pdf_working(original_text, braille_text, title="Menu in Braille"):
    """
    Create a PDF file with original text and its Braille translation.
    
    Args:
        original_text: Original text content
        braille_text: Braille translation
        title: PDF title
        
    Returns:
        BytesIO object containing the PDF
    """
    try:
        # Create a BytesIO object to store the PDF
        buffer = io.BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Create a custom style for Braille text
        braille_style = ParagraphStyle(
            'Braille',
            parent=normal_style,
            fontName='Helvetica',  # Use standard font to avoid issues
            fontSize=14,
            leading=18,
            spaceAfter=12
        )
        
        # Create the content
        content = []
        
        # Add title
        content.append(Paragraph(title, title_style))
        content.append(Spacer(1, 12))
        
        # Add original text section
        content.append(Paragraph("Original Text", heading_style))
        content.append(Spacer(1, 6))
        
        # Split original text by lines and add each as a paragraph
        for line in original_text.split('\n'):
            if line.strip():
                content.append(Paragraph(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), normal_style))
            else:
                content.append(Spacer(1, 12))
        
        content.append(Spacer(1, 24))
        
        # Add Braille section
        content.append(Paragraph("Braille Translation", heading_style))
        content.append(Spacer(1, 6))
        
        # Split Braille text by lines and add each as a paragraph
        for line in braille_text.split('\n'):
            if line.strip():
                content.append(Paragraph(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), braille_style))
            else:
                content.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(content)
        
        # Reset buffer position to the beginning
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error in create_braille_pdf: {str(e)}")
        raise


def create_braille_pdf1(original_text, braille_text, title="Menu in Braille"):
    """
    Create a PDF file with original text and its Braille translation.
    
    Args:
        original_text: Original text content
        braille_text: Braille translation
        title: PDF title
        
    Returns:
        BytesIO object containing the PDF
    """
    # Create a BytesIO object to store the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Create a custom style for Braille text
    braille_style = ParagraphStyle(
        'Braille',
        parent=normal_style,
        fontName='BrailleFont' if font_registered else 'Helvetica',
        fontSize=14,
        leading=18,
        spaceAfter=12
    )
    
    # Create the content
    content = []
    
    # Add title
    content.append(Paragraph(title, title_style))
    content.append(Spacer(1, 12))
    
    # Add original text section
    content.append(Paragraph("Original Text", heading_style))
    content.append(Spacer(1, 6))
    
    # Split original text by lines and add each as a paragraph
    for line in original_text.split('\n'):
        if line.strip():
            content.append(Paragraph(line, normal_style))
        else:
            content.append(Spacer(1, 12))
    
    content.append(Spacer(1, 24))
    
    # Add Braille section
    content.append(Paragraph("Braille Translation", heading_style))
    content.append(Spacer(1, 6))
    
    # Split Braille text by lines and add each as a paragraph
    for line in braille_text.split('\n'):
        if line.strip():
            content.append(Paragraph(line, braille_style))
        else:
            content.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(content)
    
    # Reset buffer position to the beginning
    buffer.seek(0)
    return buffer


def create_braille_pdf_with_comparison(original_text, braille_text, title="Menu in Braille"):
    """
    Create a PDF file with side-by-side comparison of original text and Braille.
    
    Args:
        original_text: Original text content
        braille_text: Braille translation
        title: PDF title
        
    Returns:
        BytesIO object containing the PDF
    """
    try:
        # Create a BytesIO object to store the PDF
        buffer = io.BytesIO()
        
        # Register a Unicode font that supports Braille
        try:
            pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
            braille_font = 'DejaVu'
        except:
            # Fallback to default font if DejaVu is not available
            braille_font = 'Helvetica'
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = ParagraphStyle(
            'Normal',
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            wordWrap='CJK'
        )
        braille_style = ParagraphStyle(
            'Braille',
            fontName=braille_font,
            fontSize=10,
            leading=12,
            wordWrap='CJK'
        )
        
        # Create the content
        content = []
        
        # Add title
        content.append(Paragraph(title, title_style))
        content.append(Spacer(1, 12))
        
        # Split text into paragraphs
        orig_paragraphs = original_text.split('\n\n')
        braille_paragraphs = braille_text.split('\n\n')
        
        # Ensure both lists have the same length
        max_paragraphs = max(len(orig_paragraphs), len(braille_paragraphs))
        orig_paragraphs = orig_paragraphs + [''] * (max_paragraphs - len(orig_paragraphs))
        braille_paragraphs = braille_paragraphs + [''] * (max_paragraphs - len(braille_paragraphs))
        
        # Process each paragraph separately
        for i in range(max_paragraphs):
            # Create section header for each paragraph
            if i > 0:
                content.append(Spacer(1, 20))
            
            content.append(Paragraph(f"Section {i+1}", heading_style))
            content.append(Spacer(1, 8))
            
            # Create a table for this paragraph
            data = [["Original Text", "Braille Translation"]]
            
            # Split paragraph into lines
            orig_lines = orig_paragraphs[i].split('\n')
            braille_lines = braille_paragraphs[i].split('\n')
            
            # Ensure both line lists have the same length
            max_lines = max(len(orig_lines), len(braille_lines))
            orig_lines = orig_lines + [''] * (max_lines - len(orig_lines))
            braille_lines = braille_lines + [''] * (max_lines - len(braille_lines))
            
            # Process each line
            for j in range(max_lines):
                # Escape special characters
                orig = orig_lines[j].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                braille = braille_lines[j].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                
                # Create paragraphs with proper wrapping
                orig_para = Paragraph(orig, normal_style)
                braille_para = Paragraph(braille, braille_style)
                
                data.append([orig_para, braille_para])
            
            # Create a table with fixed width columns and automatic row heights
            available_width = doc.width - 24  # Account for margins
            col_width = available_width / 2
            
            table = Table(data, colWidths=[col_width, col_width], repeatRows=1)
            
            # Style the table
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
                ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
            ]))
            
            content.append(table)
        
        # Build the PDF
        doc.build(content)
        
        # Reset buffer position to the beginning
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error in create_braille_pdf_with_comparison: {str(e)}")
        # Create a simple PDF with error message
        simple_buffer = io.BytesIO()
        doc = SimpleDocTemplate(simple_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        content = [Paragraph(f"Error creating PDF: {str(e)}", styles['Normal'])]
        doc.build(content)
        simple_buffer.seek(0)
        return simple_buffer


def create_braille_pdf_with_comparison_single_line(original_text, braille_text, title="Menu in Braille"):
    """
    Create a PDF file with side-by-side comparison of original text and Braille.
    
    Args:
        original_text: Original text content
        braille_text: Braille translation
        title: PDF title
        
    Returns:
        BytesIO object containing the PDF
    """
    try:
        # Create a BytesIO object to store the PDF
        buffer = io.BytesIO()
        
        # Register a Unicode font that supports Braille
        pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Create a custom style for Braille text with Unicode support
        braille_style = ParagraphStyle(
            'Braille',
            parent=normal_style,
            fontName='DejaVu',  # Use DejaVu font which supports Unicode Braille
            fontSize=14,
            leading=18
        )
        
        # Create the content
        content = []
        
        # Add title
        content.append(Paragraph(title, title_style))
        content.append(Spacer(1, 12))
        
        # Process text line by line
        orig_lines = original_text.split('\n')
        braille_lines = braille_text.split('\n')
        
        # Make sure both lists have the same length
        max_len = max(len(orig_lines), len(braille_lines))
        orig_lines = orig_lines + [''] * (max_len - len(orig_lines))
        braille_lines = braille_lines + [''] * (max_len - len(braille_lines))
        
        # Break content into smaller chunks (10 lines per table)
        chunk_size = 10
        for chunk_start in range(0, max_len, chunk_size):
            chunk_end = min(chunk_start + chunk_size, max_len)
            
            # Create a table for this chunk
            table_data = [["Original Text", "Braille Translation"]]
            
            for i in range(chunk_start, chunk_end):
                orig = orig_lines[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                braille = braille_lines[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                
                # Limit the length of each cell to prevent overflow
                if len(orig) > 100:
                    orig = orig[:97] + "..."
                if len(braille) > 100:
                    braille = braille[:97] + "..."
                
                table_data.append([orig, braille])
            
            # Create the table
            table = Table(table_data, colWidths=[doc.width/2-12, doc.width/2-12])
            table.setStyle(TableStyle([
                ('FONT', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONT', (1, 0), (1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (1, 0), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('LINEABOVE', (0, 1), (-1, -1), 1, colors.black),
                ('FONT', (0, 1), (0, -1), 'Helvetica'),
                ('FONT', (1, 1), (1, -1), 'DejaVu')
            ]))
            
            content.append(table)
            content.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(content)
        
        # Reset buffer position to the beginning
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error in create_braille_pdf_with_comparison: {str(e)}")
        # Create a simple PDF with error message
        simple_buffer = io.BytesIO()
        doc = SimpleDocTemplate(simple_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        content = [Paragraph(f"Error creating PDF: {str(e)}", styles['Normal'])]
        doc.build(content)
        simple_buffer.seek(0)
        return simple_buffer


def create_braille_pdf_with_comparison_slow(original_text, braille_text, title="Menu in Braille"):
    """
    Create a PDF file with side-by-side comparison of original text and Braille.
    
    Args:
        original_text: Original text content
        braille_text: Braille translation
        title: PDF title
        
    Returns:
        BytesIO object containing the PDF
    """
    try:
        # Create a BytesIO object to store the PDF
        buffer = io.BytesIO()
        
        # Register a Unicode font that supports Braille
        pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Create a custom style for Braille text with Unicode support
        braille_style = ParagraphStyle(
            'Braille',
            parent=normal_style,
            fontName='DejaVu',  # Use DejaVu font which supports Unicode Braille
            fontSize=14,
            leading=18
        )
        
        # Create the content
        content = []
        
        # Add title
        content.append(Paragraph(title, title_style))
        content.append(Spacer(1, 12))
        
        # Process text line by line
        orig_lines = original_text.split('\n')
        braille_lines = braille_text.split('\n')
        
        # Make sure both lists have the same length
        max_len = max(len(orig_lines), len(braille_lines))
        orig_lines = orig_lines + [''] * (max_len - len(orig_lines))
        braille_lines = braille_lines + [''] * (max_len - len(braille_lines))
        
        # Break content into smaller chunks (10 lines per table)
        chunk_size = 10
        for chunk_start in range(0, max_len, chunk_size):
            chunk_end = min(chunk_start + chunk_size, max_len)
            
            # Create a table for this chunk
            table_data = [["Original Text", "Braille Translation"]]
            
            for i in range(chunk_start, chunk_end):
                orig = orig_lines[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                braille = braille_lines[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                
                # Limit the length of each cell to prevent overflow
                if len(orig) > 100:
                    orig = orig[:97] + "..."
                if len(braille) > 100:
                    braille = braille[:97] + "..."
                
                table_data.append([orig, braille])
            
            # Create the table
            table = Table(table_data, colWidths=[doc.width/2-12, doc.width/2-12])
            table.setStyle(TableStyle([
                ('FONT', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONT', (1, 0), (1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (1, 0), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('LINEABOVE', (0, 1), (-1, -1), 1, colors.black),
                ('FONT', (0, 1), (0, -1), 'Helvetica'),
                ('FONT', (1, 1), (1, -1), 'DejaVu')
            ]))
            
            content.append(table)
            content.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(content)
        
        # Reset buffer position to the beginning
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error in create_braille_pdf_with_comparison: {str(e)}")
        # Create a simple PDF with error message
        simple_buffer = io.BytesIO()
        doc = SimpleDocTemplate(simple_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        content = [Paragraph(f"Error creating PDF: {str(e)}", styles['Normal'])]
        doc.build(content)
        simple_buffer.seek(0)
        return simple_buffer


def create_braille_pdf_with_comparison_wrong(original_text, braille_text, title="Menu in Braille"):
    """
    Create a PDF file with side-by-side comparison of original text and Braille.
    
    Args:
        original_text: Original text content
        braille_text: Braille translation
        title: PDF title
        
    Returns:
        BytesIO object containing the PDF
    """
    try:
        # Create a BytesIO object to store the PDF
        buffer = io.BytesIO()
        
        # Register a Unicode font that supports Braille
        pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Create a custom style for Braille text with Unicode support
        braille_style = ParagraphStyle(
            'Braille',
            parent=normal_style,
            fontName='DejaVu',  # Use DejaVu font which supports Unicode Braille
            fontSize=14,
            leading=18
        )
        
        # Create the content
        content = []
        
        # Add title
        content.append(Paragraph(title, title_style))
        content.append(Spacer(1, 12))
        
        # Create a simpler table structure
        table_data = [["Original Text", "Braille Translation"]]
        
        # Process text line by line
        orig_lines = original_text.split('\n')
        braille_lines = braille_text.split('\n')
        
        # Make sure both lists have the same length
        max_len = max(len(orig_lines), len(braille_lines))
        orig_lines = orig_lines + [''] * (max_len - len(orig_lines))
        braille_lines = braille_lines + [''] * (max_len - len(braille_lines))
        
        # Add each line pair to the table
        for i in range(max_len):
            orig = orig_lines[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            braille = braille_lines[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Create paragraphs with appropriate styles
            orig_para = Paragraph(orig, normal_style)
            braille_para = Paragraph(braille, braille_style)
            
            table_data.append([orig_para, braille_para])
        
        # Create the table
        table = Table(table_data, colWidths=[doc.width/2-12, doc.width/2-12])
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONT', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (1, 0), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('LINEABOVE', (0, 1), (-1, -1), 1, colors.black)
        ]))
        
        content.append(table)
        
        # Build the PDF
        doc.build(content)
        
        # Reset buffer position to the beginning
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error in create_braille_pdf_with_comparison: {str(e)}")
        # Create a simple PDF with error message
        simple_buffer = io.BytesIO()
        doc = SimpleDocTemplate(simple_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        content = [Paragraph(f"Error creating PDF: {str(e)}", styles['Normal'])]
        doc.build(content)
        simple_buffer.seek(0)
        return simple_buffer


def create_braille_pdf_with_comparison_working(original_text, braille_text, title="Menu in Braille"):
    """
    Create a PDF file with side-by-side comparison of original text and Braille.
    
    Args:
        original_text: Original text content
        braille_text: Braille translation
        title: PDF title
        
    Returns:
        BytesIO object containing the PDF
    """
    try:
        # Create a BytesIO object to store the PDF
        buffer = io.BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Create a custom style for Braille text - use standard font
        braille_style = ParagraphStyle(
            'Braille',
            parent=normal_style,
            fontName='Helvetica',
            fontSize=14,
            leading=18
        )
        
        # Create the content
        content = []
        
        # Add title
        content.append(Paragraph(title, title_style))
        content.append(Spacer(1, 12))
        
        # Create a simpler table structure
        data = [["Original Text", "Braille Translation"]]
        
        # Process text line by line
        orig_lines = original_text.split('\n')
        braille_lines = braille_text.split('\n')
        
        # Make sure both lists have the same length
        max_len = max(len(orig_lines), len(braille_lines))
        orig_lines = orig_lines + [''] * (max_len - len(orig_lines))
        braille_lines = braille_lines + [''] * (max_len - len(braille_lines))
        
        # Add each line pair to the table
        for i in range(max_len):
            orig = orig_lines[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            braille = braille_lines[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            data.append([orig, braille])
        
        # Create the table
        table = Table(data, colWidths=[doc.width/2-12, doc.width/2-12])
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (1, 0), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('LINEABOVE', (0, 1), (-1, -1), 1, colors.black),
            ('FONT', (0, 1), (0, -1), 'Helvetica'),
            ('FONT', (1, 1), (1, -1), 'Helvetica')
        ]))
        
        content.append(table)
        
        # Build the PDF
        doc.build(content)
        
        # Reset buffer position to the beginning
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error in create_braille_pdf_with_comparison: {str(e)}")
        # Return the error message in a simple PDF
        simple_buffer = io.BytesIO()
        doc = SimpleDocTemplate(simple_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        content = [Paragraph(f"Error creating PDF: {str(e)}", styles['Normal'])]
        doc.build(content)
        simple_buffer.seek(0)
        return simple_buffer


def create_braille_pdf_with_comparison1(original_text, braille_text, title="Menu in Braille"):
    """
    Create a PDF file with side-by-side comparison of original text and Braille.
    
    Args:
        original_text: Original text content
        braille_text: Braille translation
        title: PDF title
        
    Returns:
        BytesIO object containing the PDF
    """
    # Create a BytesIO object to store the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Create a custom style for Braille text
    braille_style = ParagraphStyle(
        'Braille',
        parent=normal_style,
        fontName='BrailleFont' if font_registered else 'Helvetica',
        fontSize=14,
        leading=18
    )
    
    # Create the content
    content = []
    
    # Add title
    content.append(Paragraph(title, title_style))
    content.append(Spacer(1, 12))
    
    # Split text into lines
    original_lines = original_text.split('\n')
    braille_lines = braille_text.split('\n')
    
    # Ensure both lists have the same length
    max_lines = max(len(original_lines), len(braille_lines))
    original_lines = original_lines + [''] * (max_lines - len(original_lines))
    braille_lines = braille_lines + [''] * (max_lines - len(braille_lines))
    
    # Create a table for side-by-side comparison
    table_data = [
        [Paragraph("Original Text", heading_style), Paragraph("Braille Translation", heading_style)]
    ]
    
    # Add each line as a row in the table
    for i in range(max_lines):
        original_para = Paragraph(original_lines[i], normal_style) if original_lines[i].strip() else Spacer(1, 12)
        braille_para = Paragraph(braille_lines[i], braille_style) if braille_lines[i].strip() else Spacer(1, 12)
        table_data.append([original_para, braille_para])
    
    # Create the table
    table = Table(table_data, colWidths=[doc.width/2.0-12, doc.width/2.0-12])
    
    # Style the table
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, 0), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey)
    ]))
    
    content.append(table)
    
    # Build the PDF
    doc.build(content)
    
    # Reset buffer position to the beginning
    buffer.seek(0)
    return buffer
