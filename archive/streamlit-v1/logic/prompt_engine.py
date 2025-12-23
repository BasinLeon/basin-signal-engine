"""
Basin Signal Engine - The 'Basin Brain' (Prompt Engine)
This is where the magic happens. We don't use generic prompts.
We use the Agency OS persona to force 'Revenue Architecture' output.

The core differentiator: Pain Point Extraction -> Skill Mapping -> High-Agency Rewrite
"""


def construct_basin_prompt(resume_text: str, job_description: str, target_persona: str, use_deep_recon: bool = False) -> list:
    """
    Constructs the specific 'Revenue Architect' system prompt to guide the LLM.
    Forces the model to ignore generic HR fluff and focus on 'Systems > Hires'.
    
    Args:
        resume_text: The master resume content (Source of Truth)
        job_description: Target job description (The Signal)
        target_persona: The buyer persona to tune output for
        
    Returns:
        list: OpenAI-compatible messages array
    """
    
    # 1. Define the Persona Constraints (The "Lens")
    persona_configs = {
        "The Operator (Process & Efficiency)": {
            "focus_area": "Operational Rigor, Data Integrity, Risk Mitigation, Efficiency Gains, Process Optimization.",
            "forbidden_words": "spearheaded, passionate, motivated, visionary, innovative",
            "required_tone": "Precise, quantitative, structured. Think 'Google Trust & Safety' or 'Revenue Operations Lead'.",
            "output_style": "Emphasize metrics, SLAs, and process improvements. Use terms like 'reduced friction', 'increased throughput', 'systematized'."
        },
        "The Visionary (Growth & Scale)": {
            "focus_area": "Market Expansion, New Revenue Streams, Zero-to-One, Partnership Ecosystems, GTM Strategy.",
            "forbidden_words": "maintained, supported, assisted, coordinated, helped",
            "required_tone": "Bold, forward-looking, architectural. Think 'Series B CRO' or 'GTM Architect'.",
            "output_style": "Emphasize growth multiples, market creation, and strategic vision. Use terms like 'scaled', 'launched', 'architected'."
        },
        "The Technologist (Stack & Architecture)": {
            "focus_area": "Tech Stack Integration, Automation, API Workflows, Python/GenAI Implementation, Data Pipelines.",
            "forbidden_words": "negotiated, managed relationships, soft skills, team player",
            "required_tone": "Technical, systematic, engineering-first. Think 'Solutions Architect' or 'Staff Engineer'.",
            "output_style": "Emphasize technical implementation, system design, and tooling. Use terms like 'engineered', 'deployed', 'automated'."
        }
    }
    
    # Get persona config or default to Visionary
    config = persona_configs.get(target_persona, persona_configs["The Visionary (Growth & Scale)"])
    
    # 2. The System Instruction (The "Basin Protocol")
    # Deep Recon Logic Injection
    if use_deep_recon:
        output_instructions = """
Return ONLY valid JSON with exactly these keys:

{
  "strategic_dossier": {
    "bleeding_neck": "Identify the #1 expensive problem they are trying to fix (e.g., Churn, Low Pipeline, Compliance Risk).",
    "buyer_persona": "Analyze the hiring manager's psyche: 'Risk-Averse Gatekeeper' vs 'Velocity-Obsessed Founder'.",
    "the_landmine": "What is the one thing the candidate must NOT say? (e.g., 'I like slow processes')."
  },
  "gap_analysis": "Markdown formatted analysis with the 3 pain points detected and how the resume addresses each",
  "summary": "A 3-4 sentence professional summary that directly addresses the pain points. Start with role title. Use active voice. Include at least one metric.",
  "email_blurb": "A 'Sniper' email/DM (150 words). HOOK: Address 'The Bleeding Neck'. PROOF: Cite specific Resume metric. CLOSE: Specific 'Strategy Drop'.",
  "key_bullets": ["3-5 tailored bullet points from the resume that best prove ability to solve the pain points"]
}
"""
    else:
        output_instructions = """
Return ONLY valid JSON with exactly these keys:

{
  "gap_analysis": "Markdown formatted analysis with the 3 pain points detected and how the resume addresses each",
  "summary": "A 3-4 sentence professional summary that directly addresses the pain points. Start with role title. Use active voice. Include at least one metric.",
  "email_blurb": "A 150-word max 'Sniper' email/DM to the hiring manager. Format:\\nSubject: [Compelling subject line]\\n\\n[Opening hook referencing their specific pain]\\n[Value: specific project/outcome that solves it]\\n[Close: 'Worth a brief exchange?']",
  "key_bullets": ["3-5 tailored bullet points from the resume that best prove ability to solve the pain points"]
}
"""

    output_format_section = f"""
═══════════════════════════════════════════════════════════════
OUTPUT FORMAT (STRICT JSON)
═══════════════════════════════════════════════════════════════

{output_instructions}

DO NOT include any text outside the JSON object. DO NOT use markdown code blocks around the JSON.
"""
    
    # Reassemble the final system prompt with the variable section
    system_prompt = f"""You are 'Basin', an Executive Career Architect and GTM Strategist for Basin & Associates.

Your goal is to translate technical competence into commercial value using the "Zero-to-One" framework.

═══════════════════════════════════════════════════════════════
THE BASIN PHILOSOPHY
═══════════════════════════════════════════════════════════════

1. **Systems > Hires:** We don't just 'manage teams'; we build 'engines' and 'workflows'.
2. **Signal > Noise:** Do not use fluff. Every bullet point must have a Metric or an Outcome.
3. **High Agency:** Use active verbs (Built, Scaled, Engineered, Architected). Never use passive verbs (Responsible for, Helped with).
4. **Architecture > Activity:** Show systems thinking, not task completion.

═══════════════════════════════════════════════════════════════
YOUR TASK
═══════════════════════════════════════════════════════════════

1. **Analyze the JD:** Extract the top 3 'Commercial Pain Points' the company is trying to solve.
   Examples: High Churn, Low Pipeline, Data Mess, No US Market Presence, Manual Processes.

2. **Map the Resume:** Find the candidate's specific skills/experience that directly solve those pains.
   DO NOT INVENT FACTS. Only use evidence from the Source of Truth (Master Resume).

3. **The Pivot:** Rewrite the Professional Summary and Key Bullets to bridge the gap.
   Every statement must prove the candidate can solve the identified pain points.

{ "4. **Strategic Recon:** Generate the 'Bleeding Neck' analysis and 'Sniper Pitch' logic." if use_deep_recon else "" }

═══════════════════════════════════════════════════════════════
CONSTRAINTS (THE BASIN STANDARD)
═══════════════════════════════════════════════════════════════

- **Target Persona:** {target_persona}
- **Focus Area:** {config['focus_area']}
- **Forbidden Words:** {config['forbidden_words']}
- **Required Tone:** {config['required_tone']}
- **Output Style:** {config['output_style']}

{output_format_section}
"""

    # 3. The User Input (The Data)
    user_content = f"""═══════════════════════════════════════════════════════════════
CANDIDATE MASTER RESUME (Source of Truth)
═══════════════════════════════════════════════════════════════

{resume_text}

═══════════════════════════════════════════════════════════════
TARGET JOB DESCRIPTION (The Signal)
═══════════════════════════════════════════════════════════════

{job_description}

═══════════════════════════════════════════════════════════════
INSTRUCTION
═══════════════════════════════════════════════════════════════

Perform the full Basin Protocol analysis.
Output ONLY valid JSON matching the specified format.
Ensure the summary sounds human and conversational, not robotic.
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]


def get_persona_options() -> list:
    """
    Returns the available persona options for the UI.
    
    Returns:
        list: Persona option strings
    """
    return [
        "The Operator (Process & Efficiency)",
        "The Visionary (Growth & Scale)",
        "The Technologist (Stack & Architecture)"
    ]


def get_persona_description(persona: str) -> str:
    """
    Returns a brief description of what each persona optimizes for.
    
    Args:
        persona: The selected persona string
        
    Returns:
        str: Description of the persona's focus
    """
    descriptions = {
        "The Operator (Process & Efficiency)": "Optimizes for: Ops Leaders, Trust & Safety, Revenue Operations, Data Quality roles.",
        "The Visionary (Growth & Scale)": "Optimizes for: GTM roles, Growth, Sales Leadership, Startup CxO positions.",
        "The Technologist (Stack & Architecture)": "Optimizes for: Solutions Architects, Technical PM, Platform Engineering roles."
    }
    return descriptions.get(persona, "")
