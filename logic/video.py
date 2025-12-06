"""
Basin Signal Engine - Video Layer
Handles video recording and analysis using Gemini's multimodal capabilities.

The "Eye" of the Brain - Video Understanding for Interview Coaching.
"""

import os
import tempfile
import base64
from pathlib import Path


# ═══════════════════════════════════════════════════════════════
# VIDEO ANALYSIS (Using Gemini's Native Video Understanding)
# ═══════════════════════════════════════════════════════════════

def analyze_video_pitch(video_bytes: bytes, context: str = "") -> dict:
    """
    Analyze a video pitch/interview using Gemini's video understanding.
    
    Args:
        video_bytes: Raw video data
        context: Optional context (job description, role, etc.)
        
    Returns:
        dict: Analysis results with feedback on delivery, content, presence
    """
    import google.generativeai as genai
    
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Google API Key required for video analysis.")
    
    genai.configure(api_key=api_key)
    
    # Save video to temp file
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        temp_file.write(video_bytes)
        temp_path = temp_file.name
    
    try:
        # Upload the video file to Gemini
        video_file = genai.upload_file(temp_path, mime_type="video/mp4")
        
        # Wait for processing
        import time
        while video_file.state.name == "PROCESSING":
            time.sleep(2)
            video_file = genai.get_file(video_file.name)
        
        if video_file.state.name == "FAILED":
            raise ValueError("Video processing failed")
        
        # Create the analysis prompt
        analysis_prompt = f"""
You are an Executive Interview Coach analyzing a candidate's video pitch.

CONTEXT: {context if context else "General interview/pitch assessment"}

Analyze this video and provide detailed feedback in the following structure:

## 1. CONTENT ANALYSIS
- Key points delivered
- Clarity of message
- Use of metrics/specifics
- Missing elements

## 2. DELIVERY ASSESSMENT
- Pace and rhythm (too fast, too slow, good)
- Vocal confidence (1-10)
- Filler words detected
- Energy level

## 3. PRESENCE & BODY LANGUAGE
- Eye contact assessment
- Posture and positioning
- Hand gestures (distracting or enhancing)
- Facial expressions
- Professional appearance

## 4. OVERALL SCORE
- Executive Presence Score: X/10
- Content Quality Score: X/10
- Delivery Score: X/10

## 5. TOP 3 IMPROVEMENTS
1. [Most critical improvement]
2. [Second priority]
3. [Third priority]

## 6. WHAT WORKED WELL
- [Strength 1]
- [Strength 2]
- [Strength 3]

Be direct and actionable. This is coaching, not encouragement.
"""
        
        # Use Gemini 2.0 Flash for video analysis
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content([video_file, analysis_prompt])
        
        # Clean up the uploaded file
        genai.delete_file(video_file.name)
        
        return {
            "success": True,
            "analysis": response.text,
            "model": "gemini-2.0-flash-exp"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "analysis": None
        }
    finally:
        Path(temp_path).unlink(missing_ok=True)


def analyze_video_frames(video_bytes: bytes, num_frames: int = 5) -> dict:
    """
    Fallback: Extract frames and analyze as images if video upload fails.
    
    Args:
        video_bytes: Raw video data
        num_frames: Number of frames to extract
        
    Returns:
        dict: Analysis based on key frames
    """
    # This is a fallback if direct video upload doesn't work
    # Would extract frames using cv2 and analyze as images
    return {
        "success": False,
        "error": "Frame extraction not implemented. Use direct video upload.",
        "analysis": None
    }


# ═══════════════════════════════════════════════════════════════
# VIDEO TO AUDIO EXTRACTION
# ═══════════════════════════════════════════════════════════════

def extract_audio_from_video(video_bytes: bytes) -> bytes:
    """
    Extract audio track from video for transcription.
    Requires ffmpeg to be installed.
    
    Args:
        video_bytes: Raw video data
        
    Returns:
        bytes: Audio data (WAV format)
    """
    import subprocess
    
    # Save video to temp file
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as video_temp:
        video_temp.write(video_bytes)
        video_path = video_temp.name
    
    # Create temp path for audio output
    audio_path = video_path.replace(".mp4", ".wav")
    
    try:
        # Extract audio using ffmpeg
        subprocess.run([
            "ffmpeg", "-i", video_path,
            "-vn",  # No video
            "-acodec", "pcm_s16le",  # WAV format
            "-ar", "16000",  # Sample rate for Whisper
            "-ac", "1",  # Mono
            "-y",  # Overwrite
            audio_path
        ], check=True, capture_output=True)
        
        # Read the audio file
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        
        return audio_bytes
        
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Audio extraction failed: {e.stderr.decode()}")
    finally:
        Path(video_path).unlink(missing_ok=True)
        Path(audio_path).unlink(missing_ok=True)


# ═══════════════════════════════════════════════════════════════
# VIDEO UTILITIES
# ═══════════════════════════════════════════════════════════════

def get_video_info(video_bytes: bytes) -> dict:
    """
    Get basic info about a video file.
    
    Args:
        video_bytes: Video data
        
    Returns:
        dict: Video information
    """
    size_mb = len(video_bytes) / (1024 * 1024)
    
    return {
        "size_bytes": len(video_bytes),
        "size_mb": round(size_mb, 2),
        "format": "mp4",  # Assumed
        "max_size_mb": 100  # Gemini limit
    }


def validate_video(video_bytes: bytes) -> dict:
    """
    Validate video for Gemini processing.
    
    Args:
        video_bytes: Video data
        
    Returns:
        dict: Validation result
    """
    info = get_video_info(video_bytes)
    
    if info["size_mb"] > 100:
        return {
            "valid": False,
            "message": f"Video too large ({info['size_mb']}MB). Max is 100MB."
        }
    
    if info["size_mb"] < 0.01:
        return {
            "valid": False,
            "message": "Video file appears empty or corrupted."
        }
    
    return {
        "valid": True,
        "message": f"Video ready ({info['size_mb']}MB)"
    }
