# 🏗️ Basin Signal Engine

> *AI-Powered Career Intelligence Platform*

Transform your resume into targeted narratives that match job requirements. Built with multi-modal input (Text, Voice, Video) and multi-LLM support (OpenAI, Google, Groq, Ollama).

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### 🎯 Core Intelligence

- **Pain Point Extraction** — Identifies real business problems from job descriptions
- **Evidence Mapping** — Maps your experience to those specific needs
- **Persona Targeting** — Tunes output for Operators, Visionaries, or Technologists

### 🎤 Multi-Modal Input

- **📄 Text/File** — Upload PDF/MD/TXT or paste directly
- **🎤 Voice** — Record your background, transcribed with Whisper
- **📹 Video** — Upload a pitch video for AI coaching (Gemini 2.0)

### 🤖 Multi-LLM Support

| Provider | Models | Cost |
|----------|--------|------|
| ⚡ **Groq** | Llama 3.3 70B, Mixtral | **FREE** |
| 🦙 **Ollama** | Llama 3.2, DeepSeek R1 | **FREE (local)** |
| ☁️ **OpenAI** | GPT-4o, GPT-4o Mini | Paid |
| ☁️ **Google** | Gemini 1.5 Flash/Pro | Free tier |

### 🔊 Voice Output

- **Text-to-Speech** — Generate audio cover letters with OpenAI TTS
- **Multiple voices** — Onyx, Nova, Alloy, Echo, Fable, Shimmer

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOURUSERNAME/basin-signal-engine.git
cd basin-signal-engine
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional)

```bash
cp .env.example .env
# Edit .env with your keys (or enter in sidebar)
```

**Free Options:**

- **Groq**: [console.groq.com](https://console.groq.com) - FREE, super fast
- **Ollama**: `brew install ollama && ollama pull llama3.2` - FREE, local

### 3. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## 📐 The Basin Protocol

| Principle | Meaning |
|-----------|---------|
| **Systems > Hires** | Build engines, not just manage teams |
| **Signal > Noise** | Every claim has a metric |
| **Architecture > Activity** | Show systems thinking |

---

## 🏗️ Architecture

```text
/basin-signal-engine
├── app.py                    # Streamlit Interface
├── requirements.txt          # Dependencies
├── .env                      # API Keys (git-ignored)
│
├── /logic
│   ├── ingest.py             # PDF/Text Extraction
│   ├── prompt_engine.py      # System Prompts
│   ├── generator.py          # Multi-LLM Router
│   ├── voice.py              # Speech-to-Text & TTS
│   └── video.py              # Video Analysis
│
└── /assets
    └── master_resume.md      # Template Resume
```

---

## 📤 Output

1. **Gap Analysis** — 3 pain points with resume evidence
2. **Professional Summary** — Tailored 3-4 sentence summary
3. **Sniper Email Blurb** — 150-word outreach message
4. **Audio Cover Letter** — TTS-generated audio version

---

## 🎭 Persona Targeting

| Persona | Best For |
|---------|----------|
| **The Operator** | Ops Leaders, RevOps, Trust & Safety |
| **The Visionary** | GTM, Growth, Sales Leadership |
| **The Technologist** | Solutions Architects, Technical PM |

---

## 🧪 Mock Mode

Test UI without API calls:

```python
# In logic/generator.py, set:
MOCK_MODE = True
```

---

## 🔮 Roadmap

- [x] Multi-LLM support (OpenAI, Gemini, Groq, Ollama)
- [x] Voice input (Whisper STT)
- [x] Audio output (OpenAI TTS)
- [x] Video pitch analysis (Gemini 2.0)
- [ ] PDF export for tailored resumes
- [ ] Chrome extension for one-click JD capture
- [ ] User authentication & saved sessions

---

## 📜 License

MIT License - Build freely.

---

**Basin & Associates** | Built on the Zero-to-One Protocol
