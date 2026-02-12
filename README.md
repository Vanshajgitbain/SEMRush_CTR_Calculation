# CTR Processor with AI-Powered Company Detection

## 🚀 Quick Start (Local)

### 1. Get Groq API Key (Free)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Create a new API key
4. Copy your API key

### 2. Add API Key to Secrets File

The API key is stored in `.streamlit/secrets.toml` (already created):

```toml
GROQ_API_KEY = "your_api_key_here"
```

**Already done!** The file is created. Just verify it has your API key.

### 3. Run Locally

```powershell
cd "C:\Users\78594\OneDrive - Bain\Documents\Training\New folder"
streamlit run streamlit_app.py
```

Visit: `http://localhost:8501`

---

## 📤 Push to GitHub

```powershell
git add .
git commit -m "Add CTR Processor with AI company detection"
git push origin main
```

**✅ Your API key is safe!** (`.streamlit/secrets.toml` is in `.gitignore`)

---

## ☁️ Deploy to Streamlit Cloud

### Step 1: Push to GitHub (Done ✅)

### Step 2: Create Streamlit Cloud App

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your GitHub repo, branch, and `streamlit_app.py`
4. Click **"Deploy"**

### Step 3: Add API Key to Streamlit Cloud

1. Your app will appear on Streamlit Cloud
2. Click **three dots ⋮** → **Settings**
3. Go to **"Secrets"** tab
4. Paste this:
```toml
GROQ_API_KEY = "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"
```
5. Click **"Save"**

### Step 4: Done! 🎉

Your app is now live on Streamlit Cloud with AI company detection!

---

## 📁 Project Structure

```
├── streamlit_app.py          # Main app
├── company_config.json       # Learned companies
├── requirements.txt          # Dependencies
├── .streamlit/
│   └── secrets.toml         # Local API key (not pushed to GitHub)
├── .gitignore               # Protects secrets
└── README.md                # This file
```

---

## ✨ Features

✅ AI-powered company detection using Groq  
✅ Automatic learning of new companies  
✅ No manual configuration needed  
✅ Secure API key handling  
✅ Works locally and on Streamlit Cloud  
✅ CTR calculation and Excel export  

---

## 🔑 Security Best Practices

- **✅ API key in `.streamlit/secrets.toml`** (not in code)
- **✅ `.gitignore` prevents secrets from GitHub**
- **✅ Streamlit Cloud secrets are separate from code**
- **❌ Never hardcode API keys in your code**
- **❌ Never commit `.streamlit/secrets.toml` to GitHub**

---

## 🐛 Troubleshooting

**"GROQ_API_KEY not configured"**
- Make sure `.streamlit/secrets.toml` has your API key
- If on Streamlit Cloud, add it via Settings → Secrets

**"Unknown Company"**
- Ensure Column A has company keywords
- Company names should be recognizable (e.g., "IDFC First Bank", "Bank of America")

**App won't start**
- Check if all packages are installed: `pip install -r requirements.txt`
- Make sure you're in the right directory

