from glom import glom
from faker import Faker

from core.models import BiographicDetails, NetworkSignature
from core.models.post import Post
from core.clients.vetric.twitter import (VtTwSpecs,
                                         set_tweet_post_card,
                                         set_tweet_post_photo)
from core.dotty_dictionary import dotty

from tests.unit.flows.mapping_specs.mapping_targets import Targets
from tests.unit.flows.mapping_specs.schemas import PersonalDetailsTest

fake = Faker()


class TestMappingsSpecs:
    def test_vetric_twitter_search(self):
        target = Targets.vtrc_tw_search
        spec = VtTwSpecs.search_spec
        result = glom(target, spec)
        assert result

        for i, person in enumerate(result):
            personal_details = person.get("personal_details")
            biographic_details = person.get("biographic_details")
            network_signature = person.get("network_signature")

            BiographicDetails(**biographic_details)
            NetworkSignature(**network_signature)
            if i < 2:
                PersonalDetailsTest(**personal_details)

    def test_vetric_twitter_profile_details_by_screen_name(self):
        target = Targets.vtrc_tw_profile_details_by_screen_name
        spec = VtTwSpecs.profile_spec
        result = glom(target, spec)
        assert result

    def test_vetric_twitter_profile_tweets(self):
        target = Targets.vtrc_tw_profile_tweets
        unique_spec = VtTwSpecs.unique_tweets_spec

        for i, tweet in enumerate(target.get('tweets')):
            tweet = glom(tweet.get('tweet'), unique_spec)
            tweet = dotty(tweet)
            tweet['twitter_post_view_count'] = int(
                tweet.get("twitter_post_view_count"))
            if tweet.get("twitter_quoted_post"):
                tweet['twitter_quoted_post'] = glom(
                    tweet.get("twitter_quoted_post.result"), unique_spec)
                tweet['twitter_quoted_post.twitter_post_card'] = (
                    set_tweet_post_card(tweet, 'twitter_quoted_post'))
                tweet['twitter_quoted_post.twitter_post_photo'] = (
                    set_tweet_post_photo(tweet, 'twitter_quoted_post.'))
            if tweet.get("twitter_retweeted_post"):
                tweet['twitter_retweeted_post'] = glom(
                    tweet.get("twitter_retweeted_post.result"), unique_spec)
                tweet['twitter_retweeted_post.twitter_post_card'] = (
                    set_tweet_post_card(tweet, 'twitter_retweeted_post'))
                tweet['twitter_retweeted_post.twitter_post_photo'] = (
                    set_tweet_post_photo(tweet, 'twitter_retweeted_post.'))

            if tweet.get('twitter_post_card'):
                tweet['twitter_post_card'] = set_tweet_post_card(
                    tweet, '')

            if tweet.get('twitter_post_photo'):
                tweet['twitter_post_photo'] = set_tweet_post_photo(tweet, '')

            if i < 2:
                assert Post(**tweet.to_dict())
