# Build-AI-AMD
Learning resources for the AMD Build AI course, including study notes and Python code to help students understand AI concepts and build AI projects.

# 🍳 Local AI Cooking Agent

A local AI-powered cooking assistant built with Python, Streamlit, LangChain, and Ollama. The application helps users discover recipes based on the ingredients they have available and provides cooking instructions through a conversational interface.

The project uses the Llama 3.2 (3B) language model locally through Ollama, so it does not require a paid cloud LLM API.

## ✨ Features

- **Ingredient-Based Recipe Suggestions:** Find possible dishes using available ingredients.
- **Missing Ingredient Detection:** Identify ingredients needed to prepare a recipe.
- **Step-by-Step Instructions:** Get cooking instructions for supported recipes.
- **Conversational Interface:** Ask cooking-related questions through a Streamlit chat interface.
- **Local LLM Integration:** Run Llama 3.2 (3B) using Ollama.
- **Recipe Matching Tools:** Use Python functions as tools for the AI agent.
- **Ingredient Normalization:** Handle common ingredient aliases, such as potato/potatoes and eggplant/baingan.
- **Session-Based Conversation:** Maintain conversation messages during the current Streamlit session.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12.x | Main programming language |
| Streamlit | Web interface |
| LangChain | Agent and tool orchestration |
| Ollama | Run the language model locally |
| Llama 3.2 (3B) | Understand requests and generate responses |

## 🧠 How It Works

1. The user enters available ingredients and asks a cooking question.
2. Streamlit collects the ingredients and user request.
3. The agent receives the request and can select an appropriate Python tool.
4. The tool searches the built-in recipe collection or retrieves recipe details.
5. The tool results are returned to the language model.
6. The model generates a response, which Streamlit displays to the user.

**Architecture:**

User → Streamlit UI → LangChain Agent → Llama 3.2 via Ollama → Python Recipe Tools → Recipe Results → Response

## 📂 Project Structure

```text
Cooking_Agent/
│
├── app.py              # Main Streamlit application and agent logic
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .venv/              # Virtual environment (created locally)
```

The `.venv/` directory is generated on your computer and should not be uploaded to GitHub.

## 💻 Prerequisites

Before running the project, install the following:

- Windows 10/11, or another supported operating system
- Python 3.12.x (recommended for this setup)
- Git
- Ollama
- An internet connection for the initial installation and model download

**Python version:** This README uses Python 3.12.x. If your existing project has already been tested with another Python version, use that tested version instead.

## 🚀 Installation and Setup

### Step 1: Clone the GitHub Repository

Open PowerShell or the VS Code terminal and run:

```powershell
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Replace the URL with your actual GitHub repository URL.

Navigate into the project directory:

```powershell
cd YOUR_REPOSITORY
```

Alternatively, if you have already downloaded or cloned the project, open its folder directly in the terminal.

### Step 2: Check Python Installation

Check your Python version:

```powershell
python --version
```

Expected version for this guide:

```text
Python 3.12.x
```

If Python is not recognized, install Python from:

https://www.python.org/downloads/

During installation on Windows, enable the option to add Python to PATH if available.

### Step 3: Create a Virtual Environment

A virtual environment keeps this project's Python dependencies separate from other projects.

Run:

```powershell
python -m venv .venv
```

This creates a `.venv` directory inside the project folder.

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After successful activation, the terminal should show something similar to:

```text
(.venv) PS C:\path\to\your\project>
```

**If PowerShell blocks activation:** You can use the virtual environment's Python executable directly without changing the Windows execution policy:

```powershell
.\.venv\Scripts\python.exe --version
```

Use the same executable for package installation and application execution in the following steps if activation does not work.

### Step 5: Install Python Dependencies

If the repository contains a `requirements.txt` file, install its dependencies with:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you do not have a `requirements.txt` file yet, create one containing:

```text
streamlit
langchain
langchain-ollama
```

Then install the dependencies.

**Note:** These are the core packages used by the application. For reproducible installations, test the project and pin compatible package versions in `requirements.txt`.

### Step 6: Install Ollama

Download and install Ollama for Windows:

https://ollama.com/download/windows

After installation, open a new terminal and verify that Ollama is available:

```powershell
ollama --version
```

Ollama runs the language model locally on your computer.

### Step 7: Download the Llama Model

Download the Llama 3.2 3B model:

```powershell
ollama pull llama3.2:3b
```

The download may take some time, depending on your internet connection.

Verify that the model is installed:

```powershell
ollama list
```

You should see `llama3.2:3b` in the available models.

### Step 8: Test the Model

Run:

```powershell
ollama run llama3.2:3b
```

Try asking:

```text
Suggest a simple recipe using potatoes and tomatoes.
```

If the model responds, exit the interactive session by typing `/bye`.

Ollama must be running when you use the Cooking Agent. If the application cannot connect to Ollama, open the Ollama desktop application or start the Ollama service.

### Step 9: Run the Streamlit Application

Ensure your terminal is in the directory containing `app.py`.

Run:

```powershell
python -m streamlit run app.py
```

If you are not activating the virtual environment, run the application through its Python executable:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open this address in your browser to use the Cooking Agent.

## 🍲 Example Usage

Enter the following ingredients in the sidebar:

```text
potato, tomato, egg
```

Then ask:

```text
What can I cook with these ingredients?
```

You can also ask questions such as:

- Suggest a simple potato recipe.
- Which ingredients are missing for Potato Tomato Curry?
- Give me the steps for Simple Egg Curry.
- Suggest a recipe that uses tomatoes and eggs.

The suggestions and instructions depend on the recipes available in the application's built-in collection and the model's response.

## 🧰 Tools Used by the Agent

The application includes Python tools such as:

- `find_recipe_ideas()` — searches supported recipes using the user's available ingredients.
- `check_missing_ingredients()` — checks which ingredients are present or missing for a recipe.
- `get_recipe_details()` — retrieves recipe ingredients, cooking time, and instructions.

These tools let the agent access structured recipe information instead of relying only on the language model's generated knowledge.

## ⚠️ Current Limitations

- The current prototype uses a small, predefined recipe collection in `app.py`.
- It does not yet use a separate SQL or NoSQL recipe database.
- Recipe coverage is limited to the recipes already defined in the application.
- Ingredient matching depends on the current normalization and matching logic.
- Generated responses may contain inaccuracies; always verify cooking instructions and food-safety guidance.
- Performance depends on available system resources and the local model.

## 🔮 Future Improvements

- Integrate a larger recipe dataset.
- Add a SQLite or PostgreSQL database.
- Support cuisine, dietary preference, and cooking-time filters.
- Rank recipes by ingredient coverage and missing ingredients.
- Add a form for users to contribute recipes.
- Improve the user interface and recipe presentation.
- Add automated tests and more robust error handling.

## 🐛 Troubleshooting

### 1. `streamlit` is not recognized

Run:

```powershell
python -m streamlit run app.py
```

Or use the virtual environment's Python executable.

### 2. Ollama connection error

Check that Ollama is installed and running:

```powershell
ollama list
```

If necessary, start Ollama and try running the application again.

### 3. Model not found

Download the model:

```powershell
ollama pull llama3.2:3b
```

Ensure that the model name in `app.py` matches the installed model.

### 4. `ModuleNotFoundError`

Install the project's dependencies in the correct virtual environment:

```powershell
python -m pip install -r requirements.txt
```

### 5. Windows blocks a native Python package

If Windows reports that an application-control policy blocked a native package, inspect the Windows Code Integrity logs and verify that the package is compatible and trusted. Do not download random DLL files or disable Windows security to work around the error.

## 🔒 Security

- Do not upload API keys, passwords, or other secrets.
- Do not commit your virtual environment.
- Add `.venv/`, `__pycache__/`, and other generated files to `.gitignore`.
- Ollama model files are stored separately from the Git repository.

## 🤝 Contributing

Contributions and suggestions are welcome. You can improve the recipe collection, add database integration, enhance ingredient matching, or improve the interface.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application.
5. Submit a pull request.

## 📄 License

Choose a suitable open-source license for your repository and add its license file if you intend to permit reuse.

---

**Built with Python, Streamlit, LangChain, and Ollama.**

A learning project exploring local language models, tool calling, and practical AI agent development.
