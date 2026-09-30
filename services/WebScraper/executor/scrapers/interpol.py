import asyncio
import json
from datetime import datetime
from parsel import Selector
from tempora import parse_timedelta
from urllib.parse import unquote, urlencode, urlunparse
from typing import List
import re
from glom import glom, Assign
from core.dotty_dictionary import dotty
import random

from .decorators import async_playwright_run

from core.documents import (SearchRequestDoc,
                            SearchResponseDoc,
                            EnrichRequestDoc)

from core.clients.interpol import api, InterpolSpecs


class InterpolPlaywrightScenario:

    @classmethod
    async def enrich(cls, doc: EnrichRequestDoc, *args, **kwargs):

        if not (profile_url := doc.profile_url):
            return {}

        interpol_id = profile_url.split('#')[-1]

        mapped_result = {}
        try:
            response = await cls.safe_api_call(api.search.enrich, interpol_id)
            images_response = await cls.safe_api_call(api.search.images, interpol_id)

            response_body = response.body
            images_response_body = images_response.body
            mapped_result = glom(response_body, InterpolSpecs.enrich_specs)

            mapped_images = glom(images_response_body, InterpolSpecs.images_specs)

            mapped_result = glom(mapped_result, Assign('personal_details.visuals.interpol_photos',
                                mapped_images['personal_details']['visuals']['interpol_photos']))

        except Exception as e:
            print(e)
            return None

        return mapped_result

    @classmethod
    @async_playwright_run()
    async def enrich_with_scraper(cls, context, *args, profile_url=None, **kwargs):
        """
        Deprecated due to use of Interpol API, instead use enrich method
        """
        response = {}

        page = await context.new_page()
        # Skip images loading for page to decrease trafik
        await page.route("**/*", lambda route: route.abort()
                         if route.request.resource_type == "image"
                         else route.continue_())
        try:
            await page.goto(profile_url, timeout=60000)
        except Exception:
            return response
        await page.wait_for_load_state()
        await asyncio.sleep(2)
        # NOTE: screnshot dump for debug
        # await page.screenshot(path="screenshot.png", full_page=True)
        html = await page.content()
        selector = Selector(html)

        identity_container = selector.xpath(
            "(//h3[text()='Identity particulars']/following-sibling::div[1])[1]")

        last_name = identity_container.xpath(
            ".//td[normalize-space(text())='Family name']/following-sibling::td//strong[@id='name']/text()").get()
        first_name = identity_container.xpath(
            ".//td[normalize-space(text())='Forename']/following-sibling::td//strong[@id='forename']/text()").get()
        gender = identity_container.xpath(
            ".//td[normalize-space(text())='Gender']/following-sibling::td//strong[@id='sex_id']//span[not(contains(@class, 'hidden'))]/text()").get()
        birth_date = identity_container.xpath(
            ".//td[normalize-space(text())='Date of birth']/following-sibling::td//strong[@id='date_of_birth']/text()").get()
        place_of_birth = identity_container.xpath(
            ".//td[normalize-space(text())='Place of birth']/following-sibling::td//strong//span[@id='place_of_birth']/text()").get()
        country_of_birth = identity_container.xpath(
            ".//td[normalize-space(text())='Place of birth']/following-sibling::td//strong//span[@id='country_of_birth_id']/text()").get()
        nationality = identity_container.xpath(
            ".//td[normalize-space(text())='Nationality']/following-sibling::td//strong[@id='nationalities']/text()").get()
        marks_and_characterstics = identity_container.xpath(
            ".//td[normalize-space(text())='Distinguishing marks and characteristics']/following-sibling::td//strong[@id='distinguishing_marks']/text()").get()

        physical_container = selector.xpath(
            "(//div[contains(@class, 'physicalDescriptionContent')])[1]")

        height = physical_container.xpath(
            ".//td[normalize-space(text())='Height']/following-sibling::td//strong[@id='height']/span[@class='heightCount']/text()").get()
        weight = physical_container.xpath(
            ".//td[normalize-space(text())='Weight']/following-sibling::td//strong[@id='weight']/span[@class='weightCount']/text()").get()
        hair_color = physical_container.xpath(
            ".//td[normalize-space(text())='Colour of hair']/following-sibling::td//strong[@id='hairs_id']/text()").get()
        eye_color = physical_container.xpath(
            ".//td[normalize-space(text())='Colour of eyes']/following-sibling::td//strong[@id='eyes_colors_id']/text()").get()

        languages = selector.xpath(
            ".//td[normalize-space(text())='Language(s) spoken']/following-sibling::td//strong/text()").getall()
        charges = selector.xpath("(.//p[@id='charge'])[1]/text()").get()

        profile_photo = selector.xpath(
            ".//div[@class='wantedsingle__wrappercolumns']//img[contains(@src, 'https://ws-public.interpol.int/') and @class='redNoticeLargePhoto__img']/@src").get()

        photos = selector.xpath(
            ".//div[@class='wantedsingle__wrappercolumns']//img[contains(@src, 'https://ws-public.interpol.int/')]/@src").getall()

        response = {
            "personal_details": {
                "name": {
                    "first_name": {
                        'interpol_f_name': first_name
                    },
                    "last_name": {
                        'interpol_l_name': last_name
                    },
                    "full_name": {
                        "interpol_full_name": f"{first_name} {last_name}"
                    }
                },
                "birth_year_birthday": {
                    "birthday": {
                        "interpol_birthday": birth_date
                    }
                },
                "visuals": {
                    "profile_photo": {
                        "interpol_profile_picture": profile_photo
                    },
                    "interpol_photos": photos,
                },
                "gender": {
                    "interpol_gender": gender,
                },
                "additional_details": {
                    "interpol_details": {
                        "height": height,
                        "weight": weight,
                        "eye_color": eye_color,
                        "hair_color": hair_color,
                        "identifiers": marks_and_characterstics,

                        "nationality": nationality,
                        "place_of_birth": f"{place_of_birth}{country_of_birth}",

                        "spoken_languages": languages,

                        "charges": charges,
                    }
                },
            },
            "network_signature": {
                "url": {
                    "interpol_profile_url": profile_url
                }
            },
            "source": "interpol",
            "resource": "web_scraper",
        }

        return response

    @classmethod
    @async_playwright_run()
    async def search(cls, context, doc: SearchRequestDoc, *args, **kwargs
                     ) -> List[SearchResponseDoc]:
        docs = []

        params = {
            'forename':  doc.f_name,
            'name': doc.l_name,
        }

        try:
            response = await cls.safe_api_call(api.search.search, params=params)
            response_body = response.body
        except Exception as e:
            print(e)
            return docs

        spec = InterpolSpecs.search_specs
        mapped_results = glom(response_body, spec)


        try:
            for result in mapped_results:
                result = dotty(result)

                result.setdefault(
                    "personal_details.name.first_name.f_name", doc.f_name)
                result.setdefault(
                    "personal_details.name.last_name.l_name", doc.l_name)
                result.setdefault(
                    "personal_details.name.full_name.full_name", doc.name)
                result["source"] = 'interpol'
                result["urn"] = doc.urn
                result["search_id"] = doc.search_id

                result = result.to_dict()

                _doc = SearchResponseDoc(**result)

                docs.append(_doc)
        except Exception as e:
            print(e)

        return docs

    @classmethod
    async def safe_api_call(cls, func, *args, **kwargs):
        response = None
        for _ in range(5):
            try:
                response = func(*args, **kwargs)
                if response.status_code == 200:
                    break
            except Exception as e:
                print(e)
            await asyncio.sleep(random.randint(1, 3))
        return response
