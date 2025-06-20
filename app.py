import streamlit as st
import os
import subprocess
import requests
import html  # for escaping PUML code

# Page configuration
st.set_page_config(page_title="PUML Diagram Generator", page_icon="🧠", layout="centered")

# Clean modern CSS
st.markdown("""
    <style>
    .bubble {
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 100%;
        font-size: 15px;
    }
    .user {
        background-color: #1a73e8;
        color: white;
        text-align: right;
        margin-left: 30%;
    }
    .assistant {
        background-color: #2e2e2e;
        color: white;
        margin-right: 30%;
        white-space: pre-wrap;
        overflow-wrap: break-word;
    }
    .diagram-container {
        border: 1px solid #444;
        background-color: #1e1e1e;
        padding: 20px;
        margin-top: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 PUML Diagram Generator")

# Dropdown for diagram type
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

with st.sidebar:
    st.markdown("### Diagram Type")
    selected_diagram = st.selectbox("", diagram_types)

# Prompt formatter
def format_prompt(user_input, diagram_type):
    return f"""
"You are to act as a PlantUML diagram generator. Given a user's diagram request, reply only with the correct, valid PlantUML code as plain text. Do NOT include JSON, objects, explanations, or comments. Just the raw @startuml code."
diagram_type = "{diagram_type}"
User: {user_input}

Assistant:
""".strip()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous messages
for msg in st.session_state.messages:
    css_class = "user" if msg["role"] == "user" else "assistant"
    content = html.escape(msg["content"]) if msg["role"] == "assistant" else msg["content"]
    st.markdown(f'<div class="bubble {css_class}">{content}</div>', unsafe_allow_html=True)

# Handle new input
user_input = st.chat_input("Describe your diagram...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="bubble user">{user_input}</div>', unsafe_allow_html=True)

    prompt = format_prompt(user_input, selected_diagram)

    try:
        # Call Ollama
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma3", "prompt": prompt, "stream": False},
            timeout=30
        )
        res.raise_for_status()
        def clean_puml_output(puml_code: str) -> str:
            lines = puml_code.splitlines()
            cleaned = [line for line in lines if "[object Object]" not in line]
            return "\n".join(cleaned).strip()

        assistant_reply = clean_puml_output(res.text)


        # Save to PUML file
        with open("puml.txt", "w") as f:
            f.write(assistant_reply)
            f.flush()
            os.fsync(f.fileno())

        # Run PlantUML to generate SVG
        proc = subprocess.run(
            ["java", "-jar", "plantuml.jar", "-tsvg", "puml.txt"],
            capture_output=True,
            text=True
        )

        if proc.returncode == 0 and os.path.exists("puml.svg"):
            with open("puml.svg", "r", encoding="utf-8") as f:
                svg = f.read()

            # Store and show PUML response with escaping
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            escaped_code = html.escape(assistant_reply)
            st.markdown(f'<div class="bubble assistant"><pre><code>{escaped_code}</code></pre></div>', unsafe_allow_html=True)

            # Show diagram
            st.markdown('<div class="diagram-container">', unsafe_allow_html=True)
            st.markdown(svg, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error(f"PlantUML Error:\n{proc.stderr}")

        # Optional cleanup
        for f in ["puml.png", "puml.xml"]:
            if os.path.exists(f):
                os.remove(f)

    except Exception as e:
        err_msg = f"❌ Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": err_msg})
        st.markdown(f'<div class="bubble assistant">{err_msg}</div>', unsafe_allow_html=True)
