# 🧠 PUML Diagram Generator

Generate PlantUML diagrams from natural language using a local LLM!  
This Streamlit app allows you to describe your desired diagram in simple English, and it will automatically generate:

- 🔤 Raw PlantUML (PUML) code  
- 🖼 SVG diagram rendering  
- 💾 Downloadable diagram output  

---

## 📌 Why This App?

Most UML tools require drag-and-drop or strict syntax. This app removes that complexity by using a **local Large Language Model (LLM)** to understand your intent and convert it to PUML.

All processing happens **offline**, using:

- **[Ollama](https://ollama.com/)** to run the LLM (e.g., Gemma)
- **`plantuml.jar`** to render the diagrams
- **Streamlit** for the interactive frontend

---

## 🖼 Supported Diagram Types

- Sequence Diagram  
- Use Case Diagram  
- Class Diagram  
- Object Diagram  
- Activity Diagram (legacy)  
- Component Diagram  
- Deployment Diagram  
- State Diagram  
- Timing Diagram  

---

## ⚙️ Prerequisites

Before running the app, make sure the following are installed:

### ✅ 1. Python 3.9+

Install [Python](https://www.python.org/downloads/) and then:

```bash
pip install streamlit requests
```

### ✅ 2. Java Runtime Environment (JRE)

`plantuml.jar` requires Java to run.

- Download from: https://www.oracle.com/java/technologies/javase-downloads.html  
- Verify installation:

```bash
java -version
```

### ✅ 3. PlantUML JAR file

This renders the PUML code into SVG diagrams.

- Download: https://plantuml.com/download  
- Place `plantuml.jar` in the same directory as `app.py`

### ✅ 4. Ollama (Local LLM engine)

This runs the LLM offline (e.g., Gemma, Mistral, LLaMA2).

- Download & install: https://ollama.com/download  
- After installation, verify:

```bash
ollama --version
```

---

## 🚀 Before You Run the App

### ✅ Step 1: Pull a Model (Only Once)

Ollama uses LLMs like `gemma:2b`. You need to pull the model before first use:

```bash
ollama run gemma:2b
```

This will download and run the model interactively — just exit afterward.

### ✅ Step 2: Start Ollama Server

Start the Ollama API server, which your app connects to:

```bash
ollama serve
```

This will expose `http://localhost:11434/api/generate` for the app.

---

## ▶️ How to Run the App

In another terminal (after `ollama serve` is running):

```bash
streamlit run app.py
```

Then open the URL shown (usually http://localhost:8501)

---

## 🧠 How It Works

1. You describe your diagram in plain English.  
2. The app formats your prompt and sends it to `gemma` via Ollama API.  
3. The response contains raw PUML code.  
4. The app writes the PUML to `puml.txt`.  
5. `plantuml.jar` converts `puml.txt` into an SVG image.  
6. You see the diagram and can download it.  

All of this happens **locally** — no internet required after setup!

---

## 📂 Project Structure

```
.
├── app.py              # Streamlit app
├── puml.txt            # Generated PUML code
├── puml.svg            # Output diagram
├── plantuml.jar        # PUML renderer
└── README.md
```

---

## 🧱 Future Enhancements

- 🌐 Export PNG, PDF versions  
- 🗂 Diagram history & versioning  
- 🧾 Editable PUML output   


## 🧠 Credits

- [Ollama](https://ollama.com/)  
- [PlantUML](https://plantuml.com/)  
- [Streamlit](https://streamlit.io/)  

---
