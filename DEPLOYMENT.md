# Streamlit Cloud Deployment Guide

## Prerequisites

✅ GitHub account  
✅ Streamlit account  
✅ Groq API key  
✅ Code pushed to GitHub  

---

## Step-by-Step Deployment

### Step 1: Push Code to GitHub ✅

Your code is ready! Just commit and push:

```powershell
git add .
git commit -m "CTR Processor with AI company detection"
git push origin main
```

**Verify:**
- All files are on GitHub
- `.streamlit/secrets.toml` is NOT in the repo (check `.gitignore`)

### Step 2: Deploy to Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"New app"**
3. Select your GitHub repository
4. Configure:
   - **Repository:** Your-Username/Your-Repo
   - **Branch:** main
   - **Main file path:** streamlit_app.py
5. Click **"Deploy"**

The app will start deploying (might take 1-2 minutes)

### Step 3: Add Secrets to Streamlit Cloud

Once deployed:

1. Click the **three dots ⋮** (top right)
2. Select **"Settings"**
3. Go to **"Secrets"** tab
4. Paste your API key:
   ```toml
   GROQ_API_KEY = "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"
   ```
5. Click **"Save"**
6. Your app will auto-refresh with the API key loaded

### ✅ Done! Your app is live!

Your app will be available at: `https://share.streamlit.io/your-username/your-repo/main/streamlit_app.py`

(Exact URL shown on Streamlit Cloud dashboard)

---

## How Secrets Work

### Local (Your Computer)
- API key in `.streamlit/secrets.toml`
- App accesses via `st.secrets.get("GROQ_API_KEY")`

### Streamlit Cloud
- Secrets added via web dashboard
- App accesses via same `st.secrets.get("GROQ_API_KEY")`
- **No code changes needed!**

---

## File Structure for Deployment

```
your-repo/
├── streamlit_app.py           ✅ Deployed
├── company_config.json        ✅ Deployed
├── requirements.txt           ✅ Deployed
├── README.md                  ✅ Deployed
├── .streamlit/
│   └── secrets.toml          ❌ NOT deployed (in .gitignore)
├── .gitignore                ✅ Deployed
└── .git/                      Hidden
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'groq'"
- Streamlit Cloud reads `requirements.txt` automatically
- Make sure `groq` is in requirements.txt ✅ Done

### "GROQ_API_KEY not configured"
- Add it to Streamlit Cloud Secrets (Settings → Secrets)
- Wait ~30 seconds for the app to redeploy

### App crashes after deploying
- Check Streamlit Cloud logs (click "Manage app" → "Logs")
- Usually means missing dependency or API key issue

### Want to update code?
- Push to GitHub: `git push`
- Streamlit Cloud auto-redeploys in ~30 seconds
- No need to redeploy manually

---

## Cost

**Streamlit Cloud:** Free tier available  
**Groq:** Free tier (100+ requests per minute)

Both have generous free tiers!

---

## Support

- **Streamlit:** [docs.streamlit.io](https://docs.streamlit.io)
- **Groq:** [console.groq.com/docs](https://console.groq.com/docs)
