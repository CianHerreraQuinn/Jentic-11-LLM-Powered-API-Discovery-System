from pathlib import Path
from modules.discovery import DiscoveryEngine, DummySearchProvider


def test_discovery_engine_dummy():
    engine = DiscoveryEngine(provider=DummySearchProvider())
    results = engine.discover("weather")
    # Ensure non-empty and within configured caps
    assert 0 < len(results) <= engine.settings.global_result_cap
    # Scores should be assigned
    assert all(r.score is not None for r in results)
    # Sorted by score descending
    scores = [float(r.score) for r in results if r.score is not None]
    assert scores == sorted(scores, reverse=True)

    # Persist and verify file exists
    out_path = engine.persist("weather", results)
    assert out_path.exists()
    data = out_path.read_text()
    assert '"domain": "weather"' in data
