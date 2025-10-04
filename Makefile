dev:
	uv run fastapi dev app/main.py

start:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

studio:
	uv run langgraph dev --allow-blocking