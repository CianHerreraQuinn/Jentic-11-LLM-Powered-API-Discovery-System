"""Configuration loader for the API Discovery System.

Centralizes reading of YAML-based settings so that modules do not hard-code
paths or magic numbers. Keeps a thin cached layer to avoid repeated disk I/O.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import yaml

DEFAULT_CONFIG_PATH = Path("configs/settings.yaml")


class ConfigError(Exception):
    """Raised when configuration cannot be loaded or is invalid."""


@dataclass(slots=True)
class SearchConfig:
    default_query_limit: int
    domains_base_dir: Path
    queries_filename: str
    allow_duplicates: bool = False
    max_results_per_query: int = 5
    global_result_cap: int = 15
    allowed_domain_keywords: tuple[str, ...] = ()
    blocked_domain_keywords: tuple[str, ...] = ()


class Settings:
    """Container for all top-level configuration sections."""

    def __init__(self, raw: Dict[str, Any]):
        self._raw = raw
        search_section = raw.get("search") or {}
        try:
            self.search = SearchConfig(
                default_query_limit=int(search_section.get("default_query_limit", 5)),
                domains_base_dir=Path(search_section.get("domains_base_dir", "domains")),
                queries_filename=str(search_section.get("queries_filename", "queries.yaml")),
                allow_duplicates=bool(search_section.get("allow_duplicates", False)),
                max_results_per_query=int(search_section.get("max_results_per_query", 5)),
                global_result_cap=int(search_section.get("global_result_cap", 15)),
                allowed_domain_keywords=tuple(search_section.get("allowed_domain_keywords", [])),
                blocked_domain_keywords=tuple(search_section.get("blocked_domain_keywords", [])),
            )
        except (TypeError, ValueError) as e:  # pragma: no cover - defensive
            raise ConfigError(f"Invalid search configuration: {e}") from e

    @property
    def raw(self) -> Dict[str, Any]:  # pragma: no cover - simple accessor
        return self._raw


_CACHED_SETTINGS: Settings | None = None


def load_settings(path: Path | None = None, force_reload: bool = False) -> Settings:
    """Load settings from YAML (cached by default).

    Parameters
    ----------
    path: optional Path to override default config file.
    force_reload: bypass cache if True.
    """
    global _CACHED_SETTINGS
    cfg_path = path or DEFAULT_CONFIG_PATH
    if _CACHED_SETTINGS is not None and not force_reload:
        return _CACHED_SETTINGS
    if not cfg_path.exists():
        raise ConfigError(f"Config file not found: {cfg_path}")
    try:
        data = yaml.safe_load(cfg_path.read_text()) or {}
    except yaml.YAMLError as e:  # pragma: no cover - unlikely unless malformed
        raise ConfigError(f"Invalid YAML in config {cfg_path}: {e}") from e
    _CACHED_SETTINGS = Settings(data)
    return _CACHED_SETTINGS


__all__ = [
    "ConfigError",
    "SearchConfig",
    "Settings",
    "load_settings",
]
