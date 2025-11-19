# Environment Setup Guide

Complete guide for creating and managing Python environments for the LangFlow + watsonx.ai demo.

## 📋 Table of Contents

- [Python 3.11 Requirements](#python-311-requirements)
- [Virtual Environment Methods](#virtual-environment-methods)
- [Platform-Specific Setup](#platform-specific-setup)
- [IDE Integration](#ide-integration)
- [Troubleshooting](#troubleshooting)

## 🐍 Python 3.11 Requirements

This project requires **Python 3.11** or higher.

### Why Python 3.11?

- ✅ Improved performance (10-60% faster)
- ✅ Better error messages
- ✅ Native async improvements
- ✅ Modern type hints support
- ✅ Required by latest LangFlow versions

### Check Your Python Version

```bash
python --version
# or
python3 --version
```

Expected output: `Python 3.11.x` or `Python 3.12.x`

## 🔧 Virtual Environment Methods

### Method 1: venv (Standard, Recommended)

**Create environment:**
```bash
# Unix/macOS
python3.11 -m venv venv

# Windows
python -m venv venv
```

**Activate:**
```bash
# Unix/macOS
source venv/bin/activate

# Windows (cmd)
venv\Scripts\activate.bat

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Git Bash (Windows)
source venv/Scripts/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Deactivate:**
```bash
deactivate
```

### Method 2: Using Makefile

**Unix/macOS/Linux:**
```bash
make install
```

**Windows (with Make):**
```bash
make install
# or
make windows-install
```

### Method 3: conda/mamba (Alternative)

**Create environment:**
```bash
conda create -n langflow-demo python=3.11
conda activate langflow-demo
pip install -r requirements.txt
```

**Or with mamba (faster):**
```bash
mamba create -n langflow-demo python=3.11
mamba activate langflow-demo
pip install -r requirements.txt
```

### Method 4: pyenv + venv

**Install specific Python version:**
```bash
pyenv install 3.11.7
pyenv local 3.11.7
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Method 5: pipenv (Alternative)

```bash
pipenv --python 3.11
pipenv install
pipenv shell
```

### Method 6: poetry (Alternative)

```bash
poetry env use 3.11
poetry install
poetry shell
```

## 🖥️ Platform-Specific Setup

### Linux (Ubuntu/Debian)

```bash
# Install Python 3.11 if not available
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Create and activate environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Linux (Fedora/RHEL)

```bash
# Install Python 3.11
sudo dnf install python3.11

# Create and activate environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### macOS

**Using Homebrew:**
```bash
# Install Python 3.11
brew install python@3.11

# Create and activate environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Using pyenv (Recommended):**
```bash
# Install pyenv
brew install pyenv

# Install Python 3.11
pyenv install 3.11.7
pyenv local 3.11.7

# Create environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for comprehensive Windows guide.

**Quick start:**
```cmd
REM Using Command Prompt
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

```powershell
# Using PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 🎯 IDE Integration

### Visual Studio Code

**Automatic Setup:**
1. Open project folder
2. VS Code detects venv automatically
3. Select interpreter: `Python 3.11.x ('venv')`

**Manual Setup:**
1. Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
2. Type "Python: Select Interpreter"
3. Choose `./venv/bin/python`

**Settings (.vscode/settings.json):**
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "python.testing.pytestEnabled": true
}
```

### PyCharm

**Setup:**
1. File → Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select "Existing environment"
4. Choose `venv/bin/python` (or `venv\Scripts\python.exe` on Windows)
5. Click OK

**Configure Project:**
1. Mark `agent_langflow` as sources root
2. Enable pytest for testing
3. Set Black as formatter

### Jupyter Notebook

**Setup IPython kernel:**
```bash
source venv/bin/activate
pip install ipykernel
python -m ipykernel install --user --name=langflow-demo --display-name="LangFlow Demo (3.11)"
```

**Use in Jupyter:**
1. Start Jupyter: `jupyter notebook`
2. Select kernel: "LangFlow Demo (3.11)"

### Sublime Text

**Install Package Control**, then:

1. Install "Anaconda" package
2. Configure Python path in settings:
```json
{
    "python_interpreter": "/path/to/venv/bin/python"
}
```

## 🔍 Verifying Installation

### Check Python Version in Environment

```bash
# Activate environment first
source venv/bin/activate  # Unix
# or
venv\Scripts\activate.bat  # Windows

# Check Python version
python --version
# Should show: Python 3.11.x

# Check which python
which python  # Unix
# or
where python  # Windows
# Should point to venv
```

### Check Installed Packages

```bash
# List all packages
pip list

# Check specific packages
pip show langflow
pip show langchain-ibm
pip show python-dotenv
```

### Verify Imports

```bash
python -c "import langflow; print('LangFlow OK')"
python -c "from langchain_ibm import ChatWatsonx; print('LangChain IBM OK')"
python -c "from dotenv import load_dotenv; print('DotEnv OK')"
```

### Test Full Setup

```bash
# Make sure .env exists
cp .env.example .env
# Edit .env with your credentials

# Run test
python agent_langflow.py --simple
```

## 🐛 Troubleshooting

### Issue: "Python 3.11 not found"

**Solution:**
```bash
# Check available Python versions
ls /usr/bin/python*  # Unix
# or
where python*  # Windows

# Install Python 3.11
# See platform-specific sections above
```

### Issue: "venv module not found"

**Solution (Ubuntu/Debian):**
```bash
sudo apt install python3.11-venv
```

**Solution (macOS):**
```bash
# Already included with Python from Homebrew
# If issue persists, reinstall:
brew reinstall python@3.11
```

### Issue: "No module named 'pip'"

**Solution:**
```bash
# Recreate venv
rm -rf venv
python3.11 -m venv venv --without-pip
source venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python
```

### Issue: "Permission denied" during installation

**Solution (Unix):**
```bash
# Don't use sudo with venv
# Instead ensure you own the directory
sudo chown -R $USER:$USER .
```

**Solution (Windows):**
- Run Command Prompt/PowerShell as Administrator
- Or install to user directory: `pip install --user`

### Issue: "Cannot activate venv on Windows PowerShell"

**Solution:**
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\venv\Scripts\Activate.ps1
```

### Issue: "Package conflicts during installation"

**Solution:**
```bash
# Clear pip cache
pip cache purge

# Reinstall with no cache
pip install --no-cache-dir -r requirements.txt

# Or create fresh environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "SSL certificate errors"

**Solution:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## 🔄 Updating Environment

### Update All Packages

```bash
pip install --upgrade -r requirements.txt
```

### Update Specific Package

```bash
pip install --upgrade langflow
```

### Freeze Current State

```bash
pip freeze > requirements-lock.txt
```

### Recreate from Scratch

```bash
# Remove old environment
rm -rf venv  # Unix
# or
rmdir /s /q venv  # Windows

# Create new
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📊 Environment Information

### Display Environment Details

```bash
# Using Makefile
make show-env

# Manual
python --version
pip --version
pip list
echo $VIRTUAL_ENV  # Unix
echo %VIRTUAL_ENV%  # Windows
```

### Export Environment

```bash
# Create exact replica
pip freeze > requirements-exact.txt

# Include development dependencies
pip freeze > requirements-dev.txt
```

## 🚀 Best Practices

### 1. Always Use Virtual Environments

✅ **DO:**
```bash
python -m venv venv
source venv/bin/activate
pip install package
```

❌ **DON'T:**
```bash
sudo pip install package  # Global install
```

### 2. Keep requirements.txt Updated

```bash
pip freeze > requirements.txt
```

### 3. Use .gitignore

Ensure `venv/` is in .gitignore:
```gitignore
venv/
.venv/
env/
ENV/
```

### 4. Document Python Version

In README.md or pyproject.toml:
```toml
requires-python = ">=3.11"
```

### 5. Regular Updates

```bash
pip list --outdated
pip install --upgrade package
```

## 📚 Additional Resources

- [Python venv documentation](https://docs.python.org/3/library/venv.html)
- [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)
- [pyenv GitHub](https://github.com/pyenv/pyenv)
- [Conda Documentation](https://docs.conda.io/)

---

**Environment setup complete!** 🎉

Your Python 3.11 environment is ready for LangFlow + watsonx.ai development!
