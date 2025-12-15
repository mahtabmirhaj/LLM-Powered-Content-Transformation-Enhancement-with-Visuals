# Repository Guidelines

## Project Structure & Module Organization
- `ExampleCode/` — standalone experiments (AzureOpenAIDiagramAsCode, OpenRouter, etc.) pairing numbered setup scripts with Python drivers such as `diagram-as-code_azure-openai-llm.py`; keep assets beside each module.
- `ExampleService/` — service wrappers (SlideSpeak, PPTAgent references) that expose the experiments through APIs or UIs; store service-specific infra files within each subfolder.
- `Research/` — deeper studies. `my-local-deep-researcher` follows `pyproject.toml` + `src/my_local_deep_researcher` and ships Docker + LangGraph configs, while `STORM/` and similar folders provide supporting research data.
- `EricssonTechnologyReview/`, `ExampleThesis/`, and other PDF collections are immutable source material—add new revisions instead of editing in place.

## Build, Test, and Development Commands
- Standard workflow: `./ExampleCode/<module>/1_install-uv.sh`, `2_uv-create-venv.sh`, `3_install-requirements.sh`, then `source .venv/bin/activate`.
- Execute demos with uv, e.g., `uv run python ExampleCode/AzureOpenAIDiagramAsCode/diagram-as-code_azure-openai-llm.py` or `uv run python ExampleCode/OpenRouter/openrouter_local-image-to-text.py` after exporting variables via the provided `4_set-env-*.sh` helpers.
- For LangGraph work, run `cd Research/my-local-deep-researcher && uv run langgraph dev --reload`; container validation uses `docker build -t local-deep-researcher . && docker run --rm -p 2024:2024 local-deep-researcher`.

## Coding Style & Naming Conventions
- Python: 4-space indents, snake_case modules, Google-style docstrings, and type-hinted public functions. Keep entry scripts thin and push logic into `src/...` packages.
- Apply the repo’s Ruff profile (`uv run ruff check .`) and, when touching typed packages, `uv run mypy src`.
- Shell scripts stay executable, lower-kebab-case (numeric prefixes when ordering matters), and should guard with `set -euo pipefail`.

## Testing Guidelines
- Prefer `pytest` with files under `<module>/tests/test_*.py`. Mock external services by pointing the same env vars (`OPENAI_API_KEY`, `GROQ_API_KEY`, etc.) to local fakes.
- Run `uv run pytest` from the module root; for script-only demos, document and run a deterministic smoke command before submitting (e.g., `uv run python ... --dry-run`).

## Commit & Pull Request Guidelines
- Use short imperative commits similar to existing history ("Add OpenRouter image pipeline"). Keep each experiment or service change in its own commit.
- PRs should summarize motivation, list touched folders, call out new secrets or env flags, and embed sample output, screenshots, or Mermaid snippets when behavior changes.
- Update module READMEs whenever you alter setup steps, environment variables, or directory conventions.

## Security & Configuration Tips
- Never commit `.env` files or real keys—extend the `*_set-env-variables*.sh` helpers or provide sanitized `.env.example` diffs instead.
- Centralize credentials per module and prefer new files when ingesting proprietary PDFs so the original sources remain traceable.
