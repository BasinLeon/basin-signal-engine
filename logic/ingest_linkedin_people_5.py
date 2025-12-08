
import sqlite3
import re

# LinkedIn People Data Block - Batch 5
DATA = """
Katie Thyfault
Katie Thyfault  • 1st
Hiring Process Development | Employee, Client, and Candidate Experience Advocate
Bennett, Colorado, United States
Message
Past: ...Closely work with clients to determine needs and hiring process...

Michelle Meyers, PHR
Michelle Meyers, PHR  • 1st
Global Talent Acquisition Leader @ dbt Labs 🚀
New York, New York, United States
Message
About: I’ve steered organizations through start-up chaos and hypergrowth sprints, leading strategy for hiring, people operations, and leadership development on multiple continents
8K followers

Rishab Sharma
Rishab Sharma  • 1st
Senior Technical Recruiter | SaaS, AI & Web3 | Talent Strategist
San Francisco Bay Area
Message
Current: ...processes/interviews, ATS implementation, job descriptions, salary benchmarking, sourcing, hiring full time senior engineers, interns, visual designers, optimising recruitment processes, working...
11K followers

Niyousha Linden
Niyousha Linden  • 1st
Executive Search - Recruiter
Orange County, California, United States
Message
Past: Balanced quality and volume to consistently meet hiring goals while maintaining a high talent bar

Levin John
Levin John  • 1st
Sales Hiring @ Cisco | Driving Recruitment Excellence | Building High-Performing Teams | Employer Branding
Bengaluru, Karnataka, India
Message
Current: ...acquisition goals for key senior hiring ▪ Built and maintained a robust and diverse pipeline of highly skilled candidates, ensuring readiness...

Divan Gamaliel
Divan Gamaliel  • 1st
Founder: ZAPHIRE - Building the world's first all-video social hiring platform for the modern world
New York City Metropolitan Area
Message
Current: After nearly 2 decades in the tech space navigating the job market as both a job seeker and a hiring manager, I decided to innovate the hiring process which is often flawed by inefficiencies, disconnection,...
6K followers

Stefan Moro NRF Cert RP
Stefan Moro NRF Cert RP  • 1st
Recruitment Team Lead, Temporary Division at FRS Recruitment
Ireland
Message
Current: FRS Recruitment are the only recruitment co-operative in Ireland
6K followers

Sarah Focone
Sarah Focone  • 1st
TA Consultant | 4+ Years in Recruitment Strategy, Hiring Processes & Talent Development | Growing Teams with Purpose
Springfield, Massachusetts Metropolitan Area
Message
About: ...expert, brings strong problem-solving skills, clear communication, and a focus on making the hiring process easy for both candidates and campus partners

Lianne Gong
Lianne Gong  • 1st
Sr. Manager, G&A and R&D Recruiting @ Gong
United States
Message
Current: My team oversees hiring for the following teams:...
13K followers

Kevin Krull
Kevin Krull  • 1st
Strategic Leader | AI Implementation & Innovation | Talent Operations
Atlanta Metropolitan Area
Message
Past: ...● Technical Expertise:  Communicated with technical hiring managers to qualify complex requisitions and communicate market trends across Java, C#, Python,...

Alex Lehman
Alex Lehman  • 1st
GTM Talent @ Iru | Global Talent Acquisition | Sales Talent Acquisition | Human Resources | Onboarding
Miami, Florida, United States
Message
About: I focus on creating a smooth, engaging candidate experience, improving hiring processes, and supporting our GTM leaders as they scale and build their teams
8K followers

Kimberly Kent
Kimberly Kent  • 1st
Director @ Eastward Partners | Executive Search & Human Capital Consulting for Private Equity | VC | Investment Banking | Technology | Finance
Costa Mesa, California, United States
Message
Current: Eastward Partners Inc is a venture backed, retained Executive Search and Human Capital Consulting firm with offices in New York City, Miami, Chicago, and San Diego

Matthew Bing
Matthew Bing  • 1st
Lead Talent Acquisition Manager at Kinetix
Auburn, Georgia, United States
Message
Current: We hire the best and brightest for some of the most sought after career opportunties

Elisabeth Lampert
Elisabeth Lampert  • 1st
Recruiting Professional
Cincinnati, Ohio, United States
Message
Skills: Recruiting

Puneet Khemani
Puneet Khemani  • 1st
Strategic Leader for Federal, IT & Media Clients | Scaling Talent | Delivering Excellence
United States
Message
Current: Responsible for overseeing the recruitment process and ensuring the delivery of high-quality candidates to meet the needs

Nikole Keslar
Nikole Keslar  • 1st
Expert Recruiting Solutions for Scaling Companies
Jupiter, Florida, United States
Message
Current: ...fractional recruiting resources to help high-growth organizations attract and hire the best talent

Sonia Bose
Sonia Bose  • 1st
Senior Technical Talent Partner- Startup & Growth Stage Specialist
Cupertino, California, United States
Message
Current: Partnered with hiring managers to define roles, source candidates, and facilitate structured interview processes
2K followers

Alyssa Marchinek
Alyssa Marchinek  • 1st
Full-Cycle Recruiter & Client Relationship Manager at Here's Help Staffing & Recruiting connecting top talent with real opportunities in the Hudson Valley
New York City Metropolitan Area
Message
Current: Since 1986, Here's Help Staffing & Recruiting has continued to provide Temporary Placement, Direct Hire and Executive Recruiting Services to businesses throughout the Hudson Valley
3K followers

Alex Miller
Alex Miller  • 1st
Talent Acquisition Leader
United States
Message
Skills: Hiring, Recruiting, Executive Search

Samantha McHale
Samantha McHale  • 1st
Recruiting Enablement | Employee Experience | Employer Branding
Santa Barbara, California, United States
Message
Current: ...our culture, drive candidate engagement, and deliver operational excellence across the global hiring journey
12K followers

Katie E. Breault
Katie E. Breault  • 1st
Chief Delivery Officer | Driving Skills-First, Inclusive Hiring for Fortune 500 Companies
Greater Boston
Message
Current: ...in their employment process and easily shift toward championing inclusive, equitable, skills-based hiring practices
5K followers

Sarah Frank
Sarah Frank  • 1st
Hiring Denver-based Implementation Managers Senior Recruiter | Career Coach | ADHD
Rome, Latium, Italy
Message
Current: ...editing job descriptions, creating and implementing a new recruiting strategy + launching the first hiring road map
4K followers

Britta Dance
Britta Dance  • 1st
hiring for startups
United States
Message
Past: Tech sourcer for AWS global infrastructure hiring

Brett Landen Gray
Brett Landen Gray  • 1st
Sales Executive - Slalom Consulting - GTM
Berthoud, Colorado, United States
Message
About: Demonstrated success managing the hiring needs of local, out-of-state and international territories

Josh Burkwist
Josh Burkwist  • 1st
Co-Founder and CEO | HireSource.ai
San Francisco, California, United States
Message
Current: Name Your Price – Set your budget at BluefinRecruiting.us and start hiring on your terms

Laura Dean
Laura Dean  • 1st
Senior Talent Acquisition Lead, Corporate Recruiter, Executive Recruiter, and Technical Recruiter | English Language Teaching Assistant and TEFL Instructor | Nutrition Consultant
Greater Chicago Area
Message
About: Expert in managing talent pipelines and relationships with hiring managers and executive leadership

Kayla Lewis
Kayla Lewis  • 1st
✨Executive Search Specialist | Your Edge in Leadership Hiring | A track record of excellence across: Sales • BD • Marketing • HR • Ops • PM • Technical • Executive Admin • C-Suite✨
United States
Message
Current: Use data to sharpen and improve hiring outcomes
3K followers

Jody Hilton
Jody Hilton  • 1st
Marketing & Growth Executive │ VP of Marketing │ Head of Growth │ Driving Scalable Acquisition for High-Growth Companies
Roseville, California, United States
Message
Current: ...Support clients with both individual hires and ongoing hiring programs...
27K followers

Erika Gray
Erika Gray  • 1st
Principal Recruiter + Recruiting Manager, Tech & Sales
United States
Message
About: Whether it’s guiding candidates through the hiring process, mentoring junior recruiters, or collaborating with hiring managers, I’m all about boosting...

Bryan Dyer
Bryan Dyer  • 1st
Career transitions aren't a stroll in the park. Remember that you are not your job or your career search. Give yourself grace.
Greater Boston
Message
About: ...leadership roles at State Street, and a deep commitment to creating inclusive and impactful hiring strategies, I’ve built a career connecting people with meaningful opportunities
23K followers

Michelle Hurd
Michelle Hurd  • 1st
Talent Acquisition Leader | Semiconductor & Tech Hiring | Scaling Distributed Teams
Greater Sacramento
Message
About: I have a proven track record of driving strategic hiring initiatives, implementing innovative recruiting processes, and leading remote and distributed...
30K followers

Rennie Nastor
Rennie Nastor  • 1st
Senior Talent Acquisition Partner at Five9
San Francisco, California, United States
Message
Current: Five9 is hiring! Please visit our Careers page or contact me (Rennie

Rohi (Roy) Touitou
Rohi (Roy) Touitou  • 1st
Connecting talent and leaders in Tech, Exec Search, GTM
London, England, United Kingdom
Message
Current: - Executive search...

Jaziel Brey
Jaziel Brey  • 1st
Tech Recruiter and L&D Professional at Chan Zuckerberg Initiative
San Francisco Bay Area
Message
Past: As one of the leading temp agencies, we know who is hiring and the types of workers they need

Felix Frydberg / Recruiter
Felix Frydberg / Recruiter  • 1st
Houston-Based Accounting & Finance Recruiter | Connecting Companies with Top Talent 🤖 Million Dollar Producer/ CEO Club 2024
Houston, Texas, United States
Message
Current: Talent recruitment, business development, client service in direct-hire and contract/temporary staffing
10K followers

Nick Lee
Nick Lee  • 1st
Chief Operating Officer
Los Angeles Metropolitan Area
Message
Current: Perfect Hire, a revolutionary AI interviewing software designed to transform the hiring process

Jason Alexander
Jason Alexander  • 1st
Chief Revenue Officer & Co-Founder at BANKW Staffing, LLC | Executive Career Coach | Public Speaker | Serial Entrepreneur | Author | jalexander@bankwstaffing.com
Greater Boston
Message
Current: We provide temporary, temporary-to-hire, and direct placement services in southern New Hampshire and northern Massachusetts with offices in...

David Kerr
David Kerr  • 1st
Recruiter @ Incendia - Legal, Software/IT (Crypto / Blockchain Enthusiast), Marketing, Sales, A&F. 
C-Suite & Individual Contributors (Permanent & Contract/Interium).
Norwell, Massachusetts, United States
Message
Current: As a seasoned recruiter with extensive experience in the industry, I excel at filling professional roles across a diverse...
14K followers
"""

def parse_and_ingest_people_batch5():
    conn = sqlite3.connect("basin_nexus.db")
    cursor = conn.cursor()
    
    # Pre-processing to remove non-data lines from known list + "Previous", "Next", numbers
    ignore_phrases = ["People", "Actively hiring", "Locations", "Current companies", "All filters", "Reset", 
                "Hiring? Find people", "Get matched", "Get started", "Are these results helpful?",
                "Your feedback", "View my services", "Visit my website", "Book an appointment",
                "About", "Accessibility", "Help Center",
                "Privacy & Terms", "Ad Choices", "Advertising", "Business Services", "Get the LinkedIn app", "More",
                "Previous", "Next", "Page ", "1st", "2nd"]
    
    lines = [l.strip() for l in DATA.split('\n') if l.strip()]
    filtered_lines = []
    
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
                
                # Name often repeats in Name line, so take first part if • present
                if "•" in name_line:
                    name = name_line.split("•")[0].strip()
                elif i >= 4 and "•" in filtered_lines[i-4]:
                    name = filtered_lines[i-4].split("•")[0].strip()
                else:
                    name = name_line
                
                # Extract Company Logic
                company = ""
                headline_clean = headline
                
                separators = [" at ", " @ ", " with ", " from "]
                for sep in separators:
                    if sep in headline_clean:
                        potential_company = headline_clean.split(sep)[-1].split("|")[0].strip()
                        # Shorten if too long (likely a sentence descriptor)
                        if len(potential_company) < 40:
                            company = potential_company
                        break
                
                # Deal linkage
                deal_id = None
                if company:
                    cursor_check = conn.cursor()
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
                        
                # Classification Tag
                is_connector = "Connector" in notes or "matchmaker" in notes or "intro" in notes
                contact_type = "Recruiter"
                if "Sales" in headline and "Recruiting" not in headline: contact_type = "Peer"
                if is_connector: contact_type = "Connector"

                people.append({
                    "name": name,
                    "title": headline,
                    "company": company, 
                    "location": location,
                    "deal_id": deal_id,
                    "notes": notes,
                    "type": contact_type
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
            p['type'],
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
    parse_and_ingest_people_batch5()
