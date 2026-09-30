from core.models.visuals import Visuals


def get_cover_photos(visuals: Visuals):
    cover_photos = []
    if fb_cover := visuals.fb_cover_photo:
        cover_photos.append(str(fb_cover))
    if profile_photo := visuals.profile_photo:
        if twitter_cover := profile_photo.twitter_cover_photo:
            cover_photos.append(str(twitter_cover))
    return cover_photos


def get_cover_photos_ds_app(visuals: Visuals):
    cover_photos = []
    cover_photo_keys = [
        'background_image',
        'fb_cover_photo',
        'twitter_cover_photo',
        'linkedin_cover_photo'
    ]
    try:
        for key, value in visuals.model_dump().items():
            if key in cover_photo_keys and value:
                cover_photos.append(
                    {"hash": str(value), "source": str(value)})
    except Exception as e:
        print(f"Error getting cover photos: {e}")

    return cover_photos


def get_profile_photos_ds_app(visuals: Visuals):
    profile_photos = []
    try:
        if profile_photo := visuals.profile_photo:
            for key, photo in profile_photo.model_dump().items():
                if photo:
                    profile_photos.append(
                        {"hash": str(key), "source": str(photo)})
    except Exception as e:
        print(f"Error getting profile photos: {e}")
    return profile_photos
