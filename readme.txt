# LLM-Based RAG System

## Overview

This project is designed to create a Retrieval-Augmented Generation (RAG) system using a Large Language Model (LLM). The system integrates with an API to scrape content from the internet and uses an API to serve the LLM-generated answers. A simple front-end interface is provided to interact with the system. 
Note: ONLY use the packages provided in the requirements.txt file (similar/alternative packages are ok only if they perform similar task/function). 

## Setup Instructions

### Step 1 : Set Up a Virtual Environment

You can use `venv` or `conda` to create an isolated environment for this project.

#### Using `venv`

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

#### Using `conda`

```bash
conda create --name project_env python=3.8
conda activate project_env
```
### Step 2: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the root directory and add your API keys in a way it can be accessed in the app.


### Step 4: Run the Flask Backend

Navigate to the `flask_app` directory and start the Flask server:

```bash
cd flask_app_langchain
python app_langchain.py
```

### Step 5: Run the Streamlit Frontend

In a new terminal, run the Streamlit app:

```bash
cd streamlit_app
streamlit run app.py
```

### Step 6: Open the Application

Open your web browser and go to `http://localhost:8501`. You can now interact with the system by entering your query.


