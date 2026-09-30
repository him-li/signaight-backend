from core.models.utils import dedupe_posts
from core.models.post import Post


def test_no_duplicates_returns_same_list():
    posts = [
        Post(instagram_post_id="1"),
        Post(instagram_post_id="2"),
        Post(twitter_post_id="t1"),
        Post(linkedin_post_url="https://a.com"),
    ]
    post_dicts = [p.model_dump() for p in posts]
    result = dedupe_posts(post_dicts)
    assert len(result) == len(post_dicts)


def test_instagram_duplicates_are_removed():
    p1 = Post(instagram_post_id="dup")
    p2 = Post(instagram_post_id="dup")
    p3 = Post(instagram_post_id="unique")
    posts = [p1, p2, p3, p1]
    post_dicts = [p.model_dump() for p in posts]
    result = dedupe_posts(post_dicts)
    assert len(result) == 2


def test_linkedin_duplicates_are_removed():
    p1 = Post(linkedin_post_url="https://linkedin.com/p/1")
    p2 = Post(linkedin_post_url="https://linkedin.com/p/1")
    p3 = Post(linkedin_post_url="https://linkedin.com/p/2")
    posts = [p1, p2, p3, p1]
    post_dicts = [p.model_dump() for p in posts]
    result = dedupe_posts(post_dicts)
    assert len(result) == 2


def test_mixed_platforms():
    i1 = Post(instagram_post_id="insta1")
    i2 = Post(instagram_post_id="insta1")
    fb1 = Post(fb_post_text="hi")
    fb2 = Post(fb_post_text="hi")
    combined = [i1, fb1, i2, fb2]
    combined_dicts = [p.model_dump() for p in combined]
    result = dedupe_posts(combined_dicts)
    assert len(result) == 2
