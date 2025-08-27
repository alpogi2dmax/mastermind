# Mastermind Game Backend

This is the backend for a Mastermind-style game built with **Flask** and **Flask-RESTful**.  
It provides API endpoints for generating secret codes, evaluating guesses, giving hints, and maintaining a leaderboard.

---

## Features

- Generate a secret code with customizable difficulty and length
- Evaluate player guesses
- Provide hints
- Track game attempts and timing
- Leaderboard for Easy, Normal, and Hard difficulties
- RESTful API ready for frontend integration

---

## Tech Stack

- Python 3.8+
- Flask
- Flask-RESTful
- Flask-CORS
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow / Marshmallow-SQLAlchemy
- Requests (for code generation via random.org)
- Pytest & Pytest-Mock for testing

---

## Frontend Integration

This backend is designed to work with a separate frontend application built in **React**.  

- Frontend repository: [Mastermind Frontend](https://github.com/alpogi2dmax/mastermind-frontend)
- The frontend communicates with this backend via RESTful API endpoints.
- Update the frontend’s API URL configuration to point to this backend’s URL (e.g., `http://localhost:5000` for local development).
- CORS is enabled in this backend to allow requests from the frontend during development.

---

## Installation

1. Clone the repository:

```bash
git clone git@github.com:alpogi2dmax/mastermind.git
cd mastermind
```

2. Create and activate a virtual envieronment:

```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3.  Install dependencies:

```bash
pip install -r requirements.txt
```

** Running the Server

```bash
python app.py
```

---

## API Endpoints

| Endpoint              | Method        | Description                               |
|-----------------------|---------------|-------------------------------------------|
| /api/generate         | POST          | Generate a secret code for a new game     |
| /api/evaluate         | POST          | Evaluate a player's guess                 |
| /api/gethint          | GET           | Reveal a hint for the secret code         |
| /api/settings         | GET           | Retrieve game settings                    |
| /api/getleaderboard   | GET           | Get top 10 scores per difficulty          |


---

## Development Workflow

1. Start the backend locally:

```bash
python app.py
```

2. Start the frontend (from the frontend repo):

```bash
npm install
npm run dev
```

3. Open the frontend in our browser. It will communicate with the backend API automatically.

---

## Project Structure

mastermind/
│
├─ app.py                  # Flask app entrypoint
├─ config.py               # Default game settings & DB URI
├─ extensions.py           # SQLAlchemy & Migrate instances
├─ game.py                 # Global GAME object and reset logic
├─ models.py               # Score model
├─ schema.py               # Marshmallow schema for Score
├─ resources/              # RESTful resources
│   ├─ generate.py
│   ├─ evaluate.py
│   ├─ hint.py
│   ├─ settings.py
│   └─ leaderboard.py
├─ tests/                  # Pytest test files
└─ requirements.txt

---

## Notes

- Uses erqwurests to fetch random integers from random.org for secret code generation.
- GAME is a global object that stores current game state.
- Leaderboard are stored in the database, adn the backend returns the top 10 scores per difficulty.