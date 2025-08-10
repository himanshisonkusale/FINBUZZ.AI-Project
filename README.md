# 🚀 FINBUZZ.AI

**An intelligent financial analysis and insights platform powered by AI**

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

FINBUZZ.AI is a comprehensive financial analysis platform that leverages artificial intelligence to provide insights, analytics, and intelligent financial recommendations. The platform features multiple analysis modules and an interactive interface for financial data processing.

## 📁 Project Structure

```
FINBUZZ.AI/
├── 📁 user_data/                # User-specific data and uploads
│   └── (user files and data)
├── 📄 ag.py                     # Main application entry point
├── 📄 tab2.py                   # Secondary analysis module
├── 📄 tab3.py                   # Tertiary analysis module
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Environment variables
├── 📄 packages.txt              # System packages for deployment
├── 📄 runtime.txt               # Python runtime specification
├── 🖼️ finbuzz.png               # Application logo/assets
├── 📁 venv/                     # Virtual environment (created during setup)
└── 📄 README.md                 # This file
```

## ⚡ Prerequisites

Before you begin, ensure you have the following requirements:

- **Operating System**: Windows 10/11, macOS 10.14+, or Ubuntu 18.04+
- **Python**: Version 3.12.x (required)
- **Memory**: Minimum 4GB RAM recommended
- **Storage**: At least 2GB free space

## 🛠️ Installation Guide

### Step 1: Verify Python 3.12 Installation

First, check if Python 3.12 is already installed:

```bash
python3.12 --version
```

**Expected Output:**
```
Python 3.12.x
```

If you see this output, skip to [Step 2](#step-2-create-virtual-environment). Otherwise, continue with the installation below.

### Installing Python 3.12

#### 🍎 **macOS (Using Homebrew)**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12
brew install python@3.12
brew link python@3.12 --force
```

#### 🐧 **Linux (Ubuntu/Debian)**
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

#### 🪟 **Windows**

**Option 1: Official Python.org Installer (Recommended)**
1. Visit: https://www.python.org/downloads/windows/
2. Download the Python 3.12.x Windows installer
3. Run installer and **✅ CHECK "Add Python 3.12 to PATH"**
4. Complete the installation

**Option 2: Using Winget**
```powershell
winget install --id Python.Python.3.12
```

**Option 3: Using Chocolatey**
```powershell
choco install python --version=3.12.0
```

### Step 2: Create Virtual Environment

Navigate to your project directory and create a virtual environment:

```bash
# Create virtual environment
python3.12 -m venv venv
```

### Step 3: Activate Virtual Environment

#### 🍎 **macOS/Linux:**
```bash
source venv/bin/activate
```

#### 🪟 **Windows (PowerShell):**
```powershell
.\venv\Scripts\activate
```

#### 🪟 **Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

### Step 4: Verify Installation

After activation, verify you're using the correct Python version:

```bash
python --version
```

**Expected Output:**
```
Python 3.12.x
```

You should also see `(venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

## ⚙️ Configuration

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install System Dependencies

#### 🍎 **macOS:**
```bash
brew install espeak
```

#### 🐧 **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install espeak espeak-data libespeak1 libespeak-dev
```

#### 🪟 **Windows:**

**Option 1: Chocolatey (Recommended)**
```powershell
choco install espeak
```

**Option 2: Manual Installation**
1. Visit: https://espeak.sourceforge.net/download.html
2. Download the Windows ZIP installer
3. Extract to a folder (e.g., `C:\espeak`)
4. Add the espeak binary folder to your system PATH

### Step 3: Environment Configuration

1. **Copy the example environment file:**
   ```bash
   cp configuration/.env.example configuration/.env
   ```

2. **Edit the `.env` file** with your specific configuration:
   ```bash
   nano configuration/.env
   # or use your preferred text editor
   ```

## 🚀 Running the Application

### Local Development

1. **Ensure your virtual environment is activated:**
   ```bash
   # You should see (venv) in your prompt
   source venv/bin/activate  # macOS/Linux
   # or
   .\venv\Scripts\activate   # Windows
   ```

2. **Start the FINBUZZ.AI agent:**
   ```bash
   python ag.py
   ```

3. **Access the application:**
   - Open your web browser
   - Navigate to: `http://localhost:7860`
   - The FINBUZZ.AI interface should load

### Expected Startup Output

```
🚀 Starting FINBUZZ.AI...
📊 Loading financial modules...
✅ Tab2 module initialized
✅ Tab3 module initialized
🌐 Server running on http://localhost:7860
```

## ✨ Features

- **🤖 AI-Powered Analysis**: Advanced financial insights using machine learning
- **📊 Multi-Tab Interface**: Organized analysis across different modules
- **📈 Real-time Data Processing**: Live financial data analysis
- **🔊 Audio Feedback**: Text-to-speech capabilities for accessibility
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🔐 Secure Data Handling**: Privacy-focused user data management

## 🔧 Troubleshooting

### Common Issues and Solutions

#### ❌ **"python3.12 command not found"**
**Solution:** Python 3.12 is not installed or not in PATH
- Follow the [Python 3.12 installation guide](#installing-python-312) above
- On Windows, ensure "Add to PATH" was checked during installation

#### ❌ **"pip install fails"**
**Solution:** Virtual environment issues
```bash
# Deactivate and recreate venv
deactivate
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install --upgrade pip
pip install -r requirements.txt
```

#### ❌ **"espeak not found"**
**Solution:** System dependencies not installed
- Follow the [system dependencies installation](#step-2-install-system-dependencies) for your OS

#### ❌ **Port 7860 already in use**
**Solution:** Another application is using the port
```bash
# Find process using port 7860
lsof -i :7860  # macOS/Linux
netstat -ano | findstr :7860  # Windows

# Kill the process or change port in ag.py
```

#### ❌ **Module import errors**
**Solution:** Dependencies not properly installed
```bash
pip install --upgrade -r requirements.txt
```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs** in the terminal where you ran `python ag.py`
2. **Verify all dependencies** are installed correctly
3. **Ensure Python 3.12** is being used: `python --version`
4. **Check your virtual environment** is activated: look for `(venv)` in prompt

## 📊 Performance Tips

- **Memory Usage**: The application typically uses 500MB-1GB RAM
- **Startup Time**: First launch may take 30-60 seconds to load AI models
- **Browser Compatibility**: Chrome, Firefox, Safari, and Edge are supported
- **Data Processing**: Large datasets may require additional memory

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
# Activate virtual environment
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Update packages
pip install --upgrade -r requirements.txt
```

### Backing Up User Data
```bash
# Create backup of user data
cp -r user_data/ user_data_backup_$(date +%Y%m%d)/
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

---

**🎉 Happy Analyzing with FINBUZZ.AI!**

*Made with ❤️ by the FINBUZZ.AI Team*
