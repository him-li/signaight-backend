import logging
from mlflow.exceptions import MlflowException
from mlflow.genai import (
    load_prompt as mlflow_load_prompt,
    register_prompt as mlflow_register_prompt,
    set_prompt_alias as mlflow_set_prompt_alias,
)
from mlflow import set_tracking_uri

from langsearch.config import settings
from langchain_core.prompts import PromptTemplate
from langsearch.graph.prompts import PROMPT_TEMPLATES, PROMPTS_WITH_ITERATIONS


def load_prompt(prompt_name: str, iteration_number: int = 0) -> str:
    mlflow_logger = logging.getLogger("mlflow.prompt_registry")
    mlflow_logger.setLevel(logging.ERROR)
    alias = settings.ENVIRONMENT
    try:
        if settings.MLFLOW_TRACKING_URI:
            set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        if iteration_number > 0:
            # Here we control the prompt version for different iterations
            prompt_name = PROMPTS_WITH_ITERATIONS[prompt_name].get(iteration_number, PROMPTS_WITH_ITERATIONS[prompt_name][0])
        return mlflow_load_prompt(f"prompts:/{prompt_name}@{alias}")
    except MlflowException as e:
        prompt = PROMPT_TEMPLATES[prompt_name]
        mlflow_logger.error(f"Prompt not found: {prompt_name}")
        _register_prompt(prompt_name, prompt, alias)
        return mlflow_load_prompt(f"prompts:/{prompt_name}@{alias}")
    except Exception as e:
        mlflow_logger.error(f"Error loading prompt: {str(e)}")
        return None


def _register_prompt(prompt_name: str, prompt: str, alias: str):
    mlflow_logger = logging.getLogger("mlflow.prompt_registry")
    mlflow_logger.setLevel(logging.ERROR)
    try:
        mlflow_register_prompt(name=prompt_name, template=prompt)
        mlflow_set_prompt_alias(name=prompt_name, alias=alias, version=1)
    except Exception as e:
        mlflow_logger.error(f"Error registering prompt {prompt_name}: {str(e)}")
        return None
