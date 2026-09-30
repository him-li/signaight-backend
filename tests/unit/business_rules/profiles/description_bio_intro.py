# flake8: noqa
import pytest


@pytest.fixture
def profile_with_international_travel_intro():
    return {
        "biographic_details": {
            'description_bio_intro': {
                'introduction': "traveler",
                'linkedin_headline': "🌐",
                'instagram_bio': "🛴",
                'twitter_description': {
                    'description_text': "🛳️🗺️"
                }
            }
        }
    }


@pytest.fixture
def profile_with_international_travel_intro_only_emojis():
    return {
        "biographic_details": {
            'description_bio_intro': {
                'linkedin_headline': "🌐",
                'instagram_bio': "🛴",
                'twitter_description': {
                    'description_text': "🛳️🗺️"
                }
            }
        }
    }


@pytest.fixture
def profile_with_description_bio_intro_empty():
    return {
        "biographic_details": {
            'description_bio_intro': {
            }
        }
    }


@pytest.fixture
def profile_with_foodie_intro():
    return {
        "biographic_details": {
            'description_bio_intro': {
                "instagram_bio": "foodie",
                "xing_profile_about_me": "Sink your teeth into a juicy burger! 🍔 Loaded with your favorite toppings, it's the perfect comfort food.",
                "google_bio": "Refresh with a colorful fruit salad. 🍓🍇🍍 Packed with vitamins and a burst of flavor in every bite!",
                "twitter_description": {
                    "description_text": "🍕🍔🍣",
                },
                "fb_profile_intro": {
                    "fb_profile_intro_text": "Craving some fresh, delicious sushi? 🍣 Let's roll with it! Maki or nigiri, there's no wrong choice!",
                }
            }
        }
    }


@pytest.fixture
def profile_with_no_foodie_intro():
    return {
        "biographic_details": {
            'description_bio_intro': {
                "instagram_bio": "adventurer",
                "xing_profile_about_me": "Passionate about traveling and capturing moments! 📷 Life is an adventure!",
                "google_bio": "Discovering new places and experiences. 🗺️ The world is full of wonders!",
                "twitter_description": {
                    "description_text": "🌍🗺️📷",
                },
                "fb_profile_intro": {
                    "fb_profile_intro_text": "Exploring the world, one adventure at a time! 🌍 Let's make memories and discover new horizons!",
                }
            }
        }
    }


@pytest.fixture
def profile_with_jihadist_intro():
    return {
        "biographic_details": {
            'description_bio_intro': {
                "instagram_bio": "أنغماسي",
                "xing_profile_about_me": "Sink your teeth into a juicy burger! 🍔 Loaded with your favorite toppings, it's the perfect comfort food.",
                "google_bio": "Refresh with a colorful fruit salad. 🍓🍇🍍 Packed with vitamins and a burst of flavor in every bite!",
                "twitter_description": {
                    "description_text": "🍕🍔🍣",
                },
                "fb_profile_intro": {
                    "fb_profile_intro_text": "Craving some fresh, delicious sushi? 🍣 Let's roll with it! Maki or nigiri, there's no wrong choice!",
                }
            }
        }
    }


@pytest.fixture
def profile_with_salafist_intro():
    return {
        "biographic_details": {
            'description_bio_intro': {
                "instagram_bio": "adventurer",
                "xing_profile_about_me": "Passionate about traveling and capturing moments! 📷 Life is an adventure!",
                "google_bio": "Discovering new places and experiences. 🗺️ The world is full of wonders!",
                "twitter_description": {
                    "description_text": "بدعة",
                },
                "fb_profile_intro": {
                    "fb_profile_intro_text": "Exploring the world, one adventure at a time! 🌍 Let's make memories and discover new horizons!",
                }
            }
        }
    }


@pytest.fixture
def profile_with_jihadist_intro_non_arabic_term():
    return {
        "biographic_details": {
            'description_bio_intro': {
                "instagram_bio": "Inghimasi",
                "xing_profile_about_me": "Sink your teeth into a juicy burger! 🍔 Loaded with your favorite toppings, it's the perfect comfort food.",
                "google_bio": "Refresh with a colorful fruit salad. 🍓🍇🍍 Packed with vitamins and a burst of flavor in every bite!",
                "twitter_description": {
                    "description_text": "🍕🍔🍣",
                },
                "fb_profile_intro": {
                    "fb_profile_intro_text": "Craving some fresh, delicious sushi? 🍣 Let's roll with it! Maki or nigiri, there's no wrong choice!",
                }
            }
        }
    }


@pytest.fixture
def profile_with_salafist_intro_non_arabic_term():
    return {
        "biographic_details": {
            'description_bio_intro': {
                "instagram_bio": "adventurer",
                "xing_profile_about_me": "Passionate about traveling and capturing moments! 📷 Life is an adventure!",
                "google_bio": "Discovering new places and experiences. 🗺️ The world is full of wonders!",
                "twitter_description": {
                    "description_text": "Jihad",
                },
                "fb_profile_intro": {
                    "fb_profile_intro_text": "Exploring the world, one adventure at a time! 🌍 Let's make memories and discover new horizons!",
                }
            }
        }
    }
