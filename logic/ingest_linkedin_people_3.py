
import sqlite3
import re

# LinkedIn People Data Block - Batch 3
DATA = """
Cindy Lech
Cindy Lech  • 1st
Sourcing Recruiter at Care Oregon
Portland, Oregon, United States
Message
About: ...Recruiter and Physical Therapist with a passion for caring for and serving others - whether it is a hiring manager needing staff, a candidate looking for their next career move, or a colleague who needs...

Donna Singer
Donna Singer  • 1st
National Director, Recruiting Enablement
Sonoma, California, United States
Message
Past: Partnering with hiring Managers to assist with hiring demand, recruitment planning and candidate acquisition...

Shuriah Bledsoe, MBA, HRM
Shuriah Bledsoe, MBA, HRM  • 1st
Workforce Development Manager
Atlanta Metropolitan Area
Message
Past: ...model to train staff in sourcing more effective and qualified candidates while optimizing the hiring process
2K followers

Travis Minor
Travis Minor  • 1st
💼 Executive Recruiter | 🤝 Connecting professionals with great companies | 🌟 Top 1% of Recruiting Firms in North America
Greater Sacramento
Message
About: As an integral member of CulverCareers, a top 1% Recruiting Firm in North America, I have successfully placed talented individuals in leading organizations since...

Alexandra Bilbruck
Alexandra Bilbruck  • 1st
Hiring @ Attentive!
San Francisco Bay Area
Message
Past: ...processes to the entire engineering org by working directly with engineering leadership and the hiring managers to create a streamlined process

Jody Ho
Jody Ho  • 1st
Recruiting Manager, AI at Meta
San Jose, California, United States
Message
Current: Specialized hiring in AI

Violetta Krotova
Violetta Krotova  • 1st
Recruitment Leader | 5K+ candidates interviewed | 20k+ resumes reviewed | Follow for job search strategies & leadership
Los Angeles, California, United States
Message
Past: ...make a direct and immediate impact on any organization, and we are in direct communication with the hiring manager assuring we get the job done right the first time
2K followers

Jessica Rodriguez
Jessica Rodriguez  • 1st
Recruiter at Waymo (formerly the Google self-driving car project)
San Jose, California, United States
Message
Past: Worked directly with hiring managers to qualify requirements and to ensure positive manager experience (hiring managers ranged...

Kira Roman
Kira Roman  • 1st
Technical Recruiter @ Skylo
San Francisco Bay Area
Message
Past: -Facilitated positive cross functional relationships with hiring managers across the organization, ensuring their headcount would be met with quality talent

Mark Rocha
Mark Rocha  • 1st
Head of Talent Acquisition | Team Leader | Company Builder | TA Business Partner
San Francisco Bay Area
Message
Current: ...practices comply with relevant laws and regulations, promoting diversity and inclusion in hiring.  *Budget Management: Manage the talent acquisition budget, ensuring resources are allocated effectively...

Louis Diaz
Louis Diaz  • 1st
Senior Manager Talent Acquisition at Oak Street Health | Expert in Full-Cycle Recruiting & Team Leadership | Passionate about Innovative HR Solutions
Greater Tampa Bay Area
Message
Current: ...SOP creation, cross-functional alignment, and system training for Talent Acquisition and hiring partners
7K followers

Stephanie Klinger
Stephanie Klinger  • 1st
Senior Recruiter
Seattle, Washington, United States
Message
About: As a Senior Recruiter at CareerPaths NW, LLC, I specialize in direct hire placements across the Pacific Northwest (PNW)

Jessie Bunting
Jessie Bunting  • 1st
We are hiring!
Encinitas, California, United States
Message
Past: ...- Implemented process including the build out of Greenhouse and weekly meetings with hiring managers...

Stephanie Swanbeck
Stephanie Swanbeck  • 1st
Senior Talent Acquisition Partner - Product and Design at Glassdoor
San Francisco Bay Area
Message
About: ...to follow the advice of Lawrence Bossidy, “I’m convinced that nothing we do is more important than hiring and developing people

Bryan Grauss
Bryan Grauss  • 1st
Senior Talent Acquisition Leader
Palo Alto, California, United States
Message
Current: HR Leader, Recruiting Leader, HR Systems Implementer

Diana Volynec
Diana Volynec  • 1st
VP, Sr. Talent Director at Robert Half Management Resources
San Francisco Bay Area
Message
Current: ...- Full cycle, high volume recruiting, identifying, hiring, placing...

Blaine Gorman
Blaine Gorman  • 1st
Sr. Director, People Business Partner & Talent Management at Kiva 
People & Culture Leader/Podcast Co-Host/Circuit Speaker/DEIB Expert
San Francisco, California, United States
Message
Current: ...Hireology ATS in 8 weeks and rolled-out training to global company subsidiaries, and then hiring managers

Yogesh Chandani
Yogesh Chandani  • 1st
Vice President | Driving GenAI Talent & Solutions | AI Hiring | Business Growth through Innovation
San Francisco Bay Area
Message
Current: Talent Acquisition: I collaborate with hiring managers and department heads to understand their talent requirements and develop tailored...

David Collins
David Collins  • 1st
Talent Partner |  Executive Talent
San Francisco Bay Area
Message
Current: ...-Executive recruiting & leadership hiring – In three years completed 60+ VP, C-suite, and board-level hires across GTM, Product, Engineering,...

Love Dhir
Love Dhir  • 1st
Accounts / Recruitment Manager | Recruitment & Operations | US / Canada Staffing
Santa Clara, California, United States
Message
About: Work closely with hiring managers to define job requirements, set recruitment timelines, and refine the selection process

Courtney Connelly
Courtney Connelly  • 1st
Recruitment Specialist | Talent Sourcing | Interviewing | Onboarding
Durham, North Carolina, United States
Message
Skills: Hiring, Recruiting, Human Resources (HR)

Tracey Schorsch
Tracey Schorsch  • 1st
Senior Principal at Paul Bridges Group- Recruitment to Recruitment | R2R | Rec to Rec | Search for Search | Headhunting Headhunters
Charlotte Metro
Message
About: ...mentoring recruitment teams, and developing strategies that achieve both immediate and long-term hiring goals

Marie Waldman
Marie Waldman  • 1st
Talent Acquisition Partner
United States
Message
Current: Tracked hires, requisitions, job postings, etc.

Natalia Klikova
Natalia Klikova • 1st
Recruiting with daily.jobs
San Jose, California, United States
Message
Current: Sr. Director of Recruiting  at daily.jobs

Anne Magalski
Anne Magalski  • 1st
Regional Vice President at Trillium Staffing
Flint, Michigan, United States
Message
Current: Leads the region in a manner that continually improves employee morale, and provides for disciplinary consistency, fairness, and training effectiveness

Jennifer Beckus  (She/Her/Hers)
Jennifer Beckus  (She/Her/Hers)  • 1st
Senior Talent Acquisition Partner
San Jose, California, United States
Message
Current: I am hiring for our Marketplace team

Daisy Chen
Daisy Chen  • 1st
Senior HR Generalist at OCBridge. WE ARE HIRING!!!
San Francisco Bay Area
Message
Current: Our comprehensive suite of services encompasses Director Hire options (Contingent, Contained, One-Off Retainer Searches), Recruiting as a Service (RaaS), and...

Maria Amigon, SHRM-CP
Maria Amigon, SHRM-CP  • 1st
Recruitment & Selection, Employee Engagement , Training & Development
Chicago, Illinois, United States
Message
Skills: Hiring, Recruiting, New Hire Orientations

J Wilder
J Wilder  • 1st
Sales & Recruiting Specialist
San Diego, California, United States
Message
Past: Improved overall time-to-fill metrics and hiring process effectiveness
11K followers

Daniel Torres, PHR
Daniel Torres, PHR  • 1st
Talent Acquisition and People Operations Leader
San Diego, California, United States
Message
About: ...led initiatives that kept teams engaged, optimized remote work strategies, and maintained critical hiring efforts despite industry-wide slowdowns
5K followers
"""

def parse_and_ingest_people_batch3():
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
             
        # Skip purely numeric lines or single characters that aren't useful
        if line.isdigit() or len(line) < 3:
            continue
            
        filtered_lines.append(line)
        
    people = []
    i = 0
    
    # Heuristic: 
    # [Name]
    # [Name • 1st]
    # [Headline]
    # [Location]
    # [Message]
    
    while i < len(filtered_lines):
        line = filtered_lines[i]
        
        if line == "Message":
            try:
                location = filtered_lines[i-1]
                headline = filtered_lines[i-2]
                name_line = filtered_lines[i-3]
                
                # Check consistency
                # The name line should contain "• 1st" strictly? 
                # In this paste, sometimes "Name\nName • 1st" is standard.
                
                # If i-3 is "Name • 1st", then Name is simple.
                if "•" in name_line:
                    name = name_line.split("•")[0].strip()
                elif "•" in filtered_lines[i-4]: # Check one line up if Name repeated
                    name_line = filtered_lines[i-4]
                    name = name_line.split("•")[0].strip()
                else:
                    # Fallback
                    name = name_line
                
                # Extract Company
                company = ""
                headline_clean = headline.replace("We’re HIRING", "").strip()
                
                if " at " in headline_clean:
                    company = headline_clean.split(" at ")[-1].split("|")[0].strip()
                elif " @ " in headline_clean:
                    company = headline_clean.split(" @ ")[-1].split("|")[0].strip()
                elif " with " in headline_clean:
                    company = headline_clean.split(" with ")[-1].split("|")[0].strip()
                
                # Notes
                notes = ""
                if i+1 < len(filtered_lines):
                    potential_note = filtered_lines[i+1]
                    if not potential_note.startswith("Message") and "followers" not in potential_note:
                        notes = potential_note

                # Deal linkage: Look for matching company in existing Deals to auto-link
                deal_id = None
                cursor_check = conn.cursor()
                if company:
                    cursor_check.execute("SELECT id FROM crm_deals WHERE company LIKE ? OR company LIKE ? LIMIT 1", (f"%{company}%", f"{company}%"))
                    row = cursor_check.fetchone()
                    if row:
                        deal_id = row[0]

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
    parse_and_ingest_people_batch3()
