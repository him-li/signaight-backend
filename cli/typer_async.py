from typer import Typer, Argument, Option
from asyncio import run
from functools import wraps


class AsyncTyper(Typer):
    def async_command(self, *args, **kwargs):
        def decorator(async_func):
            @wraps(async_func)
            def sync_func(*_args, **_kwargs):
                return run(async_func(*_args, **_kwargs))

            self.command(*args, **kwargs)(sync_func)
            return async_func

        return decorator


__all__ = [
    "AsyncTyper",
    "Argument",
    "Option",
]
