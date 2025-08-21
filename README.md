# 🚀 FINBUZZ.AI

An intelligent financial analysis and insights platform powered by AI, now featuring **Autonomous AI Trading Agent** capabilities

![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg) ![Status](https://img.shields.io/badge/status-active-brightgreen.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![AI Trading](https://img.shields.io/badge/AI-Trading%20Agent-ff6b35.svg) ![AutoGen](https://img.shields.io/badge/Microsoft-AutoGen-blue.svg) ![Version](https://img.shields.io/badge/version-v2.0.0-purple.svg)

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🤖 NEW: AI Trading Agent](#-new-ai-trading-agent)
- [📁 Project Structure](#-project-structure)
- [⚡ Prerequisites](#-prerequisites)
- [🛠️ Installation Guide](#️-installation-guide)
- [⚙️ Configuration](#️-configuration)
- [🚀 Running the Application](#-running-the-application)
- [✨ Features](#-features)
- [📈 Trading Agent Features](#-trading-agent-features)
- [🔧 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🎯 Overview

FINBUZZ.AI is a comprehensive financial analysis platform that leverages artificial intelligence to provide insights, analytics, and intelligent financial recommendations. The platform now features an **advanced AI Trading Agent** that can autonomously execute trading strategies using Microsoft AutoGen framework with real-time market data analysis.

### 🆕 What's New
- **🤖 Autonomous AI Trading Agent**: Fully automated trading with Microsoft AutoGen
- **📊 Real-time Market Analysis**: Live 1-minute candlestick data processing
- **🧠 Intelligent Decision Making**: AI-powered BUY/SELL/HOLD decisions
- **📈 Advanced Technical Analysis**: Volume spikes, momentum, and trend analysis
- **💡 Learning System**: Adapts strategy based on trading performance
- **⚡ Multiple Speed Modes**: Fast simulation and real-time trading modes

## 🤖 NEW: AI Trading Agent

### 🎯 Core Capabilities
- **Autonomous Trading**: AI agent makes independent trading decisions
- **Risk Management**: Intelligent position sizing and stop-loss mechanisms
- **Technical Analysis**: Real-time calculation of SMA, momentum, and volume indicators
- **Performance Tracking**: Comprehensive P&L analysis and win rate optimization
- **Market Adaptation**: Learning system that improves strategy over time

### 🔥 Key Features
```
✅ Real-time 1-minute candlestick analysis
✅ Intelligent position sizing (up to 90% capital deployment)
✅ Advanced risk management with 2% stop-losses
✅ Volume spike detection and momentum analysis
✅ Adaptive learning from trading history
✅ Premium UI with dark theme and real-time charts
✅ Multiple API support (OpenAI GPT-4 / Google Gemini)
✅ Fallback deterministic strategy when no API available
```

## 📁 Project Structure

```
FINBUZZ.AI/
├── 📁 user_data/                # User-specific data and uploads
│   └── (user files and data)
├── 📁 data/                     # Trading data storage
│   └── (market data CSVs)
├── 📄 app.py                    # 🆕 AI Trading Agent Gradio Interface
├── 📄 trader_agent.py           # 🆕 Core AI Trading Logic with AutoGen
├── 📄 market.py                 # 🆕 Market Data Processing & Streaming
├── 📄 portfolio.py              # 🆕 Portfolio Management System
├── 📄 charting.py               # 🆕 Advanced Candlestick Visualization
├── 📄 ag.py                     # Original application entry point
├── 📄 tab2.py                   # Secondary analysis module
├── 📄 tab3.py                   # Tertiary analysis module
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Environment variables (API keys)
├── 📄 packages.txt              # System packages for deployment
├── 📄 runtime.txt               # Python runtime specification
├── 📁 venv/                     # Virtual environment
└── 📄 README.md                 # This file
```

## ⚡ Prerequisites

Before you begin, ensure you have the following requirements:

- **Operating System**: Windows 10/11, macOS 10.14+, or Ubuntu 18.04+
- **Python**: Version 3.12.x (required)
- **Memory**: Minimum 4GB RAM recommended (8GB for AI Trading Agent)
- **Storage**: At least 2GB free space
- **Internet Connection**: Required for real-time market data
- **API Keys** (optional): OpenAI or Google Gemini for enhanced AI trading

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

If you see this output, skip to Step 2. Otherwise, continue with the installation below.

### Installing Python 3.12

#### 🍎 macOS (Using Homebrew)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12
brew install python@3.12
brew link python@3.12 --force
```

#### 🐧 Linux (Ubuntu/Debian)

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

#### 🪟 Windows

**Option 1: Official Python.org Installer (Recommended)**

1. Visit: https://www.python.org/downloads/windows/
2. Download the Python 3.12.x Windows installer
3. Run installer and ✅ **CHECK "Add Python 3.12 to PATH"**
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

**🍎 macOS/Linux:**
```bash
source venv/bin/activate
```

**🪟 Windows (PowerShell):**
```powershell
.\venv\Scripts\activate
```

**🪟 Windows (Command Prompt):**
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

#### 🍎 macOS:
```bash
brew install espeak
```

#### 🐧 Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install espeak espeak-data libespeak1 libespeak-dev
```

#### 🪟 Windows:

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

Create your environment file:

```bash
cp .env.example .env
```

Edit the `.env` file with your specific configuration:

```bash
nano .env
# or use your preferred text editor
```

### 🔑 API Keys Setup (Optional but Recommended)

For enhanced AI trading capabilities, add API keys to your `.env` file:

```env
# For OpenAI GPT-4 (recommended)
OPENAI_API_KEY=your_openai_api_key_here

# Alternative: For Google Gemini
GEMINI_API_KEY_TraderAgent=your_gemini_api_key_here

# Trading configuration
USE_LLM=true
```

**💡 Note**: The AI Trading Agent works without API keys using a sophisticated fallback strategy, but performs best with AI models.

## 🚀 Running the Application

### Original FINBUZZ.AI Platform

Ensure your virtual environment is activated:

```bash
# You should see (venv) in your prompt
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\activate   # Windows
```

Start the FINBUZZ.AI platform:

```bash
python ag.py
```

Access the application:
- Open your web browser
- Navigate to: **http://localhost:7860**
- The FINBUZZ.AI interface should load

### 🆕 AI Trading Agent

To run the new **AI Trading Agent**:

```bash
python app.py
```

Access the AI Trading Agent:
- Open your web browser  
- Navigate to: **http://localhost:7860**
- You'll see the **AI-Powered Autonomous Trading Agent** interface

### 🎯 Expected Startup Output

```
🚀 Starting FINBUZZ.AI AI Trading Agent...
🤖 Loading Microsoft AutoGen framework...
📊 Initializing market data streams...
🧠 AI Trading intelligence activated...
✅ Portfolio management system ready
✅ Real-time charting engine loaded
✅ Risk management protocols active
🌐 Server running on http://localhost:7860
```

## ✨ Features

### Core FINBUZZ.AI Features
- 🤖 **AI-Powered Analysis**: Advanced financial insights using machine learning
- 📊 **Multi-Tab Interface**: Organized analysis across different modules
- 📈 **Real-time Data Processing**: Live financial data analysis
- 🔊 **Audio Feedback**: Text-to-speech capabilities for accessibility
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🔐 **Secure Data Handling**: Privacy-focused user data management

## 📈 Trading Agent Features

### 🎯 Agent Setup Tab
```
🚀 LAUNCH AI TRADING AGENT
├── 💰 Starting Cash Configuration (₹10,000 default)
├── 📈 NSE Ticker Selection (e.g., HUDCO.NS)
├── 🤖 Microsoft AutoGen Integration
├── 📊 Real-time Market Context Preview
└── ⚡ Instant Agent Deployment
```

### 🎯 AI Agent Trading Tab
```
🎯 INTELLIGENT TRADING MODES
├── ⚡ Fast (1min per bar) - Rapid Simulation
├── 🕒 Real-time (5m) - Live Market Simulation
├── 🤖 START/PAUSE/STEP Controls
├── 📊 Premium Candlestick Charts
├── 💼 Live Portfolio Tracking
└── 🧠 Real-time Decision Logs
```

### 🎯 AI Analytics Tab
```
📊 PERFORMANCE DASHBOARD
├── 📈 Cumulative P&L Tracking
├── 📊 Trade Distribution Analysis  
├── 💰 Portfolio Value Monitoring
├── 🎯 Win Rate Calculations
├── 📋 Detailed Trading Statistics
└── ⏱️ Auto-refresh Analytics
```

### 🧠 AI Intelligence Features

#### **Decision Making Engine**
- **Technical Analysis**: SMA (5, 10, 20), momentum, volume spikes
- **Pattern Recognition**: Learning from successful and failed trades
- **Risk Assessment**: Dynamic position sizing based on market conditions
- **Performance Adaptation**: Strategy adjusts based on win/loss rates

#### **Trading Strategies**
```
🎯 AGGRESSIVE INTELLIGENT POLICY
├── 💪 High Conviction Trades: Up to 50% of capital
├── 🎯 Medium Conviction: 25-35% of capital  
├── 🔍 Low Conviction Scalps: 10-20% of capital
├── 📈 Scale Into Winners: Add to profitable positions
├── ⛔ Smart Stop Losses: 2% automatic exits
└── 💰 Partial Profit Taking: Sell 1/3 on 3%+ gains
```

#### **Learning & Adaptation**
- **Performance Tracking**: Win rate, average P&L, best/worst trades
- **Pattern Memory**: Remembers successful setups and market conditions  
- **Adaptive Sizing**: More aggressive when performing well, conservative when struggling
- **Market Context**: Time-of-day patterns and volume analysis

### 🎨 Premium User Interface

#### **Dark Theme Design**
- **JetBrains Mono Font**: Professional coding aesthetic
- **Neon Green Accents**: High-contrast visibility  
- **Real-time Charts**: Plotly-powered candlestick visualization
- **Responsive Layout**: Works on all screen sizes

#### **Interactive Elements**
- **Live Trading Markers**: BUY/SELL signals on charts
- **Hover Details**: Comprehensive trade information
- **Auto-refresh**: Real-time updates without page reload
- **Performance Metrics**: Live P&L and win rate tracking

## 🔧 Troubleshooting

### Common Issues and Solutions

#### ❌ "python3.12 command not found"
**Solution**: Python 3.12 is not installed or not in PATH
- Follow the Python 3.12 installation guide above
- On Windows, ensure "Add to PATH" was checked during installation

#### ❌ "pip install fails"
**Solution**: Virtual environment issues
```bash
# Deactivate and recreate venv
deactivate
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install --upgrade pip
pip install -r requirements.txt
```

#### ❌ "espeak not found"
**Solution**: System dependencies not installed
- Follow the system dependencies installation for your OS

#### ❌ Port 7860 already in use
**Solution**: Another application is using the port
```bash
# Find process using port 7860
lsof -i :7860  # macOS/Linux
netstat -ano | findstr :7860  # Windows

# Kill the process or change port in app.py/ag.py
```

#### ❌ Module import errors
**Solution**: Dependencies not properly installed
```bash
pip install --upgrade -r requirements.txt
```

#### ❌ "No data returned for ticker"
**Solution**: Market data issues
- Ensure you're using valid NSE ticker format (e.g., HUDCO.NS)
- Check internet connection for yfinance data download
- Try different ticker symbols

#### ❌ "AI Agent not making trades"
**Solution**: API key or model issues
- Check `.env` file for valid API keys
- Verify `USE_LLM=true` in environment
- Agent will use fallback strategy without API keys

### 🆘 Getting Help

If you encounter issues not covered here:

1. **Check Logs**: Monitor the terminal where you ran `python app.py`
2. **Verify Dependencies**: Ensure all packages are installed correctly
3. **Python Version**: Confirm Python 3.12 is active: `python --version`
4. **Virtual Environment**: Look for `(venv)` in your terminal prompt
5. **API Configuration**: Verify API keys in `.env` file
6. **Market Hours**: Ensure trading during NSE market hours (9:15 AM - 3:30 PM IST)

## 📊 Performance Tips

### System Requirements
- **Memory Usage**: 
  - Original platform: 500MB-1GB RAM
  - AI Trading Agent: 1-2GB RAM (more with AI models)
- **Startup Time**: 
  - First launch: 30-60 seconds to load AI models
  - Subsequent launches: 15-30 seconds
- **Browser Compatibility**: Chrome, Firefox, Safari, and Edge supported
- **Data Processing**: Large datasets may require additional memory

### Optimization Tips
- **Fast Mode**: Use "Fast (1min per bar)" for quick backtesting
- **Real-time Mode**: Use "Real-time (5m)" for live market simulation  
- **API Usage**: OpenAI GPT-4 provides best trading decisions
- **Memory Management**: Close unused browser tabs during trading
- **Network**: Stable internet connection required for real-time data

## 🔄 Updates and Maintenance

### Updating Dependencies

```bash
# Activate virtual environment
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Update packages
pip install --upgrade -r requirements.txt
```

### Backing Up Trading Data

```bash
# Create backup of trading data
cp -r data/ data_backup_$(date +%Y%m%d)/
cp -r user_data/ user_data_backup_$(date +%Y%m%d)/
```

### 🔄 Updating API Keys

Edit your `.env` file to update API keys:
```env
# Update with new keys
OPENAI_API_KEY=your_new_openai_key
GEMINI_API_KEY_TraderAgent=your_new_gemini_key
```

## 🤝 Contributing

We welcome contributions to both the original platform and the new AI Trading Agent! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing trading feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### 🎯 Areas for Contribution
- **Trading Strategies**: New AI trading algorithms
- **Technical Indicators**: Additional market analysis tools
- **UI Improvements**: Enhanced user interface features
- **Performance Optimization**: Speed and memory improvements
- **Documentation**: Improved guides and examples
- **Testing**: Unit tests and integration tests

## 📄 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software in accordance with the license terms.

### MIT License

```
MIT License

Copyright (c) 2025 FINBUZZ.AI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 📋 License Terms Summary

- ✅ **Commercial Use**: Use for commercial purposes
- ✅ **Modification**: Modify the source code
- ✅ **Distribution**: Distribute original or modified versions
- ✅ **Private Use**: Use privately without restrictions
- ⚠️ **Liability**: Authors not liable for damages
- ⚠️ **Warranty**: No warranty provided

### 🔒 Additional Terms

- **Attribution**: Include copyright notice in distributions
- **Trading Risk**: Use trading features at your own risk
- **API Costs**: User responsible for third-party API costs (OpenAI/Gemini)
- **Market Data**: Comply with data provider terms of service

---

## 🎉 Happy Trading and Analyzing with FINBUZZ.AI!

### 🚀 Quick Start Commands

```bash
# Clone and setup
git clone <repository-url>
cd FINBUZZ.AI
python3.12 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run original platform
python ag.py

# Run AI Trading Agent  
python app.py
```

### 🌟 What's Next?
- **Multi-Asset Trading**: Support for multiple NSE stocks
- **Options Trading**: AI agent for options strategies
- **Portfolio Optimization**: AI-powered portfolio allocation
- **Social Trading**: Share and copy successful strategies
- **Mobile App**: Native iOS/Android applications

---

*Made with ❤️ by the FINBUZZ.AI Team*

*Powered by Microsoft AutoGen • OpenAI GPT-4 • Google Gemini • Python 3.12*
