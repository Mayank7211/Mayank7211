import io
import re
from typing import List

from docx import Document as DocxDocument
from PyPDF2 import PdfReader


def parse_pdf(file_content: bytes) -> List[str]:
    """Parse PDF and extract text chunks."""
    try:
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text_chunks = []
        
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text.strip():
                # Clean up whitespace
                text = re.sub(r'\s+', ' ', text).strip()
                text_chunks.append(f"[Page {page_num + 1}] {text}")
        
        return text_chunks
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")


def parse_docx(file_content: bytes) -> List[str]:
    """Parse DOCX and extract text chunks."""
    try:
        doc = DocxDocument(io.BytesIO(file_content))
        text_chunks = []
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                text_chunks.append(text)
        
        return text_chunks
    except Exception as e:
        raise ValueError(f"Failed to parse DOCX: {str(e)}")


def parse_text(file_content: bytes) -> List[str]:
    """Parse plain text and extract chunks."""
    try:
        text = file_content.decode('utf-8')
        # Split by paragraphs (double newlines) or sentences
        paragraphs = text.split('\n\n')
        text_chunks = [p.strip() for p in paragraphs if p.strip()]
        return text_chunks
    except Exception as e:
        raise ValueError(f"Failed to parse text file: {str(e)}")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split long text into overlapping chunks for better context."""
    chunks = []
    words = text.split()
    
    current_chunk = []
    current_size = 0
    
    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1
        
        if current_size >= chunk_size:
            chunk_text = ' '.join(current_chunk)
            if chunk_text.strip():
                chunks.append(chunk_text)
            
            # Create overlap by keeping last few words
            overlap_words = int(overlap / 6)  # Rough estimate of words
            current_chunk = current_chunk[-overlap_words:] if overlap_words > 0 else []
            current_size = sum(len(w) + 1 for w in current_chunk)
    
    # Add remaining text
    if current_chunk:
        chunk_text = ' '.join(current_chunk)
        if chunk_text.strip():
            chunks.append(chunk_text)
    
    return chunks


async def parse_document(filename: str, file_content: bytes) -> List[str]:
    """Parse document based on file type and return text chunks."""
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        chunks = parse_pdf(file_content)
    elif filename_lower.endswith('.docx'):
        chunks = parse_docx(file_content)
    elif filename_lower.endswith('.txt'):
        chunks = parse_text(file_content)
    else:
        raise ValueError(f"Unsupported file type: {filename}")
    
    # Further chunk large text blocks
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > 500:
            sub_chunks = chunk_text(chunk, chunk_size=500, overlap=50)
            final_chunks.extend(sub_chunks)
        else:
            final_chunks.append(chunk)
    
    return [c for c in final_chunks if c.strip()]  # Remove empty chunks
