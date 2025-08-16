import pytest
from modules.search import (
    DomainQueryLoader,
    get_domain_queries,
    QuerySourceError,
)
from pathlib import Path


def test_domain_query_loader_happy_path():
    queries = DomainQueryLoader(domain="weather").get_queries(limit=5)
    assert len(queries) == 5
    # Ensure order preserved and non-empty
    assert queries[0].startswith("weather API")
    # Unique check
    assert len(set(q.lower() for q in queries)) == 5


def test_limit_enforced():
    queries = get_domain_queries("weather", limit=3)
    assert len(queries) == 3


def test_missing_file_raises(tmp_path: Path):
    # Point loader to temp base_dir without queries file
    loader = DomainQueryLoader(domain="unknown", base_dir=tmp_path)
    with pytest.raises(QuerySourceError):
        loader.get_queries()


def test_invalid_yaml_raises(tmp_path: Path):
    d = tmp_path / "weather"
    d.mkdir(parents=True)
    bad_file = d / "queries.yaml"
    bad_file.write_text("::not yaml::")
    loader = DomainQueryLoader(domain="weather", base_dir=tmp_path)
    with pytest.raises(QuerySourceError):
        loader.get_queries()


def test_empty_queries_raises(tmp_path: Path):
    d = tmp_path / "weather"
    d.mkdir(parents=True)
    (d / "queries.yaml").write_text("queries: []\n")
    loader = DomainQueryLoader(domain="weather", base_dir=tmp_path)
    with pytest.raises(QuerySourceError):
        loader.get_queries()
