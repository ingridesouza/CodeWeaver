# CodeWeaver


This project demonstrates an autonomous multi-agent workflow built with CrewAI and Django REST Framework.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your API keys.
3. Run the Django server:
   ```bash
   cd backend
   python manage.py migrate
   python manage.py runserver
   ```

## API Usage

Send a POST request to `/api/generate/` with a JSON body:
```json
{
  "prompt": "Build a simple todo application"
}
```
The endpoint triggers the multi-agent workflow and returns the path to a zip archive with the generated project.
