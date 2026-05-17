# SHL Assessment Recommendation Chatbot

## Overview

This project is an AI-powered chatbot that recommends suitable SHL assessments based on hiring requirements and job roles.

The system uses:
- FastAPI backend
- Streamlit chatbot UI
- Retrieval-based recommendation engine
- SHL assessment catalog data

Users can enter hiring requirements such as:
- Java Backend Developer
- Data Analyst
- Sales Manager

The chatbot then recommends relevant SHL assessments with links and assessment types.

---

## Features

- Conversational chatbot interface
- SHL assessment recommendations
- Technical and business role matching
- Comparison mode support
- FastAPI REST API
- Streamlit frontend
- GitHub integrated deployment

---

## Tech Stack

- Python
- FastAPI
- Streamlit
- JSON-based retrieval engine
- Requests
- Uvicorn

---

## Project Structure

```text
app.py                -> FastAPI backend
streamlit_app.py      -> Streamlit frontend
retriever.py          -> Recommendation engine
metadata.json         -> SHL assessment metadata
requirements.txt      -> Dependencies
```

---

## Run Locally

### 1. Start Backend

```bash
uvicorn app:app --reload
```

### 2. Start Frontend

```bash
streamlit run streamlit_app.py
```

---

## Example Queries

- Senior Java Backend Developer
- Data Analyst with SQL skills
- Frontend React Developer
- Sales Manager

---

## Demo

The chatbot recommends suitable SHL assessments along with:
- assessment name
- assessment type
- SHL assessment link

---

## Author

Nitish Yadav
