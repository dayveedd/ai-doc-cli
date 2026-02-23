# AI Document Architect 📄🤖

A powerful CLI tool that uses Google's Gemini AI to generate, iterate upon, and export professional PDF documents (Resumes, Proposals, Reports, etc.) directly from your terminal.

## ✨ Features
* **Interactive AI Chat:** Brainstorm and edit your document in real-time.
* **Rich Console Rendering:** View beautifully formatted Markdown in your terminal before exporting.
* **Professional PDF Styling:** Converts Markdown to styled PDFs using WeasyPrint.
* **Persistent History:** The AI remembers your previous edits, allowing for iterative document building.

---

## 🛠 Prerequisites

Before installing, you must have the following graphics libraries installed on your system (required for PDF rendering):

### macOS \ Linux
```bash
brew install pango libffi

Linux (Ubuntu/Debian)
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libffi-dev

🚀 Installation
Set your Gemini API Key:
Obtain a key from Google AI Studio and add it to your shell profile:

export GEMINI_API_KEY="your_api_key_here"

Install the package:
Navigate to the project root and run:

pip install .

⌨️ Usage
Simply type the following command to launch the architect:

Bash
ai-doc
```

```
Commands within the app:
Just type anything: Talk to the AI to generate or edit content.

/pdf [filename.pdf] : Export the current text to a styled PDF file.

/exit : Close the application.

📂 Project Structure
ai_doc/ : Core Python package containing the logic.

pyproject.toml : Build system requirements and CLI entry points.

main.py : Interactive loop and API integration.

```