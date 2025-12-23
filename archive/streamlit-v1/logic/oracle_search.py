"""
BASIN::NEXUS // ORACLE ARRAY (SEARCH ENGINE)
The "Google" for your personal career data.
Uses RAG (Retrieval Augmented Generation) to answer questions based on your Resumes, Notes, and Portfolio.
"""

import streamlit as st
import os
import glob
from logic.generator import generate_plain_text as run_groq_inference


from logic.database import get_all_deals, get_all_contacts

def get_search_index():
    """Build a simple in-memory index of all markdown files AND database records."""
    index = []
    
    # 1. MARKDOWN FILES (Assets)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")
    search_files = glob.glob(os.path.join(assets_dir, "*.md"))
    
    # Add manual files
    readme_path = os.path.join(base_dir, "GITHUB_PROFILE_README.md")
    if os.path.exists(readme_path): search_files.append(readme_path)
    
    for file_path in search_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                filename = os.path.basename(file_path)
                index.append({
                    "source": filename,
                    "content": content,
                    "type": "Doctum"
                })
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
            
    # 2. CRM DEALS (Database)
    deals = get_all_deals()
    for deal in deals:
        # Convert record to searchable text blob
        content = f"Company: {deal['company']}\nRole: {deal['role']}\nStage: {deal['stage']}\nSignal: {deal['signal']}\nNotes: {deal.get('notes', '')}"
        index.append({
            "source": f"Deal - {deal['company']}",
            "content": content,
            "type": "Deal",
            "metadata": deal
        })
        
    # 3. CRM CONTACTS (Database)
    contacts = get_all_contacts()
    for contact in contacts:
        content = f"Name: {contact['name']}\nCompany: {contact.get('company', '')}\nRole: {contact.get('role', '')}\nType: {contact.get('contact_type', '')}\nNotes: {contact.get('notes', '')}"
        index.append({
            "source": f"Contact - {contact['name']}",
            "content": content,
            "type": "Contact",
            "metadata": contact
        })
            
    return index

def search_nexus(query, index):
    """
    Perform a semantic search (simulated via keyword density for now) 
    and return relevant chunks.
    """
    results = []
    query_terms = query.lower().split()
    
    for doc in index:
        score = 0
        content_lower = doc["content"].lower()
        
        # Simple frequency scoring
        for term in query_terms:
            count = content_lower.count(term)
            score += count * 10
            
            # Boost for exact matches in source title (Company name match)
            if term in doc['source'].lower():
                score += 50
        
        # Semantic Boosts for Special Queries
        if "cluster" in query.lower() and doc.get("type") == "Deal":
             # Boost Deals that have linked contacts
             if "Linked Contacts" in doc.get("metadata", {}).get("notes", ""): 
                 score += 100
             # Or if we can infer it (requires more complex join logic not present in single doc)
             
        if score > 0:
            results.append({
                "source": doc["source"],
                "score": score,
                "preview": doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"],
                "full_content": doc["content"],
                "type": doc.get("type", "Doc")
            })
            
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def get_high_value_clusters():
    """Returns a list of companies that have BOTH a Deal and at least one Contact."""
    deals = get_all_deals()
    contacts = get_all_contacts()
    
    clusters = {}
    for d in deals:
        c_name = d['company']
        clusters[c_name] = {"deal": d, "contacts": []}
        
    for c in contacts:
        # Check against existing deal keys (case insensitive)
        c_company = c.get('company')
        if not c_company: continue
        
        # Find matching key
        match = next((k for k in clusters.keys() if k.lower() == c_company.lower()), None)
        if match:
            clusters[match]["contacts"].append(c)
            
    # Filter only those with contacts
    return {k:v for k,v in clusters.items() if v["contacts"]}

def render_oracle_search():
    """Render the main search interface."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">🧬 ORACLE SEARCH</h1>
        <p style="color: #888;">QUERY THE BASIN::NEXUS KNOWLEDGE GRAPH</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search Bar
    query = st.text_input("Ask the Oracle...", placeholder="e.g. 'What was my churn reduction at Sense?' or 'List my top python projects'")
    
    if query:
        with st.spinner("Oracle is thinking..."):
            # 1. Retrieve Context
            index = get_search_index()
            results = search_nexus(query, index)
            
            if not results:
                st.warning("No direct matches found in the archives.")
                return

            # 2. Build Context for LLM
            top_docs = results[:3]
            context_text = "\n\n---\n\n".join([f"Source: {doc['source']}\nContent: {doc['full_content']}" for doc in top_docs])
            
            # 3. Generate Answer
            system_prompt = f"""
            You are the ORACLE, the central intelligence of the BASIN::NEXUS system.
            You have access to the user's career data (Resumes, Notes, Readmes).
            
            USER QUERY: {query}
            
            CONTEXT FROM ARCHIVES:
            {context_text}
            
            INSTRUCTIONS:
            - Answer the user's query expertly using the provided context.
            - Be concise, professional, and "high-tech" in tone.
            - Cite the source filename if relevant.
            - If the context doesn't contain the answer, say "Data not found in current archives."
            
            TONE: Executive, Cybernetic, Efficient.
            """
            
            response = run_groq_inference(system_prompt, "Answer brief and accurate.")
            
            # 4. Display Result
            st.markdown(f"""
            <div style="background: rgba(20, 20, 30, 0.8); border: 1px solid #00d4ff; border-radius: 12px; padding: 25px; margin-bottom: 20px;">
                <h3 style="color: #00d4ff; margin-top: 0;">🔮 ORACLE ANSWER</h3>
                <div style="font-size: 1.1rem; line-height: 1.6; color: #fff;">
                    {response}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 5. SPECIAL: CLUSTER INTELLIGENCE (If relevant)
            if "cluster" in query.lower() or "network" in query.lower() or "connect" in query.lower():
                clusters = get_high_value_clusters()
                if clusters:
                     st.markdown("### 🧬 DETECTED CLUSTERS (Deal + Contact Overlap)")
                     for comp, data in clusters.items():
                         with st.expander(f"🔵 {comp} ({len(data['contacts'])} Contacts)", expanded=True):
                             st.caption(f"🎯 Role: {data['deal']['role']}")
                             for c in data['contacts']:
                                 st.markdown(f"- **{c['name']}**: {c['role']}")

            # 6. Show Sources
            st.markdown("### 📚 SOURCE ARTIFACTS")
            cols = st.columns(3)
            for i, res in enumerate(top_docs):
                with cols[i]:
                    st.markdown(f"""
                    <div style="background: #111; border: 1px solid #333; border-radius: 8px; padding: 15px;">
                        <div style="color: #FFD700; font-size: 0.8rem; font-weight: bold;">{res['source']}</div>
                        <div style="color: #666; font-size: 0.7rem; margin-top: 5px;">Relevance: {res['score']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("View Content"):
                        st.text(res['full_content'])

