from typing import List, Dict
from glom import glom
from mergedeep import merge, Strategy

from core.clients.vetric.twitter import (
    api,
    VtTwSpecs,
    set_tweet_post_card,
    set_tweet_post_photo
)
from core.documents import (
    EnrichRequestDoc,
    EnrichResponseDoc,
    SearchResponseDoc,
    SearchRequestDoc
)
from core.dotty_dictionary import dotty
from core.logging import logger


class VetricTwitterAPI():

    async def search(
            self,
            doc: SearchRequestDoc
    ) -> List[SearchResponseDoc]:
        params = {"query": doc.name}
        docs = []
        try:
            response = await api.async_search.people(params=params)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return None

        spec = VtTwSpecs.search_spec
        mapped_results = glom(response_body, spec)

        try:
            for result in mapped_results:
                result = dotty(result)
                personal_details = {
                    "name": {
                        "first_name": {
                            "f_name": doc.f_name
                        },
                        "last_name": {
                            "l_name": doc.l_name
                        },
                        "full_name": {
                            "full_name": doc.name,
                            "twitter_full_name": result.get(
                                "personal_details.name.full_name."
                                "twitter_full_name")
                        }
                    },
                    "email": {
                        "email_address": ([doc.email_address] if
                                          doc.email_address else None)
                    },
                    "visuals": {
                        "profile_photo": {
                            "twitter_profile_picture": result.get(
                                "personal_details.visuals.profile_photo."
                                "twitter_profile_picture"),
                            "twitter_cover_photo": result.get(
                                "personal_details.visuals.profile_photo."
                                "twitter_cover_photo")
                        }
                    },
                    "location": {
                        "twitter_location":  result.get(
                            "personal_details.location.twitter_location")
                    }
                }
                result["personal_details"] = personal_details
                result["source"] = "twitter"
                result["resource"] = doc.resource
                result["urn"] = doc.urn
                result["search_id"] = doc.search_id
                result = result.to_dict()
                _doc = SearchResponseDoc(**result)
                docs.append(_doc)
        except Exception as e:
            print(e)
            pass
        return docs

    async def enrich(self, doc: EnrichRequestDoc) -> EnrichResponseDoc | None:
        data = {}
        if enriched_profile_details := await self._enrich_profile_details(doc):
            data = merge(data, enriched_profile_details)

        if data.get("network_signature",
                    {}).get("user_id", {}).get("twitter_user_id"):
            doc.source_id = data.get("network_signature",
                                     {}).get("user_id",
                                             {}).get("twitter_user_id")
            if enriched_profile_tweets := (
                    await self._enrich_profile_tweets(doc)):
                data = merge(data, enriched_profile_tweets,
                             strategy=Strategy.REPLACE)

        if data:
            data['urn'] = doc.urn
        return EnrichResponseDoc(**data) if data else None

    async def _enrich_profile_details(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        if isinstance(username, list):
            username = username[0]
        source_id = doc.username
        try:
            response = await api.async_profile.profile_details_by_screen_name(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return
        spec = VtTwSpecs.profile_spec
        mapped = glom(response_body, spec, default={})

        return mapped if mapped else None

    async def _enrich_profile_tweets(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.profile_tweets_by_id(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return
        unique_spec = VtTwSpecs.unique_tweets_spec

        posts = []
        for tweet in response_body.get('tweets'):
            tweet = glom(tweet.get('tweet'), unique_spec)
            tweet = dotty(tweet)
            if tweet.get('twitter_post_view_count'):
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

            posts.append(tweet.to_dict())

        if posts:
            tweets = {'posts': posts}
        return tweets if posts else None
