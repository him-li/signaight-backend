"""Define the configurable parameters for the agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated, Any

from langsearch.models.search_input import SearchInput

@dataclass(kw_only=True)
class Context:
    """The context for the agent."""

    person_str_json: str = field(
        default="",
        metadata={
            "description": "The person object as string (generated using json.dumps)"
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="google_genai/gemini-2.5-pro",
        metadata={
            "description": "The name of the language model to use for the agent's main interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    max_search_results: int = field(
        default=10,
        metadata={
            "description": "The maximum number of search results to return for each search query."
        },
    )

    iteration_number: int = field(
        default=0,
        metadata={
            "description": "The number of the iteration of the graph. "
            "This is used to track the number of the iteration of the graph."
        },
    )

    match_options: list[str] = field(
        default_factory=list,
        metadata={
            "description": "The positive match options for the graph. "
            "This is used to track the positive match options for the graph."
        },
    )

    reuse_match_options: list[str] = field(
        default_factory=list,
        metadata={
            "description": "The reuse match options for the graph. "
            "This is used to track the which match options to reuse for the graph."
        },
    )

    system_prompt: Any = field(
        default=None,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )

    google_match_prompt: Any = field(
        default=None,
        metadata={
            "description": "The system will ask the LLM if the url and content are related to the person"
            "This prompt sets the context and behavior for the agent."
        },
    )

    url_details_prompt: Any = field(
        default=None,
        metadata={
            "description": "The system will ask the LLM to extract Url details from the content"
            "This prompt sets the context and behavior for the agent."
        },
    )

    sm_match_prompt: Any = field(
        default=None,
        metadata={
            "description": "The system will ask the LLM to match Social Media profile data with the person information"
            "This prompt sets the context and behavior for matching Social Media profiles."
        },
    )

    person_search_query_prompt: Any = field(
        default=None,
        metadata={
            "description": "The system will ask the LLM to generate search queries to find the person"
            "This prompt sets the context and behavior for generating search queries."
        },
    )

    person_social_media_search_query_prompt: Any = field(
        default=None,
        metadata={
            "description": "The system will ask the LLM to generate search queries to find the person's Social Media profile"
            "This prompt sets the context and behavior for generating search queries."
        },
    )

    structured_extraction_prompt: str = field(
        default=None,
        metadata={
            "description": "The system will ask the LLM to extract structured data from content"
            "This prompt instructs the LLM to return structured output matching the ExtractedCandidate model."
        },
    )

    
    def __post_init__(self) -> None:
        """Fetch env vars for attributes that were not passed as args."""
        for f in fields(self):
            if not f.init:
                continue

            current_value = getattr(self, f.name)
            try:
                # First try identity check (fastest, works if same object)
                if current_value is f.default:
                    is_default = True
                else:
                    # Try normal equality comparison
                    is_default = current_value == f.default
            except (TypeError, AttributeError, ValueError):
                # If comparison fails (e.g., MLflow-wrapped object vs string),
                # fall back to string comparison
                try:
                    is_default = str(current_value) == str(f.default)
                except Exception:
                    # Last resort: assume not default if we can't compare
                    is_default = False
            
            if is_default:
                setattr(self, f.name, os.environ.get(f.name.upper(), f.default))
