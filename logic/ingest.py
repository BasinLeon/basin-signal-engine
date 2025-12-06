"""
Basin Signal Engine - Data Ingestion Layer
The 'ETL' layer that extracts raw text from uploaded files.
Handles PDFs, Markdown, and plain text inputs.
"""

import PyPDF2
import io


def extract_text_from_upload(uploaded_file):
    """
    Ingests the raw file stream (PDF or Text) and returns clean string data.
    Acts as the 'Data Supply Chain' of the Basin Resume OS.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        str: Extracted text content or error message
    """
    if uploaded_file is None:
        return ""
    
    try:
        # Handle PDFs
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            return text.strip()
        
        # Handle Markdown/Text files
        elif uploaded_file.type in ["text/plain", "text/markdown", "application/octet-stream"]:
            # Read bytes and decode to string
            content = uploaded_file.getvalue()
            
            # Try UTF-8 first, fall back to latin-1
            try:
                return content.decode("utf-8").strip()
            except UnicodeDecodeError:
                return content.decode("latin-1").strip()
        
        else:
            # Attempt generic text decoding for unknown types
            try:
                return uploaded_file.getvalue().decode("utf-8").strip()
            except Exception:
                raise ValueError(f"Unsupported file format: {uploaded_file.type}")
                
    except Exception as e:
        return f"Error reading file: {str(e)}"


def validate_resume_content(text: str) -> dict:
    """
    Validates that extracted resume content has sufficient signal.
    
    Args:
        text: Extracted text from resume
        
    Returns:
        dict: Validation result with 'valid' bool and 'message' string
    """
    if not text or len(text.strip()) < 100:
        return {
            "valid": False,
            "message": "Resume content too short. Minimum 100 characters required."
        }
    
    # Check for key resume indicators
    signal_keywords = ["experience", "skills", "education", "project", "role", "built", "managed"]
    text_lower = text.lower()
    found_keywords = sum(1 for kw in signal_keywords if kw in text_lower)
    
    if found_keywords < 2:
        return {
            "valid": False,
            "message": "Resume lacks expected structure. Ensure it contains experience/skills sections."
        }
    
    return {
        "valid": True,
        "message": f"Resume validated: {len(text)} characters, {len(text.split())} words."
    }
