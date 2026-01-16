# Fixpert 🧠

Fixpert is a production-grade VS Code extension that brings AI-powered error analysis directly into your development workflow.  
Select an error from your editor or terminal and get clear, structured explanations with actionable debugging steps — powered by Google’s Gemini models.

---

## ✨ Features

- ⚡ **Instant Error Analysis**  
  Analyze error logs, stack traces, and terminal output with a single right-click.

- 🩺 **Root Cause Identification**  
  AI pinpoints the most **likely causes** of errors along with their **confidence scores** and explains *why* they happen.

- 🛠️ **Actionable Fixes**  
  Step-by-step suggestions to help you resolve issues quickly and confidently.

- 🔒 **Privacy-First Design**  
  - Stateless analysis by default  
  - Optional explanation history (opt-in only)  
  - Raw error logs are never stored

- 💻 **Deep VS Code Integration**  
  Works seamlessly in both the editor and the integrated terminal.

---

## 📦 Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **Fixpert**
4. Click **Install**

---

## 🔑 Required Setup

Fixpert requires an API key before first use.

### Step 1: Open Fixpert Settings
- Open VS Code **Settings**
- Search for **Fixpert**

### Step 2: Add Your API Key
- Paste your **Google Gemini API key** into:
1. Fixpert : Api Key

### Step 3: Allow Workspace Access

Make sure the API key is set for:
- ✅ **User**
- ✅ **Workspace**

Once this is done, Fixpert is ready to use.

---

## 🚀 How to Use Fixpert

### Explain an error from the editor
1. Select the error text in your code
2. Right-click
3. Click **Explain with AI**
4. Fixpert analyzes the error and provides an explanation

### Explain a terminal error
1. Select the error output in the terminal
2. Right-click
3. Click **Explain with AI**
4. Fixpert analyzes the error and suggests fixes

---

## ⚙️ Configuration

Fixpert can be configured from VS Code settings.

| Setting | Description |
|--------|-------------|
| `fixpert.apiKey` | Your Google Gemini API key |
| `fixpert.enableHistory` | Save structured explanations locally (optional) |

### Example configuration

```json
{
  "fixpert.apiKey": "YOUR_API_KEY",
  "fixpert.enableHistory": true
}
