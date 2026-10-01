.PHONY: docs lint test format run

## docs: build the Engineering Handbook (.docx + .pdf) into docs/build/
docs:
	uv run --locked python scripts/build_docs.py

## lint: check style, formatting and types (ruff + mypy --strict)
lint:
	uv run --locked ruff check .
	uv run --locked ruff format --check .
	uv run --locked mypy

## test: run the pytest suite
test:
	uv run --locked pytest

## format: reformat the code with ruff
format:
	uv run --locked ruff format .

## run: start the development server with auto-reload
run:
	uv run --locked uvicorn app.main:create_app --factory --reload
