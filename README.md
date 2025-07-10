# Web Q&A App with Ollama, LangChain, and Streamlit

This app lets you enter **any URL**, scrapes its content, and answers your questions using a local language model powered by **Ollama** and **LangChain**.

---

## Step-by-Step Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/Nani1432/qa_project.git
cd qa_project

## Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

## Install required Python packages
pip install -r requirements.txt

#Install Ollama locally
Download Ollama from https://ollama.com/download

ollama pull phi:2.7b

## Run the Streamlit app
streamlit run main.py
