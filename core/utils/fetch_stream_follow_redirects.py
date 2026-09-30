import httpx
from io import BytesIO

from typing import Optional

REDIRECT_STATUSES = {301, 302, 303, 307, 308}

def download_follow_redirects_streaming(
    url: str,
    headers: dict,
    logger,
    max_redirects: int = 5,
) -> tuple[Optional[bytes], Optional[str], Optional[str]]:
    with httpx.Client(follow_redirects=False, timeout=30.0) as http_client:
        current_url = url
        for _ in range(max_redirects + 1):
            # Open a NEW streaming context for each hop
            with http_client.stream("GET", current_url, headers=headers) as resp:
                status = resp.status_code
                # Handle redirect (DON'T read body; just follow)
                if status in REDIRECT_STATUSES and resp.headers.get("Location"):
                    target = str(httpx.URL(current_url).join(resp.headers["Location"]))
                    logger.info(f"Redirect {status} → {target}")
                    # leave this 'with' (closing the stream), then loop with new URL
                    current_url = target
                    continue

                # Non-redirect: validate and stream body
                if status not in (200, 202, 206):
                    logger.warning(f"Unexpected status {status} for {current_url}")
                    return None, current_url, resp.headers.get("content-type")

                buf = BytesIO()
                for chunk in resp.iter_bytes():
                    buf.write(chunk)
                return buf.getvalue(), current_url, resp.headers.get("content-type")

        raise httpx.TooManyRedirects(f"Exceeded {max_redirects} redirects")

