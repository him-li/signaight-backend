from typing import Any, List, Optional

from pydantic import BaseModel
from core.models.flags import Flag, FlagSubCategory


def _as_dict(obj: Any) -> dict:
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    return obj.__dict__


def _get_float(x: Any, default: float = 0.0) -> float:
    if x is None:
        return default
    if isinstance(x, tuple) and len(x) == 1:  # guard for (5.0,) bug
        x = x[0]
    return float(x)


def _subcat_key(sc: Any) -> Optional[str]:
    return _as_dict(sc).get("sub_category")


def update_person_flag(
    self_key,
    sub_categories: List[FlagSubCategory],
    category: str,
    description,
    sub_category_to_delete:str = '',
    max_value: float = 10,
):
    try:
        key_dict = (
            self_key.model_dump() if not isinstance(self_key, dict) else dict(self_key)
        )
        existing_list = list(key_dict.get("sub_categories") or [])

        if sub_category_to_delete:
            existing_list = [
                sc for sc in existing_list
                if _subcat_key(sc) != sub_category_to_delete
            ]
            
        idx = {_subcat_key(sc): i for i, sc in enumerate(existing_list)}
        

        for sc_new in sub_categories:
            new_d = _as_dict(sc_new)
            name = new_d.get("sub_category")
            if name in idx:  # replace existing
                existing_list[idx[name]] = sc_new  # replace (or merge here if you want)
            else:  # brand-new subcategory
                existing_list.append(sc_new)
                idx[name] = len(existing_list) - 1

        total = sum(
            _get_float(_as_dict(sc).get("severity"), 0.0) for sc in existing_list
        )
        total = max(0.0, min(total, max_value))

        self_key = {
            "severity": total,
            "category": category,
            "sub_categories": existing_list,
            "description": description,
        }

    except AttributeError:
        total = sum(
            _get_float(_as_dict(sc).get("severity"), 0.0) for sc in sub_categories
        )
        total = max(0.0, min(total, max_value))

        self_key = {
            "severity": total,
            "category": category,
            "sub_categories": sub_categories,
            "description": description,
        }

    if total >= 0.01:
        return Flag(**self_key)
