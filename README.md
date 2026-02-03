# Mimitaz

Award-level CLI AI Assistant.

## Prerequisites

- Python 3.10 or higher

## Installation

Follow these steps to set up Mimitaz locally.

### 1. Clone the repository

```bash
git clone <repository_url>
cd mimitaz
```

### 2. Create and activate a virtual environment

It is recommended to use a virtual environment to manage dependencies.

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install the package

Install the package in editable mode with its dependencies.

```bash
cd mimitaz  # Ensure you are in the directory containing pyproject.toml
pip install -e .
```

### 4. Verify Installation

After installation, you can run the `mz` command to verify it's working.

```bash
mz --help
```

## Uninstallation

To remove Mimitaz from your system:

### 1. Deactivate the virtual environment (if active)

```bash
deactivate
```

### 2. Uninstall the package

If you installed it using pip:

```bash
pip uninstall mimitaz
```

### 3. Remove the project files

Delete the project directory.

**On Linux/macOS:**
```bash
rm -rf mimitaz
```

**On Windows:**
```powershell
Remove-Item -Recurse -Force mimitaz
```

## Development

This project was built with:
- **Typer**: For building the CLI interface.
- **Rich**: For beautiful terminal formatting.
- **Hatchling**: For the build specification.
