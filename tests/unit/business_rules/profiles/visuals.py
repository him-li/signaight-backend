# flake8: noqa
import pytest


@pytest.fixture
def profile_with_cover_no_sociable_events():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "visuals": {
                "fb_cover_photo": "s3://signaight-dev/profile_photos/6/ae/66654/6ae66654-37dc-4767-b101-4d75ab30c136.jpg",
            }
        }
    }


@pytest.fixture
def profile_with_cover_with_sociable_events():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "visuals": {
                "fb_cover_photo": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
            }
        }
    }


@pytest.fixture
def profile_with_visuals_empty():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "visuals": {
            }
        }
    }


@pytest.fixture
def profile_with_cover_weapons():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "visuals": {
                "fb_cover_photo": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg",
            }
        }
    }


@pytest.fixture
def profile_with_profile_picture_weapons():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "visuals": {
                "profile_photo": {
                    "profile_picture": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg",
                }
            }
        }
    }


@pytest.fixture
def profile_with_fb_profile_picture_weapons():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "visuals": {
                "profile_photo": {
                    "facebook_profile_picture": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg",
                }
            }
        }
    }

@pytest.fixture
def grayfox_with_pictures():
    return {
             "pictures": [
            {
                "picture": "https:/v2_images/default_avatar_240x240.jpg",
                "source": "imageshack"
            },
            {
                "picture": "https://d2exd72xrrp1s7.cloudfront.net/www/1n/1n90ox72yvyet14f9zkvek61qy302lkgdg-u857470169527-full/16b5c899d90",
                "source": "komoot"
            },
            {
                "picture": "https://lh3.googleusercontent.com/a-/AOh14GjZzjQRzwVDIFqS00WbxDetpB-stamJAEgkByqcAA=s100",
                "source": "notion"
            },
            {
                "picture": "https://s3.amazonaws.com/garmin-connect-prod/profile_images/543d1dab-c4be-4958-ace4-d752331702c4-73819736.png",
                "source": "garmin"
            },
            {
                "picture": "https://gravatar.com/avatar/cd6c8d8129f4f381c2360c2a795f4f1a?size=125&d=https%3A%2F%2Fassets.untappd.com%2Fsite%2Fassets%2Fimages%2Fdefault_avatar_v3_gravatar.jpg%3Fv%3D2",
                "source": "untappd"
            },
            {
                "picture": "https://assets.untappd.com/photos/2018_04_13/7fe822724ac76f23da3ae8a59098fce8_640x640.jpg",
                "source": "untappd"
            },
            {
                "picture": "https://plex.tv/users/6c938ffc95ffd0a9/avatar?t=1671019238907",
                "source": "plex"
            },
            {
                "picture": "https://1.gravatar.com/avatar/97473bb21bb9a6f96525d1cbdd296d0aafce8f9906d8d97d63a04fdf4ce67406",
                "source": "gravatar"
            },
            {
                "picture": "https://dl-web.dropbox.com/account_photo/get/pid_uphoto%3AAAAAABHLc7kbnfl3uLE53c8yyWrCeYHygEcqhs7NcKryexaxqDk2k0bW5KTYA8GMWq5cH6Q6wKJKA-ONsWE2?size=128x128&vers=1547220064409",
                "source": "dropbox"
            },
            {
                "picture": "https://www.skiline.cc/shared/profile/photos/large.png",
                "source": "skiline"
            },
            {
                "picture": "https://polarsteps.s3.amazonaws.com/u_128038/1726b349-2480-4eb4-b2e1-9a62952b043e_profile.jpg",
                "source": "polarsteps"
            },
            {
                "picture": "https://graph.facebook.com/10207130486452426/picture?height=256&width=256",
                "source": "strava"
            },
            {
                "picture": "https://images.chesscomfiles.com/uploads/v1/user/37969292.099ed86a.200x200o.cd5ceff7678e.jpeg",
                "source": "chess"
            },
            {
                "picture": "https://avatars.githubusercontent.com/u/3865042",
                "source": "github"
            },
            {
                "picture": "https://miro.medium.com/v2/0*whbS47EeQwjBE_nh.",
                "source": "medium"
            },
            {
                "picture": "https://simg-ssl.duolingo.com/avatar/default_2/xlarge",
                "source": "duolingo"
            },
            {
                "picture": "https://lh3.googleusercontent.com/a-/ALV-UjVttbXMjWF--zOIWAvsCt0AgTqdv9IKNhJh1GHPcPh0IcadGBZpIA",
                "source": "google"
            }
        ],
    }


