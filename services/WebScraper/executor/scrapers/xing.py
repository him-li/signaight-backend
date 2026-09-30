import asyncio
import json
from datetime import datetime
from parsel import Selector
from tempora import parse_timedelta
from urllib.parse import unquote, urlencode, urlunparse
from typing import List
import re

from .decorators import async_playwright_run

from core.documents import (SearchRequestDoc,
                            SearchResponseDoc)
from core.logging import logger


class XingPlaywrightScenario:

    @classmethod
    @async_playwright_run()
    async def search(cls, context, doc: SearchRequestDoc, *args, **kwargs
                     ) -> List[SearchResponseDoc]:
        search_url = cls.construct_url(doc=doc)

        username = kwargs.get('username')
        password = kwargs.get('password')
        # add check for session id here via cookies or local storage
        if username and password:
            try:
                auth_data = await cls.login(context, username, password)  # noqa
            except Exception as e:
                logger.error(f"login exception {str(e)}")
                return []
            if not auth_data:
                return []

        page = await context.new_page()

        try:
            for _ in range(3):
                await page.goto(search_url, timeout=60000)
                await page.wait_for_load_state()
                # NOTE: at slow networks page could still render data even
                # load state success
                await asyncio.sleep(6)

                if 'login' in page.url:
                    continue
                else:
                    break

            # NOTE: screnshot dump for debug
            # await page.screenshot(path="screenshot3.png", full_page=True)
            html = await page.content()
            selector = Selector(html)

        except Exception as e:
            logger.error(str(e))
            return

        docs = []

        # profiles = selector.xpath(
        #    "//div[@role='list' and @data-qa='results-list']/a")
        profiles = selector.xpath(
            "//ol[@data-testid='search-list']/li"
            "/div[@data-testid='members-search-result-item']"
        )
        for profile in profiles:
            # Figure out whether there is a work paragraph,
            # a location paragraph or both.
            paragraphs = profile.xpath(
                ".//div[contains(@class,'ContentContainer')]/div/p")
            if len(paragraphs) >= 2:
                work = paragraphs[0]
                loc = paragraphs[1]
            elif len(paragraphs) == 1:
                # TODO: may not work with new 18.04.2025 layout
                # If there is a link it is a work paragraph, otherwise location
                if paragraphs[0].xpath("./a"):
                    work = paragraphs[0]
                    loc = None
                else:
                    loc = paragraphs[0]
                    work = None
            elif len(paragraphs) == 0:
                work, loc = None, None
            if work:
                if work_title := work.xpath("./text()").get():
                    work_title = work_title.strip(" ,")
                else:
                    work_title = ""
                if work_company := work.xpath("./a/text()").get():
                    work_company = work_company.strip(" ,")
                else:
                    work_company = ""
            else:
                work_title = ""
                work_company = ""
            if loc:
                # Check if City data is available
                loc_data = loc.xpath("./text()").get()
                if work_company in loc_data:
                    loc_data = loc_data.replace(work_company, '').strip(" ,")
            else:
                loc_data = None

            data = {
                "personal_details": {
                    "name": {
                        "first_name": {"f_name": doc.f_name},
                        "last_name": {"l_name": doc.l_name},
                        "full_name": {
                            "full_name": doc.name,
                            "xing_full_name": profile.xpath(
                                ".//h2[@data-xds='Headline']/text()").get(
                            ).strip()
                        }
                    },
                    "email": {
                        "email_address": ([doc.email_address] if
                                          doc.email_address else None)
                    },
                    "visuals": {
                        "profile_photo": {
                            "xing_profile_picture": profile.xpath(
                                ".//img/@src").get()
                        }
                    },
                    "location": {
                        "xing_country_province_address": loc_data
                    }
                },
                "network_signature": {
                    "username": {
                        "xing_username": profile.xpath("./a/@href")
                        .get().split('/')[-1],
                    },

                    "url": {
                        "xing_profile_url": (
                            r"https://www.xing.com" + profile.xpath(
                                "./a/@href").get())
                    },
                    "misc": {
                        "xing_profile_type": (
                            "premium" if bool(
                                profile.xpath(
                                    ".//span[@data-xds='Flag']/span[@data-xds="
                                    "'BodyCopy']/text()").get(
                                )) else "regular"),
                    }
                },
                "biographic_details": {
                    "work": {
                        "xing_work": {
                            "positions": [{
                                "title": work_title,
                                "company_name": work_company
                            },]
                        }
                    }
                },
                "source": "xing",
                "resource": "web_scraper",
                "urn": doc.urn,
                "search_id": doc.search_id
            }
            _doc = SearchResponseDoc(**data)
            docs.append(_doc)
        return docs

    @classmethod
    def construct_url(cls, doc: SearchRequestDoc):
        base_url = "https://www.xing.com/search/members"

        params = {
            "name": doc.name,
            # "company": doc.work,
            # "city": doc.city,
        }

        query = urlencode(params)
        url = urlunparse(('', '', base_url, '', query, ''))

        return url

    @classmethod
    @async_playwright_run()
    async def enrich(cls, context, doc, *args, **kwargs):
        response = {}
        if not (profile_url := doc.profile_url):
            return response

        username = kwargs.get('username')
        password = kwargs.get('password')
        # add check for session id here via cookies or local storage
        if username and password:
            try:
                auth_data = await cls.login(context, username, password)  # noqa
            except Exception as e:
                logger.error(f"login exception {str(e)}")
                return response
            if not auth_data:
                return response

        page = await context.new_page()

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

        # profile container object
        profile_container = selector.xpath("//main[@id='content']")
        _xing_id = profile_container.xpath("//div[@id='XingIdModule']")
        if not _xing_id:
            return response
        _xing_id = Selector(_xing_id.get())

        full_name = fn.strip() if (
            fn := _xing_id.xpath("//h1/text()").get()) else None

        xing_profile_type = _xing_id.xpath("//h1/div/div/button/span/span/text()").get()  # noqa

        xing_profile_picture = _xing_id.xpath(
            "//div[@data-xds='ProfileImage']//img/@src").get()

        # NOTE: xing respond with geodata strictly depends on local browser
        # headers also for some reason selector works wrong so Selector
        # reinit used as workaround
        location = _xing_id.xpath("//svg[@data-xds='IconLocationPin']/..")
        if location:
            location = Selector(location.get())
            xing_location = "{}{}".format(
                location.xpath("//div/p/strong/text()").get(),
                location.xpath("//div/p/text()").get()
            )
        else:
            xing_location = None

        if xing_current_position := _xing_id.xpath(
                "//svg[@data-xds='IconJobs']/../div/p/text()").extract():
            xing_current_position.insert(1, _xing_id.xpath(
                "//svg[@data-xds='IconJobs']/../div/p/strong/text()").get())
            xing_current_position = "".join(xing_current_position)
        else:
            xing_current_position = None

        # Number of contacts
        xing_contacts = _xing_id.xpath(".//button[@data-xds='TextButton']/div/span/span/strong/text()").get()  # noqa

        # contact details
        contact_details = await cls.get_contact_details(page, profile_url)

        # skills extraction
        skills = {}
        skills_container = profile_container.xpath(
            "//div[@id='ProfileSkillsModule']")

        top_skills_container = skills_container.xpath(
            ".//div[./h2//span[text()='Top skills']]")
        skills['top_skills'] = (
            [{'name': skill.get()} for skill
             in top_skills_container.xpath(
                 ".//div[@data-xds='Tag']/div/span/text()")])

        hard_skills_container = skills_container.xpath(
            ".//div[./h2[text()='Hard skills']]")
        skills['hard_skills'] = (
            [{'name': skill.get()} for skill
             in hard_skills_container.xpath(
                 ".//div[@data-xds='Tag']/div/span/text()")])

        soft_skills_container = skills_container.xpath(
            ".//div[./h2[text()='Soft skills']]")
        skills['soft_skills'] = (
            [{'name': skill.get()} for skill
             in soft_skills_container.xpath(
                 ".//div[@data-xds='Tag']/div/span/text()")])

        timeline_container = profile_container.xpath(
            "//div[@id='ProfileTimelineModule']")

        # timeline work experience
        positions = timeline_container.xpath(
            "//div[contains(@data-qa, 'work_experience')]")
        for key, item in enumerate(positions):
            _item = Selector(item.get())
            # parse duration
            intervals = _item.xpath("//p[@data-xds='Meta']/text()").get()
            duration, period, = cls.parse_duration_and_period(intervals)

            description = _item.xpath("//p[@data-xds='BodyCopy']/span/text()")
            description = (
                str(
                    description[-1].get()).strip(' -') if len(description) > 0
                else None)

            surn = item.xpath("./@data-qa").get()

            if surn:
                surn = surn.replace('timeline-', '').replace('-entry', '')

            _work = {
                'duration': duration,
                'period': period,
                'title': _item.xpath(
                    "//h2[@data-qa='timeline-headline']/text()").get(),
                'company_name': _item.xpath(
                    ".//div/div/p[@data-xds='BodyCopy']/text()").get(),
                'xing_company_url': _item.xpath(
                    "//a[@href]/@href").get(),
                'company_logo_url': _item.xpath(
                    "//img[@title='Logo']/@src").get(),
                'description': description,
                **(await cls.get_more_data(
                    page,
                    surn=surn,
                    profile_url=profile_url))
            }

            positions[key] = _work

        # timeline education experience
        xing_schools = timeline_container.xpath(
            "//div[contains(@data-qa, 'school')]")
        for key, item in enumerate(xing_schools):
            _item = Selector(item.get())
            # parse duration
            intervals = _item.xpath("//p[@data-xds='Meta']/text()").get()
            duration, period, = cls.parse_duration_and_period(intervals)

            description = _item.xpath("//p[@data-xds='BodyCopy']/span/text()")
            description = (str(
                description[-1].get()).strip(' -') if len(description) > 0
                else None)

            surn = item.xpath("./@data-qa").get()

            if surn:
                surn = surn.replace('timeline-', '').replace('-entry', '')

            xing_schools[key] = {
                'duration': duration,
                'period': period,
                'degree_name': _item.xpath(
                    "//h2[@data-qa='timeline-headline']/text()").get(),
                'school_name': _item.xpath(
                    ".//div/div/p[@data-xds='BodyCopy']/text()").get(),
                'school_url': _item.xpath(
                    "//a[@href]/@href").get(),
                'school_logo_url': _item.xpath(
                    "//img[@title='Logo']/@src").get(),
                'description': description,
                **(await cls.get_more_data(page,
                                           surn=surn,
                                           profile_url=profile_url,
                                           is_school=True))
            }

        # languages
        language_container = profile_container.xpath(
            "//div[@id='ProfileLanguagesModule']")
        xing_languages = language_container.xpath(
            "//div[./h2[@data-xds='Headline'] and "
            ".//div/p[@data-xds='BodyCopy'] and "
            ".//div/div[@data-xds='ProgressBar']]")

        for key, item in enumerate(xing_languages):
            _item = Selector(item.get())
            xing_languages[key] = {
                'language': _item.xpath("//h2/text()").get(),
                'proficiency': _item.xpath(
                    ".//p[@data-xds='BodyCopy']/text()")[-1].get(),
            }

        # Accomplishments
        accomplishments_container = profile_container.xpath(
            "//div[@id='AccomplishmentsModule']")
        accomplishments = accomplishments_container.xpath(
            "./div/div/div[2]//h2[@data-xds='Headline']"
        )
        for idx, accomplishment in enumerate(accomplishments):
            accomplishments[idx] = {
                'issue_date': accomplishment.xpath(
                    "./preceding-sibling::p[@data-xds='Meta']/text()").get(),
                'name': accomplishment.xpath("./text()").get(),
                'qualification_url': accomplishment.xpath
                ("./following-sibling::a[@data-xds='Hyperlink']/@href").get()
            }

        # Profile links
        url = (profile_container.xpath(
            "//div[@id='ContactsModule']//iframe[@id='tab-content']/@src").
            get())
        response['web_profiles'] = await cls.get_web_profiles(page, url)

        # Interests
        xing_interest_hobbies = ([interest.get().strip() for interest
                                  in profile_container.xpath(
            "//div[@id='ProfileInterestsModule']//div[@data-xds='Tag']"
            "/div/span/text()"
        )
        ])
        response['interests'] = {
            'xing_interests': xing_interest_hobbies
        }

        # Profile stats
        stats = profile_container.xpath(
            "//div[@id='ProfileStatsModule']//div/div[./p[@data-xds='BodyCopy'"
            "] and ./div]/div/text()").get().split('/')
        stats = [stat.strip() for stat in stats]

        response['stats'] = {
            'member_since': stats[0],
            'profile_visits': stats[1]
        }

        location = {
            'current_location': {
                'xing_location': xing_location
            }
        }

        private_address = contact_details.get('private', {}).get('address')
        business_address = contact_details.get(
            'business', {}).get('xing_business_address')
        if contact_details and private_address:
            location = {**location, **private_address}
        elif contact_details and business_address:
            location = {**location, **business_address}

        about_me = profile_container.xpath(
            ".//div[@id='ProfileAboutMeModule']//p[@data-xds='BodyCopy'"
            "]/text()").get()

        personal_details = {
            'name': {
                'full_name': {
                    'xing_full_name': full_name
                }
            },

            'location': location,

            'email': {
                'xing_private_email': contact_details.get('private', {}).get(
                    'xing_private_email', None),
                'xing_business_email': contact_details.get('business', {}).get(
                    'xing_business_email')
            },
            'phone': {
                'xing_business_phone': contact_details.get('business', {}).get(
                    'xing_business_phone')
            },
            'visuals': {
                'profile_photo': {
                    'xing_profile_picture': xing_profile_picture
                }
            },
            'languages': {
                'xing_languages': xing_languages
            }
        }
        response['personal_details'] = personal_details

        biographic_details = {
            'education': {
                'xing_schools': xing_schools
            },
            'work': {
                'xing_work': {
                    'positions': positions,
                    'skills': skills,
                    'qualifications_achievements': accomplishments
                }
            },
            'description_bio_intro': {
                'xing_profile_about_me': about_me
            }
        }
        response['biographic_details'] = biographic_details
        response['source'] = 'xing'

        match = re.search(r'/profile/([^/]+)(/web_profiles)?$', profile_url)
        username = match.group(1)
        network_signature = {
            "username": {
                "xing_username": username
            },
            "misc": {
                "xing_profile_type": xing_profile_type
            }
        }
        response['network_signature'] = network_signature

        # NOTE: debug only
        # with open('response.json', 'w') as f:
        #     json.dump(response, f)

        return response

    @classmethod
    async def get_more_data(cls, page, surn, profile_url, is_school=False):
        if not surn:
            return None

        response = {}

        match = re.search(r'/profile/([^/]+)(/web_profiles)?$', profile_url)
        username = match.group(1)

        timeline_url = "https://www.xing.com/profile/my_profile/timeline/show"
        url = f'{timeline_url}/{username}/{surn}'

        # Go to the profiles
        try:
            await page.goto(url, timeout=60000)
        except Exception:
            return response
        await page.wait_for_load_state()
        await asyncio.sleep(2)
        # NOTE: debug only
        # await page.screenshot(path="screenshot_web-profiles.png",
        #                       full_page=True)
        html = await page.content()
        selector = Selector(html)

        if not is_school:
            response['location'] = selector.xpath(
                ".//dt[text()='Location']/following-sibling::dd/text()").get()
            response['company_industry'] = selector.xpath(
                ".//dt[text()='Industry']/following-sibling::dd/text()").get()
            response['company_website_url'] = selector.xpath(
                ".//a[@rel='noopener noreferrer']/@href").get()
            response['company_number_of_employees'] = selector.xpath(
                ".//dt[text()='No. of employees']/following-sibling::dd/text()"
            ).get()
        else:
            response['degree_type'] = selector.xpath(
                ".//dt[text()='Degree']/following-sibling::dd/text()").get()
        return response

    # NOTE: Maybe not needed anymore but left as workaround id
    # auth does not work well
    @classmethod
    async def get_logged_out_data(cls, selector):
        response = {}
        # profile container object
        profile_container = selector.xpath(
            "//div[contains(@class, 'profile_view-profile_view')]")
        for _xing_id in profile_container.xpath("//div[contains(@class, 'src-xing_id-container')]"):  # noqa
            response['full_name'] = _xing_id.xpath("//h1/text()").get()
            response['photo'] = _xing_id.xpath(
                "//img[contains(@class, 'super-ellipsestyles__Image')]/@src"
            ).get()
            response['occupation'] = _xing_id.xpath(
                "//div[contains(@class, "
                "'occupations-occupations-occupationText')]/p/text()").get()
            response['profile_type'] = _xing_id.xpath(
                "//div/div/button/span/span/text()").get()
            # NOTE: for some reason at page location at English,
            # here is localized
            response['location'] = "{}{}".format(
                _xing_id.xpath(
                    "//div[contains(@class, 'location-location-locationText')"
                    "]/p/strong/text()").get(),
                _xing_id.xpath(
                    "//div[contains(@class, 'location-location-locationText')"
                    "]/p/text()").get()
            )

        # skills extraction
        response['skills'] = (
            [skill.get().strip() for skill
             in profile_container.xpath(
                "//div[@data-qa='skills-section']//div[@data-qa='skills-tags']"
                "/text()")])
        timeline_container = profile_container.xpath(
            "//div[@data-qa='timeline-section']")

        # timeline work experience
        work = timeline_container.xpath("//li[@data-qa='we-entry']")
        for key, item in enumerate(work):
            _item = Selector(item.get())

            # parse duration
            intervals = _item.xpath(
                "//div[contains(@class, 'entry-time')]/p/text()").get()
            duration, period, = cls.parse_duration_and_period(intervals)

            work[key] = {
                'duration': duration,
                'period': period,
                'occupation': _item.xpath(
                    "//h4[contains(@class, 'entry-occupation')]/text()").get(),
                'organization': _item.xpath(
                    "//*[contains(@class, 'entry-organization')]/text()"
                ).get(),
                'organization_url': _item.xpath(
                    "//a[contains(@class, 'entry-organization')]/@href").get(),
                'organization_logo': _item.xpath("//img/@src").get(),
                'description': _item.xpath(
                    "//p[contains(@class, 'bottom_description-description')]/"
                    "text()").get(),
            }
        response['work'] = work

        # timeline education experience
        education = timeline_container.xpath(
            "//li[@data-qa='education-entry']")
        for key, item in enumerate(education):
            _item = Selector(item.get())

            # parse duration
            intervals = _item.xpath(
                "//div[contains(@class, 'entry-time')]/p/text()").get()
            duration, period, = cls.parse_duration_and_period(intervals)

            education[key] = {
                'duration': duration,
                'period': period,
                'occupation': _item.xpath(
                    "//h4[contains(@class, 'entry-occupation')]/text()").get(),
                'organization': _item.xpath(
                    "//*[contains(@class, 'entry-organization')]/text()"
                ).get(),
                'organization_url': _item.xpath(
                    "//a[contains(@class, 'entry-organization')]/@href").get(),
                'organization_logo': _item.xpath("//img/@src").get(),
                'description': _item.xpath(
                    "//p[contains(@class, 'bottom_description-description')]/"
                    "text()").get(),
            }
        response['education'] = education

        # languages
        language_container = profile_container.xpath(
            "//div[@data-qa='language-skills-section']")
        languages = language_container.xpath(
            "//li[contains(@class, 'language_snippet-container')]")
        for key, item in enumerate(languages):
            _item = Selector(item.get())
            languages[key] = {
                'language': _item.xpath("//h3/text()").get(),
                'grade': _item.xpath(
                    "//p[contains(@class, 'language_snippet-levelTitle')]/"
                    "text()").get(),
            }
        response['languages'] = languages

        # interests extraction
        response['interests'] = ([interest.get().strip() for interest
                                  in profile_container.xpath(
            "//div[@data-qa='interests-section']//span[contains(@class, "
            "'tagstyles__TextTruncation')]/div/text()"
        )
        ])
        return response

    @classmethod
    async def get_web_profiles(cls, page, url):
        if not url:
            return None

        # Go to the profiles
        try:
            await page.goto(url, timeout=60000)
        except Exception:
            return None

        await page.wait_for_load_state()
        await asyncio.sleep(2)
        # NOTE: debug only
        # await page.screenshot(path="screenshot_web-profiles.png",
        #                       full_page=True)
        html = await page.content()
        selector = Selector(html)

        # Parsing the links using json
        links = selector.xpath(
            "//div[contains(@class, 'links')]/@data-links").get()
        if links:
            links = json.loads(links)

        return links

    @classmethod
    async def get_contact_details(cls, page, profile_url):
        url = profile_url + r'/xing-id/contact-details'
        response = dict()

        # Go to the contact details page
        try:
            await page.goto(url, timeout=60000)
        except Exception:
            return response

        await page.wait_for_load_state()
        await asyncio.sleep(2)
        html = await page.content()
        selector = Selector(html)

        # NOTE: debug only
        # with open('contact_details.html', 'w') as f:
        #     f.write(html)

        # Business
        business_section = selector.xpath(
            "//h2[@data-xds='Headline' and text()='Business']"
            "/following-sibling::div[position()=1]")
        business = dict()

        # Business Address
        address_container = business_section.xpath(
            "//div[@id='profile-contact-label-adress']"
            "/following-sibling::div[position()=1]")

        if address_container:
            business['xing_business_address'] = {
                'xing_street_address': address_container.xpath(
                    ".//div[@data-qa='profile-contact-street-address']/text()"
                ).get(),
                'xing_zip_address': address_container.xpath(
                    ".//div[@data-qa='profile-contact-zip-address']/text()"
                ).get(),
                'xing_country_province_address': address_container.xpath(
                    ".//div[@data-qa='profile-contact-country-province-address"
                    "']/text()").get(),
            }
        else:
            business['xing_business_address'] = None

        # Business Email
        business['xing_business_email'] = business_section.xpath(
            ".//div[text()='E-mail']/following-sibling::div[position()=1]"
            "/a/text()").get()

        # Business phone
        business['xing_business_phone'] = business_section.xpath(
            ".//div[text()='Mobile']/following-sibling::div[position()=1]"
            "/a/text()").get()

        # Private
        private_section = selector.xpath(
            "//h2[@data-xds='Headline' and text()='Private']"
            "/following-sibling::div[position()=1]")
        private = dict()

        # Private Address
        address_container = private_section.xpath(
            ".//div[@id='profile-contact-label-adress']"
            "/following-sibling::div[position()=1]")

        if address_container:
            private['address'] = {
                'xing_street_address': address_container.xpath(
                    ".//div[@data-qa='profile-contact-street-address']/text()"
                ).get(),
                'xing_zip_address': address_container.xpath(
                    ".//div[@data-qa='profile-contact-zip-address']/text()"
                ).get(),
                'xing_country_province_address': address_container.xpath(
                    ".//div[@data-qa='profile-contact-country-province-address"
                    "']/text()").get(),
            }
        else:
            private['address'] = None

        # Private Email
        private['xing_private_email'] = private_section.xpath(
            ".//div[text()='E-mail']/following-sibling::"
            "div[position()=1]/a/text()").get()

        response['business'] = business
        response['private'] = private

        return response

    @classmethod
    async def login(cls, context, username, password):
        # check session for expiration. if not expired use session.
        # otherwise login required
        try:
            cookies = await context.cookies()
            for cookie in cookies:
                # full name looks like "name":
                # "ab.storage.sessionId.bd5d74db-085a-4722-a85a-7080dbaa6faa"
                if "sessionId" in cookie['name']:
                    cookie_value = unquote(cookie['value'])
                    cookie_value = json.loads(cookie_value)
                    # NOTE: maybe UTC could an issue
                    # TODO: Timestamp in cookies used as integer with
                    # 1000 multiplier like 1709639440208
                    if datetime.now() < datetime.fromtimestamp(
                            cookie_value.get('e', datetime.now())/1000):
                        logger.debug("Session used")
                        return True
        except Exception:
            logger.debug("login used")
            pass
        await context.clear_cookies()
        page = await context.new_page()
        await page.goto("https://login.xing.com", timeout=60000)
        await asyncio.sleep(1)
        await page.wait_for_load_state()

        consent_btn = page.locator("#consent-accept-button")
        if await consent_btn.is_visible():
            await consent_btn.click()
        # NOTE: debug only
        # await page.screenshot(path="login_screenshot.png", full_page=True)

        await page.locator("#username").fill(username)
        await page.locator("#password").fill(password)
        await page.locator("#perm").check()
        await page.locator("button[type='submit']").dispatch_event('click')
        await page.wait_for_load_state()
        return True

    @classmethod
    def parse_duration_and_period(cls, intervals):
        try:
            duration, period = intervals.split(",")
            duration = parse_timedelta(
                duration.strip().replace("and", '')).days
            duration = {
                "years": duration // 365,
                "months": (duration - (duration // 365) * 365) // 30
            }
        except Exception:
            duration = None
        # parse period
        # TODO: for some reason in try ... except ... it release none
        # even without exception code work well
        try:
            # If there is no duration the date may be formatted
            # as: "YYYY - YYYY"
            if duration:
                period = period.split("-")
            else:
                period = intervals.split("-")

            date_from = None
            date_to = None
            if len(period) == 2:
                date_from, date_to = period
            else:
                date_from = period[0]
            period = {
                'date_from': date_from.strip(),
                'date_to': date_to.strip()
            }

            # In case of "YYYY - YYYY"(1999 - 2002) calulate duration
            if not duration:
                try:
                    duration = {
                        # Same year range(ie: 1999-1999) will be considered
                        # 1 year instead of 0
                        "years": max(int(date_to.strip()) - int(
                            date_from.strip()), 1),
                        "months": 0
                    }

                except Exception as e:
                    logger.error(e)
                    duration = None
        except Exception:
            period = None

        return duration, period
