# Contributing Guide

Thank you for considering contributing to the Jentic API Discovery System!

## Quick Start
1. Fork the repo & clone your fork.
2. Create a virtual environment: `python3 -m venv .venv && source .venv/bin/activate`.
3. Install deps: `pip install -r requirements.txt` (and optionally `pip install -e .[dev]`).
4. Run tests: `pytest -q`.
5. Create a feature branch: `git checkout -b feat/<short-description>`.
6. Make changes with tests (where deterministic) and docs.
7. Run `pytest -q` again—keep it green.
8. Commit using conventional commits (e.g. `feat: add parser skeleton`).
9. Open a Pull Request to `main`.

## Conventional Commit Types
`feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`.

## Code Style / Practices
- Use type hints consistently.
- Keep functions small & pure (side-effect free where possible).
- Externalize configuration (no hard-coded magic numbers/paths).
- Avoid premature optimization; prefer clarity.

## Testing Strategy
- Deterministic logic: unit tests (pytest).
- Stochastic / external: abstract behind interfaces and mock.
- Add at least one regression test when fixing bugs.

## Security / Safety
- Never commit secrets or API keys.
- Treat external HTML content as untrusted; sanitize before LLM use (future modules).

## Adding a New Domain
1. Add `domains/<domain>/queries.yaml` (max 5 initial curated queries).
2. (Optional) Add `config.yaml` with domain specifics.
3. Run discovery: `python scripts/discover.py <domain>`.

## Roadmap Contribution
See open issues labeled `module:next` or propose enhancements via a feature request issue.

## Pull Request Checklist
- [ ] Tests added/updated & passing
- [ ] README / docs updated if behavior or usage changes
- [ ] No unrelated formatting churn
- [ ] CI passing

Thanks for helping build a reliable, extensible API discovery platform!
