"""
BASIN::NEXUS - Whisper Transcription Module
Real-time speech-to-text for voice practice
"""

import os
import tempfile
from typing import Optional, Dict, Any

# Try to import Whisper dependencies
WHISPER_AVAILABLE = False
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    pass

# Alternative: Use Groq's Whisper API (faster, cloud-based)
GROQ_WHISPER_AVAILABLE = False
try:
    from groq import Groq
    GROQ_WHISPER_AVAILABLE = True
except ImportError:
    pass


class WhisperTranscriber:
    """
    Transcription engine with multiple backends:
    1. Groq Whisper API (faster, recommended)
    2. Local Whisper model (offline fallback)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = None
        self.backend = None
        
        # Prefer Groq API (faster)
        if self.api_key and GROQ_WHISPER_AVAILABLE:
            self.backend = "groq"
            self.client = Groq(api_key=self.api_key)
        elif WHISPER_AVAILABLE:
            self.backend = "local"
            # Load smallest model for speed
            self.model = whisper.load_model("base")
        else:
            self.backend = None
    
    def is_available(self) -> bool:
        """Check if transcription is available"""
        return self.backend is not None
    
    def get_backend(self) -> str:
        """Get current backend name"""
        return self.backend or "none"
    
    def transcribe(self, audio_file, language: str = "en") -> Dict[str, Any]:
        """
        Transcribe audio file to text
        
        Args:
            audio_file: File path or file-like object
            language: Language code (default: English)
            
        Returns:
            Dict with 'text', 'confidence', 'words' (if available)
        """
        if not self.backend:
            return {
                "text": "",
                "error": "No transcription backend available. Install 'openai-whisper' or set GROQ_API_KEY.",
                "confidence": 0
            }
        
        try:
            if self.backend == "groq":
                return self._transcribe_groq(audio_file, language)
            elif self.backend == "local":
                return self._transcribe_local(audio_file, language)
        except Exception as e:
            return {
                "text": "",
                "error": str(e),
                "confidence": 0
            }
    
    def _transcribe_groq(self, audio_file, language: str) -> Dict[str, Any]:
        """Transcribe using Groq's Whisper API"""
        # Handle file-like objects
        if hasattr(audio_file, 'read'):
            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            
            with open(tmp_path, "rb") as f:
                transcription = self.client.audio.transcriptions.create(
                    file=f,
                    model="whisper-large-v3-turbo",
                    response_format="verbose_json"
                )
            
            os.unlink(tmp_path)  # Clean up
        else:
            # File path provided
            with open(audio_file, "rb") as f:
                transcription = self.client.audio.transcriptions.create(
                    file=f,
                    model="whisper-large-v3-turbo",
                    response_format="verbose_json"
                )
        
        return {
            "text": transcription.text,
            "confidence": 0.95,  # Groq doesn't return confidence
            "duration": getattr(transcription, 'duration', 0),
            "language": language,
            "backend": "groq"
        }
    
    def _transcribe_local(self, audio_file, language: str) -> Dict[str, Any]:
        """Transcribe using local Whisper model"""
        # Handle file-like objects
        if hasattr(audio_file, 'read'):
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            result = self.model.transcribe(tmp_path, language=language)
            os.unlink(tmp_path)
        else:
            result = self.model.transcribe(audio_file, language=language)
        
        return {
            "text": result["text"],
            "confidence": 0.9,
            "segments": result.get("segments", []),
            "language": result.get("language", language),
            "backend": "local"
        }


def analyze_speech(text: str) -> Dict[str, Any]:
    """
    Analyze transcribed speech for interview coaching
    
    Returns:
        Dict with word_count, filler_count, has_metric, wpm_estimate, etc.
    """
    if not text:
        return {
            "word_count": 0,
            "filler_count": 0,
            "has_metric": False,
            "filler_words": [],
            "power_words": [],
            "metrics_found": []
        }
    
    words = text.split()
    word_count = len(words)
    
    # Filler words to detect
    filler_patterns = [
        "um", "uh", "like", "you know", "basically", "actually",
        "literally", "kind of", "sort of", "i mean", "so yeah",
        "right", "yeah", "okay so", "well"
    ]
    
    text_lower = text.lower()
    filler_count = sum(text_lower.count(filler) for filler in filler_patterns)
    filler_words = [f for f in filler_patterns if f in text_lower]
    
    # Power words (executive presence)
    power_patterns = [
        "delivered", "achieved", "grew", "built", "led", "managed",
        "increased", "optimized", "scaled", "launched", "drove",
        "revenue", "pipeline", "growth", "strategy", "results"
    ]
    power_words = [p for p in power_patterns if p in text_lower]
    
    # Metric detection (numbers, percentages)
    import re
    metrics_found = re.findall(r'\d+(?:\.\d+)?%?', text)
    has_metric = len(metrics_found) > 0
    
    # Structure signals (STAR, SOAR)
    structure_words = ["situation", "task", "action", "result", "obstacle", "impact"]
    structure_count = sum(1 for s in structure_words if s in text_lower)
    
    return {
        "word_count": word_count,
        "filler_count": filler_count,
        "has_metric": has_metric,
        "filler_words": filler_words,
        "power_words": power_words,
        "metrics_found": metrics_found,
        "structure_score": structure_count,
        "power_score": len(power_words)
    }


# Singleton instance
_transcriber = None

def get_transcriber(api_key: Optional[str] = None) -> WhisperTranscriber:
    """Get or create the transcriber singleton"""
    global _transcriber
    if _transcriber is None:
        _transcriber = WhisperTranscriber(api_key)
    return _transcriber
