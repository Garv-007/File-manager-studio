"""
File Manager Studio
A polished Streamlit UI wrapped around a classic file-handling CRUD project
(Create / Read / Update / Delete text files) — built for portfolio showcase.

Run with:
    streamlit run file_manager_app.py
"""

import os
from pathlib import Path
from datetime import datetime

import streamlit as st

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
WORKSPACE = Path("file_manager_workspace")
WORKSPACE.mkdir(exist_ok=True)

st.set_page_config(
    page_title="File Manager Studio",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main { background-color: #0e1117; }

        .app-header {
            padding: 1.6rem 2rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            border: 1px solid #2d3748;
            margin-bottom: 1.5rem;
        }
        .app-header h1 {
            margin: 0;
            font-size: 2rem;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .app-header p {
            margin: 0.3rem 0 0 0;
            color: #9ca3af;
            font-size: 0.95rem;
        }

        .stat-card {
            background: #161b22;
            border: 1px solid #2d3748;
            border-radius: 12px;
            padding: 1rem 1.2rem;
            text-align: center;
        }
        .stat-card h2 {
            margin: 0;
            color: #38bdf8;
            font-size: 1.6rem;
        }
        .stat-card p {
            margin: 0.2rem 0 0 0;
            color: #9ca3af;
            font-size: 0.85rem;
        }

        .file-row {
            background: #161b22;
            border: 1px solid #2d3748;
            border-radius: 10px;
            padding: 0.6rem 1rem;
            margin-bottom: 0.4rem;
            font-family: 'Courier New', monospace;
            font-size: 0.88rem;
            color: #e5e7eb;
        }

        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            border: 1px solid #2d3748;
        }

        .footer-note {
            text-align: center;
            color: #6b7280;
            font-size: 0.8rem;
            margin-top: 3rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1>🗂️ File Manager Studio</h1>
        <p>A clean CRUD interface for local text files — Create, Read, Update, Delete — built with Python + Streamlit.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Stats row
# --------------------------------------------------------------------------
all_files = sorted([p for p in WORKSPACE.iterdir() if p.is_file()])
total_size_kb = sum(p.stat().st_size for p in all_files) / 1024

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="stat-card"><h2>{len(all_files)}</h2><p>Files in workspace</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><h2>{total_size_kb:.1f} KB</h2><p>Total size</p></div>', unsafe_allow_html=True)
with c3:
    last_mod = max((p.stat().st_mtime for p in all_files), default=None)
    last_str = datetime.fromtimestamp(last_mod).strftime("%d %b, %H:%M") if last_mod else "—"
    st.markdown(f'<div class="stat-card"><h2>{last_str}</h2><p>Last modified</p></div>', unsafe_allow_html=True)

st.write("")

# --------------------------------------------------------------------------
# Sidebar navigation
# --------------------------------------------------------------------------
st.sidebar.title("⚙️ Operations")
operation = st.sidebar.radio(
    "Choose an action",
    ["📄 Create", "👀 Read", "✏️ Update", "🗑️ Delete", "📁 Explorer"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Workspace folder: `{WORKSPACE.resolve().name}/`")
st.sidebar.caption("All file operations are sandboxed to this folder for safety.")


def safe_path(filename: str) -> Path:
    """Keep every operation confined inside the workspace folder."""
    return WORKSPACE / Path(filename).name


# --------------------------------------------------------------------------
# CREATE
# --------------------------------------------------------------------------
if operation == "📄 Create":
    st.subheader("Create a new file")
    with st.form("create_form", clear_on_submit=False):
        filename = st.text_input("File name", placeholder="notes.txt")
        content = st.text_area("File content", placeholder="Type what you want to write...", height=180)
        submitted = st.form_submit_button("Create File", use_container_width=True)

    if submitted:
        if not filename.strip():
            st.error("Please enter a file name.")
        else:
            path = safe_path(filename)
            if path.exists():
                st.error(f"⚠️ A file named **{path.name}** already exists.")
            else:
                path.write_text(content, encoding="utf-8")
                st.success(f"✅ **{path.name}** created successfully!")
                st.rerun()

# --------------------------------------------------------------------------
# READ
# --------------------------------------------------------------------------
elif operation == "👀 Read":
    st.subheader("Read a file")
    if not all_files:
        st.info("No files yet — create one first.")
    else:
        choice = st.selectbox("Select a file", [p.name for p in all_files])
        if choice:
            path = safe_path(choice)
            try:
                content = path.read_text(encoding="utf-8")
                st.caption(f"Size: {path.stat().st_size} bytes  •  Modified: {datetime.fromtimestamp(path.stat().st_mtime).strftime('%d %b %Y, %H:%M')}")
                st.code(content if content.strip() else "(empty file)", language="text")
            except Exception as err:
                st.error(f"An error occurred: {err}")

# --------------------------------------------------------------------------
# UPDATE
# --------------------------------------------------------------------------
elif operation == "✏️ Update":
    st.subheader("Update a file")
    if not all_files:
        st.info("No files yet — create one first.")
    else:
        choice = st.selectbox("Select a file", [p.name for p in all_files])
        path = safe_path(choice) if choice else None

        action = st.radio("What do you want to do?", ["Rename", "Append", "Overwrite"], horizontal=True)

        if action == "Rename":
            new_name = st.text_input("New file name")
            if st.button("Rename", use_container_width=True):
                if not new_name.strip():
                    st.error("Enter a new name first.")
                else:
                    new_path = safe_path(new_name)
                    if new_path.exists():
                        st.error("A file with that name already exists.")
                    else:
                        path.rename(new_path)
                        st.success(f"✅ Renamed to **{new_path.name}**")
                        st.rerun()

        elif action == "Append":
            extra = st.text_area("Text to append", height=140)
            if st.button("Append", use_container_width=True):
                with open(path, "a", encoding="utf-8") as fs:
                    fs.write("\n" + extra)
                st.success(f"✅ Appended to **{path.name}**")
                st.rerun()

        elif action == "Overwrite":
            new_content = st.text_area("New content (replaces the file entirely)", height=180)
            if st.button("Overwrite", use_container_width=True, type="primary"):
                path.write_text(new_content, encoding="utf-8")
                st.success(f"✅ Overwrote **{path.name}**")
                st.rerun()

# --------------------------------------------------------------------------
# DELETE
# --------------------------------------------------------------------------
elif operation == "🗑️ Delete":
    st.subheader("Delete a file")
    if not all_files:
        st.info("No files yet — create one first.")
    else:
        choice = st.selectbox("Select a file", [p.name for p in all_files])
        st.warning("This action cannot be undone.")
        confirm = st.checkbox(f"Yes, I want to permanently delete **{choice}**")
        if st.button("Delete File", type="primary", use_container_width=True, disabled=not confirm):
            safe_path(choice).unlink()
            st.success(f"🗑️ **{choice}** deleted successfully.")
            st.rerun()

# --------------------------------------------------------------------------
# EXPLORER
# --------------------------------------------------------------------------
elif operation == "📁 Explorer":
    st.subheader("Workspace explorer")
    if not all_files:
        st.info("No files yet — create one to see it here.")
    else:
        for p in all_files:
            size = p.stat().st_size
            modified = datetime.fromtimestamp(p.stat().st_mtime).strftime("%d %b %Y, %H:%M")
            st.markdown(
                f'<div class="file-row">📄 <b>{p.name}</b> &nbsp;|&nbsp; {size} bytes &nbsp;|&nbsp; modified {modified}</div>',
                unsafe_allow_html=True,
            )

st.markdown('<div class="footer-note">Built with Python & Streamlit — a UI layer over core file-handling logic (Create · Read · Update · Delete).</div>', unsafe_allow_html=True)