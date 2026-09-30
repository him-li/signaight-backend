from core.config import Settings as BaseSettings


class ExecutorSettings(
        BaseSettings):
    REDUCER_SEARCH_RESULTS_PER_SOURCE_LIMIT: int = 100


settings = ExecutorSettings()
