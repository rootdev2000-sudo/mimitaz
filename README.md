# mimitaz

<div align="center">

```text
 ███╗   ███╗██╗███╗   ███╗
 ████╗ ████║██║████╗ ████║
 ██╔████╔██║██║██╔████╔██║
 ██║╚██╔╝██║██║██║╚██╔╝██║
 ██║ ╚═╝ ██║██║██║ ╚═╝ ██║
 ╚═╝     ╚═╝╚═╝╚═╝     ╚═╝
```

**The Professional's AI Terminal Companion**  
*Latency-Optimized • Pipe-Ready • Provider-Agnostic*

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg?style=flat-square)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-6366F1.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-10B981.svg?style=flat-square)](https://www.python.org/)

</div>

---

## ⚡ What is Mimitaz?

**Mimitaz** (`mim`) is a commercial-grade command-line interface designed for software engineers who live in the terminal.

We stripped away the web UI bloat, the "regenerate" buttons, and the waiting. Mimitaz connects your shell directly to the world's best intelligence models (GPT-4, Claude 3.5, Local Llama) with **zero friction**.

It is not a chatbot. It is a **Unix power-tool** for intelligence.

## ✨ Why Mimitaz?

- **🚀 Speed of Thought**: Optimistic UI rendering means you never stare at a blank screen. It feels instant.
- **🔌 Unix Native**: Designed to live in pipelines. Pipe `git diff` into it. Pipe its code output into files.
- **🎨 Swiss Design**: A "Zero-Chrome" interface. No ASCII clutter. Just rigorous typography and syntax highlighting.
- **🔓 Provider Freedom**: Don't get locked in. Swap between OpenAI, Anthropic, and Local models with a single config flag.
- **🛡️ Production Ready**: Type-safe configuration, robust error handling, and privacy-first implementation (keys stay local).

---

## 🛠️ Installation

### Quick Installation (pipx / uv)

```bash
pipx install git+https://github.com/rootdev2000-sudo/mimitaz.git
```

### Developer Setup (Source)

Install via `pip` in editable mode for development:

```bash
# Clone the repository
git clone https://github.com/rootdev2000-sudo/mimitaz.git
cd mimitaz

# Setup environment
python3 -m venv venv
source venv/bin/activate

# Install
pip install -e .
```

---

## 🎮 Usage Workflows

Mimitaz adapts to three distinct modes of operation.

### 1. The "Flow" (Interactive REPL)
For deep debugging, architecture planning, or complex reasoning.

```bash
mim
```
> Opens a persistent, context-aware session.

### 2. The "Shot" (Quick Command)
For syntax lookups, quick scripts, or explanations.

```bash
mim "Write a regex to match email addresses"
```

### 3. The "Pipe" (Automation)
The true power of Mimitaz. Integrate AI into your existing CLI tools.

```bash
# Refactor code automatically
cat legacy.py | mim "Refactor this to be functional style" > modern.py

# Generate commit messages
git diff --staged | mim "Write a semantic commit message"
```

---

## ⚙️ Configuration

Mimitaz offers a dedicated CLI for seamless configuration management, avoiding manual file edits.

### 🔑 Authentication
Securely manage your API keys.

```bash
# Set your API Key (Defaults to GLM/ZhipuAI)
mim token set "your-api-key"

# Set key for specific providers
mim token set "sk-..." --provider openai
mim token set "sk-ant-..." --provider anthropic
```

### 🎛️ Settings
Manage preferences directly from the terminal.

```bash
# List all current configurations
mim config list

# Change the active provider
mim config set provider openai

# Change the default model
mim config set model gpt-4-turbo

# Enable debug mode persistently
mim config set debug true
```

### 🌍 Environment Variables (Advanced)
For CI/CD or specialized setups, standard environment variables take precedence:

```bash
export MIMITAZ_PROVIDER="openai"
export MIMITAZ_OPENAI_KEY="sk-..."
```

---

<div align="center">
  <p><b>Designed for the fun </b></p>
  <p>Created by <a href="https://github.com/omik">Omik</a></p>
</div>
