import json
from langchain_core.messages import ToolMessage
from datetime import datetime
from bs4 import BeautifulSoup
import re

def normalize_google_result(google_result: dict) -> dict:
    """Normalize a Google search result dictionary.

    This function ensures that the result dictionary has consistent keys and formats.
    It can be extended to include more normalization rules as needed.

    Args:
        result (dict): The original Google search result.

    Returns:
        dict: The normalized Google search result.
    """
    

    normalized_result = {
        item["url"]: {k: v for k, v in item.items() if k != "url"} for item in list(google_result.values()) if check_urls_valid(item)
    }
    return normalized_result

def normalize_linkedin_result(social_media_result: dict) -> dict:
    """Normalize a LinkedIn search result dictionary.

    This function ensures that the result dictionary has consistent keys and formats.
    It can be extended to include more normalization rules as needed.
    """
    normalized_result = {
        result.get("network_signature", {})
        .get("url", {})
        .get("linkedin_profile_url")[0]: {
            "url": result.get("network_signature", {})
            .get("url", {})
            .get("linkedin_profile_url")[0],
            "content": result,
            "images": [
                result.get("personal_details", {})
                .get("visuals", {})
                .get("profile_photo", {})
                .get("linkedin_profile_picture")
            ],
        }
        for result in social_media_result
    }

    return normalized_result

def normalize_facebook_result(social_media_result: dict) -> dict:
    """Normalize a Facebook search result dictionary.

    This function ensures that the result dictionary has consistent keys and formats.
    It can be extended to include more normalization rules as needed.
    """
    normalized_result = {
        result.get("network_signature", {})
        .get("url", {})
        .get("facebook_profile_url")[0]: {
            "url": result.get("network_signature", {})
            .get("url", {})
            .get("facebook_profile_url")[0],
            "content": result,
            "images": [
                result.get("personal_details", {})
                .get("visuals", {})
                .get("profile_photo", {})
                .get("facebook_profile_picture")
            ],
        }
        for result in social_media_result
    }
    return normalized_result

def normalize_instagram_result(social_media_result: dict) -> dict:
    """Normalize a Instagram search result dictionary.

    This function ensures that the result dictionary has consistent keys and formats.
    It can be extended to include more normalization rules as needed.
    """
    normalized_result = {
        result.get("network_signature", {})
        .get("url", {})
        .get("instagram_profile_url")[0]: {
            "url": result.get("network_signature", {})
            .get("url", {})
            .get("instagram_profile_url")[0],
            "content": result,
            "images": [
                result.get("personal_details", {})
                .get("visuals", {})
                .get("profile_photo", {})
                .get("instagram_profile_picture")
            ],
        }
        for result in social_media_result
    }
    return normalized_result

def normalize_result(social_media_result: dict, source: str) -> dict:
    """Normalize a result dictionary.

    This function ensures that the result dictionary has consistent keys and formats.
    It can be extended to include more normalization rules as needed.
    """
    match source:
        case 'google':
            return normalize_google_result(social_media_result)
        case 'linkedin':
            return normalize_linkedin_result(social_media_result)
        case 'facebook':
            return normalize_facebook_result(social_media_result)
        case 'instagram':
            return normalize_instagram_result(social_media_result)
        case _:
            raise ValueError(f"Invalid source: {source}")

def check_urls_valid(input_dict):

    if (input_dict["status_code"] == 200
                # add some more logic here as needed
            ):
        return True
    return False

def extract_body_content(response_content: str) -> str:
    """Extract content from body tag only"""
    # soup = BeautifulSoup(response_content, 'html.parser')
    # try:
    #     text = soup.getText()
    #     return text
    # except Exception as e:
    #     return response_content
    soup = BeautifulSoup(response_content, 'html.parser')
    body = soup.find('body')
    if body:
        # Remove script and style elements
        for script in body(["script", "style"]):
            script.decompose()

        # Get text content
        text = body.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()
    else:
        return ""
