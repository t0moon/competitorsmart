# CompetitorSmart

**Language / 语言**:
[简体中文](README.md) |
[English](README.en.md) |
[Español](README.es.md) |
[Français](README.fr.md) |
[Deutsch](README.de.md) |
[日本語](README.ja.md) |
[한국어](README.ko.md) |
[Português (Brasil)](README.pt-BR.md)

An AI-assisted competitive intelligence toolkit for **Product Managers / PMMs**.  
The main workflow uses a **LangGraph ReAct Agent**: it searches and crawls web evidence with DuckDuckGo, calls **Zhipu GLM** (OpenAI-compatible API), and generates a structured **11-section** Markdown report (market, competitor tiers, product capabilities, monetization, growth, SWOT, moats, opportunities, and more).

Default model and API base are centrally maintained in `src/constants.py` (current default: `glm-4.7`).

---

## Features

| Item | Description |
|------|-------------|
| Agent workflow | Search -> crawl -> reason; key conclusions include source URLs, with section and length constraints |
| Report output | `outputs/agent/<timestamp>_agent_report.md` |
| Model & keys | Zhipu; supports `ZHIPU_API_KEY_1` to `ZHIPU_API_KEY_4` (any one works) |
| Input modes | CLI competitor list, or structured `competitors_input.json` context (market, category, website copy, etc.) |

`requirements.txt` also includes CRM/Notion/sheet integrations for extension use; **to run end-to-end report generation, only Zhipu key + Agent dependencies are required** (see below).

---

## Prerequisites

- **Python**: 3.10+ recommended
- **Copy env template**: copy `.env.example` to `.env`, and set at least `ZHIPU_API_KEY_1`
- **Optional**: override the default Zhipu OpenAI-compatible endpoint using `ZHIPU_API_BASE_URL`

**Security**: never commit `.env`. The repo already ignores it. If you use Git, you can set `git config core.hooksPath githooks` to enable pre-commit checks and reduce accidental secret commits.

---

## Installation

```bash
pip install -r requirements.txt
```

If Agent-only dependencies are missing, install them directly:

```bash
pip install langgraph langchain-openai duckduckgo-search
```

---

## Usage

```bash
# If competitors_input.json exists in root and includes competitors
python main.py

# Quick run with competitor names (comma-separated), optional market context
python main.py --competitors "CompetitorA,CompetitorB" --market "SaaS CRM"

# Use structured JSON input (recommended: include website_copy, sales_notes, etc.)
python main.py --input competitors_input.json

# Validate config and dependencies only, without API calls
python main.py --dry-run
```

**Report directory**: `outputs/agent/`.

---

## Report Structure (Agent Template)

Final Markdown includes these fixed level-2 sections (see `SYSTEM_PROMPT` in `src/agent/graph.py`):

1. Executive Summary  
2. Market and Category Analysis  
3. Competitor Selection and Tiering  
4. Core Capability Breakdown (subsections per competitor)  
5. Business Model Analysis  
6. Growth and Distribution Strategy  
7. Users and Use Cases  
8. Strengths/Weaknesses Comparison (SWOT / matrix)  
9. Key Differentiators and Moats  
10. Opportunities and Strategic Recommendations  
11. Data Appendix (including source list)  

Some runs may take longer; if you hit quota/rate limits, switch API keys or retry later.

---

## Input Notes

- **`--competitors`**: names only; good for quick runs. Agent discovers websites and third-party sources automatically.  
- **`competitors_input.json`**: can include fields like `market`, `product_category`, `geography`, `our_product`, `competitors[].name`, `category`, `website`, `website_copy`, `sales_notes`, etc., aligned with `Config` loading logic in `src/config.py`.  
- For manual competitor profiling, refer to `src/templates/competitor_profile.md`.

---

## Repository Structure (Core)

```text
main.py                    CLI entry
competitors_input.json     Structured input example (custom name allowed via --input)
outputs/agent/             Agent-generated Markdown reports

src/
  constants.py             Default model and Zhipu API base
  config.py                Env variables and JSON input parsing
  agent/                   LangGraph Agent (tools, graph, validation)
  integrations/ai/         Zhipu OpenAI-compatible client and key selection
  models/                  Data models for competitors, etc.
  prompts/                 Legacy multi-step prompt templates (not used in current main flow)
  templates/               Competitor profile references

skills/                    PM skill libraries (Claude / Lenny, etc.) for analysis support
AGENTS.md                  Detailed instructions for collaborators and AI agents
```

---

## Methodology Tips

- Balance narrative with feature-level evidence, and frame conclusions in buyer language.  
- Acknowledge competitor strengths first, then explain differentiation for stronger credibility.  
- Prefer verifiable sources; AI accelerates collection, but business judgment still needs human validation.  
- Competitive intelligence should be continuously updated; each report is a snapshot, not a final answer.

---

## Further Reading

- Environment variable details: `.env.example`  
- Skills and project conventions: **[AGENTS.md](AGENTS.md)**
