# AI Error Log Analyzer & Explainer 🧠

A production-grade developer tool that brings AI-powered error analysis directly into your VS Code workflow. It analyzes error logs, stack traces, and terminal output to provide clear, structured explanations and actionable debugging steps using Google's Gemini models.

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/backend-FastAPI-green)
![TypeScript](https://img.shields.io/badge/extension-VS%20Code-blue)
![Model](https://img.shields.io/badge/AI-Gemini%202.5-purple)

## ✨ Features

*   ** Instant Analysis**: Select any error text in your editor or terminal and get an immediate diagnosis.
*   **🩺 Root Cause Identification**: Uses advanced AI to pinpoint the most likely root causes with confidence scores.
*   **🛠️ Actionable Fixes**: Provides specific, step-by-step suggestions to resolve the issue.
*   **🔒 Privacy-First**:
    *   **Stateless by Default**: Errors are analyzed and immediately discarded.
    *   **Opt-in History**: Explicitly enable history to save structured summaries to a local SQLite database.
    *   **No Raw Log Storage**: Even with history enabled, raw logs (containing potential secrets) are *never* saved.
*   **💻 Terminal Integration**: Right-click context menu support in the VS Code integrated terminal.

## 🏗️ Architecture

The system consists of two main components:
1.  **Backend (Python/FastAPI)**: Handles the AI logic, sanitization, and optional database storage.
2.  **Frontend (VS Code Extension)**: Captures user input, communicates with the backend, and renders the explanations in a rich Webview.

## 🚀 Getting Started

### Prerequisites

*   **Python 3.8+**
*   **Node.js 16+** (for building the extension)
*   **Google Gemini API Key** (Get one [here](https://aistudio.google.com/app/apikey))

### 1. Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install fastapi uvicorn google-genai sqlmodel python-dotenv
    ```
4.  Configure your API key:
    *   Create a new `.env` file in backend directory.
    *   Add your key:
        ```env
        GEMINI_API_KEY= "your_actual_api_key_here"
        ```
5.  Start the server:
    ```bash
    uvicorn main:app --reload --port 8000
    ```

### 2. Extension Setup

1.  Open the project in VS Code.
2.  Navigate to the extension directory:
    ```bash
    cd extension
    ```
3.  Install dependencies:
    ```bash
    npm install
    ```
4.  Launch the Extension:
    *   Press **F5** (or go to **Run and Debug** > **Run Extension**).
    *   A new "Extension Development Host" window will open.

## 📖 Usage

### Analyzing from Editor
1.  Highlight an error log or stack trace in any file.
2.  Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).
3.  Run **"Explain with AI"**.
4.  (Alternatively) Right-click the selection -> **Explain with AI**.

### Analyzing from Terminal
1.  Select text in the Integrated Terminal.
2.  Right-click the selection.
3.  Choose **Explain with AI** from the context menu.

### Enabling History (Opt-in)
To save your error explanations for later reference:
1.  Open VS Code Settings (`Ctrl+,`).
2.  Search for `Error Explainer`.
3.  Check **Enable History**.
4.  Analyzed errors will now be saved to `backend/database.db`.

## 🛠️ Configuration

| Setting | Default | Description |
| :--- | :--- | :--- |
| `errorExplainer.backendUrl` | `http://127.0.0.1:8000` | URL of the running FastAPI backend. |
| `errorExplainer.enableHistory` | `false` | Enable local persistence of error summaries. |
