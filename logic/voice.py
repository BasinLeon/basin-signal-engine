"""
Basin Signal Engine - Voice Layer
Handles audio recording, transcription (Whisper), and TTS output.

The "Ear" and "Voice" of the Brain.
Compatible with Python 3.13
"""

import os
import tempfile
from pathlib import Path


# ═══════════════════════════════════════════════════════════════
# VOICE INPUT: TRANSCRIPTION (The Ear)
# ═══════════════════════════════════════════════════════════════

def transcribe_audio(audio_bytes: bytes, use_api: bool = True) -> str:
    """
    Transcribe audio bytes to text using OpenAI Whisper.
    
    Args:
        audio_bytes: Raw audio data from the recorder
        use_api: If True, uses OpenAI Whisper API. If False, uses local model.
        
    Returns:
        str: Transcribed text
    """
    if use_api:
        return _transcribe_with_api(audio_bytes)
    else:
        return _transcribe_local(audio_bytes)


def _transcribe_with_api(audio_bytes: bytes) -> str:
    """
    Transcribe using OpenAI Whisper API (requires API key).
    Fast, accurate, costs ~$0.006/min.
    """
    from openai import OpenAI
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key required for transcription.")
    
    client = OpenAI(api_key=api_key)
    
    # Save audio to temp file (API requires file-like object)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(audio_bytes)
        temp_path = temp_file.name
    
    try:
        with open(temp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcript
    finally:
        # Clean up temp file
        Path(temp_path).unlink(missing_ok=True)


def _transcribe_local(audio_bytes: bytes) -> str:
    """
    Transcribe using local Whisper model (slower, no API cost).
    Requires: pip install openai-whisper
    """
    import whisper
    
    # Load model (cached after first load)
    model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
    
    # Save audio to temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(audio_bytes)
        temp_path = temp_file.name
    
    try:
        result = model.transcribe(temp_path)
        return result["text"]
    finally:
        Path(temp_path).unlink(missing_ok=True)


# ═══════════════════════════════════════════════════════════════
# VOICE OUTPUT: TEXT-TO-SPEECH (The Voice)
# ═══════════════════════════════════════════════════════════════

def generate_speech(text: str, voice: str = "onyx") -> bytes:
    """
    Generate audio from text using OpenAI TTS.
    
    Args:
        text: The text to convert to speech
        voice: Voice option - "alloy", "echo", "fable", "onyx", "nova", "shimmer"
               Recommended: "onyx" (professional male), "nova" (professional female)
               
    Returns:
        bytes: Audio data (mp3 format)
    """
    from openai import OpenAI
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key required for TTS.")
    
    client = OpenAI(api_key=api_key)
    
    # Generate speech
    response = client.audio.speech.create(
        model="tts-1",  # Use "tts-1-hd" for higher quality
        voice=voice,
        input=text
    )
    
    # Return raw audio bytes
    return response.content


def get_voice_options() -> list:
    """
    Returns available TTS voice options.
    
    Returns:
        list: Voice option tuples (display_name, voice_id)
    """
    return [
        ("Onyx (Professional Male)", "onyx"),
        ("Nova (Professional Female)", "nova"),
        ("Alloy (Neutral)", "alloy"),
        ("Echo (Warm Male)", "echo"),
        ("Fable (Expressive)", "fable"),
        ("Shimmer (Soft Female)", "shimmer"),
    ]


# ═══════════════════════════════════════════════════════════════
# AUDIO UTILITIES (No external dependencies)
# ═══════════════════════════════════════════════════════════════

def get_audio_size_info(audio_bytes: bytes) -> dict:
    """
    Get basic info about audio bytes.
    
    Args:
        audio_bytes: Audio data
        
    Returns:
        dict: Info about the audio (size, estimated duration)
    """
    size_bytes = len(audio_bytes)
    # Rough estimate: WAV at 16kHz mono is about 32KB per second
    estimated_duration = size_bytes / 32000
    
    return {
        "size_bytes": size_bytes,
        "size_kb": size_bytes / 1024,
        "estimated_duration_seconds": estimated_duration
    }


def save_transcript_to_asset(transcript: str, title: str, metadata: dict = None) -> str:
    """
    Save a transcript as a markdown file in the assets directory for Oracle indexing.
    
    Args:
        transcript: The text content
        title: Title for the filename (e.g. "Mock Interview NVIDIA")
        metadata: Optional dict of metadata to add as frontmatter
        
    Returns:
        str: Path to the saved file
    """
    import datetime
    import re
    
    # Clean title for filename
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"TRANSCRIPT_{date_str}_{safe_title}.md"
    
    # Resolve assets dir
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    filepath = os.path.join(assets_dir, filename)
    
    # Construct content
    content = f"# {title}\n"
    content += f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    
    if metadata:
        for k, v in metadata.items():
            content += f"**{k}:** {v}\n"
            
    content += "\n---\n\n"
    content += "## Transcript\n\n"
    content += transcript
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    return filepath
