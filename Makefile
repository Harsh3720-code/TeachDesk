.PHONY: docs

## docs: build the Engineering Handbook (.docx + .pdf) into docs/build/
docs:
	uv run --locked python scripts/build_docs.py
