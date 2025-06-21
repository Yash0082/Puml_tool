import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import subprocess
import codecs
import re

# Setup
st.set_page_config(page_title="PUML Diagram Generator", page_icon="🧠")
st.title("🧠 PUML Diagram Generator")

# Dropdown options
diagram_types = [
    "Sequence diagram",
    "Usecase diagram",
    "Class diagram",
    "Object diagram",
    "Activity diagram (legacy syntax)",
    "Component diagram",
    "Deployment diagram",
    "State diagram",
    "Timing diagram"
]

# Load .env API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API"))

# Gemini model setup
model = genai.GenerativeModel("gemini-1.5-flash")

# Format prompt
def format_prompt(user_input, diagram_type):
    return f"""
You are a PlantUML (PUML) diagram generator.

Generate only raw PlantUML code for the following {diagram_type}.

Do NOT return:
- Markdown formatting
- JSON
- [object Object]
- Explanations

Just return plain PUML like:
@startuml
title Sample Title
actor User
User -> System: Sample interaction
@enduml

Now generate for:
"{user_input}"
""".strip()

# Text cleanup
def decode_escape_sequences(text: str) -> str:
    return codecs.decode(text, 'unicode_escape')

def clean_puml_response(text: str) -> str:
    lines = text.splitlines()
    lines = [line for line in lines if "[object Object]" not in line]
    return "\n".join(lines).strip()

def strip_objects(text: str) -> str:
    return re.sub(r"\{.*?\}", "", text)

# State
if "messages" not in st.session_state:
    st.session_state.messages = []

# UI Input + Dropdown
col1, col2 = st.columns([3, 2])
with col1:
    user_input = st.chat_input("Describe your diagram...")
with col2:
    selected_diagram = st.selectbox("Diagram Type", diagram_types, label_visibility="collapsed")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown("**Generated PUML Code:**")
        st.code(msg["content"], language="plantuml")

# On input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt = format_prompt(user_input, selected_diagram)

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        decoded = decode_escape_sequences(raw)
        cleaned = strip_objects(clean_puml_response(decoded))
        assistant_reply = cleaned

        with open("puml.txt", "w", encoding="utf-8") as f:
            f.write(assistant_reply)
            f.flush()
            os.fsync(f.fileno())

        proc = subprocess.run(
            ["java", "-jar", "plantuml.jar", "-tsvg", "puml.txt"],
            capture_output=True,
            text=True
        )

        if proc.returncode == 0 and os.path.exists("puml.svg"):
            with open("puml.svg", "r", encoding="utf-8") as f:
                svg = f.read()

            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            st.markdown("**Generated PUML Code:**")
            st.code(assistant_reply, language="plantuml")

            st.markdown("### Rendered Diagram:")
            st.markdown(svg, unsafe_allow_html=True)

            st.download_button("Download SVG", svg, "diagram.svg", mime="image/svg+xml")
        else:
            st.error(f"PlantUML Error:\n{proc.stderr}")

    except Exception as e:
        err_msg = f"❌ Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": err_msg})
        st.error(err_msg)
