## Jentic API Discovery System (MVP)

![CI](https://github.com/CianHerreraQuinn/Jentic-11-LLM-Powered-API-Discovery-System/actions/workflows/ci.yml/badge.svg)

Initial MVP focused on discovering weather APIs and their key acquisition steps. The codebase is deliberately modular to enable future domain expansion (finance, sports, news, etc.) with minimal code changes.

### Current Scope (Modules Implemented)
Implemented:
- Module 1: Search Strategy (query curation / validation)
- Module 2: Source Discovery (dummy provider, ranking, artifact persistence)

Pending (future modules): parsing, spec generation, key handling, validation, scoring.

### Architecture Overview (Planned)
```
domains/        # Per-domain configs (queries, parameters)
modules/        # Reusable modules (search, parse, spec_gen, key_handler, ...)
apis/           # Generated outputs per provider (OpenAPI specs, key docs)
scripts/        # Helper scripts (key request, test calls)
tests/          # Automated tests (pytest)
```

### Module 1: Search Strategy (Implemented)
Goal: Provide a deterministic, testable way to supply domain-specific search queries that upstream discovery components will execute using external search APIs (to be added later). Queries are stored in YAML for transparency and easy curation.

Features:
- YAML-backed query lists per domain.
- Enforces configurable maximum queries (MVP: 5) to control cost & rate limits.
- Validation of duplicates / empty entries.
- Extensible strategy pattern for future dynamic LLM augmentation.

### Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

### Adding a New Domain (Early Pattern)
1. Create `domains/<domain>/queries.yaml` with up to 5 curated queries.
2. (Future) Add `config.yaml` describing special parsing/auth patterns.
3. Use the same loader API: `DomainQueryLoader(domain="<domain>").get_queries()`.

### Roadmap (High-Level)
| Module | Status | Notes |
|--------|--------|-------|
| Search Strategy | ✅ | Implemented with tests |
| Source Discovery | ✅ | Dummy provider + ranking + artifact |
| Parsing & Extraction | ⏳ | HTML / doc parsing, key info extraction |
| Spec Generation | ⏳ | LLM-driven OpenAPI creation |
| Key Handling | ⏳ | Scripts & instruction generation |
| Validation / Anti-Hallucination | ⏳ | Multi-source + structural checks |
| Confidence Scoring | ⏳ | Aggregated signal weighting |

### Testing Philosophy
Test-Driven Development (TDD) is used where logic is deterministic (e.g., query loading, validation). For stochastic or external integrations (LLMs, search APIs), future tests will employ abstraction layers + mocks.

### Security & Safety (Forward Looking)
- No secrets stored in repo.
- Future: central secrets manager integration for API keys.
- Sanitization of external content before LLM prompting.

### License
Licensed under the MIT License (see `LICENSE`).

### Contributing
Early stage. Keep modules small, pure, and covered by tests. Avoid coupling domain-specific logic into shared modules.
