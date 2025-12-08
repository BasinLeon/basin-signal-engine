
import sqlite3
import re

# LinkedIn People Data Block
# Note: Format is Name -> Title -> Location -> Message/Connect button text -> Details
# Based on the paste, a rough heuristic state machine is needed again.

DATA = """
Krista Cardoza
Krista Cardoza  • 1st
Principal Talent Acquisition Advisor at OpenText
San Clemente, California, United States
Message
Past: ...FY09Q3 – 125% of quota for both pipeline and number of opportunities, created new hire training packet for BDC Org and chosen as a mentor for new hires...
12K followers

Morgan Benner
Morgan Benner  • 1st
Here to help you #FindYourFutureInSteel
Springboro, Ohio, United States
Message
Past: ...Train all new hires on POS and customer service skills...

Nikki Ward
Nikki Ward  • 1st
Senior Director - Recruiting @ Rose International | Business Administration
Versailles, Missouri, United States
Message
About: With over two decades of experience in talent acquisition, currently serving as Senior Director of Recruiting at Rose International, contributing to strategic recruiting initiatives and fostering strong...

Ashley Abrishami
Ashley Abrishami  • 1st
Vice President of Recruitment, Operations and Development
Roseville, California, United States
Message
Past: Provided assistance to the hiring managers in the interviewing and hiring of potential employees and interns
2K followers

Shirin Parineh
Shirin Parineh  • 1st
Talent. People. Employee Experience.
San Francisco, California, United States
Message
Current: ...from the world’s fastest-growing companies, HIGHER’s goal is to provide a leveling up for the talent acquisition function by amplifying the impact of the most ambitious professionals in this space

Nora Madzar
Nora Madzar  • 1st
Team Lead, Sales Leadership Recruiter at Verkada
San Francisco Bay Area
Message
Past: Number one Recruiting team Q2 2022: 138% to plan
5K followers

Lisa Souther
Lisa Souther  • 1st
Director of Recruiting at Therapydia
San Mateo, California, United States
Message
Past: Developed the necessary talent pipelines and execution plans to meet the hiring plans, balancing internal resources, contractors, and capabilities
9K followers

Parisa Mohseni, M.S.
Parisa Mohseni, M.S. • 1st
Talent Acquisition Partner
San Francisco Bay Area
Message
Past: Set up interviews with hiring manager and track the process through onboarding
12K followers

Brian Pototo
Brian Pototo  • 1st
Vice President, Talent Acquisition
San Francisco Bay Area
Message
Past: Developed hiring strategy to staff project team and successfully made initial senior level hires

Vishal Sambre
Vishal Sambre  • 1st
Senior Talent Acquisition Specialist (Diversity Hiring)
San Jose, California, United States
Message
Current: Strengthened diversity recruitment efforts by aligning hiring practices with company and project-specific diversity requirements
21K followers

Uz Ma
Uz Ma  • 1st
Hiring Manager at SpanIdea - Hiring via jobeze.com !
Milpitas, California, United States
Message
About: Currently working as a Hiring Manager at SpanIdea

Puay Kua
Puay Kua  • 1st
Strategic Talent Acquisition Partner
San Francisco, California, United States
Message
Current: ...- Participate in hiring events e.g. AfroTech...

Christina Gibbons
Christina Gibbons  • 1st
Dedicated Recruiter hiring for innovative companies and always looking for top-tier talent!
San Francisco Bay Area
Message
Current: ...Our emphasis lies within recruiting experienced Sales, Engineering, Product, Marketing, and Professional Service professionals with...

Christina Perez-De La Torre
Christina Perez-De La Torre  • 1st
Staffing Leader | 20+ Years in Workforce Solutions | Temp & Direct Hire Staffing for all Industries
Los Angeles Metropolitan Area
Message
Skills: Hiring, Hiring Personnel, Recruiting

Sarah Mossadaq (Fennell)
Sarah Mossadaq (Fennell)  • 1st
Talent Acquisition @ Mattel Inc.
Los Angeles Metropolitan Area
Message
Current: Gather interview feedback and share with hiring team
7K followers

Shelly Yarbrough
Shelly Yarbrough  • 1st
Talent Acquisition Manager
Kennesaw, Georgia, United States
Message
Current: · Recruiting & Staffing – We bring together the right companies with the right talent on a direct hire, contract, and temp-to-hire basis

Chandan Sinha
Chandan Sinha  • 1st
Team Lead - Technical Recruitment at Intelliswift, An LTTS Company!
Newark, California, United States
Message
About: Currently the majority focus is Direct Hiring is US, Canada and LATAM

Elaine Voronin
Elaine Voronin  • 1st
Recruiting Leader @ Sardine 🐟 | We’re hiring!
San Jose, California, United States
Message
Past: ...regular reporting and insights to internal and external stakeholders, ensuring alignment on hiring progress and strategy

Marcia Bray
Marcia Bray  • 1st
Recruiting Leader with The Jacobson Group
Little Elm, Texas, United States
Message
Past: ...Ensuring that on-boarding department has all of the necessary documentation for new hires...

Raelene Conkin
Raelene Conkin  • 1st
NVIDIA pioneered accelerated computing to tackle challenges no one else can solve. Our work in AI and the metaverse is transforming the world's largest industries and profoundly impacting society.
San Francisco Bay Area
Message
Current: ...email highlighting Recruiting/HM partnership which was added to Nvidia's Workday open req flow to hiring managers
8K followers

Ashley Wheeler
Ashley Wheeler  • 1st
Recruiter at Westways Staffing Services, Inc
Modesto-Merced Area
Message
Past: ● Manage the hiring process through sourcing and interviewing candidates, offering and negotiating positions,...

Randy Levinson
Randy Levinson  • 1st
Experienced HR Operations and Talent Acquisition professional. Expertise in Global HR Program Management, and full-cycle recruiting for GTM, SW/HW, Semiconductor, DL/ML Scientists, Sales & Marketing, and G&A.
San Francisco Bay Area
Message
Current: ● Coaching hiring managers and organizational leadership on candidate review, selection, and hiring best practices
9K followers

Cecillia (Remley) Ashworth
Cecillia (Remley) Ashworth  • 1st
Principal Recruiter - Customer Success / Global Customer Support- DocuSign
San Francisco, California, United States
Message
Past: Worked with Path Forward to drive our hiring initiative for our "retrunship" program

Todd Dehlin
Todd Dehlin  • 1st
Talent Acquisition Leader
San Francisco, California, United States
Message
Past: ...Nurtured relationships with key stakeholders to understand hiring priorities and budget constraints, and establish flexible processes with a focus on candidate...
13K followers

Emily Aroz
Emily Aroz  • 1st
Hiring @ Uber
San Francisco, California, United States
Message
Past: Partner with Account Managers to obtain a clear understanding of position requirements from hiring managers and exchange market data

Adriana Aden Rodrigues
Adriana Aden Rodrigues • 1st
Principal Recruiter at Jobot
Orange County, California, United States
Message

Claire Fleming Sidhu
Claire Fleming Sidhu  • 1st
People Person | Career Hype Woman | Helping tech startups build founding teams
Irvine, California, United States
Message
Current: Hiring across GTM, Ops, Engineering, and Product
16K followers

Nick Esquivel
Nick Esquivel • 1st
Recruitment
Los Angeles, California, United States
Message
Skills: Strategic Hiring, Recruiting, Staffing Services
3K followers

Shawn Fletcher
Shawn Fletcher  • 1st
Talent Acquisition Partner - Senior
Ashville, Ohio, United States
Message
Current: Shawn has extensive talent management/recruiting experience that focuses on Risk Analyst, specifically Quantitative Risk Analyst, Actuary, Credit...
20K followers

Karey Larson
Karey Larson  • 1st
Recruiting Director @ Spotlight Inc. | IT Talent Acquisition
Denver Metropolitan Area
Message
Current: Recruiting Director at Spotlight Inc.

Lindsay Forbes
Lindsay Forbes  • 1st
Director of Talent Acquisition |
Roseville, California, United States
Message
Current: Director of Talent Acquisition at FlexCare Medical Staffing

Lisa Fuentes
Lisa Fuentes  • 1st
Talent Acquisition Senior Recruiter
Tracy, California, United States
Message
Past: Screening, qualifying suitable candidates and providing a short-list to the hiring manager

Jobin Joseph
Jobin Joseph  • 1st
Sr Recruiting Manager at JobTracks
Los Angeles Metropolitan Area
Message
About: ...Experienced in Volume/Mass Hiring and Niche Skill Hiring...

Ernesto Zelaya
Ernesto Zelaya  • 1st
Senior Manager Talent Acquisition at Gainsight
San Francisco Bay Area
Message
About: Trusted by hiring managers as a strategic advisor
6K followers

Christi Seaback
Christi Seaback  • 1st
Vice President of Operations and Service Delivery @ Hire Energy | Business Administration
Houston, Texas, United States
Message
Past: ...site tours, PPE and safety requirements, presentations and legal interviewing coaching for hiring managers...

Alaina Bernal
Alaina Bernal  • 1st
HR Talent Partner at RingCentral
Fremont, California, United States
Message
Skills: Hiring, Recruiting, Corporate Recruiting

Troy Knapp
Troy Knapp  • 1st
Senior Director, Head of Talent Acquisition
San Francisco Bay Area
Message
Past: ...and attrition challneges while consolidating and standardizing sourcing, interviewing, and hiring.   ✔ Led teams of up 25 direct reports to partner with hiring managers, business partners, and staff...
6K followers

Brian Diaz
Brian Diaz  • 1st
Director of Talent Acquisition
Houston, Texas, United States
Message
Past: Rebuilt confidence in Talent Acquisition team between all hiring managers and departments by revamping requisition process and conducting intake calls...

Tracy Hacha
Tracy Hacha  • 1st
Recruitment Manager
Miami, Florida, United States
Message
Past: Full-Cycle Talent Acquisition: Led the sourcing, recruiting, interviewing, hiring, training, and onboarding of new team members to ensure seamless workforce integration

Jillian Nava
Jillian Nava  • 1st
Corporate Talent Acquisition Manager @ HomeRise | Social Networking, HR, Recruiting
Burlingame, California, United States
Message
Current: ...a smooth transition that streamlines processes and improves the experience for candidates and hiring managers

Lauren Taylor
Lauren Taylor  • 1st
Senior Talent Acquisition Partner - I'm Hiring!
Austin, Texas, United States
Message
Current: We are an international community of GTM Recruiters from the world’s fastest-growing SaaS companies

Kendal Krawl
Kendal Krawl  • 1st
Talent Acquisition Partner @ Calendly
San Diego, California, United States
Message
About: I'm Kendal, a Recruitment and People Operations professional with 6 years of experience in hiring and managing top talent for high-growth startups and SMBs within the B2B, SaaS, FinTech, eCommerce,...

Parvinder (Tony) G
Parvinder (Tony) G • 1st
Full Lifecycle Recruiting Management • Talent Acquisition • Thought Leadership • Organization Development • Strategic Planning / Execution • Head Hunting • Relationship Management • Global Organizations
San Francisco Bay Area
Message
Past: Led hiring manager training sessions to streamline interview loops and improve structured hiring practices

John Ledterman
John Ledterman  • 1st
Sr. Recruiter-Account Manager
Tulsa, Oklahoma, United States
Message
Current: Managing and Recruiting for Client's Recruitment Initiatives in the Aerospace Industry

Brian Smith
Brian Smith  • 1st
Managing Partner at Primary Recruiting Services
Greater Orlando
Message
Current: We specialize in recruiting Finance & Accounting, Energy, and Civil Engineering professionals throughout the US
10K followers

Tammi  Taylor Heaton, ARM, CSP
Tammi  Taylor Heaton, ARM, CSP  • 1st
Co-CEO | National Recruiting & Franchise Staffing Organization
Fresno, California, United States
Message
About: ...Warehouse, Clerical, Administrative & Financial Services Staffing | Screening, Interviewing, Hiring, Human Resources | Sales & Marketing, Executive Business Management | Customer Relations, Customer...

Zafar Parkar
Zafar Parkar  • 1st
Hiring
Sunnyvale, California, United States
Message
Current: Partner with hiring managers to understand their recruiting needs in order to create and execute an effective...

Marissa Snyder
Marissa Snyder  • 1st
Senior Talent Acquisition Specialist at Arm
San Diego, California, United States
Message
Current: ...I specifically support hiring for our Solutions Engineering organization, with a focus on architecture careers

Sunidhi Goel
Sunidhi Goel  • 1st
IIM Indore | AHRM | Talent Management | Project Management | Google Analytics | Leadership Hiring | Hiring Top Talent |
United States
Message
Past: ...process once the candidate accepts the offer in the candidate portal and connecting with onboarding team & Hiring Manager for hassle free onboarding
22K followers

Joshua Garcia
Joshua Garcia • 1st
Talent Partner - GTM
United States
Message
About: ...with key stakeholders, and collaborate with diverse teams across various geographies and organizations. As a hiring leader, I align my professionalism, core values, and integrity with the company mission
"""

def parse_and_ingest_people():
    conn = sqlite3.connect("basin_nexus.db")
    cursor = conn.cursor()
    
    # Filtering Logic
    lines = [l.strip() for l in DATA.split('\n') if l.strip()]
    filtered_lines = []
    
    # We ignore standard UI elements but keep "Message" as an anchor
    ignore_phrases = ["People", "Actively hiring", "Locations", "Current companies", "All filters", "Reset", 
                      "Hiring? Find people", "Get matched", "Get started", "Are these results helpful?",
                      "Your feedback", "View my services", "About", "Accessibility", "Help Center",
                      "Privacy & Terms", "Ad Choices", "Advertising", "Business Services", "Get the LinkedIn app", "More"]
    
    for line in lines:
        if line in ["1st", "2nd", "Message", "Following", "Connect"]:
             filtered_lines.append(line) # Keep anchors
             continue
             
        # Skip numeric navigation but allow "12K followers"
        if line.isdigit() or line.startswith("Page ") or line in ["Previous", "Next"]:
            continue
            
        if any(phrase in line for phrase in ignore_phrases):
             continue
             
        filtered_lines.append(line)
        
    people = []
    i = 0
    
    # Pattern seems to be:
    # 1. Name (sometimes repeated)
    # 2. Name • 1st (Degree)
    # 3. Title/Headline
    # 4. Location
    # 5. Message (Anchor)
    # 6. Description/Details
    
    while i < len(filtered_lines):
        line = filtered_lines[i]
        
        # Anchor on "Message" or "Connect" (though for 1st connections it is Message)
        if line == "Message":
            # Go backwards to find structure
            try:
                location = filtered_lines[i-1]
                headline = filtered_lines[i-2]
                name_line_degree = filtered_lines[i-3]
                
                # Check if i-3 has "• 1st"
                if "•" in name_line_degree:
                    name = name_line_degree.split("•")[0].strip()
                    
                    # Extract Company if possible from Headline
                    # "Recruiter at Google" -> Google
                    company = ""
                    if " at " in headline:
                        company = headline.split(" at ")[-1].split("|")[0].strip()
                    elif " @ " in headline:
                        company = headline.split(" @ ")[-1].split("|")[0].strip()
                    elif " with " in headline:
                        company = headline.split(" with ")[-1].split("|")[0].strip()
                    
                    # Search for description after Message
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
            continue
            
        cursor.execute("""
            INSERT INTO crm_contacts (name, role, company, contact_type, status, relationship_strength, notes, channel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p['name'], 
            p['title'][:100], # Trucate headline to fit role roughly
            p['company'], 
            "Recruiter" if "Recrut" in p['title'] or "Talent" in p['title'] or "Hiring" in p['title'] else "Peer",
            "1. Connected",
            1, # Weak tie initially
            f"Location: {p['location']}\nNote: {p['notes']}",
            "LinkedIn"
        ))
        inserted += 1
        
    conn.commit()
    conn.close()
    print(f"Successfully inserted {inserted} new contacts.")

if __name__ == "__main__":
    parse_and_ingest_people()
