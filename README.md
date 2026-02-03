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

### Professional Setup (Recommended)

Install via `pip` in editable mode for maximum control:

```bash
# Clone the repository
git clone https://github.com/omik/mimitaz.git
cd mimitaz/mimitaz

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

Control your intelligence supply chain via environment variables or a `.env` file.

```bash
# Provider Selection (openai | anthropic | mock)
export MIMITAZ_PROVIDER="openai"

# Credentials
export MIMITAZ_OPENAI_KEY="sk-..."
export MIMITAZ_ANTHROPIC_KEY="sk-ant-..."

# Tuning
export MIMITAZ_MODEL="gpt-4-turbo-preview"
export MIMITAZ_DEBUG="false"
```

---

<div align="center">
  <p><b>Designed for the fun </b></p>
  <p>Created by <a href="https://github.com/omik">Omik</a></p>
</div>
