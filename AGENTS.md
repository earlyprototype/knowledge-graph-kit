# AGENTS.md

## Cursor Cloud specific instructions

### Product overview

Knowledge Graph Kit is a Python toolkit for building file-based knowledge graphs and viewing them in an interactive web UI (`viewer.html`). There is no monorepo, Docker, database, or npm frontend — only Python + static HTML/JS.

### Required services

| Service | Port | Start command |
|---------|------|---------------|
| HTTP static server | 8000 | From repo root: `python3 core/server.py --directory examples/systems-map-example --no-browser` |

Optional (not needed for core dev): Flask Gemini chat API on port 8001 via `start_server.py` in full templates; requires `gemini_config.json` and `pip install flask flask-cors` (Flask is not in `requirements.txt`).

### Standard commands

See `README.md` and `CONTRIBUTING.md` for full setup. Typical dev workflow:

```bash
pip install -r requirements.txt
cd examples/systems-map-example && python3 build_map.py
python3 core/server.py --directory examples/systems-map-example --no-browser
```

Open `http://localhost:8000/viewer.html`. The viewer loads vis-network and marked from CDNs — network access is required for the full UI.

### Lint / test

There is no configured linter, formatter, or automated test suite in this repo. Manual verification:

- `python3 examples/basic_usage.py` — exercises `GraphManager` against all four templates
- `python3 examples/systems-map-example/build_map.py` — regenerates example graph data
- Serve the example and confirm `viewer.html` and `_data/entities.json` return HTTP 200

### Gotchas

- **Graph data path**: Example and templates store data at `_data/entities.json` (not `data/` as shown in some README diagrams).
- **Systems template schema**: The systems-map example uses a `components` key in JSON, not `primary`.
- **Serving from repo root**: Use `core/server.py --directory <project-dir>`; the example has no local `server.py`.
- **Wizard is interactive**: `setup_wizard.py` prompts for input — use manual template copy + `init.py` for non-interactive setup.
- **No hot reload**: Restart the HTTP server after changing graph JSON or static files.
