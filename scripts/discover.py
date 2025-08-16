#!/usr/bin/env python
"""CLI script to run Module 2 discovery using the dummy provider.

Usage:
  python scripts/discover.py weather
"""
from __future__ import annotations

import sys
from modules.discovery import DiscoveryEngine


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python scripts/discover.py <domain>")
        return 1
    domain = argv[1]
    engine = DiscoveryEngine()
    results = engine.discover(domain)
    path = engine.persist(domain, results)
    print(f"Discovered {len(results)} results for domain '{domain}'.")
    for r in results:
        print(f"- {r.score:4.1f} {r.title} -> {r.url}")
    print(f"Artifact written: {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover - manual invocation
    raise SystemExit(main(sys.argv))
