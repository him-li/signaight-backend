import asyncio
from dateutil import parser
from parsel import Selector
from urllib.parse import urlencode, urlunparse
from typing import List

from .decorators import async_playwright_run

from core.documents import (SearchRequestDoc,
                            SearchResponseDoc)

scheme = "https"
netloc = "www.eumostwanted.eu"
base_url = "https://eumostwanted.eu/"


class EUMostWantedPlaywrightScenario:

    @classmethod
    @async_playwright_run()
    async def search(cls, context, doc: SearchRequestDoc, *args, **kwargs
                     ) -> List[SearchResponseDoc]:
        search_url = cls.construct_search_url(doc=doc)

        page = await context.new_page()

        await page.route("**/*", lambda route: route.abort()
                         if route.request.resource_type == "image"
                         else route.continue_())

        docs = []
        try:
            await page.goto(search_url)
            await page.wait_for_load_state()
            await asyncio.sleep(2)
            # NOTE: screenshot dump for debug
            #await page.screenshot(path="screenshot.png", full_page=True)
        except Exception as e:
            print(str(e))
            return docs

        html = await page.content()
        selector = Selector(html)

        # Gettings all the profile urls from the search result
        profiles = selector.xpath("//ol//li//h3//a")

        for profile in profiles:
            profile_url = profile.xpath("./@href").get()

            profile_url = profile_url.split("#", 1)[-1]

            profile_url = urlunparse((scheme, netloc, profile_url, '', '', ''))
            print(profile_url)

            profile_data = await cls.get_profile_data(page, profile_url)
            data = {
                "personal_details": {
                    "name": {
                        "first_name": {"f_name": doc.f_name},
                        "last_name": {"l_name": doc.l_name},
                        "full_name": {
                            "full_name": doc.name,
                            "eumw_full_name": f"{profile_data.get('first_name')} {profile_data.get('last_name')}"
                        }
                    },
                    "birth_year_birthday": {
                        "birthday": {
                            "eumw_birthday": profile_data.get('date_of_birth')
                        }
                    },
                    "visuals": {
                        "profile_photo": {
                            "eumw_profile_picture": profile_data.get('profile_picture')
                        },
                        "eumw_photos": profile_data.get('photo_urls', []),
                    },
                    "gender": {
                        "eumw_gender": profile_data.get('gender'),
                    },
                    'languages': {
                        'eumw_languages': profile_data.get('languages'),
                    },
                    'nationality': {
                        'eumw_nationality': profile_data.get('nationality'),
                    },
                    "additional_details": {
                        "eumw_details": {

                            "ethnic_origin": profile_data.get('ethnic_origin'),

                            "state_of_case": profile_data.get('state_of_case'),
                            "info": profile_data.get('info'),
                            "crime": profile_data.get('crime'),
                            "date_published": profile_data.get('date_published'),
                        },
                        "physical_identifiers": {
                            'height': {
                                'eumw_height': profile_data.get('height')
                            },
                            'eye_color': {
                                'eumw_eye_color': profile_data.get('eye_color')
                            },
                            'identifiers': {
                                'eumw_identifiers': profile_data.get('identifiers')
                            },
                        },
                    }
                },
                "network_signature": {
                    "url": {
                        "eumw_profile_url": profile_url
                    }
                },
                "source": "eumw",
                "resource": "web_scraper",
                "urn": doc.urn,
                "search_id": doc.search_id
            }

            _doc = SearchResponseDoc(**data)
            docs.append(_doc)

        return docs

    @classmethod
    async def get_profile_data(cls, page, profile_url):

        if not profile_url:
            return None

        await page.goto(profile_url)
        await page.wait_for_load_state()
        await asyncio.sleep(2)
        # NOTE: screnshot dump for debug
        #await page.screenshot(path="screenshot.png", full_page=True)
        html = await page.content()
        selector = Selector(html)

        response = {}

        try:
            last_name, first_name = selector.xpath(
                "//div[contains(concat(' ',normalize-space(@class),' '),' field--name-field-w-first-name ')]/text()").get().strip().split(", ")
        except Exception as e:
            print(e)
            last_name, first_name = "", ""

        response['first_name'] = first_name
        response['last_name'] = last_name

        response['crime'] = selector.xpath(
            "//div[@class='field-label' and text()='Crime']/following-sibling::*//div[@class='field__item']/text()").get()
        response['is_dangerous'] = bool(selector.xpath(
            ".//div[@class='is-dangerous']/text()").get())
        response['gender'] = selector.xpath(
            "//div[@class='field-label' and text()='Sex']/following-sibling::div[@class='field__item']/text()").get()
        response['height'] = selector.xpath(
            "//div[@class='field-label' and text()='Approximate height']/following-sibling::div[@class='field__item']/text()").get()
        response['identifiers'] = selector.xpath(
            "//div[@class='field-label' and text()='Identifiers']/following-sibling::div[@class='field__items']//div[@class='field__item']/text()").getall()
        response['eye_color'] = selector.xpath(
            "//div[@class='field-label' and text()='Eye colour']/following-sibling::div[@class='field__item']/text()").get()

        birthday = selector.xpath(
            "//div[@class='field-label' and text()='Date of birth']/following-sibling::div[@class='field__item']/time/text()").get()

        if birthday:
            birthday = parser.parse(
                birthday.split('(')[0]).strftime(r"%d/%m/%Y")

        response['date_of_birth'] = birthday

        response['nationality'] = selector.xpath(
            "//div[@class='field-label' and text()='Nationality']/following-sibling::div/div[@class='field__item']/text()").get()
        response['ethnic_origin'] = selector.xpath(
            "//div[@class='field-label' and text()='Ethnic origin']/following-sibling::div[@class='field__item']/text()").get()
        response['spoken_languages'] = selector.xpath(
            "//div[@class='field-label' and text()='Spoken languages']/following-sibling::div[@class='field__items']//div[@class='field__item']/text()").getall()
        response['state_of_case'] = selector.xpath(
            "//div[@class='field-label' and text()='State of case']/following-sibling::div[@class='field__item']/text()").get()
        response['date_published'] = selector.xpath(
            "//div[@class='field-label' and text()='published']/following-sibling::div[@class='field__item']/text()").get()

        photos_urls = selector.xpath(
            "//div[@class='wanted_top_left']//div[contains(concat(' ',normalize-space(@class),' '),' field__item ')]//img/@src").getall()

        for idx, url in enumerate(photos_urls):
            photos_urls[idx] = urlunparse((scheme, netloc, url, '', '', ''))
        response['photo_urls'] = photos_urls

        if photos_urls:
            response['profile_picture'] = photos_urls[0]
        else:
            response['profile_picture'] = None

        response['info'] = " ".join([l.strip() for l in selector.xpath(
            "//div[@class='wanted_bottom_right']//text()").getall()])

        return response

    @classmethod
    def construct_search_url(cls, doc: SearchRequestDoc, ):

        scheme = "https"
        netloc = "www.eumostwanted.eu"
        path = "/search/node"
        params = {"keys": doc.name}
        query_string = urlencode(params)
        url = urlunparse((scheme, netloc, path, '', query_string, ''))
        return url
