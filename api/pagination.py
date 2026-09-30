from __future__ import annotations

from typing import Any, Generic, Optional, Sequence, TypeVar
from fastapi_pagination import Params
from fastapi_pagination.ext.beanie import paginate  # noqa
from fastapi_pagination.bases import BasePage, AbstractParams
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero
from math import ceil

T = TypeVar("T")


class Page(BasePage[T], Generic[T]):
    page: Optional[GreaterEqualOne] = 0
    size: Optional[GreaterEqualOne] = 10
    pages: Optional[GreaterEqualZero] = 0

    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        *,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> Page[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        pages = ceil(total / params.size) if total is not None else None

        return cls(
            total=total,  # type: ignore[arg-type]
            items=items,
            page=params.page,
            size=params.size,
            pages=pages,
            **kwargs,
        )
