
import sqlite3
import re

# LinkedIn People Data Block - Batch 2
DATA = """
Stephanie Barbu
Stephanie Barbu  • 1st
Talent Acquisition Leader | People-First Manager | Former Meta & Google
Austin, Texas, United States
Message
Current: ...interview guides, and resources that bring clarity, alignment, and confident decision-making to hiring teams
4K followers

Bernadet Kalta
Bernadet Kalta  • 1st
We’re HIRING 🚀
San Jose, California, United States
Message
Past: ...Staffing is a global executive search firm connecting rock star job candidates with all types of hiring managers

Tom Molina
Tom Molina • 1st
Sr Recruiter - Available for new job opportunities.
Mountain View, California, United States
Message
About: Specialties:Technical Recruiter, Business Development Manager, Recruiting Manager/ Project Engineering

Daniel Ross
Daniel Ross  • 1st
CHRO & SVP Human Resources at Day & Zimmermann
Philadelphia, Pennsylvania, United States
Message
Past: Maintain organized, accurate documentation on all candidates, searches, hiring manager interactions and other recruiting activities to ensure OFCCP compliance

Orion Drow
Orion Drow  • 1st
Life Sciences Hiring Consultant
San Diego, California, United States
Message
Past: Give me a call at (858) 866-8676 for help with hiring or job searches, or check us out at www

Paul Stevens
Paul Stevens  • 1st
Senior Staffing Consultant - RETIRED
Pleasanton, California, United States
Message
About: Senior contract staffing professional, providing full cycle on-site recruiting services to leading technology companies in the SF Bay Area

Karl Kizer
Karl Kizer  • 1st
Senior Recruiter at Bloom Energy
Santa Clara, California, United States
Message
About: We are hiring! Please check LinkedIn for all of our amazing jobs at Bloomenergy

Kim Tran-Young
Kim Tran-Young  • 1st
Senior Director, Talent Acquisition @ Pinterest
San Jose, California, United States
Message
Past: ...- Employee referral program management - Hiring coordination for domestic and international hiring – interview scheduling, offer generation, new...
15K followers

Chris Adams
Chris Adams  • 1st
Talent (ex-Uber, Google, Venture)
San Francisco Bay Area
Message
Skills: Hiring, Recruiting, Corporate Recruiting

Kaycee Satava
Kaycee Satava  • 1st
Senior Recruiter
Portland, Oregon, United States
Message
Current: ...LinkedIn Recruiter Indeed

Marisol Estrada
Marisol Estrada  • 1st
Recruitment Specialist🧿
Greater Chicago Area
Message
Past: Responsible for the day to day activities in the branch/On – site recruitment, hiring, maintaining candidate pool, fulfillment of all job orders that are submitted by our clients,...
876 followers

Andrew Cesarz
Andrew Cesarz  • 1st
Talent Acquisition Leader @ Airwallex
San Francisco, California, United States
Message
About: ...and lead Recruiting teams that provide the best recruiting experience possible for candidates and hiring managers

Sara Gutierrez
Sara Gutierrez  • 1st
Senior Technical Recruiter @ Meta | SHRM-CP | ex-Salesforce
San Francisco Bay Area
Message
Past: Partnered with Recruiters and Hiring Managers to align on hiring needs while maintaining a positive candidate experience

Sabrina Parnett
Sabrina Parnett  • 1st
Senior National Executive Recruiter           "KNOW us before you NEED us!"
Long Beach, California, United States
Message
About: Leveraging my extensive network and expertise, I provide guidance and support throughout the hiring process as a Senior National Executive Recruiter
2K followers

Khanh Ly
Khanh Ly  • 1st
Talent Consultant | Technical Recruitment | HR Operations
San Francisco, California, United States
Message
Past: Optimize recruiting operations by integrating data-driven hiring insights, improving diversity hiring initiatives, and refining employer branding strategies

Becki Clague
Becki Clague • 1st
Owner, California People Search
San Mateo, California, United States
Message
Past: Always focused on the needs of my clients, I proactively  sought additional communication with hiring managers and senior management to ensure alignment with regard to staffing plans, candidate...

Maria Di Re
Maria Di Re • 1st
Recruiting and Training Manager | Hiring, onboarding, training, compliance, HR operations
Greater Seattle Area
Message
Past: Consulted and collaborated with clients, hiring managers, and key stakeholders to understand hiring needs, define and post job requirements, and establish recruiting strategies

Ashley Bannias
Ashley Bannias  • 1st
VP, Talent Acquisition @ Flux Resources & Mathys + Potestio
Surprise, Arizona, United States
Message
Current: Currently leading full Recruiting function for both of our staffing brands, Flux Resources & Mathys + Potestio

Sam Guzman
Sam Guzman  • 1st
Director, Technical Recruiting at Instacart 🥕 (Pronouns: he/him)
San Diego Metropolitan Area
Message
Past: ...through various channels, screening candidates, scheduling all interviews, managing candidates and hiring teams throughout the interview process, and extending/ negotiating offers

Austin McGill
Austin McGill • 1st
Workforce Partners & Lineman Network
San Diego Metropolitan Area
Message
About: Especially if your hiring needs vary throughout the year or if your business operates without an HR department or in-house...
3K followers
"""

def parse_and_ingest_people_batch2():
    conn = sqlite3.connect("basin_nexus.db")
    cursor = conn.cursor()
    
    # Simple strict parsing for this clean format
    # Name
    # Name • 1st
    # Headline
    # Location
    # Message
    # Notes
    
    lines = [l.strip() for l in DATA.split('\n') if l.strip()]
    filtered_lines = []
    
    # We ignore standard UI junk but keep "Message" as an anchor
    ignore_phrases = ["People", "Actively hiring", "Locations", "Current companies", "All filters", "Reset", 
                      "Hiring? Find people", "Get matched", "Get started", "Are these results helpful?",
                      "Your feedback", "View my services", "About", "Accessibility", "Help Center",
                      "Privacy & Terms", "Ad Choices", "Advertising", "Business Services", "Get the LinkedIn app", "More",
                      "Previous", "Next", "Page 1"]
    
    for line in lines:
        if line in ["1st", "2nd", "Message", "Following", "Connect"]:
             filtered_lines.append(line) # Keep anchors
             continue
             
        if line.isdigit() or line.startswith("Page ") or line in ["Previous", "Next"]:
            continue
            
        if any(phrase in line for phrase in ignore_phrases):
             continue
             
        filtered_lines.append(line)
        
    people = []
    i = 0
    
    while i < len(filtered_lines):
        line = filtered_lines[i]
        
        # Anchor on "Message" or "Connect"
        if line == "Message":
            try:
                location = filtered_lines[i-1]
                headline = filtered_lines[i-2]
                name_line_degree = filtered_lines[i-3]
                
                # Check structure
                if "• 1st" in name_line_degree or "•" in name_line_degree:
                    name = name_line_degree.split("•")[0].strip()
                    
                    # Extract Company
                    company = ""
                    if " at " in headline:
                        company = headline.split(" at ")[-1].split("|")[0].strip()
                    elif " @ " in headline:
                        company = headline.split(" @ ")[-1].split("|")[0].strip()
                    elif " with " in headline:
                        company = headline.split(" with ")[-1].split("|")[0].strip()
                    elif "We’re HIRING" in headline:
                         company = "Hiring (Unknown)"
                    elif "Available" in headline:
                         company = "Open to Work"
                    
                    # Notes
                    notes = ""
                    if i+1 < len(filtered_lines):
                        details = filtered_lines[i+1]
                        if not details.startswith("Message") and "•" not in details:
                            notes = details
                    
                    people.append({
                        "name": name,
                        "title": headline,
                        "company": company, 
                        "location": location,
                        "notes": notes
                    })
            except IndexError:
                pass
        i += 1
        
    print(f"Found {len(people)} people. Inserting...")
    
    inserted = 0
    for p in people:
        # Check duplicate
        cursor.execute("SELECT id FROM crm_contacts WHERE name = ?", (p['name'],))
        if cursor.fetchone():
            print(f"Duplicate skipped: {p['name']}")
            continue
            
        cursor.execute("""
            INSERT INTO crm_contacts (name, role, company, contact_type, status, relationship_strength, notes, channel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p['name'], 
            p['title'][:100], 
            p['company'], 
            "Recruiter" if "Recrut" in p['title'] or "Talent" in p['title'] or "Hiring" in p['title'] else "Peer",
            "1. Connected",
            1, 
            f"Location: {p['location']}\nNote: {p['notes']}",
            "LinkedIn"
        ))
        inserted += 1
        
    conn.commit()
    conn.close()
    print(f"Successfully inserted {inserted} new contacts.")

if __name__ == "__main__":
    parse_and_ingest_people_batch2()
