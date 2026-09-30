from urllib.parse import urlparse


def extract_instagram_username(url: str) -> str:
    """
    Extracts the Instagram username from a profile URL.
    Example: https://www.instagram.com/natgeoscience -> 'natgeoscience'
    """
    path = urlparse(url).path.strip(
        "/")   # get the path part, e.g. '/natgeoscience/'
    return path.split("/")[0] if path else ""
