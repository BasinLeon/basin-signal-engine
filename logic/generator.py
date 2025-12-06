"""
Basin Signal Engine - The Engine Room (Generator)
Handles LLM API calls and output formatting.
Supports: OpenAI (GPT-4o) and Google Gemini

Includes MOCK_MODE for testing UI without burning API credits.
"""

import os
import json
import time


# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Set to True to test UI without API key
MOCK_MODE = False

# Default settings
DEFAULT_TEMPERATURE = 0.7


# ═══════════════════════════════════════════════════════════════
# MODEL OPTIONS
# ═══════════════════════════════════════════════════════════════

def get_model_options() -> list:
    """
    Returns available model options for the UI.
    
    Returns:
        list: Model option tuples (display_name, model_id)
    """
    return [
        # ⚡ GROQ (FREE Cloud - Super Fast!)
        ("⚡ Llama 3.3 70B (Groq - FREE)", "groq:llama-3.3-70b-versatile"),
        ("⚡ Llama 3.1 8B (Groq - FREE)", "groq:llama-3.1-8b-instant"),
        ("⚡ Mixtral 8x7B (Groq - FREE)", "groq:mixtral-8x7b-32768"),
        # 🏠 Local Models via Ollama
        ("🦙 Llama 3.2 (Local - 3B)", "ollama:llama3.2"),
        ("� DeepSeek R1 (Local - 8B)", "ollama:deepseek-r1:8b"),
        # ☁️ Cloud Models (Paid)
        ("☁️ GPT-4o (OpenAI)", "gpt-4o"),
        ("☁️ Gemini 1.5 Flash (Google)", "gemini-1.5-flash"),
    ]


def get_provider(model: str) -> str:
    """Determine the provider based on model name."""
    if model.startswith("groq:"):
        return "groq"
    if model.startswith("ollama:"):
        return "ollama"
    if model.startswith("gemini") or model.startswith("models/gemini"):
        return "google"
    if model.startswith("claude"):
        return "anthropic"
    return "openai"


# ═══════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ═══════════════════════════════════════════════════════════════

def generate_signal_output(messages: list, model: str = None) -> dict:
    """
    Calls the LLM (or returns mock data) to generate the architectural output.
    Automatically routes to the correct provider based on model name.
    
    Args:
        messages: The messages array from prompt_engine.py
        model: Model ID (determines provider automatically)
        
    Returns:
        dict: Parsed response with 'summary', 'email_blurb', 'gap_analysis', 'key_bullets'
    """
    if MOCK_MODE:
        return _get_mock_data()
    
    model = model or "groq:llama-3.3-70b-versatile"
    provider = get_provider(model)
    
    if provider == "groq":
        return _generate_with_groq(messages, model)
    elif provider == "ollama":
        return _generate_with_ollama(messages, model)
    elif provider == "google":
        return _generate_with_gemini(messages, model)
    else:
        return _generate_with_openai(messages, model)


def generate_plain_text(prompt: str, model_name: str = "groq:llama-3.3-70b-versatile") -> str:
    """
    Generates plain text (non-JSON) output for conversational features like War Room.
    Mainly supports Groq for speed.
    """
    messages = [{"role": "user", "content": prompt}]
    provider = get_provider(model_name)
    
    try:
        if provider == "groq":
            from groq import Groq
            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key: return "Error: Missing GROQ_API_KEY"
            
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model=model_name.replace("groq:", ""),
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
            
        elif provider == "openai":
            from openai import OpenAI
            client = OpenAI()
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
            
        elif provider == "ollama":
            import ollama
            response = ollama.chat(
                model=model_name.replace("ollama:", ""),
                messages=messages,
            )
            return response['message']['content']
            
        elif provider == "google":
            import google.generativeai as genai
            api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if not api_key: return "Error: Missing GOOGLE_API_KEY or GEMINI_API_KEY"
            
            genai.configure(api_key=api_key)
            gemini_model = genai.GenerativeModel(model_name)
            response = gemini_model.generate_content(prompt)
            return response.text
            
        elif provider == "anthropic":
            import anthropic
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key: return "Error: Missing ANTHROPIC_API_KEY"
            
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model=model_name,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        return "Error: Provider not supported for plain text yet."
        
    except Exception as e:
        return f"Error generating text: {str(e)}"


# ═══════════════════════════════════════════════════════════════
# GROQ GENERATOR (FREE CLOUD - SUPER FAST!)
# ═══════════════════════════════════════════════════════════════

def _generate_with_groq(messages: list, model: str) -> dict:
    """Generate using Groq API. Free tier available, extremely fast!"""
    from groq import Groq
    
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq API Key missing. Get free key at console.groq.com")
    
    # Extract model name (remove 'groq:' prefix)
    model_name = model.replace("groq:", "")
    
    client = Groq(api_key=api_key)
    
    try:
        # Add JSON instruction to system prompt
        modified_messages = []
        for msg in messages:
            if msg["role"] == "system":
                modified_messages.append({
                    "role": "system",
                    "content": msg["content"] + "\n\nIMPORTANT: Return ONLY valid JSON with keys: summary, email_blurb, gap_analysis, key_bullets"
                })
            else:
                modified_messages.append(msg)
        
        response = client.chat.completions.create(
            model=model_name,
            messages=modified_messages,
            temperature=DEFAULT_TEMPERATURE,
            response_format={"type": "json_object"}
        )
        
        raw_content = response.choices[0].message.content
        return _parse_response(raw_content)
        
    except Exception as e:
        return _error_response(str(e))


# ═══════════════════════════════════════════════════════════════
# OLLAMA GENERATOR (LOCAL - NO API KEY!)
# ═══════════════════════════════════════════════════════════════

def _generate_with_ollama(messages: list, model: str) -> dict:
    """Generate using local Ollama model. No API key required!"""
    import ollama
    
    # Extract model name (remove 'ollama:' prefix)
    model_name = model.replace("ollama:", "")
    
    # Convert messages format
    system_prompt = ""
    user_content = ""
    
    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        elif msg["role"] == "user":
            user_content = msg["content"]
    
    full_prompt = f"""
{system_prompt}

{user_content}

IMPORTANT: Return ONLY valid JSON with these exact keys: "summary", "email_blurb", "gap_analysis", "key_bullets"
The key_bullets should be an array of strings.
"""
    
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": full_prompt}],
            options={"temperature": DEFAULT_TEMPERATURE}
        )
        
        raw_content = response['message']['content']
        return _parse_response(raw_content)
        
    except Exception as e:
        return _error_response(str(e))


# ═══════════════════════════════════════════════════════════════
# OPENAI GENERATOR
# ═══════════════════════════════════════════════════════════════

def _generate_with_openai(messages: list, model: str) -> dict:
    """Generate using OpenAI API."""
    from openai import OpenAI
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API Key missing. Please enter it in the Sidebar.")
    
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=DEFAULT_TEMPERATURE
        )
        
        raw_content = response.choices[0].message.content
        return _parse_response(raw_content)
        
    except Exception as e:
        return _error_response(str(e))


# ═══════════════════════════════════════════════════════════════
# GEMINI GENERATOR
# ═══════════════════════════════════════════════════════════════

def _generate_with_gemini(messages: list, model: str) -> dict:
    """Generate using Google Gemini API."""
    import google.generativeai as genai
    
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Google API Key missing. Set GOOGLE_API_KEY in the Sidebar.")
    
    genai.configure(api_key=api_key)
    
    # Convert messages format for Gemini
    # Gemini uses a different message structure
    system_prompt = ""
    user_content = ""
    
    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        elif msg["role"] == "user":
            user_content = msg["content"]
    
    # Combine for Gemini (it handles system instructions differently)
    full_prompt = f"""
{system_prompt}

{user_content}

IMPORTANT: Return ONLY valid JSON with these exact keys: "summary", "email_blurb", "gap_analysis", "key_bullets"
"""
    
    try:
        gemini_model = genai.GenerativeModel(model)
        response = gemini_model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(
                temperature=DEFAULT_TEMPERATURE,
                response_mime_type="application/json"
            )
        )
        
        raw_content = response.text
        return _parse_response(raw_content)
        
    except Exception as e:
        return _error_response(str(e))


# ═══════════════════════════════════════════════════════════════
# RESPONSE PARSING
# ═══════════════════════════════════════════════════════════════

def _parse_response(raw_content: str) -> dict:
    """Parse JSON response from LLM, with fallback for malformed responses."""
    try:
        # Try to extract JSON if wrapped in markdown
        if "```json" in raw_content:
            raw_content = raw_content.split("```json")[1].split("```")[0]
        elif "```" in raw_content:
            raw_content = raw_content.split("```")[1].split("```")[0]
        
        parsed_data = json.loads(raw_content.strip())
        
        # Validate expected keys exist
        required_keys = ["summary", "email_blurb", "gap_analysis"]
        for key in required_keys:
            if key not in parsed_data:
                parsed_data[key] = f"[Missing: {key}]"
        
        # Add optional keys with defaults
        if "key_bullets" not in parsed_data:
            parsed_data["key_bullets"] = []
            
        return parsed_data
        
    except json.JSONDecodeError:
        # Fallback: Try to extract content manually from pseudo-JSON
        result = {
            "summary": "",
            "email_blurb": "",
            "gap_analysis": "",
            "key_bullets": []
        }
        
        # Try to find each key and extract its value
        import re
        
        for key in ["summary", "email_blurb", "gap_analysis"]:
            # Look for "key": "value" or "key": value patterns
            pattern = rf'"{key}"\s*:\s*"([^"]*(?:\\.[^"]*)*)"'
            match = re.search(pattern, raw_content, re.DOTALL)
            if match:
                result[key] = match.group(1).replace('\\n', '\n').replace('\\"', '"')
            else:
                # Try without quotes for multiline content
                pattern2 = rf'"{key}"\s*:\s*["\'](.+?)["\'](?=\s*[,}}])'
                match2 = re.search(pattern2, raw_content, re.DOTALL)
                if match2:
                    result[key] = match2.group(1).replace('\\n', '\n')
        
        # If we got at least some content, return it
        if any(result[k] for k in ["summary", "email_blurb", "gap_analysis"]):
            return result
        
        # Last resort: show raw content
        return {
            "summary": "The model generated a response but couldn't format it as JSON.",
            "email_blurb": "Try using a larger model (Groq Llama 70B or GPT-4o) for better formatting.",
            "gap_analysis": f"Raw output:\n\n{raw_content[:1500]}",
            "key_bullets": []
        }


def _error_response(error_msg: str) -> dict:
    """Return standardized error response."""
    return {
        "summary": f"Error Generating Signal: {error_msg}",
        "email_blurb": "System Failure.",
        "gap_analysis": "Check API Key or Connection.",
        "key_bullets": []
    }


# ═══════════════════════════════════════════════════════════════
# MOCK DATA
# ═══════════════════════════════════════════════════════════════

def _get_mock_data() -> dict:
    """
    Returns mock data to test the Streamlit UI layout without API calls.
    Simulates processing delay for realistic UX.
    """
    time.sleep(2)  # Simulate LLM thinking time
    
    return {
        "gap_analysis": """## Pain Points Detected

**1. High CAC & Manual Outbound**
The role requires reducing customer acquisition costs through automation and systematic processes.
*Resume Match:* Built automated lead generation workflows using Clay, reducing CAC by 40%.

**2. Lack of Structured GTM Processes**
They need someone to architect repeatable go-to-market systems, not just execute campaigns.
*Resume Match:* Architected the "Global Bridge" framework for US market entry.

**3. Need for Technical Implementation**
This is a 'muddy boots' role requiring actual technical implementation, not just strategy decks.
*Resume Match:* Built "Basin Resume OS" - a GenAI pipeline for unstructured data processing.""",

        "summary": "GTM Systems Architect with a proven track record of scaling Seed to Series A revenue engines. Expert in replacing 'brute force' sales activity with architectural leverage—built automated data pipelines that reduced CAC by 40% and generated 100+ qualified leads per week. Successfully operationalized 'Zero-to-One' market entry for 5+ startups across US and African markets.",

        "email_blurb": """Subject: Solving Your GTM Automation Gap

Hi [Hiring Manager],

I noticed you're looking for someone to build systematic GTM processes—not just run campaigns. That's exactly what I do.

At my previous role, I built a 'Data Supply Chain' that:
• Reduced CAC by 40% through automated lead enrichment
• Generated 100+ verified leads/week (replacing 3 SDRs)
• Created the 'Global Bridge' framework for US market entry

I'm not looking for a job; I'm looking to build the engine.

Worth a brief exchange?

— Leon""",

        "key_bullets": [
            "Built automated lead generation workflows using Clay + Python, reducing CAC by 40% and replacing manual prospecting",
            "Architected 'Data Supply Chain' methodology that generates 100+ qualified leads per week through signal processing",
            "Developed and deployed 'Basin Resume OS': A GenAI pipeline transforming unstructured career data into targeted commercial narratives",
            "Implemented 30/60/90 execution plans for 5+ early-stage startups, achieving 115% of quota through systems, not just effort"
        ]
    }


# ═══════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════

def estimate_tokens(messages: list) -> int:
    """
    Rough estimation of token count for cost awareness.
    
    Args:
        messages: The messages array
        
    Returns:
        int: Estimated token count
    """
    total_chars = sum(len(m.get("content", "")) for m in messages)
    # Rough estimate: 4 chars per token
    return total_chars // 4
