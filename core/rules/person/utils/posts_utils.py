from typing import List

from core.models.post import Post


def build_post_photo_list(posts: List[Post], activity_type: str = "post"):
    photo_list = []
    for post in posts:
        if post.activity_type == activity_type:
            try:
                _ = (photo_list.append(
                    str(post.fb_post_photo.fb_photo.url))
                    if getattr(post, "fb_post_photo") else None)
            except Exception:
                pass
            try:
                _ = (photo_list.append(
                    str(post.fb_uploaded_photo.fb_photo.url))
                    if getattr(post, "fb_uploaded_photo") else None)
            except Exception:
                pass
            try:
                _ = (photo_list.append(str(post.instagram_post_photo))
                     if post.instagram_post_photo else None)
            except Exception:
                pass

    if len(photo_list) > 0:
        photo_list = [{"hash": url, "source": url} for url in photo_list]

    return photo_list


def build_post_photo_text_list(posts: List[Post], activity_type: str = "post"):
    posts_list = []
    posts_detected = []
    try:
        for post in posts:
            if post.activity_type == activity_type:
                source = None
                try:
                    source = (str(post.fb_post_photo.fb_photo.url)
                              if getattr(post, "fb_post_photo") else source)
                except Exception:
                    pass
                try:
                    source = (str(post.twitter_post_photo[0].post_photo)
                              if getattr(post, "twitter_post_photo") else source)
                except Exception:
                    pass
                try:
                    source = (str(post.linkedin_post_photo)
                              if getattr(post, "linkedin_post_photo") else source)
                except Exception:
                    pass
                try:
                    source = (str(post.linkedin_post_photo)
                              if getattr(post, "linkedin_post_photo") else source)
                except Exception:
                    pass
                try:
                    source = (str(post.instagram_post_photo)
                              if getattr(post, "instagram_post_photo") else source)
                except Exception:
                    pass
                try:
                    source = (str(post.fb_uploaded_photo.fb_photo.url)
                              if getattr(post, "fb_uploaded_photo") else source)
                except Exception:
                    pass


                text = (post.fb_post_text if getattr(post, "fb_post_text") else
                        post.linkedin_post_text if getattr(post,
                                                           "linkedin_post_text")
                        else post.twitter_post_text if getattr(
                            post,
                    "twitter_post_text") else
                    post.instagram_post_text if getattr(post,
                                                        "instagram_post_text")
                    else "")

                if text or source:
                    posts_list.append(
                        {"hash": str(post), "source": source if source else "", "text": text})
                    posts_detected.append(post)
    except Exception:
        pass

    return {'posts_list': posts_list, 'posts_detected': posts_detected}

def build_post_photo_text_list_extremism(posts: List[Post], activity_type: str = "post"):
    posts_list = []
    posts_detected = []
    try:
        for post in posts:
            if post.activity_type == activity_type:
                source = None
                try:
                    source = (str(post.fb_post_photo.fb_photo.url)
                              if getattr(post, "fb_post_photo") else source)
                except Exception:
                    pass
                try:
                    source = (str(post.twitter_post_photo[0].post_photo)
                              if getattr(post, "twitter_post_photo") else source)
                except Exception:
                    pass

                try:
                    source = (str(post.linkedin_post_photo)
                              if getattr(post, "linkedin_post_photo") else source)
                except Exception:
                    pass
                try:
                    source = (str(post.instagram_post_photo)
                              if getattr(post, "instagram_post_photo") else source)
                except Exception:
                    pass

                try:
                    source = (str(post.fb_uploaded_photo.fb_photo.url)
                              if getattr(post, "fb_uploaded_photo") else source)
                except Exception:
                    pass

                text = (post.fb_post_text if getattr(post, "fb_post_text") else
                        post.linkedin_post_text if getattr(post,
                                                           "linkedin_post_text")
                        else post.twitter_post_text if getattr(
                            post,
                    "twitter_post_text") else
                    post.instagram_post_text if getattr(post,
                                                        "instagram_post_text")
                    else "")

                if text or source:
                    posts_list.append(
                        {"hash": str(post), "source": source, "text": text})
                    posts_detected.append(post)
    except Exception:
        pass

    return {'posts_list': posts_list, 'posts_detected': posts_detected}

def build_post_photo_text_list_for_weapons(posts: List[Post], activity_type: str = "post"):
    posts_list = []
    posts_detected = []
    try:
        for post in posts:
            if post.activity_type == activity_type:
                source = None
                try:
                    source = (str(post.fb_post_photo.fb_photo.url)
                              if getattr(post, "fb_post_photo") else source)
                except Exception:
                    pass
                try:
                    source = (str(post.twitter_post_photo[0].post_photo)
                              if getattr(post, "twitter_post_photo") else source)
                except Exception:
                    pass

                try:
                    source = (str(post.linkedin_post_photo)
                              if getattr(post, "linkedin_post_photo") else source)
                except Exception:
                    pass
                try:
                    source = (str(post.instagram_post_photo)
                              if getattr(post, "instagram_post_photo") else source)
                except Exception:
                    pass
          
                try:
                    source = (str(post.fb_uploaded_photo.fb_photo.url)
                              if getattr(post, "fb_uploaded_photo") else source)
                except Exception:
                    pass


                if source:
                    posts_list.append(
                        {"hash": str(source), "source": source, "text": ""})
                    posts_detected.append(post)
    except Exception:
        pass
    return {'posts_list': posts_list, 'posts_detected': posts_detected}


def build_post_text_list(posts: List[Post], activity_type: str = "post"):
    text_list = []
    for post in posts:
        if post.activity_type == activity_type:
            try:
                _ = (text_list.append(post.fb_post_text)
                     if getattr(post, "fb_post_text") else None)
            except Exception:
                pass
            try:
                _ = (text_list.append(
                    post.linkedin_post_text)
                    if getattr(post, "linkedin_post_text") else None)
            except Exception:
                pass
            try:
                _ = (text_list.append(post.twitter_post_text)
                     if post.twitter_post_text else None)
            except Exception:
                pass
            try:
                _ = (text_list.append(post.instagram_post_text)
                     if post.instagram_post_text else None)
            except Exception:
                pass

    if len(text_list) > 0:
        text_list = [{"hash": url, "text": url} for url in text_list]

    return text_list
