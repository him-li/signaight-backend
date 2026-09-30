from glom import glom
from faker import Faker

from core.models.post import Post, PostAuthor
from core.models.connections import FacebookConnection
from core.models.location import FbPlaceLived


from core.clients.vetric.facebook import VtrcFbSpecs
from core.dotty_dictionary import dotty

from tests.unit.flows.mapping_specs.mapping_targets import Targets

fake = Faker()


class TestMappingsSpecs:
    def test_vetric_facebook_search(self):
        target = Targets.vtrc_fb_search_users
        spec = VtrcFbSpecs.search_edges_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            item = dotty(item)
            assert item.get("id")
            assert item.get("name")
            assert item.get("profile_picture")
            assert item.get("description")

    def test_facebook_new_search(self):
        target = Targets.vtrc_fb_search_users
        spec = VtrcFbSpecs.new_search_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            item = dotty(item)
            assert item.get("source") == "facebook"
            assert item.get("resource") == "vetric"
            assert item.get(
                "personal_details.name.full_name.facebook_full_name")
            assert item.get(
                "personal_details.visuals.profile_photo."
                "facebook_profile_picture")
            assert item.get(
                "network_signature.user_id.facebook_user_id")
            assert item.get(
                "biographic_details.description_bio_intro.introduction")
            if online_sig := item.get("network_signature.online_signature"):
                followers_count = online_sig.get("fb_followers_count")
                if followers_count:
                    assert isinstance(followers_count, int)

    def test_vetric_facebook_timeline(self):
        target = Targets.vtrc_fb_profiles_timeline
        spec = VtrcFbSpecs.timeline_specs
        result = glom(target, spec)
        assert result.get("profile_picture")
        assert result.get("fb_profile_intro")

    def test_vetric_facebook_about(self):
        target = Targets.vtrc_fb_profiles_about
        spec = VtrcFbSpecs.about_spec
        result = glom(target, spec)
        assert result
        result = dotty(result)

        assert result.get("facebook_work")
        for work in result.get("facebook_work"):
            assert work.get("fb_workplace_id")
            assert work.get("descriptive_text")
            assert work.get("period")

        assert result.get("facebook_education")
        for school in result.get("facebook_education"):
            assert school.get("fb_school_id")
            assert school.get("period")
            assert school.get("descriptive_text")

        assert result.get("facebook_locations")
        for location in result.get("facebook_locations.facebook_location"):
            assert location.get("city")
            assert location.get("type")

        assert result.get("facebook_basic_info")
        for info in result.get("facebook_basic_info"):
            assert info.get("info_type")
            assert info.get("info_data")

        assert result.get("facebook_relationships")

        assert result.get("facebook_family_members") is not None

        assert result.get("facebook_checkins")
        for checkin in result.get("facebook_checkins"):
            assert checkin.get("id")
            assert checkin.get("title")
            assert checkin.get("subtitle")
            assert checkin.get("url")
            assert checkin.get("event_image")

        assert result.get("facebook_followers")
        for follower in result.get("facebook_followers"):
            assert follower.get("name")
            assert follower.get("subtitle") is not None
            assert follower.get("url")
            assert follower.get("facebok_user_id")
            assert follower.get("facebook_profile_picture")

    def test_vetric_facebook_about_transform(self):
        target = Targets.vtrc_fb_about_update
        spec = VtrcFbSpecs.about_spec_transform
        result = glom(target, spec)
        assert result
        result = dotty(result)

        assert result.get("facebook_work")
        for work in result.get("facebook_work"):
            assert work.get("fb_workplace_id")
            assert work.get("descriptive_text")

        assert result.get("facebook_education")
        for school in result.get("facebook_education"):
            assert school.get("fb_school_id")
            assert school.get("descriptive_text")

        assert result.get("facebook_location")
        if result.get("facebook_location"):
            if current_city := result.get(
                    "facebook_location", {}):
                assert current_city.get("fb_current_city")
            if hometown := result.get("facebook_location", {}):
                assert hometown.get("fb_hometown")
            if places_lived := result.get(
                    "facebook_location", {}):
                for place in places_lived.get("fb_places_lived", []):
                    assert place.get("fb_moved_to")
                    assert place.get("fb_moved_at")

        assert result.get("facebook_basic_info")
        for info in result.get("facebook_basic_info"):
            assert info.get("info_type")
            assert info.get("info_data")

        assert result.get("facebook_languages")
        assert result.get("facebook_gender")
        assert result.get("facebook_birthday")
        assert result.get("facebook_relationships")

        assert result.get("facebook_family_members") is not None

        assert result.get("facebook_checkins")
        for checkin in result.get("facebook_checkins"):
            assert checkin.get("title")
            assert checkin.get("subtitle")
            assert checkin.get("url")
            assert checkin.get("event_image")

        assert result.get("facebook_followers")
        for follower in result.get("facebook_followers"):
            assert follower.get("name")
            assert follower.get("subtitle") is not None
            assert follower.get("url")
            assert follower.get("facebok_user_id")
            assert follower.get("facebook_profile_picture")

    def test_vetric_facebook_about_mahdi(self):
        target = Targets.vtrc_fb_profiles_about_mahdi
        spec = VtrcFbSpecs.about_spec_transform
        result = glom(target, spec)
        assert result
        result = dotty(result)

        assert result.get("facebook_work") is not None
        for work in result.get("facebook_work"):
            assert work.get("fb_workplace_id")
            assert work.get("descriptive_text")

        assert result.get("facebook_education")
        for school in result.get("facebook_education"):
            assert school.get("fb_school_id")
            assert school.get("descriptive_text")

        assert result.get("facebook_location")

        assert result.get("facebook_basic_info")

        assert result.get("facebook_relationships")

        assert result.get("facebook_family_members") is not None

        assert result.get("facebook_checkins")
        for checkin in result.get("facebook_checkins"):
            assert checkin.get("title")
            assert checkin.get("subtitle")
            assert checkin.get("url")
            assert checkin.get("event_image")

        if result.get("facebook_followers"):
            for follower in result.get("facebook_followers"):
                assert follower.get("name")
                assert follower.get("subtitle") is not None
                assert follower.get("url")
                assert follower.get("facebok_user_id")
                assert follower.get("facebook_profile_picture")

    def test_vetric_facebook_feed(self):
        target = Targets.vtrc_fb_profiles_feed
        spec = VtrcFbSpecs.feed_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            item = dotty(item)
            assert item.get("post_author")
            for author in item.get("post_author"):
                assert author.get("fb_full_name")
                assert author.get("fb_user_id")
                assert author.get("fb_gender")
                assert author.get("fb_profile_url")
                assert PostAuthor(**author)

            assert item.get("fb_post_language")
            assert item.get("fb_post_translated_to")
            assert item.get("fb_post_photo")
            assert item.get("fb_post_comments_count")
            assert item.get("fb_post_likers_count")
            assert item.get("fb_post_shares_count") is not None
            assert item.get("fb_post_reactors_count")
            assert Post(**item)

    def test_vetric_facebook_checkins(self):
        target = Targets.vtrc_fb_profiles_checkins
        spec = VtrcFbSpecs.checkins_spec
        result = glom(target, spec)
        assert result

        for check_in in result:
            assert check_in.get("title")
            assert check_in.get("region")
            assert check_in.get("date")
            assert check_in.get("event_image")
            assert check_in.get("url")

    def test_vetric_facebook_uploaded_media(self):
        target = Targets.vtrc_fb_profiles_uploaded_media
        spec = VtrcFbSpecs.uploaded_media_spec
        result = glom(target, spec)
        assert result

        for i, item in enumerate(result):
            item = dotty(item)
            assert item
            assert item.get("fb_uploaded_photo.fb_photo_id")
            assert item.get("fb_uploaded_photo.fb_photo")
            assert item.get("fb_uploaded_photo.fb_photo.url")
            assert item.get("fb_uploaded_photo.fb_photo_likes_count")
            assert item.get("fb_uploaded_photo.fb_photo_reactions_count")
            if i < 1:
                assert Post(**item.to_dict())

    def test_vtrc_fb_friends(self):
        target = Targets.vtrc_fb_friends
        spec = VtrcFbSpecs.friends_spec
        result = glom(target, spec)
        assert result
        for friend in result:
            assert friend
            friend = FacebookConnection(**friend)
            assert friend.facebook_full_name
            assert friend.facebook_user_id

    def test_vtrc_fb_about_tabs_places_lived(self):
        target = Targets.vtrc_fb_about_tabs_places_lived
        spec = VtrcFbSpecs.about_tabs_places_lived_spec
        result = glom(target, spec)
        assert result
        for location in result:
            assert location.get("field_type") == 'moved_city'
            assert location.get("fb_moved_to")
            assert location.get("fb_moved_at")
            assert FbPlaceLived(**location)

    def test_vtrc_fb_liked_pages(self):
        target = Targets.vtrc_fb_pages_likes
        spec = VtrcFbSpecs.liked_pages_spec
        result = glom(target, spec)
        assert result
        for page in result:
            assert page

    def test_vetric_facebook_new_feed(self):
        target = Targets.new_vtrc_profiles_feed
        spec = VtrcFbSpecs.new_feed_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            item = dotty(item)
            assert item.get("post_author")
            for author in item.get("post_author"):
                assert author.get("fb_full_name")
                assert author.get("fb_user_id")
                assert author.get("fb_gender")
                assert author.get("fb_profile_url")
                assert PostAuthor(**author)

            assert item.get("fb_post_language")
            assert item.get("fb_post_photo")
            assert item.get("fb_post_comments_count")
            assert item.get("fb_post_likers_count")
            assert item.get("fb_post_shares_count") is not None
            assert item.get("fb_post_reactors_count")
            assert Post(**item)

    def test_vetric_facebook_following(self):
        target = Targets.vtrc_fb_profiles_following
        spec = VtrcFbSpecs.following_spec
        result = glom(target, spec)
        assert result

        for item in result:
            assert item
            assert item.get("facebook_user_id")
            assert item.get("facebook_full_name")
            assert item.get("facebook_profile_picture")
            assert item.get("facebook_profile_url")
