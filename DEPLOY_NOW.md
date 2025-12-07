# 🚀 BASIN::NEXUS DEPLOYMENT GUIDE

## Quick Deploy to Streamlit Cloud

### Step 1: Go to Streamlit Cloud
**URL:** https://share.streamlit.io

### Step 2: Connect GitHub
1. Click "Sign up" or "Log in" with GitHub
2. Authorize Streamlit to access your repos

### Step 3: Deploy Your App
1. Click "New app"
2. Repository: `BasinLeon/basin-signal-engine`
3. Branch: `main`
4. Main file path: `app.py`

### Step 4: Configure Secrets
In the "Advanced settings" section, add:

```toml
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
```

### Step 5: Deploy!
Click "Deploy!" and wait 2-3 minutes.

**Your app will be live at:** `basin-nexus.streamlit.app` (or similar)

---

## ✅ Pre-Deployment Checklist

- [x] `requirements.txt` exists and is complete
- [x] `.streamlit/config.toml` has theme settings
- [x] `secrets.toml.example` for reference
- [x] All code committed and pushed
- [x] No hardcoded API keys in code

---

## 🔗 After Deployment

1. **Update basinleon.github.io** with live NEXUS link
2. **Update GitHub README** with deployed link
3. **Post launch announcement** on LinkedIn

---

## Troubleshooting

**If deployment fails:**
- Check the logs in Streamlit Cloud dashboard
- Ensure all packages in requirements.txt are compatible
- Verify GROQ_API_KEY is set in secrets

**If app shows errors:**
- The app handles missing API keys gracefully
- Most features work in demo mode without keys

---

*Generated: 2025-12-07 | BASIN::NEXUS v0.5*
