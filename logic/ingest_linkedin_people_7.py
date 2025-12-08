
import sqlite3
import re

# LinkedIn People Data Block - Batch 7 (GTM/Cybersecurity/Recruiters)
DATA = """
Brian Burnett
Director of Enterprise Security | CC, SOC for Cybersecurity EnCE, ACE, CCFE
Connected on October 22, 2025

Igor Zaika
Chief Technology Officer at Sensiba LLP | Infrastructure, Security & IT Operations
Connected on October 21, 2025

César Martínez
|Consultoria Ciberseguridad a Empresas|OT|Scada| Proyectos de Informática|Consultoria Sap|Administración de Empresas|
Connected on October 21, 2025

Viktor Farcic
Developer Advocate at Upbound
Connected on October 21, 2025

Alex Kremer
Teaching sales professionals how to transform their inner game while crushing quota / Host of Top 100 “The Rising Leader” podcast / Ex-Microsoft, Outreach, & DocuSign
Connected on October 20, 2025

Yadel Karim
👉 Reactivated 100,000+ “Inactive” Leads for 20+ B2C Companies (April 2023 – September 2025) 👈 | Founder at Mabiat — From Lead to Loyal Customer, Automation that Fuels Cash Flow
Connected on October 20, 2025

Judah Rosen
Experienced B2B Ent Growth Leader | Helped Generate Millions in ARR | Proven GTM Strategist | Executive Relationship Builder | Mentor
Connected on October 20, 2025

Fjolla Shaqiri
Director of Business Development EMEA & USA
Connected on October 20, 2025

Eric Svetcov
CTO/CSO, CISO Advisor, Board Advisor, CCISO Certification Author, Master CCISO Instructor, International Speaker
Connected on October 20, 2025

Jason Shearer
Chief Enterprise Architect | RISE with SAP | Innovation, AI & Cloud Transformation
Connected on October 17, 2025

Cooper Cash
VP of IT Operations at North Carolina’s Electric Cooperatives
Connected on October 17, 2025

Ryan Howard
Co-Founder @ Thrivve
Connected on October 16, 2025

Robert Stokes, GISP
IT Director with GIS expertise and IT management skills
Connected on October 15, 2025

Patrick Bulmer
CoFounder & Partner at Halo Consulting
Connected on October 15, 2025

James Wilson
Conference Group Director at AKJ Associates
Connected on October 15, 2025

Kumar Thanabalan
Senior Search Consultant - ITOPs & Cyber Security
Connected on October 14, 2025

Jon Bowles
Helping business owners save more, stress less, and keep their best people
Connected on October 9, 2025

Angelo V.
Helping GTM orgs rethink their pipegen strategy
Connected on October 8, 2025

Matheus Souza
Senior Account Executive | Edge Computing & Cybersecurity
Connected on October 8, 2025

Agustín Morrone
CEO @Vintti | The bridge to hire LATAM talent for U.S. companies
Connected on October 6, 2025

David Fox
CRO & Growth Architect | Scaling SaaS + AI $10M → $100M+ ARR | Founder, AscendRevenue
Connected on October 2, 2025

Sumit Nautiyal
GTM & RevOps Leader | Helping B2B Companies Scale from $2M→$20M ARR | 2.3x Avg Revenue Growth in 6 Months | AI Sales Systems | Economic Times Speaker
Connected on September 30, 2025

Chris Kielthy
AI & Robotics Enthusiast, GTM Headhunter
Connected on September 30, 2025

Josh Gordon
Founder + CEO @ JAC Consulting - GTM Recruitment + Startup Advisor
Connected on September 30, 2025

Arthur Orav
Connecting the Dots Between People and Progress
Connected on September 30, 2025

Ken Palafox
CoFounder ECSE/ eCommerce Growth Hacker/ Sales & Karaoke Rockstar
Connected on September 29, 2025

Ashwin Pillai
Data Scientist at Teradata with expertise in Gen AI solutions | Agentic AI
Connected on September 29, 2025

Elina Papernaya
Head of GTM at Alta
Connected on September 25, 2025

David Marom
Sales Leadership | AltaHQ | Founding Member
Connected on September 25, 2025

Beth Francis
Helping businesses transform with Salesforce’s Agentic AI | Salesforce Adoption Guru | Salesforce-certified Partner (Integration Services & Apps)
Connected on September 25, 2025

Dave Keenan
Helping people understand wellbeing — not just practise it.
Connected on September 25, 2025

Nomaan Khan
Building @ SBL – Enterprise-Level Operations & Strategy
Connected on September 25, 2025

Alexia Pauling
Connecting Entrepreneurs to Business Ownership
Connected on September 24, 2025

Nehitha Thummanapelly
Client Success Partner @ SecondBrainLabs – We Build Your AI Agent That Books Sales Calls While You Sleep || Associate software Engineer at Accenture
Connected on September 23, 2025

Richard Martinez
Investor Relations @ Sunset Ventures | Business Administration & Mathematical Finance @ USC Marshall
Connected on September 23, 2025

Oumar Kadjalma Touré
U.S. Ambassador. Director General of the Affairs and Diplomatic Advisor, The White House EOP
Connected on September 22, 2025

Anant Goel
Building future tech with Agentic AI | RegASK™ | ArtificiaI Intelligence
Connected on September 22, 2025

Peter Mollins
Marketing @ Nooks | 💟 outbound? Let's connect!
Connected on September 18, 2025

John Nejedly
Wealth Management Advisor: Building Clarity and Confidence in your Financial Future - with a Tax-Aware, Risk-Managed Approach
Connected on September 18, 2025

Ivana Vucenovic
Conscious Leadership & Mindset Mentor | Guiding People to Live, Lead & Create with Joy, Clarity & Ease | Founder of The Ease Revolution™
Connected on September 18, 2025

Ivan Melia
Identity, Access, and Developer Experience at StrongDM
Connected on September 17, 2025

Asel Tursun
Unlocking the sky
| Building autonomous first responders to save lives | CEO @ ARC | Public Safety | Manufacturing | Physical AI
Connected on September 16, 2025

Md Sayeed Khan
🏆 Founder 🏆 Web Developer 🏆 700+ Projects 🏆 WordPress & Wix Expert 🏆 Top-Rated Upwork Freelancer 🚀 Helping Businesses Grow Online with High-Impact Websites & Social Media Marketing
Connected on September 16, 2025

Tara Sakhuja
Founder at Data Dumpling AI | ex. Meta & Bumble Product Manager | Global Talent Visa Holder
Connected on September 15, 2025

Emil Jørgensen
Co-founder @ The Growth DNA | Clay Studio Partner
Connected on September 15, 2025

Abril Acosta
Business Consultant @ Vintti | The bridge to hire LATAM talent for U.S. companies | Star Wars fan | Cat Mom
Connected on September 15, 2025

Teresa Annibale
Sr. VP of Global Accounts | CRN Women of the Channel | Start-up Enthusiast | Community Outreach
Connected on September 15, 2025

Joshua Benoit
Growth & GTM @ <​oneaway​> | Helping B2B business generate revenue with outbound.
Connected on September 12, 2025

Matt Chubb
Head of Business Development @ ABM Alliance
Connected on September 12, 2025

Jessica Archer
Cybersecurity | Leadership | Sales | Advisor | Board Member | Mentor
Connected on September 11, 2025

Kevin Warner
Revenue Leader & Outbound Sales Mastermind | #PipelineCreator 💸💸
Connected on September 11, 2025

Neel Kamal
CEO @ AdamX | Become #1 on your buyer shortlist with AdamX
Connected on September 11, 2025

Yogesh Chandani
Vice President | Driving GenAI Talent & Solutions | AI Hiring | Business Growth through Innovation
Connected on September 11, 2025

Patrick Bleakley
Director at Reperio Human Capital, IT Search & Selection ✪ HIRING IN IRELAND & USA ✪ 🇮🇪🇺🇲
Ireland

Janet Lee
Co-Founder at Technique Talent | we help startups build winning teams
United States

Christine Covert
Talent Manager & Startup Growth Leader | AI • FinTech • Cyber | 0→1 Team Builder | GTM, Product & AI Recruiting | Former EY Consultant – Talent & Change Strategy
United States

Christian DeLancy
Staffing Lead, Google Cloud GTM at Google
San Francisco, California, United States

Samantha Leveston
Technical Recruiting @ Overstory🌲 | We're hiring! | Climate Tech
Greater Burlington Area

Crystal Petroski
Mother of 2 | 🔮Miracle Worker🦄 | Entrepreneur
Glastonbury, Connecticut, United States

Mark Sefaradi
Senior Recruiter | Sourcer | Talent Partner | Technical and GTM Hiring Expert
New York City Metropolitan Area
"""

def parse_and_ingest_people_batch7():
    conn = sqlite3.connect("basin_nexus.db")
    cursor = conn.cursor()
    
    # Aggressive filtering of UI noise
    ignore_phrases = ["People", "Actively hiring", "Locations", "Current companies", "All filters", "Reset", 
                "profile picture", "Message", "View my",
                "About", "Accessibility", "Help Center", "Privacy & Terms", "Ad Choices", "Advertising", "Business Services", "Get the LinkedIn app", "More",
                "Previous", "Next", "Page ", "1st", "2nd"]
    
    lines = [l.strip() for l in DATA.split('\n') if l.strip()]
    
    clean_lines = []
    for line in lines:
        if "profile picture" in line: continue
        if line == "Message": continue
        if any(x in line for x in ignore_phrases): continue
        clean_lines.append(line)
        
    people = []
    i = 0
    
    while i < len(clean_lines):
        line = clean_lines[i]
        
        # Heuristic: Name is usually short, no "|" or "@" typically (though not always)
        # Headline is usually long.
        
        name = line
        headline = ""
        location = ""
        
        if i + 1 < len(clean_lines):
             headline = clean_lines[i+1]
             
        # Check if headline is actually a "Connected on" date
        if "Connected on" in headline:
             # Then we are good.
             i += 2 # Skip Name and Headline
        elif "Connected on" in clean_lines[min(i+2, len(clean_lines)-1)]:
             # Name
             # Headline
             # Connected on
             i += 3
        else:
             # Maybe the Recruiter format (Name, Headline, Location)
             if i+2 < len(clean_lines):
                 location = clean_lines[i+2]
                 i += 3
             else:
                 i += 2

        # Extract Company
        company = ""
        headline_clean = headline
        if "@" in headline_clean:
             company = headline_clean.split("@")[1].split("|")[0].strip()
        elif " at " in headline_clean:
             company = headline_clean.split(" at ")[1].split("|")[0].strip()
        
        # Classification
        contact_type = "Peer"
        if "Recriter" in headline or "Talent" in headline or "Hiring" in headline or "Staffing" in headline:
            contact_type = "Recruiter"
        if "Founder" in headline or "Partner" in headline or "Director" in headline or "VP" in headline or "Head of" in headline or "CISO" in headline or "CRO" in headline or "CEO" in headline:
            contact_type = "VIP"  # New High Value Category

        if "GTM" in headline: contact_type += " (GTM)"
        if "Cyber" in headline or "Security" in headline: contact_type += " (Cyber)"

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
            "Imported from Batch 7 (GTM/Cyber/Recruiter)",
            "LinkedIn",
            p['deal_id']
        ))
        inserted += 1
        
    conn.commit()
    conn.close()
    print(f"Successfully inserted {inserted} new contacts.")

if __name__ == "__main__":
    parse_and_ingest_people_batch7()
