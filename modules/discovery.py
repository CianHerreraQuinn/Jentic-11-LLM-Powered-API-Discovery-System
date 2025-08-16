"""Module 2: API Source Discovery.

Transforms domain search queries into a curated set of candidate API
documentation URLs through provider abstraction, ranking, and de-duplication.

Design Highlights:
- Provider abstraction (`SearchProvider`) allows plugging in real search APIs later.
- Deterministic Dummy provider for TDD and offline development.
- Scoring heuristic favors 'official' domains via configurable keyword lists.
- Canonicalization removes tracking query params for proper de-duplication.
- Persisted artifact (JSON) enables reproducibility & later parsing.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Protocol
import json
import re
from urllib.parse import urlparse, urlunparse

from .config import load_settings
from .search import get_domain_queries


@dataclass(slots=True)
class SearchResult:
    query: str
    title: str
    url: str
    snippet: str | None
    rank: int
    provider: str
    score: float | None = None  # assigned later


class SearchProvider(Protocol):
    name: str

    def search(self, query: str, limit: int) -> List[SearchResult]:  # pragma: no cover - interface
        ...


class DummySearchProvider:
    """Deterministic placeholder provider.

    Generates pseudo-results derived from the query tokens. This avoids
    external dependencies while we build downstream logic & tests.
    """

    name = "dummy"

    def search(self, query: str, limit: int) -> List[SearchResult]:  # pragma: no cover - simple
        base = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")[:30]  # truncate to 30 chars
        results: List[SearchResult] = []
        # Simulate a mix of official and aggregator domains
        candidate_hosts = [
            f"{base}.api-docs.example.com",
            f"developer.{base}.example.com",
            f"{base}.rapidapi.com",
            f"docs.{base}.example.org",
            f"blog.{base}.example.net",
        ]
        for idx, host in enumerate(candidate_hosts[:limit]):
            url = f"https://{host}/reference"  # canonical path
            results.append(
                SearchResult(
                    query=query,
                    title=f"{query} result {idx+1}",
                    url=url,
                    snippet=f"Documentation for {query} ({host})",
                    rank=idx + 1,
                    provider=self.name,
                )
            )
        return results


# URL canonicalization - this function removes tracking parameters and fragments 
def canonicalize_url(url: str) -> str:
    """Remove tracking query params & fragments for de-duplication."""
    parsed = urlparse(url)
    # Drop query & fragment
    clean = parsed._replace(query="", fragment="")
    return urlunparse(clean)


def score_result(r: SearchResult) -> float:
    settings = load_settings()
    host = urlparse(r.url).hostname or ""
    score = 0.0
    # Official domain boost
    for kw in settings.search.allowed_domain_keywords:
        if kw.lower() in host.lower():
            score += 2.0
    for kw in settings.search.blocked_domain_keywords:
        if kw.lower() in host.lower():
            score -= 3.0
    # Rank influence (earlier rank -> small bonus)
    score += max(0.0, 1.5 - 0.1 * (r.rank - 1))
    return score


@dataclass(slots=True)
class DiscoveryArtifact:
    domain: str
    generated_at: str
    provider: str
    queries_used: List[str]
    results: List[SearchResult]

    def to_json(self) -> str:
        return json.dumps(
            {
                "domain": self.domain,
                "generated_at": self.generated_at,
                "provider": self.provider,
                "queries_used": self.queries_used,
                "results": [asdict(r) for r in self.results],
            },
            indent=2,
        )


class DiscoveryEngine:
    def __init__(self, provider: SearchProvider | None = None):
        self.provider = provider or DummySearchProvider()
        self.settings = load_settings().search

    def discover(self, domain: str) -> List[SearchResult]:
        queries = get_domain_queries(domain)
        collected: List[SearchResult] = []
        seen_urls: set[str] = set()
        for q in queries:
            batch = self.provider.search(q, limit=self.settings.max_results_per_query)
            for r in batch:
                canon = canonicalize_url(r.url)
                if canon in seen_urls:
                    continue
                r.url = canon
                r.score = score_result(r)
                collected.append(r)
                seen_urls.add(canon)
                if len(collected) >= self.settings.global_result_cap:
                    break
            if len(collected) >= self.settings.global_result_cap:
                break
        collected.sort(key=lambda x: (-(x.score or 0), x.rank))
        return collected

    def persist(self, domain: str, results: List[SearchResult]) -> Path:
        from .search import get_domain_queries  # local import to avoid cycle on typing
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = Path("apis/_discovery")
        out_dir.mkdir(parents=True, exist_ok=True)
        artifact = DiscoveryArtifact(
            domain=domain,
            generated_at=ts,
            provider=self.provider.name,
            queries_used=get_domain_queries(domain),
            results=results,
        )
        out_file = out_dir / f"{domain}_{ts}.json"
        out_file.write_text(artifact.to_json())
        return out_file


__all__ = [
    "SearchResult",
    "SearchProvider",
    "DummySearchProvider",
    "DiscoveryEngine",
    "canonicalize_url",
]
