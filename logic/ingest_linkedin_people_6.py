
import sqlite3
import re

# LinkedIn People Data Block - Batch 6 (Mixed Connections & Recruiters)
DATA = """
Keith Langbo
Keith Langbo  • 1st
We help businesses attract, hire, and retain the right people . . . using AI and culture-first hiring | Founder & CEO @ Kelaca | Investor
London Area, United Kingdom
Message
Current: ...– Acting as an embedded extension of our clients’ HR and Talent Acquisition teams to manage the entire hiring lifecycle
12K followers

Justin McGann
Justin McGann  • 1st
Vice President of Delivery - Northeast
Greater Boston
Message
Current: ...Oversee end-to-end recruiting operations, workforce planning, and delivery execution to support complex enterprise demand across multiple...

Austin Sullivan
Austin Sullivan  • 1st
Account Manager at Pursuit - Helping high-growth companies hire elite sales and marketing talent - Tech, Medical, and B2B
Dallas-Fort Worth Metroplex
Message
About: If you're looking to hire the best sales and marketing talent, I'd love to connect

Lindsay Vane
Lindsay Vane  • 1st
Senior Recruiter at Navan | Snowflake, ServiceNow Alum
San Francisco Bay Area
Message
Current: ...Consulting, Account Management and Enterprise Customer Success teams - managing the entire hiring process from sourcing to offer acceptance

Angeli Marie Del Birut
Angeli Marie Del Birut • 1st
Staffing Speacialist at Hire Partnership
Boston, Massachusetts, United States
Message
Current: Coordinate and schedule interviews between candidates and hiring managers, ensuring smooth communication

Ross Mahaffey
Ross Mahaffey  • 1st
Director of Recruiting
United States
Message
About: Previous leadership at Uber refined skills in scalable hiring solutions
13K followers

Charity Mainwaring
Charity Mainwaring  • 1st
Sr. National Recruiter | Connecting Companies with Elite Talent | High Achiever | Optimist
United States
Message
Current: 5% of our hires came from passive, headhunted talent
9K followers

Andrew MacAskill
Andrew MacAskill  • 1st
Private Equity and Life Sciences Executive Search | CCO at Fraser Dove International | Speaker | Bestselling Author On a Mission to End Career Based Misery.
Hedge End, England, United Kingdom
Message
Current: ...and Executive Search for PE and Life Science organisations who want to focus on Quality of Hire.  Our business by numbers:...
113K followers

Justin Glaser
Justin Glaser  • 1st
Senior Recruiter at Instawork
Seattle, Washington, United States
Message
Current: We’re hiring around the world
12K followers

Britt Massing
Britt Massing  • 1st
President at The Staffing Resource Group / SRG Life Sciences / SRG Government Services
Tampa, Florida, United States
Message
Current: We are able to staff for contract, contract to hire, direct placement and executive search for the Medical and Scientific industries throughout the...

# --- RECENTLY ADDED CONNECTIONS SECTION ---

Aneel Suravarapu
Aneel Suravarapu
Sr. Systems Architect at USPS | DevOps | Platform Engineer | Azure 104 Administrator Certified | AWS Solutions Architect | CompTIA Cybersecurity Analyst CySA+ Certified
Connected on December 7, 2025
Message

Mirela Xhota
Mirela Xhota
GTM Lead at inTruth | Mentor | Ex- FT (Nikkei Inc),Thomson Reuters(TSX: TRI), Decidr (ASX: DAI), Freshworks(FRSH),QuickFee(ASX: QFE),First Advantage (Nasdaq:FA)| #emotionAI #web3 #biotech  |Advisor | Angel Investor| #GTM
Connected on December 4, 2025
Message

Kathy C. Nagamine
Kathy C. Nagamine
Sr. Associate Director @ Santa Clara University | Business Development and Marketing
Connected on December 4, 2025
Message

Arkaprava De
Arkaprava De
Engineering Lead at AWS SageMaker
Connected on December 4, 2025
Message

Aman Verjee, CFA
Aman Verjee, CFA
Founder / General Partner at Practical Venture Capital
Connected on December 3, 2025
Message

Craig Kaufman
Craig Kaufman
Sr. Assistant Dean for Marketing & Communications at the Leavey School of Business at Santa Clara University
Connected on December 3, 2025
Message

Hrick Kumar Jha
Hrick Kumar Jha
Co-Founder @ SolveJet | Building Custom Solutions & Agentic Systems to Replace Manual Workflows
Connected on December 3, 2025
Message

Punam .
Punam .
HubSpot CRM | RevOps Support | Marketing Ops | Email Marketing | Pipelines, Properties & Workflows | Open to Remote Roles
Connected on December 3, 2025
Message

Elaine Zhu
Elaine Zhu
Revenue Operations Leader | Strategy × Execution × Empathy | $6.5B+ Pipeline Impact | 44% Productivity Gain
Connected on December 3, 2025
Message

Sam Oh
Sam Oh
I help businesses turn cold outreach into 5+ monthly meetings using AI automation.
Connected on December 2, 2025
Message

Michael Rosenberg
Michael Rosenberg
Senior Recruiter & Sourcer | The Job Sauce | Expert in sourcing top talent across Software Engineering, AI/ML, Product, and Corporate functions
Connected on December 2, 2025
Message

Nicole Ceranna
Nicole Ceranna
Global Talent Acquisition Leader I Talent 100 Awardee
Connected on December 1, 2025
Message

Thalia Thompson 🌊
Thalia Thompson 🌊
Principal-GTM @ Coastal | High-Growth & VC-Backed Companies | Transformational Talent
Connected on December 1, 2025
Message

Logan Ross
Logan Ross
Account Executive @ Wiza 🔮
Connected on December 1, 2025
Message

Safina Sami
Safina Sami
Lead Recruiter @ Russell Tobin | President Club Winner 2023 and 2024
Connected on November 25, 2025
Message

Shaya Zirkind
Shaya Zirkind
Building Teams and Advancing Careers | Recruiter @ Supreme Talent
Connected on November 24, 2025
Message

Xan Marcucci
Xan Marcucci
I hire killer salespeople | Founder @ Confetti | Saleswoman 5ever | Professional Speaker
Connected on November 24, 2025
Message

Burach Goldklang
Burach Goldklang
Building Teams and Advancing Careers | Executive Recruiter @ Supreme Talent | The Gold Standard in Recruitment
Connected on November 20, 2025
Message

Mauk Pekelharing
Mauk Pekelharing
Founder BONDR | Business < Brand Development | Social Selling as a Service
Connected on November 19, 2025
Message

Sean Huang, MMIE
Sean Huang, MMIE
AI-Driven Precision for RevOps & GTM Success | YC Alum | Co-founder @Matidor.com
Connected on November 17, 2025
Message

Julia Chimisova 🇺🇦
Julia Chimisova 🇺🇦
GTM Recruitment Expert | Building high-performing AI/ML, HPC, Cloud Computing, Cyber Security sales teams
Connected on October 23, 2025
Message

Jody Geiger
Jody Geiger
I help GTM leaders cut through AI hype and turn it into revenue | 20 years scaling sales orgs at Apple, Klue, Galvanize | Co-Founder, AI Sales Studio | Stop playing with AI, start executing
Connected on October 27, 2025
Message

Andreas Renner
Andreas Renner
Global Head of Enterprise Data & Analytics at Cognite
Connected on October 27, 2025
Message

"""

def parse_and_ingest_people_batch6():
    conn = sqlite3.connect("basin_nexus.db")
    cursor = conn.cursor()
    
    lines = [l.strip() for l in DATA.split('\n') if l.strip()]
    filtered_lines = []
    
    # Aggressive filtering of UI noise
    ignore_phrases = ["People", "Actively hiring", "Locations", "Current companies", "All filters", "Reset", 
                "profile picture", "Connections", "Connected on", "Message", "View my",
                "About", "Accessibility", "Help Center", "Privacy & Terms", "Ad Choices", "Advertising", "Business Services", "Get the LinkedIn app", "More",
                "Previous", "Next", "Page ", "1st", "2nd"]
    
    people = []
    i = 0
    lines = [l for l in lines if not any(ip in l for ip in ["profile picture", "Connected on", "Message"])]

    # New parsing strategy for the "Connection List" style format in the second half of paste
    # Format: 
    # Name
    # Name (duplicate)
    # Headline
    # ...
    
    # We will iterate and look for Name-like lines followed by detailed headlines
    
    count = 0 
    # To handle the mixed format (first half detailed, second half list), we use a regexheuristic
    # But since the data above is cleaned by me in the `lines` list to remove "Message" and "Connected on", 
    # we have: Name -> Name -> Headline.
    
    # Actually, looking at the raw text, the "Recently added" section has:
    # Aneel Suravarapu’s profile picture (Ignored)
    # Aneel Suravarapu (Keep)
    # Sr. Systems Architect... (Keep)
    # Connected on... (Ignored)
    # Message (Ignored)
    
    # So we are left with pairs of Name -> Headline mostly.
    
    clean_lines = []
    for line in DATA.split('\n'):
        line = line.strip()
        if not line: continue
        if "profile picture" in line: continue
        if "Connected on" in line: continue
        if line == "Message": continue
        if any(x in line for x in ignore_phrases): continue
        clean_lines.append(line)
        
    # Now valid lines should be Name, Headline order essentially
    # Some names appear twice in the raw text, we need to dedup
    # Actually most names appear once in my `clean_lines` logic if I filtered `profile picture` line.
    
    j = 0
    while j < len(clean_lines) - 1:
        name = clean_lines[j]
        headline = clean_lines[j+1]
        
        # Heuristic check: is 'headline' actually a name? 
        # If 'headline' is very short and title-cased, it might be a duplicate name line
        if name == headline:
            j += 1
            if j+1 < len(clean_lines):
                headline = clean_lines[j+1]
            else:
                break
                
        # Extract Company
        company = ""
        headline_clean = headline
        separators = [" at ", " @ ", " with ", " from ", " | "]
        # Simple extraction
        if "@" in headline_clean:
             company = headline_clean.split("@")[1].split("|")[0].strip()
        elif " at " in headline_clean:
             company = headline_clean.split(" at ")[1].split("|")[0].strip()
        
        # Classification
        contact_type = "Peer"
        if "Recruiter" in headline or "Talent" in headline or "Hiring" in headline or "Staffing" in headline:
            contact_type = "Recruiter"
        if "Founder" in headline or "Partner" in headline or "Investor" in headline or "CEO" in headline:
            contact_type = "VIP"  # New High Value Category

        # Deal Linkage
        deal_id = None
        if company:
            cursor_check = conn.cursor()
            cursor_check.execute("SELECT id FROM crm_deals WHERE company LIKE ? OR company LIKE ? LIMIT 1", (f"%{company}%", f"{company}%"))
            row = cursor_check.fetchone()
            if row:
                deal_id = row[0]

        people.append({
            "name": name,
            "title": headline,
            "company": company,
            "type": contact_type,
            "deal_id": deal_id
        })
        j += 2 # Skip pair

    print(f"Found {len(people)} possible contacts. Inserting...")
    
    inserted = 0
    for p in people:
        # Check Dupes
        cursor.execute("SELECT id FROM crm_contacts WHERE name = ?", (p['name'],))
        if cursor.fetchone():
            continue
            
        cursor.execute("""
            INSERT INTO crm_contacts (name, role, company, contact_type, status, relationship_strength, notes, channel, deal_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p['name'], 
            p['title'][:100], 
            p['company'], 
            p['type'],
            "1. Connected",
            1, 
            "Imported from Batch 6 (Recent Connections)",
            "LinkedIn",
            p['deal_id']
        ))
        inserted += 1
        
    conn.commit()
    conn.close()
    print(f"Successfully inserted {inserted} new contacts.")

if __name__ == "__main__":
    parse_and_ingest_people_batch6()
