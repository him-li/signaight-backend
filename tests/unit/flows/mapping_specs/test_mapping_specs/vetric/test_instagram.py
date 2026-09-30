from glom import glom
from faker import Faker


from core.clients.vetric.instagram import VtrcIgSpecs

from core.dotty_dictionary import dotty


from tests.unit.flows.mapping_specs.mapping_targets import Targets


fake = Faker()


class TestMappingsSpecs:
    def test_vetric_instagram_search(self):
        target = Targets.vtrc_ig_search
        spec = VtrcIgSpecs.search_spec
        result = glom(target, spec)
        assert result

        for user in result:
            user = dotty(user)

            assert user.get("instagram_full_name")
            assert user.get("instagram_user_id")
            assert user.get("instagram_username")
            assert user.get("instagram_is_private") is not None
            assert user.get("instagram_ld_profile_picture")

    def test_vetric_instagram_new_search(self):
        target = Targets.vtrc_ig_search
        spec = VtrcIgSpecs.new_search_spec
        result = glom(target, spec)
        assert result

        for user in result:
            user = dotty(user)
            assert user.get(
                "personal_details.name.full_name.instagram_full_name")
            assert user.get(
                "personal_details.visuals.profile_photo."
                "instagram_profile_picture")
            assert user.get("network_signature.user_id.instagram_user_id")
            assert user.get("network_signature.username.instagram_username")
            assert user.get(
                "network_signature.misc.instagram_is_private") is not None

    def test_vetric_instagram_info(self):
        target = Targets.vtrc_ig_info
        spec = VtrcIgSpecs.info_spec
        result = glom(target, spec)
        assert result

        result = dotty(result)

        assert result.get(
            "personal_details.name.full_name.instagram_full_name")
        assert result.get(
            "personal_details.visuals.profile_photo.instagram_profile_picture")
        assert result.get(
            "biographic_details.description_bio_intro.instagram_bio"
        ) is not None
        assert result.get(
            "biographic_details.description_bio_intro.biography_with_entities"
        ) is not None
        assert result.get(
            "biographic_details.description_bio_intro."
            "instagram_fb_link_on_profile") is not None
        assert result.get(
            "biographic_details.description_bio_intro.instagram_bio_links"
        ) is not None

    def test_vetric_instagram_new_info(self):
        target = Targets.vtrc_ig_new_info
        spec = VtrcIgSpecs.info_spec
        result = glom(target, spec)
        assert result

        result = dotty(result)

        assert result.get(
            "personal_details.name.full_name.instagram_full_name")
        assert result.get(
            "personal_details.visuals.profile_photo.instagram_profile_picture")
        assert result.get(
            "biographic_details.description_bio_intro.instagram_bio"
        ) is not None
        assert result.get(
            "biographic_details.description_bio_intro.biography_with_entities"
        ) is not None

    def test_vetric_instagram_feed(self):
        target = Targets.vtrc_ig_feed
        spec = VtrcIgSpecs.feed_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            item = dotty(item)

            assert item.get("instagram_post_text") is not None
            assert item.get("instagram_post_id")
            assert item.get("instagram_user_id")
            assert item.get("instagram_post_location")
            if item.get("instagram_post_photo"):
                assert item.get("instagram_post_photo")

            assert item.get("tagged_profiles") is not None
            for profile in item.get("tagged_profiles"):
                assert profile.get("instagram_id")
                assert profile.get("instagram_username")
                assert profile.get("instagram_full_name")
                assert profile.get("instagram_is_private") is not None
                assert profile.get("instagram_is_verified") is not None
                assert profile.get("instagram_profile_picture")

            assert item.get("instagram_post_likes_count")
            assert item.get("post_likers") is not None
            for liker in item.get("post_likers"):
                assert liker.get("instagram_id")
                assert liker.get("instagram_username")
                assert liker.get("instagram_full_name")
                assert liker.get("instagram_is_private") is not None
                assert liker.get("instagram_is_verified") is not None
                assert liker.get("instagram_profile_picture")

    def test_vetric_instagram_new_feed(self):
        target = Targets.vtrc_ig_new_feed
        spec = VtrcIgSpecs.feed_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            item = dotty(item)

            assert item.get("instagram_post_text") is not None
            assert item.get("instagram_post_id")
            assert item.get("instagram_post_location")
            if item.get("instagram_post_photo"):
                assert item.get("instagram_post_photo")

            assert item.get("tagged_profiles") is not None
            for profile in item.get("tagged_profiles"):
                assert profile.get("instagram_id")
                assert profile.get("instagram_username")
                assert profile.get("instagram_full_name")
                assert profile.get("instagram_is_private") is not None
                assert profile.get("instagram_is_verified") is not None
                assert profile.get("instagram_profile_picture")

            assert item.get("instagram_post_likes_count")
            assert item.get("post_likers") is not None
            for liker in item.get("post_likers"):
                assert liker.get("instagram_id")
                assert liker.get("instagram_username")
                assert liker.get("instagram_full_name")
                assert liker.get("instagram_is_private") is not None
                assert liker.get("instagram_is_verified") is not None
                assert liker.get("instagram_profile_picture")

    def test_vetric_instagram_following(self):
        target = Targets.vtrc_ig_following
        spec = VtrcIgSpecs.following_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            assert item.get("instagram_user_id")
            assert item.get("instagram_username")
            assert item.get("instagram_full_name")
            assert item.get("instagram_is_private") is not None
            assert item.get("instagram_profile_picture")
            assert item.get("instagram_profile_picture_id") is not None
            assert item.get("instagram_is_verified") is not None

    def test_vetric_instagram_new_following(self):
        target = Targets.vtrc_ig_new_following
        spec = VtrcIgSpecs.following_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            assert item.get("instagram_user_id")
            assert item.get("instagram_username")
            assert item.get("instagram_full_name")
            assert item.get("instagram_is_private") is not None
            assert item.get("instagram_profile_picture")
            assert item.get("instagram_is_verified") is not None

    def test_vetric_instagram_followers(self):
        target = Targets.vtrc_ig_followers
        spec = VtrcIgSpecs.followers_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            assert item.get("instagram_user_id")
            assert item.get("instagram_username")
            assert item.get("instagram_full_name")
            assert item.get("instagram_is_private") is not None
            assert item.get("instagram_profile_picture")
            assert item.get("instagram_is_verified") is not None

    def test_vetric_instagram_old_followers(self):
        target = Targets.vtrc_ig_old_followers
        spec = VtrcIgSpecs.followers_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            assert item.get("instagram_user_id")
            assert item.get("instagram_username")
            assert item.get("instagram_full_name")
            assert item.get("instagram_is_private") is not None
            assert item.get("instagram_profile_picture")
            assert item.get("instagram_is_verified") is not None
