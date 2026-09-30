from typing import List, Optional

from core.models import PersonModel
from core.models.post import Post


def merge_posts(persons: List[PersonModel]) -> Optional[List[Post]]:
    posts = []
    for p in persons:
        if p.posts:
            posts.extend(p.posts)
    return posts or None
