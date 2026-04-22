# Agon API Solver

A simple, extensible FastAPI backend designed for the Agon AI Evaluation Dashboard hackathon.

## Features
- **Extensible Architecture:** Routes, solvers, and utilities are modularly split.
- **FastAPI Foundation:** Leverages Pydantic for validation and easy serialization.
- **Level 1 Deterministic Solver:** Solves simple mathematical queries using regex without LLMs to save time and costs.
- **Fallback Logic:** Readily extensible for an LLM fallback and asset context injection via URLs.

## Project Structure
- `app/main.py` : Application entrypoint.
- `app/api/routes.py` : Defines the endpoints / workflow (Level 1 Check -> Assets -> LLM).
- `app/models/schemas.py` : Pydantic schemas validating the request/response payloads.
- `app/solvers/level1.py` : Handles our simple arithmetic cases.
- `app/solvers/llm_solver.py` : A stub for whatever LLM logic comes next.
- `app/utils/` : Helpers for fetching assets and formatting responses correctly.

## 1. Setup

Create and activate a virtual environment, then install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Running Locally

Run the application with `uvicorn`:
```bash
uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`. 
API Docs (Swagger UI) are available at `http://127.0.0.1:8000/docs`.

## 3. Testing with cURL

Since the Agon API evaluation requires a specific contract (`query` and `assets`, responding with `output`), we can test it locally.

**Level 1 Test Case:**
```bash
curl -X POST http://127.0.0.1:8000/solve \
-H "Content-Type: application/json" \
-d '{"query": "What is 10 + 15?", "assets": []}'
```

**Expected Response:**
```json
{"output": "The sum is 25."}
```
