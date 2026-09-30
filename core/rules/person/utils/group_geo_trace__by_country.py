from collections import defaultdict

def get_place_name(item) -> str:
    props = (item or {}).get("properties", {})
    return (props.get("place_name") or "").strip()

def extract_country(place_name: str) -> str:
    if not place_name:
        return None
    parts = [p.strip() for p in place_name.split(",") if p.strip()]
    return parts[-1] if parts else None

def group_by_country(items):
    grouped = defaultdict(list)
    for it in items:
        if not isinstance(it, dict):
            it = it.dict()
            country = extract_country(get_place_name(it)) or None
            if country is not None:
                grouped[country].append(it)
    return dict(grouped)
