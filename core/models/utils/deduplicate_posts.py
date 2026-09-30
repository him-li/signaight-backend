from typing import List, Dict

from core.dotty_dictionary import dotty
from core.logging import logger


def dedupe_posts(posts: List[Dict]):
    try:
        if not posts:
            return []
        seen = {}
        result = []
        for post in posts:
            post = dotty(post)
            if post.get("instagram_post_id"):
                key = ("insta", post.get("instagram_post_id"))
            elif post.get("fb_post_text"):
                key = ("fb", post.get("fb_post_text").strip())
            elif post.get("fb_post_id"):
                key = ("fb", post.get("fb_post_id"))
            elif post.get("fb_uploaded_photo.fb_photo_id"):
                key = ("fb", post.get("fb_uploaded_photo.fb_photo_id"))
            elif post.get("linkedin_post_url"):
                key = ("linkedin", post.get("linkedin_post_url"))
            elif post.get("twitter_post_id"):
                key = ("twitter", post.get("twitter_post_id"))
            else:
                key = ("raw", str(post))

            if key not in seen:
                seen[key] = True
                result.append(post.to_dict())
        return result
    except Exception as e:
        logger.error(f"Error in deduplicate posts: {e}")
        return posts
