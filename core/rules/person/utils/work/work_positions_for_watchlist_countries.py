from typing import Any, Dict, List, Optional, Union

from core.models.person import Person
from core.models.position import Position

def create_position_model_list_tagged(person: Person) -> List[Dict[str, Any]]:
    def _stringify_urls(p: Position) -> Position:
        # Make URL-like fields strings (or None) if they exist on the model
        try:
            if hasattr(p, "company_logo_url"):
                p.company_logo_url = str(p.company_logo_url) if getattr(p, "company_logo_url") else None
            if hasattr(p, "linkedin_company_url"):
                p.linkedin_company_url = str(p.linkedin_company_url) if getattr(p, "linkedin_company_url") else None
            if hasattr(p, "xing_company_url"):
                p.xing_company_url = str(p.xing_company_url) if getattr(p, "xing_company_url") else None
        except Exception:
            pass
        return p
    
    def _extract_location(p: "Position") -> Optional[str]:
        try:
            if hasattr(p, "location") and p.location:
                return str(p.location)
        except Exception:
            pass
        return None

    def _coerce_fb_to_position(item: Union[dict, Any]) -> Optional[Position]:
        """
        Accepts either a Position-like object with fb_* attrs or a dict with fb_* keys.
        Produces a Position with {company_name, title, period, location} filled from fb_*.
        """
        try:
            # Extract via getattr or dict access
            get = (lambda k: item.get(k)) if isinstance(item, dict) else (lambda k: getattr(item, k, None))
            base = item.model_dump() if hasattr(item, "model_dump") else (dict(item) if isinstance(item, dict) else {})
            base["company_name"] = base.get("company_name") or get("fb_workplace_name")
            base["title"] = base.get("title") or get("fb_work_title")
            base["period"] = base.get("period") or get("fb_work_period")
            base["location"] = base.get("location") or get("fb_workplace_location")

            # If nothing meaningful, skip
            if not (base.get("company_name") or base.get("title") or base.get("period")):
                return None

            p = Position(**base)
            return _stringify_urls(p)
        except Exception:
            return None

    def _coerce_any_to_position(item: Union[Position, dict, Any]) -> Optional[Position]:
        """
        If it's already a Position, return (after url normalize). If dict/pydantic-like, try Position(**dict).
        """
        try:
            if isinstance(item, Position):
                return _stringify_urls(item)
            # Pydantic-like with model_dump
            if hasattr(item, "model_dump"):
                p = Position(**item.model_dump())
                return _stringify_urls(p)
            if isinstance(item, dict):
                p = Position(**item)
                return _stringify_urls(p)
        except Exception:
            return None
        return None

    tagged: List[Dict[str, Any]] = []

    # --- LinkedIn ---
    try:
        li = getattr(getattr(person.biographic_details, "work", None), "linkedin_work", None)
        if li and hasattr(li, "positions") and isinstance(li.positions, list):
            for it in li.positions:
                p = _coerce_any_to_position(it)
                if p:
                    tagged.append({"position": p, "platform": "linkedin", "location": _extract_location(p)})
    except Exception:
        pass

    # --- Xing ---
    try:
        xing = getattr(getattr(person.biographic_details, "work", None), "xing_work", None)
        if xing and hasattr(xing, "positions") and isinstance(xing.positions, list):
            for it in xing.positions:
                p = _coerce_any_to_position(it)
                if p:
                    tagged.append({"position": p, "platform": "xing", "location": _extract_location(p)})
    except Exception:
        pass

    # --- Facebook ---
    try:
        fb_list = getattr(getattr(person.biographic_details, "work", None), "facebook_work", None)
        if fb_list and isinstance(fb_list, list):
            for it in fb_list:
                # FB may come as raw items with fb_* fields
                p = _coerce_fb_to_position(it)
                if p:
                    tagged.append({"position": p, "platform": "facebook", "location": _extract_location(p)})
    except Exception:
        pass

    # Sort by period.date_from desc, best-effort
    try:
        def _df(t: Dict[str, Any]):
            p = t.get("position")
            return getattr(getattr(p, "period", None), "date_from", None)
        tagged.sort(key=_df, reverse=True)
    except Exception:
        pass

    return tagged
