# GMC Sierra Rebuild Tracker

A full-stack project management application built around a real 1990 GMC Sierra engine swap — tracking tasks, budget, and build progress with an integrated AI mechanic and electrical diagram viewer.

While the dataset is specific to this build (Edelbrock Pro-Flo 4 EFI swap, 4L80E transmission), the application is designed as a general-purpose project tracker adaptable to any domain.

---

## Features

### Task & Budget Tracker
- Track rebuild tasks by status (Not Started / In Progress / Complete)
- Log actual cost per task — running total surfaced via Chart.js
- UI state (checkboxes, dropdowns, budget entries) persists across page refreshes via SQLite

### AI Mechanic (`/ask_ai`)
- Ask build-specific questions in plain English
- Powered by Llama 3.2 (local, via Ollama) — no cloud, no API cost
- Full project plan injected as system context so answers are specific to this EFI build, not generic advice
- Guards against hallucination: explicit instructions prevent the model from referencing unrelated EFI systems (e.g., ACES EFI, Wild Card) or confusing estimates with actual spend

### Wiring Diagram Viewer (`/diagrams`)
- 29 indexed electrical diagrams covering 1988–98 GM C/K Series trucks
- Browse diagrams in-browser; ask questions about specific figures
- Vision-capable: uses `llava` model to analyze diagram images when available; falls back to `llama3.2` text with diagram metadata

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask 3.0 |
| Database | SQLite3 (tasks + UI state persistence) |
| Frontend | HTML, Tailwind CSS (CDN), Chart.js, Vanilla JS |
| AI | Ollama (Llama 3.2 + llava) — local inference |
| Deployment | Docker + Docker Compose |

---

## Getting Started

### Option 1 — Docker (recommended)

Requires [Docker](https://docs.docker.com/get-docker/) and [Ollama](https://ollama.com) running locally with `llama3.2` pulled.

```bash
git clone https://github.com/Linconjoe/Full-Stack-Project-Tracker.git
cd Full-Stack-Project-Tracker
docker compose up --build
```

App runs at `http://127.0.0.1:5001`

For AI features: Ollama must be running on the host at port `11434`. The container connects via `host.docker.internal`.

### Option 2 — Local Python

```bash
git clone https://github.com/Linconjoe/Full-Stack-Project-Tracker.git
cd Full-Stack-Project-Tracker
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 create_db.py      # initialize database
python3 seed_fuel_tasks.py  # load task data
python app.py
```

App runs at `http://127.0.0.1:5000`

---

## Project Structure

```
├── app.py                    # Flask backend — all routes
├── create_db.py              # Database initialization
├── seed_fuel_tasks.py        # Task seed data
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── diagram_index.json        # Metadata for 29 wiring diagrams
├── diagrams.html             # Diagram viewer page
├── Electrical diagrams/      # GM C/K wiring diagram images (GIF)
└── gmc_sierra_rebuild_guide fuel injection full plan.html  # Main UI
```

---

## AI Architecture Note

The AI mechanic uses a **retrieval-by-injection** pattern: the full HTML rebuild plan is read at request time, stripped of tags, and prepended as system context (first 8,000 characters). This gives the model build-specific knowledge without a vector database or fine-tuning.

The prompt includes explicit anti-hallucination guards: the model is instructed to treat user-provided cost figures as ground truth and is forbidden from referencing EFI systems not present in this build.

---

## Context

This project is Lab 1 in a progressive home lab series exploring AI integration across different domains:

- **Lab 1** (this repo) — IoT + project tracking + local AI (Ollama)
- **Lab 2** — Air-gapped SOC pipeline (Bash + Ollama) — deprecated, accuracy insufficient
- **Lab 3** — Claude API SOC pipeline — 95% accuracy, production-grade
- **Lab 5** — Multi-agent CrewAI SOC (Gemini 2.5 Flash) — 44x cost reduction vs Lab 3
- **Lab 6** — Full-stack RAG knowledge system (FastAPI + Chroma + Gemini)

Each lab is a real working system, not a tutorial clone.
