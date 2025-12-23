
import sqlite3
import re

# LinkedIn People Data Block - Batch 4
DATA = """
James Bisordi
James Bisordi  • 1st
Senior Technical Recruiter @ Meta
San Francisco Bay Area
Message
Current: I work directly with our hiring partners to build strategies and roadmaps to achieve their hiring needs
6K followers

Melanie de Avellar
Melanie de Avellar  • 1st
Human Resources Manager | SHRM-CP | AWI-CH
San Francisco, California, United States
Message
Past: Manage the recruitment processes by partnering with hiring managers to define the recruitment needs and develop a strategic plan, including job description...

Ha Kwan
Ha Kwan • 1st
Chief People Officer / Head of People / Executive Search Consultant / Executive Coach
San Francisco, California, United States
Message
Current: Talent Acquisition Consulting: Retained and contingency searches, recruiting high profile roles, high volume recruiting, recruiting organizational design, recruiting and...

Kristin Kelley
Kristin Kelley  • 1st
Talent Acquisition Senior Manager - Federal Civilian Group at General Dynamics Information Technology
Washington, District of Columbia, United States
Message
About: Experienced IT Recruiter, performing full life-cycle recruiting in the Government and Commercial arena

Tami Van Wazer
Tami Van Wazer  • 1st
Technical Recruiter - Hiring top Engineering/Tech talent in the Chicagoland area (ask me about our openings) tvanwazer@sterling-engineering.com
Greater Chicago Area
Message
Past: Work directly with hiring managers to understand their needs; isolate cultural, personality, and technical requirements;...
11K followers

Katherine Ciaccio
Katherine Ciaccio • 1st
Senior Talent Acquisition Specialist at Wisk Aero
San Francisco Bay Area
Message
About: ...Partner with management on hiring needs, defining job requirements, postings, candidate screening/ recommendation, interviewing,...

Winston Thompson
Winston Thompson  • 1st
Recruiter | Sourcer | Talent Acquisition |  Sourcing Strategist
Flower Mound, Texas, United States
Message
Past: ...blockers based on historical data, utilizing role-specific market research to influence changes within our Hiring Team at the initial interview stage

Oriole Huang
Oriole Huang  • 1st
Global Sales Recruiting Leader @ Apple
Menlo Park, California, United States
Message
Current: - Partner directly with senior sales executives and functional leaders to define hiring plans, strategies, and talent mapping initiatives

Amery Zhen
Amery Zhen  • 1st
Senior Technical Recruiter
Oakland, California, United States
Message
Past: - Collaborate with hiring managers on writing job descriptions and advising on best practices...

Charity Navarre
Charity Navarre  • 1st
Talent Acquisition Manager at Ultimate Staffing Services
Portland, Oregon Metropolitan Area
Message
Current: ...we are Roth Staffing Companies, a culture-first staffing firm providing temporary, temporary-to-hire, direct hire, executive search, and strategic account services (On-Premise, MSP, VMS, 1099,...

Kelli Presto
Kelli Presto  • 1st
Building teams at Speak | Talent Acquisition Leader
San Francisco, California, United States
Message
About: ...processes into proactive, data-driven strategies that keep pace with growth and maintain high hiring standards
10K followers

Angela Bertolini (she/her)
Angela Bertolini (she/her)  • 1st
Sr Director of Talent Acquisition @ Lightmatter
Newport Beach, California, United States
Message
Past: I am a trusted advisor to C-Suite leaders and hands-on partner to client hiring managers
9K followers

Chris Jackson
Chris Jackson  • 1st
Founding Director | Helping top UK & US tech companies secure exceptional talent 🚀
St Albans, England, United Kingdom
Message
About: ✅ We manage the entire hiring process, minimizing disruption for you

Yelena Golovko
Yelena Golovko  • 1st
Sr. Biometrics Recruiter at Advanced Clinical
San Francisco, California, United States
Message
Current: Partner closely with client hiring managers and executive team

Samuel S James
Samuel S James  • 1st
People-Centered. Results-Driven. Talent Leader Igniting Success through DEI & Strategic Hiring! Talent Acquisition Maverick & DEI Advocate | Driving Client Success & Team Growth Across NA
Dublin, California, United States
Message
Current: ...is central to my work; I act as a trusted advisor, aligning our team’s efforts to meet their hiring objectives effectively
11K followers

Sahil Takkar
Sahil Takkar  • 1st
Head | Global Talent Acquisition & Recruitment Leader | Architect of High-Performance Teams | Bulk Hiring | MSP & Vendor Management | Key Account Growth, P&L Oversight | Driving Talent Strategies & Business Growh
Noida, Uttar Pradesh, India
Message
Current: ...and teams to consistently meet and exceed KPIs, including time-to-fill, offer acceptance rate, and hiring manager satisfaction
30K followers

Ronaq Lakdawala
Ronaq Lakdawala  • 1st
Executive Director
Miami-Fort Lauderdale Area
Message
Skills: Recruiting, Corporate Recruiting, Staffing Services
6K followers

Jessica Lokumkiattikul
Jessica Lokumkiattikul  • 1st
Talent @ Assort Health 🏳️‍🌈 | Agentic Voice AI for Patient Healthcare
San Francisco Bay Area
Message
Current: ...the industry's leading voice AI agents that make exceptional healthcare more accessible, and we’re hiring across all orgs
5K followers

Paul Ravetti
Paul Ravetti  • 1st
Recruiting Globally
Scottsdale, Arizona, United States
Message
Current: I partnered with Hiring Managers to ensure I provided well qualified and screened candidates

David DiBella
David DiBella  • 1st
Corporate Recruiter at 24 Seven Inc.
New York, New York, United States
Message
Current: 24 Seven is a strategic staffing & recruiting firm that identifies, recruits & secures top marketing, interactive, digital & creative talent

David Kiss
David Kiss  • 1st
Senior Talent Partner- GTM @ SoftwareONE - Apple, VMware, 24/7ai
Greensboro--Winston-Salem--High Point Area
Message
Past: ...and leading the full recruitment process from identifying candidates, screening, through to hiring. Working with Hiring Managers and other Talent Acquisition Partners filling both Sales, Engineering and...
12K followers

Jonathan "Johnny" Fantini
Jonathan "Johnny" Fantini  • 1st
Helping you hire for hard-to-fill positions.
Greater Pittsburgh Region
Message
Current: Give us a call at 724-816-7762 to see how we can help solve your hiring needs

Brandon Hilten
Brandon Hilten  • 1st
Senior Recruiter, National Field Talent Acquisition at Comcast
West Palm Beach, Florida, United States
Message
Current: Represent Company at various Job Fairs, Hiring Events, Military Career Events, Internship Programs, Resume/Interviewing presentations

Bryan McKinsey
Bryan McKinsey  • 1st
Regional Talent Acquisition Specialist II - Regions 3 & 4
Dallas, Texas, United States
Message
Past: ...Responsible for day to day interaction with client Hiring Managers and HR business partners

Kevin Aveson
Kevin Aveson  • 1st
Talent - Pebble
San Ramon, California, United States
Message
Current: - Leading Recruiting efforts for entire company - Vehicle Engineering, Product, TPM, Technicians, Sales/GTM...
16K followers

Jennifer O'Gara
Jennifer O'Gara  • 1st
Impossible is just an opinion.
West Hartford, Connecticut, United States
Message
Past: Business Development and Full-Cycle Recruiting for VC-backed startups with a focus on GTM, Finance and Operations leadership roles
19K followers

Allie Montes
Allie Montes  • 1st
Talent Acquisition Leader
Vancouver, Washington, United States
Message
About: ...One of the first steps in building out equitable and inclusive workforces is hiring people who support those goals

Alyssa Fidel
Alyssa Fidel  • 1st
TA Leader @ Zoom, cleaning enthusiast, yoga teacher, aspiring pickleballer, wannabe outdoorsy
Denver, Colorado, United States
Message
Current: ...compensation and talent market trends to maintain competitive positioning, particularly for our AI hiring efforts

Krishna Kant
Krishna Kant  • 1st
Managing Partner @ Jobma AI
Frisco, Texas, United States
Message
Current: Our digital evaluation platform is transforming how organizations discover and hire talent, offering video and audio interviewing, automated assessments, and more, all powered by AI

Lee Elkinson
Lee Elkinson  • 1st
Chief Executive Officer at Sentech Services, Inc. a Job&Talent Company
Miami-Fort Lauderdale Area
Message
Current: Our National Recruiting Center is located in Troy, Michigan serving branch offices and onsite clients across the United...
14K followers
"""

def parse_and_ingest_people_batch4():
    conn = sqlite3.connect("basin_nexus.db")
    cursor = conn.cursor()
    
    lines = [l.strip() for l in DATA.split('\n') if l.strip()]
    filtered_lines = []
    
    ignore_phrases = ["People", "Actively hiring", "Locations", "Current companies", "All filters", "Reset", 
                      "Hiring? Find people", "Get matched", "Get started", "Are these results helpful?",
                      "Your feedback", "View my services", "About", "Accessibility", "Help Center",
                      "Privacy & Terms", "Ad Choices", "Advertising", "Business Services", "Get the LinkedIn app", "More",
                      "Previous", "Next", "Page ", "1st", "2nd"]
    
    for line in lines:
        if line == "Message":
            filtered_lines.append(line)
            continue
            
        if any(phrase in line for phrase in ignore_phrases):
             continue
             
        if line.isdigit() or len(line) < 3:
            continue
            
        filtered_lines.append(line)
        
    people = []
    i = 0
    
    while i < len(filtered_lines):
        line = filtered_lines[i]
        
        if line == "Message":
            try:
                location = filtered_lines[i-1]
                headline = filtered_lines[i-2]
                name_line = filtered_lines[i-3]
                
                # Name
                if "•" in name_line:
                    name = name_line.split("•")[0].strip()
                elif i >= 4 and "•" in filtered_lines[i-4]:
                    name = filtered_lines[i-4].split("•")[0].strip()
                else:
                    name = name_line
                
                # Company
                company = ""
                headline_clean = headline
                
                if " at " in headline_clean:
                    company = headline_clean.split(" at ")[-1].split("|")[0].strip()
                elif " @ " in headline_clean:
                    company = headline_clean.split(" @ ")[-1].split("|")[0].strip()
                elif " with " in headline_clean:
                    company = headline_clean.split(" with ")[-1].split("|")[0].strip()
                elif " from " in headline_clean:
                    # Rare but happens
                    company = headline_clean.split(" from ")[-1].split("|")[0].strip()
                
                # Deal linkage
                deal_id = None
                cursor_check = conn.cursor()
                if company:
                    cursor_check.execute("SELECT id FROM crm_deals WHERE company LIKE ? OR company LIKE ? LIMIT 1", (f"%{company}%", f"{company}%"))
                    row = cursor_check.fetchone()
                    if row:
                        deal_id = row[0]
                
                # Notes
                notes = ""
                if i+1 < len(filtered_lines):
                    potential_note = filtered_lines[i+1]
                    if not potential_note.startswith("Message") and "followers" not in potential_note:
                        notes = potential_note
                        
                people.append({
                    "name": name,
                    "title": headline,
                    "company": company, 
                    "location": location,
                    "deal_id": deal_id,
                    "notes": notes
                })
            except IndexError:
                pass
        i += 1
        
    print(f"Found {len(people)} people. Inserting...")
    
    inserted = 0
    for p in people:
        cursor.execute("SELECT id FROM crm_contacts WHERE name = ?", (p['name'],))
        if cursor.fetchone():
            print(f"Duplicate skipped: {p['name']}")
            continue
            
        cursor.execute("""
            INSERT INTO crm_contacts (name, role, company, contact_type, status, relationship_strength, notes, channel, deal_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p['name'], 
            p['title'][:100], 
            p['company'], 
            "Recruiter" if "Recrut" in p['title'] or "Talent" in p['title'] or "Hiring" in p['title'] else "Peer",
            "1. Connected",
            1, 
            f"Location: {p['location']}\nNote: {p['notes']}",
            "LinkedIn",
            p['deal_id']
        ))
        inserted += 1
        
    conn.commit()
    conn.close()
    print(f"Successfully inserted {inserted} new contacts.")

if __name__ == "__main__":
    parse_and_ingest_people_batch4()
