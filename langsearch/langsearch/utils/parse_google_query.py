import urllib.parse as up

def extract_google_query(url: str) -> str:
    parsed = up.urlparse(url)
    params = up.parse_qs(parsed.query)
    return params.get("q", [""])[0]