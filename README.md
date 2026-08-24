# 🗂️ File Manager Studio

File CRUD operations in Python, wrapped in a clean Streamlit UI.

A simple terminal-based file handler — Create, Read, Update, Delete — rebuilt as a deployable web app. Same core logic, but usable by anyone without touching a command line.

**[🔗 [Live Demo](https://file-manager-studio.streamlit.app/)]

---

## 📖 Overview

This started as a plain Python script using `pathlib` and exception handling to manage local text files through terminal `input()` prompts. This version wraps that same logic in a Streamlit interface — the goal was to practice turning working code into something someone else could actually open and use.

## ✨ Features

| Operation | What it does |
| 📄 **Create** | Write a new file with content typed directly in the UI |
| 👀 **Read** | Preview any file's content, size, and last-modified time |
| ✏️ **Update** | Rename, append to, or fully overwrite a file |
| 🗑️ **Delete** | Remove a file, gated behind a required confirmation checkbox |
| 📁 **Explorer** | Browse every file in the workspace at a glance |

All operations are sandboxed to a local `file_manager_workspace/` folder — the app can never touch files outside it.

## 🛠️ Built With

- **Python** — core file-handling logic
- **Streamlit** — UI layer
- **pathlib** — safe, cross-platform path handling

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/Garv-007/file-manager-studio.git
cd file-manager-studio
pip install streamlit
```

### Run locally

```bash
streamlit run file_manager_app.py
```

## 🧠 What I Learned

- Structuring a Streamlit app around a sidebar-driven navigation flow
- Designing safe file operations (sandboxing, existence checks, confirmation gates)
- The difference between "code that works" and a tool someone else can actually use

## 🔮 Possible Next Steps

- Deploy on Streamlit Community Cloud for a live public demo
- Add file upload/download support
- Support for multiple file types beyond plain text

## 📬 Connect

Built by **Garv** — open to Data Analyst opportunities.

[LinkedIn](https://linkedin.com/in/garv-singh260) &nbsp;•&nbsp; [GitHub](https://github.com/Garv-007)
