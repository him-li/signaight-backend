"""Lazy public exports for search flows.

Importing a utility submodule must not initialize every external-provider flow.
"""

from importlib import import_module
from typing import Any


_FLOW_MODULES = {
    "complex_search_flow": ".complex_search",
    "facebook_instagram_search_flow": ".facebook_instagram_search",
    "facebook_search_enrich_flow": ".facebook_search_enrich",
    "instagram_search_enrich_flow": ".instagram_search_enrich",
    "facebook_enrich_flow": ".facebook_enrich",
    "instagram_enrich_flow": ".instagram_enrich",
    "aggregation_flow": ".aggregation",
    "twitter_search_enrich_flow": ".twitter_search_enrich",
    "twitter_enrich_flow": ".twitter_enrich",
    "linkedin_enrich_flow": ".linkedin_enrich",
    "xing_enrich_flow": ".xing_enrich",
    "active_search_flow": ".active_search",
}

__all__ = list(_FLOW_MODULES)


def __getattr__(name: str) -> Any:
    module_name = _FLOW_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(module_name, __name__), name)
    globals()[name] = value
    return value
