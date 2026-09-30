def set_tweet_post_card(tweet, post_key):
    post_card_key = f'{post_key}.twitter_post_card'
    twitter_post_card = tweet.get(post_card_key, {})

    card_fields = [
        'description_text',
        'image_url_large',
        'image_url_original_size',
        'text'
    ]

    if twitter_post_card:
        for field in card_fields:
            if not twitter_post_card.get(field):
                twitter_post_card[field] = None

        tweet[post_card_key] = twitter_post_card


def set_tweet_post_photo(tweet, post_key):
    post_photo_key = f'{post_key}twitter_post_photo'
    twitter_post_photo = tweet.get(post_photo_key, [])

    if twitter_post_photo:
        photo_list = []
        for photo in tweet.get(post_photo_key):
            photo = {'post_photo': photo}
            photo_list.append(photo)
        return photo_list
