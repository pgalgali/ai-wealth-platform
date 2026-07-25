.PHONY: web api test lint compose

web:
	npm install
	npm run dev

api:
	cd backend && uvicorn app.main:app --reload --port 8000

test:
	cd backend && pytest

lint:
	cd backend && ruff check app tests
	npm run typecheck

compose:
	docker compose -f infra/docker-compose.yml up --build
