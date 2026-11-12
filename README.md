# KrishiMitra AI – Telugu Voice-First Agricultural Assistant

A Streamlit prototype for asking farming questions in Telugu. It includes:
- Typed-question demo flow
- Rule-based Telugu responses clearly labelled as demo output
- SQLite interaction history
- Optional Gnani Prisma v3.0 transcription and Timbre v2.5 speech synthesis

## 1. Requirements
- Python 3.10+
- VS Code
- Internet connection for package installation and Gnani API calls

## 2. Create and activate a virtual environment

### Windows PowerShell
```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```cmd
.venv\\Scripts\\activate.bat
```

## 3. Install packages
```bash
pip install -r requirements.txt
```

## 4. Configure API access
Copy `.env.example` to `.env` and add your API key ID:
```env
GNANI_API_KEY_ID=your_key_id_here
```
Do not share your key or upload `.env` to GitHub.

Without a key, typed questions work in clearly labelled demo mode. Voice transcription and generated audio require real Gnani API access.

## 5. Run
```bash
streamlit run app.py
```
Open the local URL printed in the terminal, usually http://localhost:8501.

## API integration notes
- Prisma v3.0: `POST https://api.vachana.ai/stt/v3`
- Header: `X-API-Key-ID`
- Form fields: `model=prisma-v3.0`, `language_code=te-IN`, `format=transcribe`
- Timbre v2.5: `POST https://api.vachana.ai/api/v1/tts/inference`
- Telugu voice: `Suhana`

Check the current Gnani docs and your account's API permissions before production use.

## Current limitations
- The advisor is rule-based demo logic, not Evon.
- No live weather or government-scheme database is connected.
- It does not diagnose crop disease from images.
- Agricultural advice is educational; confirm treatment decisions with KVK or a qualified local agriculture officer.
