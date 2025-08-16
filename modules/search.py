"""Search Strategy Module.

Responsible for providing curated and (future) dynamically-extended search
queries for a given domain. This MVP implementation focuses on deterministic
loading & validation of YAML-defined queries to feed downstream discovery.

Design Goals:
1. Deterministic output (enables TDD & caching).
2. Configurable maximum queries (default=5) to control external search costs.
3. Validation: no duplicates, no empty strings, respects provided limit.
4. Extensibility: Strategy interface for future LLM augmentation.

Future Extensions (Not Implemented Yet):
- LLMQueryAugmentor: Expand base queries with semantic variants.
- AdaptiveQueryRefiner: Feedback loop from discovery/validation signals.
- Multi-language query generation.
"""
from __future__ import annotations # pragma: no cover - for type checking only

from dataclasses import dataclass # this is for defining data classes
from pathlib import Path # this is for working with file paths
from typing import List, Protocol # this is for type hinting
import yaml

from .config import load_settings, ConfigError


class QuerySourceError(Exception):
    """Raised when queries cannot be loaded or validated."""


class QueryStrategy(Protocol):
    """Protocol for strategies that produce search queries.

    Implementations may pull from static files, generate with LLMs, or
    compose multiple approaches. Keeping a narrow interface simplifies
    orchestration and testing.
    """

    def get_queries(self, limit: int | None = None) -> List[str]:  # pragma: no cover - interface
        ...


@dataclass
class DomainQueryLoader(QueryStrategy):
    """Load and validate domain-specific queries from a YAML file.

    YAML Format:
    ```yaml
    queries:
      - "weather API with free API key"
      - "..."
    ```
    """

    domain: str
    base_dir: Path | None = None
    filename: str | None = None

    def _file_path(self) -> Path:
        settings = load_settings()
        base_dir = self.base_dir or settings.search.domains_base_dir
        filename = self.filename or settings.search.queries_filename
        return base_dir / self.domain / filename

    def _load_raw(self) -> List[str]:
        path = self._file_path()
        if not path.exists():
            raise QuerySourceError(f"Query file not found: {path}")
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except yaml.YAMLError as e:  # pragma: no cover - unlikely unless malformed
            raise QuerySourceError(f"Invalid YAML in {path}: {e}") from e
        queries = data.get("queries")
        if not isinstance(queries, list) or not queries:
            raise QuerySourceError("'queries' list missing or empty in YAML")
        return queries

    def _validate(self, queries: List[str], limit: int | None) -> List[str]:
        cleaned: List[str] = []
        seen = set()
        for q in queries:
            q_norm = (q or "").strip()
            if not q_norm:
                continue  # skip empty strings silently
            if q_norm.lower() in seen:
                continue  # drop duplicates preserving first occurrence
            seen.add(q_norm.lower())
            cleaned.append(q_norm)
            if limit is not None and len(cleaned) >= limit:
                break
        if not cleaned:
            raise QuerySourceError("No valid queries after cleaning/validation")
        return cleaned

    def get_queries(self, limit: int | None = None) -> List[str]:
        settings = load_settings()
        effective_limit = limit if limit is not None else settings.search.default_query_limit
        raw = self._load_raw()
        return self._validate(raw, effective_limit)


def get_domain_queries(domain: str, limit: int = 5) -> List[str]:
    """Convenience function for typical usage.

    Parameters
    ----------
    domain: str
        Domain name (e.g., 'weather'). Must correspond to a folder under `domains/`.
    limit: int
        Maximum number of queries to return (default 5). Set to None for all.
    """
    loader = DomainQueryLoader(domain=domain)
    return loader.get_queries(limit=limit)


__all__ = [
    "QuerySourceError",
    "QueryStrategy",
    "DomainQueryLoader",
    "get_domain_queries",
]
