# Windows Setup Guide - Python 3.11

Complete guide for setting up LangFlow + watsonx.ai on Windows with Python 3.11.

## 📋 Prerequisites

### 1. Install Python 3.11

**Option A: Official Python Installer (Recommended)**

1. Download Python 3.11 from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **IMPORTANT**: Check "Add Python 3.11 to PATH"
4. Click "Install Now"
5. Verify installation:
   ```cmd
   python --version
   ```
   Should show: `Python 3.11.x`

**Option B: Windows Store**

1. Open Microsoft Store
2. Search "Python 3.11"
3. Click "Get" and install
4. Verify:
   ```cmd
   python --version
   ```

**Option C: Chocolatey**

```cmd
choco install python311
```

### 2. Install Git (Optional but Recommended)

Download from: https://git-scm.com/download/win

### 3. Get IBM watsonx.ai Credentials

- API Key: https://cloud.ibm.com/iam/apikeys
- Project ID: From your watsonx.ai project settings

## 🚀 Installation Methods

### Method 1: Using Make (Recommended)

**Install Make for Windows:**

**Option A: Git Bash (Comes with Git)**
```bash
# Open Git Bash
make install
make setup
make demo
```

**Option B: Chocolatey**
```cmd
choco install make
make install
make setup
make demo
```

**Option C: Scoop**
```powershell
scoop install make
make install
make setup
make demo
```

### Method 2: Using PowerShell

**Step 1: Open PowerShell as Administrator**

```powershell
# Navigate to project directory
cd path\to\agent_langflow

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Setup environment
.\run.sh setup

# Run demo
python agent_langflow.py
```

### Method 3: Using Command Prompt (cmd)

**Step 1: Open Command Prompt as Administrator**

```cmd
REM Navigate to project directory
cd path\to\agent_langflow

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
pip install -r requirements.txt

REM Run demo
python agent_langflow.py
```

### Method 4: Using Windows Subsystem for Linux (WSL)

```bash
# Install WSL if not already installed
wsl --install

# Open WSL terminal
cd /mnt/c/path/to/agent_langflow

# Use Linux commands
make install
make setup
make demo
```

## 🔧 Manual Environment Setup

### Create .env File

**Option A: Using Notepad**

1. Open Notepad
2. Copy this template:
   ```
   WATSONX_APIKEY=your_api_key_here
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   WATSONX_PROJECT_ID=your_project_id_here
   DEFAULT_MODEL=ibm/granite-3-8b-instruct
   TEMPERATURE=0.7
   MAX_TOKENS=1000
   ```
3. Save as `.env` (with quotes in filename dialog)
4. Make sure "All Files" is selected in file type dropdown

**Option B: Using PowerShell**

```powershell
@"
WATSONX_APIKEY=your_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_project_id_here
DEFAULT_MODEL=ibm/granite-3-8b-instruct
TEMPERATURE=0.7
MAX_TOKENS=1000
"@ | Out-File -FilePath .env -Encoding UTF8
```

**Option C: Using Command Prompt**

```cmd
copy .env.example .env
notepad .env
```

## 🎯 Running the Application

### Activate Virtual Environment First!

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Git Bash:**
```bash
source venv/Scripts/activate
```

### Run Interactive Demo

```cmd
python agent_langflow.py
```

### Run Simple Demo

```cmd
python agent_langflow.py --simple
```

### Start LangFlow UI

```cmd
langflow run
```

Access at: http://localhost:7860

### Using Custom Model

```cmd
python agent_langflow.py --model ibm/granite-13b-instruct-v2
```

## 🐛 Troubleshooting Windows Issues

### Issue: "python is not recognized"

**Solution:**
1. Add Python to PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311`
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts`
2. Restart Command Prompt

### Issue: "cannot be loaded because running scripts is disabled"

**Solution (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "pip: command not found"

**Solution:**
```cmd
python -m pip install --upgrade pip
```

### Issue: "Access is denied" when installing packages

**Solution:**
- Run Command Prompt or PowerShell as Administrator
- Or use: `pip install --user package_name`

### Issue: LangFlow won't start

**Solution:**
```cmd
# Reinstall LangFlow
pip uninstall langflow
pip install langflow --upgrade --no-cache-dir
```

### Issue: Port 7860 already in use

**Solution:**
```cmd
# Use different port
langflow run --port 8080

# Or find and kill process using port
netstat -ano | findstr :7860
taskkill /PID <PID_NUMBER> /F
```

### Issue: SSL Certificate errors

**Solution:**
```cmd
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## 📦 Using Make Commands on Windows

### With Git Bash (Recommended)

```bash
# Install
make install

# Setup
make setup

# Run demo
make demo

# Start UI
make ui

# Clean
make clean

# Show help
make help
```

### With PowerShell (Using make.exe)

Same commands as above, but ensure `make.exe` is in your PATH.

## 🔒 Windows Security

### Windows Defender

If Windows Defender blocks Python or scripts:

1. Open Windows Security
2. Go to "Virus & threat protection"
3. Click "Manage settings"
4. Add exclusion for project folder

### Firewall

If prompted, allow Python through firewall for LangFlow UI.

## 📊 Verify Installation

### Check Python Version

```cmd
python --version
```
Expected: `Python 3.11.x`

### Check Pip Version

```cmd
pip --version
```

### Check Installed Packages

```cmd
pip list
```

Should show:
- langflow
- langchain-ibm
- python-dotenv

### Test Import

```cmd
python -c "import langflow; print('LangFlow OK')"
python -c "from langchain_ibm import ChatWatsonx; print('LangChain IBM OK')"
python -c "from dotenv import load_dotenv; print('DotEnv OK')"
```

## 🎓 Windows-Specific Tips

### 1. Use Windows Terminal (Recommended)

Download from Microsoft Store - better than cmd/PowerShell.

### 2. File Paths

Use forward slashes or escaped backslashes:
```python
path = "C:/Users/Name/project"  # Good
path = "C:\\Users\\Name\\project"  # Also good
path = "C:\Users\Name\project"  # Bad - will fail
```

### 3. Environment Variables

View all environment variables:
```cmd
set
```

Set temporary variable (current session):
```cmd
set WATSONX_APIKEY=your_key
```

### 4. Virtual Environment Location

Windows stores venv in different location:
- Unix/Mac: `venv/bin/activate`
- Windows: `venv\Scripts\activate.bat`

## 🚀 Quick Start Summary

**For PowerShell Users:**
```powershell
# 1. Create and activate venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file (edit with your credentials)
copy .env.example .env
notepad .env

# 4. Run demo
python agent_langflow.py
```

**For Command Prompt Users:**
```cmd
REM 1. Create and activate venv
python -m venv venv
venv\Scripts\activate.bat

REM 2. Install dependencies
pip install -r requirements.txt

REM 3. Create .env file (edit with your credentials)
copy .env.example .env
notepad .env

REM 4. Run demo
python agent_langflow.py
```

**For Git Bash Users:**
```bash
# 1. Use Make
make install
make setup
make demo

# Or manual
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
./run.sh setup
python agent_langflow.py
```

## 📚 Additional Resources

- [Python on Windows](https://docs.python.org/3/using/windows.html)
- [pip Documentation](https://pip.pypa.io/en/stable/)
- [Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [LangFlow Documentation](https://docs.langflow.org/)

## 🆘 Still Having Issues?

1. Check Python version: `python --version` (must be 3.11+)
2. Check pip version: `pip --version`
3. Try running as Administrator
4. Check firewall/antivirus settings
5. Try WSL as alternative
6. Check README.md for general troubleshooting

---

**Windows Setup Complete!** 🎉

Now you can start building with LangFlow + watsonx.ai on Windows!
