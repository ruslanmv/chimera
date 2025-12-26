# 🐉 CHIMERA - Universal Desktop AI Assistant

<div align="center">

![Chimera Banner](https://img.shields.io/badge/Chimera-Universal_Desktop_AI-FF6B00?style=for-the-badge&logo=robot&logoColor=white)

**💻 Works with ANY Desktop App | 📸 Screenshot + Question = Instant Help | 🚀 VS Code • Office • UE5 • Browsers • More**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.127+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://opensource.org/licenses/MIT)
[![CI Tests](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/ruslanmv/chimera/actions)
[![Playwright](https://img.shields.io/badge/Tests-Playwright-45ba4b?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev/)

[🚀 Quick Start](#-quick-start) •
[🎯 How It Works](#-how-it-works) •
[🔌 Providers](#-llm-providers) •
[📚 Documentation](#-documentation) •
[⭐ Star Us](#-support-this-project)

</div>

---

## 🌟 What is Chimera?

**Chimera** is a **universal multimodal AI assistant** that works with **ANY desktop application**. It combines **computer vision** with **natural language processing** to provide instant help for whatever you're working on.

### 💡 The Problem

- Stuck on a coding issue in VS Code?
- Excel formula not working as expected?
- PowerPoint layout looking off?
- Unreal Engine Blueprint connection error?
- Browser DevTools confusion?
- Design tool color palette question?
- **You need help but explaining takes forever...**

### ✨ The Solution

Chimera works with **any app**:

1. **📸 Take a screenshot** of your active application (VS Code, Excel, UE5, Browser, etc.)
2. **💬 Ask a question** about what you're seeing
3. **🎯 Get step-by-step guidance** specific to your application and context

```bash
# Simple API call with screenshot + question
curl http://localhost:8000/api/v1/assist \
  -F "image=@screenshot.png" \
  -F "question=How do I fix this?" \
  -F "context=vscode"  # or excel, powerpoint, browser, ue5, etc.
```

**Response:**
```json
{
  "summary": "Syntax error - missing closing bracket",
  "steps": [
    {
      "title": "Add the missing closing bracket",
      "details": ["Go to line 42", "Add '}' at the end", "Save the file"],
      "why": "The function body is missing its closing bracket"
    },
    {
      "title": "Verify the fix",
      "details": ["Check for any remaining syntax errors", "Run your linter"],
      "why": "Ensure no other issues remain"
    }
  ]
}
```

---

## 🎯 Supported Applications

Chimera works with **10+ application categories**:

| Category | Applications | What Chimera Helps With |
|----------|-------------|------------------------|
| **💻 Code Editors** | VS Code, Sublime, Atom, IntelliJ | Debugging, syntax errors, code review, refactoring |
| **🌐 Browsers** | Chrome, Firefox, Edge, Safari | DevTools debugging, CSS issues, HTML structure |
| **📊 Office Suite** | Word, Excel, PowerPoint | Formulas, formatting, layouts, data analysis |
| **🎨 Design Tools** | Photoshop, Figma, Illustrator, Sketch | Layer management, color matching, effects, alignment |
| **🎮 3D Software** | Blender, UE5, Unity, Maya | Modeling issues, Blueprint errors, material setup |
| **🎬 Video Editing** | Premiere Pro, DaVinci Resolve, Final Cut | Timeline issues, effects, color grading |
| **🗄️ Database Tools** | MySQL Workbench, pgAdmin, DBeaver | Query optimization, schema design, error fixing |
| **💾 Terminal/CLI** | Bash, PowerShell, CMD, Zsh | Command errors, script debugging, permissions |
| **📝 Note Apps** | Notion, Obsidian, OneNote | Markdown formatting, organization, tables |
| **🔧 Any App** | Literally anything on your desktop | Context-aware assistance |

**Key Point:** Chimera automatically detects which application you're using and provides relevant, app-specific guidance.

---

## 🎯 Key Features

### 🖼️ **Multimodal Understanding**
- **Screenshot Analysis** - AI analyzes any desktop application screenshot
- **Context-Aware** - Automatically detects VS Code, Office, UE5, Browsers, Design Tools, etc.
- **App-Specific Responses** - Tailored guidance for each application
- **Universal Knowledge** - Works with 10+ application categories

### 🔌 **Flexible Provider Architecture**
- ✅ **Chimera Server (Default)** - Hosted inference, no setup required
- ✅ **Official APIs** - Bring your own OpenAI, Anthropic, Google, or IBM API keys
- ✅ **Local Models** - 100% private with Ollama or LM Studio
- ✅ **Model Agnostic** - Works with GPT-4o, Claude 3.5, Gemini Pro, and more

### 💻 **Universal Desktop Support**
- 🖥️ **Works with ANY App** - VS Code, Excel, PowerPoint, Browsers, UE5, Photoshop, Blender, and more
- 🎯 **Multi-Monitor Support** - Choose which screen to analyze
- 🟢 **Visual Monitoring** - Green border indicator when active
- 🔄 **Session History** - Track your work across all applications
- 🚀 **Fast Response Times** - Optimized for interactive workflows

### 🔒 **Privacy & Security**
- 🛡️ **Local Processing Option** - Use Ollama for 100% private analysis
- 🔐 **Encrypted API Keys** - Your credentials never leave your machine
- 🗑️ **No Screenshot Storage** - Screenshots processed and immediately deleted
- 📝 **Open Source** - Full transparency, audit the code yourself

---

## 🔥 How It Works

### The Chimera Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           ANY DESKTOP APPLICATION                           │
│   VS Code • Excel • PowerPoint • Browsers • UE5 • More     │
└──────────────────┬──────────────────────────────────────────┘
                   │
          ┌────────▼────────┐
          │  Take Screenshot │ 🟢 Green border when monitoring
          └────────┬─────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              CHIMERA DESKTOP APP                            │
│  • Multi-monitor support  • Auto context detection          │
│  • Session history        • Universal app support           │
└──────────────────┬──────────────────────────────────────────┘
                   │ POST /api/v1/assist
                   │ (image + question + context)
┌──────────────────▼──────────────────────────────────────────┐
│              CHIMERA API SERVER (FastAPI)                   │
│                 http://localhost:8000                       │
└────┬────────────────────────────────────────────────────────┘
     │
     │ Routes to selected provider:
     │
     ├──► Chimera Server (Default - Managed Hosting)
     ├──► OpenAI API (GPT-4o with Vision)
     ├──► Anthropic API (Claude 3.5 Sonnet)
     ├──► Google API (Gemini Pro Vision)
     └──► Ollama (Local LLaVA, Bakllava, etc.)
```

### Step-by-Step Process

1. **💻 Open Any App** - VS Code, Excel, PowerPoint, UE5, Browser, etc.
2. **🟢 Start Monitoring** - Click "Start Monitoring" - green border appears
3. **📸 Capture Screen** - Automatic or manual screenshot of your work
4. **💬 Ask Question** - Type what you need help with
5. **🤖 AI Analysis** - Chimera analyzes the screenshot + detects app context
6. **📋 Get Steps** - Receive app-specific, step-by-step guidance
7. **✅ Solve Issue** - Follow the steps in your application

---

## 📦 Installation

### Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **uv** - Fast Python package manager ([Install](https://github.com/astral-sh/uv))

### 1️⃣ Clone & Install

```bash
# Clone repository
git clone https://github.com/ruslanmv/chimera.git
cd chimera

# Install Python dependencies
uv sync

# Install frontend dependencies
cd frontend && npm install && cd ..
```

### 2️⃣ Launch Chimera

```bash
# Start both backend and frontend
make dev

# Or start separately:
uv run chimera-serve  # Backend API on :8000
cd frontend && npm run dev  # Desktop UI on :5173
```

### 3️⃣ Configure Your Provider (Optional)

By default, Chimera uses **Chimera Server** (our hosted inference). No setup required!

To use your own provider, create a `.env` file:

```bash
# OPTIONAL: Only needed if you want to use your own API keys

# Default Provider Selection
CHIMERA_DEFAULT_PROVIDER=chimera  # Options: chimera, openai, anthropic, google, ollama

# OpenAI API (for GPT-4o with Vision)
OPENAI_API_KEY=sk-...

# Anthropic API (for Claude 3.5 Sonnet)
ANTHROPIC_API_KEY=sk-ant-...

# Google Gemini API (for Gemini Pro Vision)
GOOGLE_API_KEY=...

# Ollama (Local models - 100% free & private)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llava:latest  # or bakllava, etc.

# Privacy Settings
CHIMERA_STORE_SCREENSHOTS=false  # Never store screenshots
CHIMERA_ANALYTICS_ENABLED=false  # Disable analytics
```

### 4️⃣ (Optional) Set Up Local Models with Ollama

For **100% private, offline** operation:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a multimodal model
ollama pull llava:latest  # or llava:13b, bakllava, etc.

# Verify it works
ollama run llava "Describe this image" < screenshot.png
```

Then set `CHIMERA_DEFAULT_PROVIDER=ollama` in your `.env` file.

---

## 🚀 Quick Start

### Using the Desktop App

1. Open the Chimera Desktop App: [http://localhost:5173](http://localhost:5173)
2. Click **"Capture Screen"** or use the keyboard shortcut
3. Type your question (e.g., "How do I fix this Blueprint node connection?")
4. Receive step-by-step guidance specific to UE5

### Using the API Directly

```python
import requests

# Prepare your screenshot and question
files = {'image': open('ue5_screenshot.png', 'rb')}
data = {
    'question': 'How do I connect these Blueprint nodes?',
    'context': 'ue5-blueprint',
    'ue5_version': '5.3'
}

# Call Chimera API
response = requests.post('http://localhost:8000/api/v1/assist', files=files, data=data)
result = response.json()

# Print steps
print(result['summary'])
for step in result['steps']:
    print(f"\n{step['title']}:")
    for detail in step['details']:
        print(f"  - {detail}")
```

### Example Response Structure

```json
{
  "summary": "Type mismatch between Vector and Float pins detected",
  "assumptions": ["UE5.3", "Blueprint Editor open", "Event Graph visible"],
  "steps": [
    {
      "title": "Add Vector Length conversion node",
      "details": [
        "Right-click in the Blueprint graph",
        "Type 'Vector Length' in the search box",
        "Click to place the node"
      ],
      "why": "Vector Length converts a Vector (X,Y,Z) to a single Float value (magnitude)"
    },
    {
      "title": "Connect the nodes properly",
      "details": [
        "Drag from your Vector output pin to the Vector Length input",
        "Drag from Vector Length output to your Float input pin",
        "Compile the Blueprint to verify"
      ],
      "why": "This chain converts the data type correctly"
    }
  ],
  "checks": [
    "If Vector Length doesn't appear, ensure you're searching in the correct context",
    "After connecting, check for any Blueprint errors in the compiler results"
  ]
}
```

---

## 🔌 LLM Providers

Chimera supports multiple AI providers. Choose based on your needs:

### 🌐 Chimera Server (Default - Recommended)

**What:** Our managed inference infrastructure
**Cost:** Included with Chimera
**Setup:** Zero configuration required
**Privacy:** Enterprise-grade, screenshots not stored
**Best For:** Most users who want it to "just work"

```bash
# Default - no configuration needed!
# Just start Chimera and use it
```

### 🔑 Official API Providers

**What:** Direct API access to OpenAI, Anthropic, Google, IBM
**Cost:** Pay-per-use (you provide API keys)
**Setup:** Add API key to `.env` file
**Privacy:** Your data sent directly to the provider
**Best For:** Users who already have API credits or subscriptions

```bash
# Example: Use OpenAI GPT-4o with Vision
CHIMERA_DEFAULT_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

**Supported Official APIs:**
- ✅ **OpenAI** - GPT-4o, GPT-4 Turbo (excellent vision capabilities)
- ✅ **Anthropic** - Claude 3.5 Sonnet, Claude 3 Opus (strong reasoning)
- ✅ **Google** - Gemini Pro Vision, Gemini 1.5 Pro (fast & accurate)
- ✅ **IBM WatsonX** - Enterprise AI platform

### 💻 Local Models (Ollama)

**What:** Run AI models on your own hardware
**Cost:** 100% free forever
**Setup:** Install Ollama + pull models
**Privacy:** 100% private, nothing leaves your machine
**Best For:** Privacy-conscious users, offline work, or limited budget

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull multimodal models
ollama pull llava:latest      # 7B parameter vision model
ollama pull llava:13b         # Larger, more capable
ollama pull bakllava          # Alternative architecture

# Configure Chimera
echo "CHIMERA_DEFAULT_PROVIDER=ollama" >> .env
echo "OLLAMA_MODEL=llava:latest" >> .env
```

### Provider Comparison

| Feature | Chimera Server | Official APIs | Ollama (Local) |
|---------|---------------|---------------|----------------|
| **Setup** | ✅ None | ⚠️ API key required | ⚠️ Install + download models |
| **Cost** | ✅ Included | ❌ Pay per request | ✅ Free forever |
| **Privacy** | ✅ Enterprise-grade | ⚠️ Sent to provider | ✅ 100% private |
| **Speed** | ✅ Fast | ✅ Fast | ⚠️ Depends on hardware |
| **Offline** | ❌ Requires internet | ❌ Requires internet | ✅ Works offline |
| **Quality** | ✅ High | ✅ Very high | ⚠️ Good (smaller models) |

---

## 📚 Examples

### Example 1: VS Code - React Debugging

**Application:** VS Code
**Screenshot:** Code with error in console
**Question:** "Why is my component not rendering?"
**Response:**
- Step 1: Check that you're importing React at the top
- Step 2: Verify the component is exported correctly
- Step 3: Check for typos in JSX syntax
- Step 4: Ensure all brackets are closed properly

### Example 2: Excel - Formula Issue

**Application:** Microsoft Excel
**Screenshot:** Spreadsheet with #REF! error
**Question:** "Why is my VLOOKUP showing an error?"
**Response:**
- Step 1: Check that your lookup range includes the return column
- Step 2: Verify the column index is not out of bounds
- Step 3: Ensure lookup value exists in the first column
- Step 4: Use absolute references ($) for the table range

### Example 3: PowerPoint - Layout Problem

**Application:** PowerPoint
**Screenshot:** Slide with misaligned elements
**Question:** "How do I align these shapes perfectly?"
**Response:**
- Step 1: Select all shapes you want to align (Ctrl+Click)
- Step 2: Go to Format → Align → Align Center
- Step 3: Use Format → Align → Distribute Horizontally for even spacing
- Step 4: Group the shapes together (Ctrl+G) to keep alignment

### Example 4: Browser DevTools - CSS Debugging

**Application:** Chrome Browser
**Screenshot:** DevTools showing layout issue
**Question:** "Why is my div not centering?"
**Response:**
- Step 1: Add `display: flex` to the parent container
- Step 2: Add `justify-content: center` for horizontal centering
- Step 3: Add `align-items: center` for vertical centering
- Step 4: Ensure parent has a defined height (e.g., `height: 100vh`)

### Example 5: Unreal Engine 5 - Blueprint

**Application:** Unreal Engine 5
**Screenshot:** Blueprint with connection error
**Question:** "Type mismatch - how do I connect these nodes?"
**Response:**
- Step 1: Identify the output (Vector) and input (Float) types
- Step 2: Right-click and search for "Vector Length" node
- Step 3: Place it between the two nodes
- Step 4: Connect Vector → Vector Length → Float

---

## 🧪 Testing

Chimera has a comprehensive enterprise testing infrastructure with automated CI/CD:

### Quick Start

```bash
# Run Python unit tests
uv run pytest tests/ -v

# Run UI tests with Playwright
cd frontend && npx playwright test

# Run full test suite
make test
```

### CI/CD Pipeline

Our GitHub Actions workflow runs on every push and PR:
- ✅ **Python Unit Tests** (Python 3.11 & 3.12)
- ✅ **UI Screenshot Tests** (Playwright)
- ✅ **Integration Tests** (Full stack)
- ✅ **Linting & Formatting** (ruff, black, eslint)
- ✅ **Security Scanning** (Trivy)

### Test Coverage

- Backend: 80%+ coverage target
- LLM Providers: 90%+ coverage
- UI Components: 70%+ coverage

**📖 Full Testing Guide**: See [docs/TESTING.md](docs/TESTING.md) for comprehensive testing documentation.

---

## 📚 Documentation

Complete guides for development and deployment:

| Guide | Description |
|-------|-------------|
| **[Testing Guide](docs/TESTING.md)** | Complete testing infrastructure, CI/CD pipeline, writing tests |
| **[Configuration Guide](docs/CONFIGURATION.md)** | Provider setup, environment variables, deployment options |
| **[API Documentation](docs/API.md)** | REST API endpoints, request/response formats |
| **[LLM Providers](backend/core/README.md)** | Provider architecture, adding new providers |

### Key Documentation Files

```bash
docs/
├── TESTING.md          # Testing infrastructure and CI/CD
├── CONFIGURATION.md    # Environment and provider configuration
└── API.md             # API reference

backend/core/
├── settings.py        # Configuration management
├── llm_provider.py    # Provider abstraction
└── model_catalog.py   # Dynamic model discovery

.github/workflows/
└── ci-test.yml        # GitHub Actions CI/CD pipeline
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                        │
│              Chimera Desktop Launcher                       │
│  • Screen capture  • Chat interface  • Settings             │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTP (POST /api/v1/assist)
┌─────────────────▼───────────────────────────────────────────┐
│                FastAPI Backend                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │             Chimera Manager                          │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │   │
│  │  │Chimera │ │OpenAI  │ │Claude  │ │ Ollama │       │   │
│  │  │Server  │ │Plugin  │ │Plugin  │ │ Plugin │       │   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘       │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Vision Processing Pipeline                   │   │
│  │  • Image preprocessing  • Prompt engineering         │   │
│  │  • Response parsing     • Step extraction            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

- **`backend/main.py`** - FastAPI server and routing
- **`backend/core/manager.py`** - Provider lifecycle and orchestration
- **`backend/core/plugin_base.py`** - Abstract base class for providers
- **`backend/plugins/*.py`** - Provider implementations
- **`frontend/src/ChimeraLauncher.jsx`** - React desktop app UI

---

## 🌟 Support This Project

If Chimera helps you build better UE5 projects:

⭐ **Star this repository** - Show your support!
🐛 **Report issues** - Help us improve
💡 **Share ideas** - Tell us what UE5 features to support next
🤝 **Contribute code** - Build together
📢 **Spread the word** - Tweet about Chimera

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Development Setup

```bash
# Fork and clone
git clone https://github.com/ruslanmv/chimera.git
cd chimera

# Create branch
git checkout -b feature/amazing-feature

# Install dev dependencies
uv sync --dev

# Make changes and test
uv run pytest

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

### What We Need Help With

- 🎮 **UE5 Expertise** - Help improve UE5-specific guidance
- 🧪 **Testing** - Test with different UE5 versions and workflows
- 📝 **Documentation** - Improve guides and examples
- 🎨 **UI/UX** - Enhance the desktop app experience
- 🔌 **Providers** - Add support for more LLM providers

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

Chimera is an **independent tool** and is **not affiliated with** Microsoft, Epic Games, Adobe, Google, or any other software companies.

- Chimera provides AI-generated guidance that may not always be accurate
- Always verify suggestions in your applications before making critical changes
- We are not responsible for any issues caused by following AI guidance
- Use at your own risk, especially in production environments
- Chimera analyzes screenshots but does not directly control or modify your applications

**Privacy Commitment:**
- We do NOT store your screenshots (unless you explicitly enable history)
- We do NOT train models on your data or projects
- We do NOT share your data with third parties
- When using Chimera Server, screenshots are processed and immediately deleted
- All analysis happens in real-time with no persistent storage

---

## 🙏 Acknowledgments

Built with amazing open-source technologies:

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Lucide Icons](https://lucide.dev/) - Beautiful icon set

Special thanks to:
- OpenAI, Anthropic, Google, IBM for their vision-capable LLM APIs
- Microsoft, Adobe, Epic Games, and all software creators
- The open-source community
- All contributors, testers, and supporters

---

<div align="center">

**Made with ❤️ for Desktop Productivity**

*"Work smarter, not harder. Get instant help for any app."*

</div>
