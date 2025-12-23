
import sqlite3
import re
from datetime import datetime

# LinkedIn Data Block - BATCH 2
DATA = """
My Jobs
Saved
In Progress
Applied
Archived
KGEN
Enterprise Sales Manager
KGEN
San Francisco, CA (Hybrid)
 
Actively reviewing applicants
Last modified 19m ago •
 
 
Easy Apply

Absorb Software
Account Executive , Verified
Absorb Software
United States (Remote)
No longer accepting applications

ClickUp
Enterprise Account Executive (AMER) , Verified
ClickUp
United States (Remote)
No longer accepting applications

Navan
Commercial Account Executive , Verified
Navan
San Francisco, CA (Hybrid)
 
Actively reviewing applicants
Last modified 1mo ago •
 
 
Easy Apply

Talkdesk
Enterprise Account Executive , Verified
Talkdesk
United States (Remote)
No longer accepting applications

Augment Code
Account Executive , Verified
Augment Code
Palo Alto, CA
No longer accepting applications

PolyAI
Enterprise Account Executive , Verified
PolyAI
San Francisco Bay Area (Remote)
No longer accepting applications

Workspot, Inc
Senior Alliances Leader , Verified
Workspot, Inc
Campbell, CA (Hybrid)
No longer accepting applications

Skylight Lending
Director of Business Development
Skylight Lending
United States (Remote)
No longer accepting applications

Access | Information Management
Business Development Executive , Verified
Access | Information Management
United States (Remote)
No longer accepting applications

Page 1 of 6
Previous

1

2

3

4

5

6

Next

My Jobs
Saved
In Progress
Applied
Archived
Sinch
Channel Manager , Verified
Sinch
United States (Remote)
No longer accepting applications

Evonence
Google Cloud Account Executive , Verified
Evonence
United States (Remote)
No longer accepting applications

Larsen & Toubro
Senior Business Development Manager , Verified
Larsen & Toubro
United States (Remote)
No longer accepting applications

Acer
Business Manager (LATAM) , Verified
Acer
San Jose, CA (Hybrid)
No longer accepting applications

Hopper
Senior Business Development Manager - Flights , Verified
Hopper
California, United States (Remote)
No longer accepting applications

Sencha
Account Executive , Verified
Sencha
EMEA (Remote)
No longer accepting applications

Proliant
Enterprise Sales Manager , Verified
ProLiant
United States (Remote)
No longer accepting applications

Betts
Account Executive , Verified
Betts Recruiting
San Francisco Bay Area (On-site)
No longer accepting applications

Persado
Customer Success Manager - Remote , Verified
Persado
San Francisco, CA (Remote)
No longer accepting applications

Page 2 of 6
Previous

1

2

3

4

5

6

Next

My Jobs
Saved
In Progress
Applied
Archived
Business Development Manager , Verified
Boldyn Networks
Boston, MA (Remote)
No longer accepting applications

BrightView Landscapes
Business Developer , Verified
BrightView Landscapes
San Jose, CA (On-site)
No longer accepting applications

EVOX Images
Business Development Manager
EVOX Images
United States (Remote)
No longer accepting applications

GoldFinch Cloud Solutions
Director - Business Development
GoldFinch Cloud Solutions
United States (Remote)
No longer accepting applications

Advantage Solutions
Customer Sales Manager , Verified
Advantage Solutions
Pleasanton, CA (Hybrid)
No longer accepting applications

NirApad9 
BDM - Sales
NirApad9
United States (Remote)
No longer accepting applications

Ivalua
Account Executive - Manufacturing , Verified
Ivalua
Redwood City, CA (Hybrid)
No longer accepting applications

BrightView Landscapes
Business Developer , Verified
BrightView Landscapes
Pleasanton, CA (On-site)
No longer accepting applications

CPI Selection
Business Development Manager
CPI Selection
United States (Remote)
No longer accepting applications

Page 3 of 6
Previous

1

2

3

4

5

6

Next
My Jobs
Saved
In Progress
Applied
Archived
Inspectorio
Senior Account Executive (SaaS)- Selling in to Retail / Fashion / CPG , Verified
Inspectorio
New York, NY (Remote)
No longer accepting applications

Thermo Systems
Business Development Manager-Life Science , Verified
Thermo Systems
United States (Remote)
No longer accepting applications

TECHEAD
Business Development Manager (marketing agency)
TECHEAD
Atlanta Metropolitan Area (Remote)
No longer accepting applications

CharterUP
Business Development Manager , Verified
CharterUP
United States (Remote)
No longer accepting applications

Supermicro
Account Manager , Verified
Supermicro
San Jose, CA (On-site)
No longer accepting applications

Brand Muscle
Client Success Account Manager , Verified
BrandMuscle
United States (Remote)
No longer accepting applications

Movable Ink
Client Experience Manager , Verified
Movable Ink
San Francisco Bay Area (Remote)
No longer accepting applications

UPTIVE
Business Development Manager (NorCal Region)
UPTIVE Manufacturing
San Francisco Bay Area (Remote)
No longer accepting applications

PackGene Biotech, Inc.
Business Development Manager
PackGene Biotech, Inc.
San Francisco, CA (Hybrid)
No longer accepting applications

Page 4 of 6
Previous

1

2

3

4

5

6


My Jobs
Saved
In Progress
Applied
Archived
STEM Education Works
Account Executive
STEM Education Works
Lafayette, IN (On-site)
No longer accepting applications

Betts
Business Development Representative , Verified
Betts Recruiting
New York City Metropolitan Area (Hybrid)
No longer accepting applications

Insight Global
Business Development Manager , Verified
Insight Global
Wisconsin, United States (Remote)
No longer accepting applications

Jitterbit
Senior Manager, Sales Development , Verified
Jitterbit
United States (Remote)
No longer accepting applications

Spark Talent Acquisition, Inc.
Business Development Manager , Verified
Spark Talent Acquisition, Inc.
Livonia, MI (Remote)
No longer accepting applications

PTW
Business Development Manager | Player Support 
PTW
United States (Remote)
No longer accepting applications

Capelli Sport
Sales Executive
Capelli Sport
San Francisco Bay Area (Hybrid)
No longer accepting applications

EquipmentShare
Territory Account Manager , Verified
EquipmentShare
Newark, CA (On-site)
No longer accepting applications

BCW Global
Senior Account Executive, Technology Public Relations , Verified
BCW Global
San Francisco, CA (On-site)
No longer accepting applications

UsableNet
Senior Business Development Executive , Verified
UsableNet
United States (Remote)
No longer accepting applications

Page 5 of 6
Previous

1

2

3

4

5

6
"""

def parse_and_ingest():
    # Connect to DB
    conn = sqlite3.connect("basin_nexus.db")
    cursor = conn.cursor()
    
    # Simple state machine for parsing
    lines = [l.strip() for l in DATA.split('\n') if l.strip()]
    
    # Filter out navigation lines
    filtered_lines = []
    # More aggressive filtering of UI noise
    ignore_phrases = ["My Jobs", "Saved", "In Progress", "Applied", "Archived", "Page", "Previous", "Next", "…", "Application viewed", "Easy Apply"]
    
    for line in lines:
        if line in ["My Jobs", "Saved", "In Progress", "Applied", "Archived", "Easy Apply"]:
             continue
        if line.startswith("Page ") or line.isdigit() or line == "Previous" or line == "Next" or line == "…":
            continue
        filtered_lines.append(line)
            
    current_job = {}
    jobs = []
    
    i = 0
    while i < len(filtered_lines):
        line = filtered_lines[i]
        
        # Check for status line (Anchor)
        is_status = False
        if line.startswith("Applied") and ("ago" in line or "m" in line or "h" in line or "w" in line):
            is_status = True
        elif line.startswith("Application viewed"):
            is_status = True
        elif line == "No longer accepting applications":
            is_status = True
        elif line == "Actively reviewing applicants":
            is_status = True
            
        if is_status:
            # Go back 3 lines to find title
            # In LinkedIn's Saved/Archived view, there is often an extra line for the Company Logo text before the Title.
            # Pattern: [Logo Text] -> [Title] -> [Company] -> [Location] -> [Status]
            # Offset:  i-4            i-3       i-2          i-1          i
            
            # OR Pattern (Applied view): [Title] -> [Company] -> [Location] -> [Status]
            # Offset:                    i-3        i-2          i-1          i
            
            # We need to distinguish.
            # Usually if there is an logo line, the Title is at i-3.
            # Wait, if there is a Logo line at i-4, my previous logic of grabbing i-3 as Title still works?
            # Let's trace:
            # i=Status
            # i-1=Location
            # i-2=Company
            # i-3=Title
            # i-4=Logo (ignored)
            
            # So yes, grabbing i-3, i-2, i-1 should still work for the core fields.
            
            if i >= 3:
                location = filtered_lines[i-1]
                company = filtered_lines[i-2]
                title = filtered_lines[i-3]
                
                # Double check these lines don't look like status lines or unrelated junk
                # "Last modified..." check
                if "Last modified" in location:
                    # Shift everything up by one line?
                    # No, "Last modified" appears AFTER status in some views, but here we are iterating.
                    # KGEN example: [Status: Actively reviewing] -> [Last modified...].
                    # Checks happen when i points to "Actively reviewing".
                    # i-1 is "San Francisco..." (Location).
                    pass

                # If the title line looks like a company name (same as company line), maybe we shifted?
                # Sometimes Logo Text = Company Name.
                # If i-3 is same as i-2?
                # Case:
                # i-2: Absorb Software
                # i-3: Account Executive
                # i-4: Absorb Software
                # They are different.
                
                # Clean title
                title = title.replace(" , Verified", "").strip()
                
                status_text = line
                stage = "2. Applied"
                
                # Map status to stage
                if "No longer accepting" in line:
                    stage = "3. Frozen/Rejected"
                    status_text = "Closed (No longer accepting)"
                elif "Actively reviewing" in line:
                    stage = "2. Under Review"
                    status_text = "Active Review"
                
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "status_text": status_text,
                    "stage": stage
                })
        i += 1

    print(f"Found {len(jobs)} jobs. Inserting...")
    
    inserted_count = 0
    for job in jobs:
        # Check duplicates
        cursor.execute("SELECT id FROM crm_deals WHERE company = ? AND role = ?", (job['company'], job['title']))
        if cursor.fetchone():
            # print(f"Duplicate found: {job['company']}")
            continue
            
        # Determine remote status for notes
        remote_status = "On-site"
        if "Remote" in job['location']: remote_status = "Remote"
        elif "Hybrid" in job['location']: remote_status = "Hybrid"
        
        notes = f"Source: LinkedIn Import (Batch 2)\nLocation: {job['location']}\nType: {remote_status}\nStatus: {job['status_text']}"
        
        cursor.execute("""
            INSERT INTO crm_deals (company, role, stage, signal, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (
            job['company'], 
            job['title'], 
            job['stage'], 
            "Medium", 
            notes
        ))
        inserted_count += 1
        
    conn.commit()
    conn.close()
    print(f"Successfully inserted {inserted_count} new deals.")

if __name__ == "__main__":
    parse_and_ingest()
