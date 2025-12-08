
import sqlite3
import re
import os

def parse_and_ingest_batch_8():
    file_path = "assets/linkedin_batch_8_raw.txt"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, "r") as f:
        content = f.read()

    # Split into chunks based on the visual separator pattern in the text, 
    # but the text copy-paste usually implies a block structure.
    # Strategy: Find lines with "• 1st" or "• 2nd" or "• 3rd" as the anchor for the Name.
    
    lines = [l.strip() for l in content.split('\n')]
    
    conn = sqlite3.connect("basin_nexus.db")
    cursor = conn.cursor()
    
    contacts = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Anchor: The Name line usually has the connection degree
        if "• 1st" in line or "• 2nd" in line or "• 3rd" in line:
            # Found a contact anchor.
            # Name is the part before " •"
            raw_name = line.split("•")[0].strip()
            # Clean up potential duplicate name repetitions if the previous line was identical
            # In the copy paste: 
            # Kyle Elliott 🌊
            # Kyle Elliott 🌊  • 1st
            # So raw_name is good.
            
            # The next few lines are Headline, Location, then "Message"
            headline = ""
            location = ""
            company = ""
            
            # Look ahead for "Message" to bound the block
            j = i + 1
            block_lines = []
            while j < len(lines) and lines[j] != "Message" and j < i + 20: # Limit lookahead
                if lines[j]: # Skip empty
                    block_lines.append(lines[j])
                j += 1
            
            # Parse the block
            if block_lines:
                # The last item in block_lines before "Message" is usually Location.
                location = block_lines[-1]
                # The items before that are Headline parts. Join them.
                headline_parts = block_lines[:-1]
                headline = " | ".join(headline_parts)
                
                # Heuristic for Company in Headline ("@ Company" or "at Company")
                # Common formats: "Role @ Company", "Role at Company"
                # If pipe separated, check first segment.
                
                # Attempt to extract Company
                # 1. Check for @
                if "@" in headline:
                    # simplistic: take text after @ until next | or end
                    try:
                        company = headline.split("@")[1].split("|")[0].strip()
                    except:
                        pass
                # 2. Check for " at "
                if not company and " at " in headline:
                    try:
                        company = headline.split(" at ")[1].split("|")[0].strip()
                    except:
                        pass
                
                # Fallback: Check "Current: Role at Company" line which might appear AFTER "Message"
                # in some copy-paste formats, but in this specific one, "Message" is followed by "Past:" or "Current:"
                # Let's check lines AFTER "Message" for "Current:"
                if not company:
                    k = j + 1 # Line after "Message"
                    while k < len(lines) and k < j + 5:
                        post_line = lines[k]
                        if post_line.startswith("Current:"):
                            # "Current: Role at Company"
                            val = post_line.replace("Current:", "").strip()
                            if " at " in val:
                                company = val.split(" at ")[1].strip()
                            elif "@" in val:
                                company = val.split("@")[1].strip()
                            # Sometimes it just lists the company description?
                            # "Current: Our platform..." -> This is a description, not company name.
                            # "Current: Partner with..."
                            break
                        k += 1

            # Determine Type
            c_type = "Peer" # Default
            hl_lower = headline.lower()
            if "recruit" in hl_lower or "talent" in hl_lower or "staffing" in hl_lower or "hiring" in hl_lower:
                c_type = "Recruiter"
            if "founder" in hl_lower or "ceo" in hl_lower or "vp" in hl_lower or "head of" in hl_lower or "director" in hl_lower:
                c_type = "VIP"
                
            # Refine Type
            if "gtm" in hl_lower: c_type += " (GTM)"
            
            contacts.append({
                "name": raw_name,
                "headline": headline[:150], # Truncate for DB
                "company": company,
                "location": location,
                "type": c_type
            })
            
            # Advance i to the end of this block
            i = j 
        else:
            i += 1

    print(f"Parsed {len(contacts)} contacts.")
    
    inserted_count = 0
    for c in contacts:
        # Check duplicate by name
        cursor.execute("SELECT id FROM crm_contacts WHERE name = ?", (c['name'],))
        if cursor.fetchone():
            continue
            
        cursor.execute("""
            INSERT INTO crm_contacts (name, role, company, contact_type, status, relationship_strength, notes, channel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c['name'],
            c['headline'],
            c['company'],
            c['type'],
            "1. Connected",
            1,
            f"Location: {c['location']} | Batch 8 Import",
            "LinkedIn"
        ))
        inserted_count += 1
        
    conn.commit()
    conn.close()
    print(f"✅ Ingested {inserted_count} new contacts into CRM.")

if __name__ == "__main__":
    parse_and_ingest_batch_8()
