import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import subprocess
import sys
import time

# Load environment variables from .env file
load_dotenv()

# Set your Gemini API key from env
genai.configure(api_key=os.getenv("GEMINI_API"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to format the prompt using a template
def format_prompt(user_input):
    template = """
    You are to create PUML diagrams code. Only provide the puml code and nothing else

    User: {question}

    Assistant:
    """
    return template.format(question=user_input)

# Streamlit app setup
st.set_page_config(page_title="Gemini Chat", page_icon="💬")
st.title("💬 PUML Diagram Generator")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Describe your diagram..."):
    # Append user's message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Format prompt with template
    prompt = format_prompt(user_input)

    # Gemini API call
    try:
        response = model.generate_content(prompt)
        assistant_reply = response.text.strip()

        # Write response to puml.txt and flush immediately
        with open("puml.txt", "w") as file:
            file.write(assistant_reply)
            file.flush()
            os.fsync(file.fileno())  # Force write to disk

        # Now safely run PlantUML subprocess
        result = subprocess.run(
            ["java", "-jar", "plantuml.jar", "puml.txt"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            if os.path.exists("puml.png"):
                st.image("puml.png", caption="Generated Diagram")
        else:
            st.error(f"PlantUML Error:\n{result.stderr}")

    except Exception as e:
        assistant_reply = f"Error: {e}"


    # Append assistant's reply to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
