# Savion  
*A personal tax‑saving assistant for Indian Income‑Tax Sections 80C & 80D*  

---

## 📖 Overview
Savion analyzes a CSV bank statement, identifies gaps in tax‑planning for  
- **Section 80C** (₹1,50,000 cap)  
- **Section 80D** (₹25,000 for self/parents, +₹5,000 for seniors)  

and recommends investment instruments to hit the maximum deduction.  
It’s delivered as a simple CLI (`savion-cli`) and can generate a dark‑theme HTML report with progress bars and AI‑generated rationales.

> **Public repo** – anyone can view the code.  
> **No secrets committed** – all sensitive keys are read from a `.env` file that’s ignored.

---

## 🚀 Quick Start

```powershell
# 1️⃣  Clone the repo
git clone https://github.com/ACLICXDD/savion-tax-assistant.git
cd savion-tax-assistant

# 2️⃣  Create & activate a virtual environment (Python 3.11+)
python -m venv .venv
.\.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # macOS/Linux

# 3️⃣  Install dependencies in editable mode
pip install -e .

# 4️⃣  Set your LLM API key (Groq/OpenAI)
echo "LLM_API_KEY=gsk_your_groq_key_here" > .env
<img width="920" height="646" alt="image" src="https://github.com/user-attachments/assets/b0dda05c-5f6b-46ff-bdf5-f54f8c5bb491" />

