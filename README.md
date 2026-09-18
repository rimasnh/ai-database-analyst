# AI Database Analyst

A secure, enterprise-style AI database analyst that answers natural-language questions over a company database. Built with **Google's Agent Development Kit (ADK) 2.0** and **Gemini 3.1 Flash Lite**, with deterministic security guardrails that block destructive SQL before it ever reaches the database.

## How it works

```
Plain-English question → ADK agent → Gemini 3.1 Flash Lite drafts SQL
    → security hook inspects the SQL → read-only query runs on SQLite
    → natural-language answer
```

The key design decision: safety is enforced by a deterministic `before_tool_callback` hook — not by asking the model nicely. The model can generate anything; the hook blocks `DROP`, `DELETE`, `UPDATE`, `INSERT`, and `ALTER` unconditionally, before execution.

## Security guardrails

- **Destructive-SQL bouncer** (`security_bouncer` in `agent.py`): an ADK 2.0 lifecycle hook that runs before every tool call and raises `PermissionError` on forbidden keywords.
- **Read-only by construction**: the only tool the agent can call is `query_database`, a single-statement SQLite lookup.
- **Defense in depth**: even if the model is tricked into emitting `DROP TABLE`, the hook kills the call before it executes.

## Quickstart

```bash
pip install google-adk python-dotenv
python setup_db.py   # creates company.db with sample employee data
```

Then launch the agent with the ADK runner / developer UI and ask questions like:

- "What is the average salary by role?"
- "List all employees in Engineering."
- "Delete all employees." → blocked: `Security Alert: Destructive command 'DELETE' blocked!`

## Project structure

| File | Purpose |
|---|---|
| `agent.py` | Agent definition, `query_database` tool, `security_bouncer` hook |
| `setup_db.py` | Creates `company.db` with sample employee data |
| `company.db` | Local SQLite demo database (regenerate anytime with `setup_db.py`) |

## Tech stack

Python · Google ADK 2.0 · Gemini 3.1 Flash Lite · SQLite

## Limitations & roadmap

- Keyword-based blocking is a solid first line of defense; a production version would add SQL parsing, per-user authorization, and audit logging.
- Demo runs on a local SQLite database with mock data.
