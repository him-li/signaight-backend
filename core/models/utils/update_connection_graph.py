from typing import List

import networkx as nx
import urllib.parse
from glom import glom
from networkx.readwrite import json_graph
from core.config import settings
from core.fields import S3Path
from core.utils.socials_list import SOCIALS


class GraphBuilder:

    def __init__(self):
        self.G = nx.DiGraph()

    def safe_get(self, obj, *attrs, default):
        spec = ".".join(attrs)

        try:
            data = glom(obj, spec, default=default)
            if not data:
                return default
            return data
        except Exception:
            return default

    def extract_full_name(self, person: dict, platform: str | None = None):

        first = None
        last = None

        if platform:
            first = self.safe_get(
                person,
                "personal_details",
                "name",
                "first_name",
                f"{platform}_f_name",
                default=None,
            )

            last = self.safe_get(
                person,
                "personal_details",
                "name",
                "last_name",
                f"{platform}_l_name",
                default=None,
            )

        # fallback to generic
        if not first:
            first = self.safe_get(
                person,
                "personal_details",
                "name",
                "first_name",
                "f_name",
                default=None,
            )

        if not last:
            last = self.safe_get(
                person,
                "personal_details",
                "name",
                "last_name",
                "l_name",
                default=None,
            )
        if not first and not last:
            for social in SOCIALS:
                first = self.safe_get(
                    person,
                    "personal_details",
                    "name",
                    "first_name",
                    f"{social}_f_name",
                    default=None,
                )

                last = self.safe_get(
                    person,
                    "personal_details",
                    "name",
                    "last_name",
                    f"{social}_l_name",
                    default=None,
                )
                if first or last:
                    break

        return " ".join(filter(None, [first, last])) or None

    def extract_platform_picture(self, person, platform: str):
        picture = self.safe_get(
            person,
            "personal_details",
            "visuals",
            "profile_photo",
            f"{platform}_profile_picture",
            default=None,
        )

        return str(picture) if picture else None

    def extract_profile_picture(self, person, platform: str | None = None):
        picture = None

        if platform:
            picture = self.extract_platform_picture(person, platform)

        if not picture:
            picture = self.safe_get(
                person,
                "personal_details",
                "visuals",
                "profile_photo",
                "profile_picture",
                default=None,
            )

        if not picture:
            for social in SOCIALS:
                picture = self.safe_get(
                    person,
                    "personal_details",
                    "visuals",
                    "profile_photo",
                    f"{social}_profile_picture",
                    default=None,
                )
                if picture:
                    break

        return self.get_presigned_link_picture(picture) if picture else None

    def get_presigned_link_picture(self, picture):
        try:
            if isinstance(picture, S3Path):
                return picture.as_url(
                    presign=True, expire_seconds=settings.AWS_S3_PRESIGNED_LINKS_TTL
                )
            return None
        except AttributeError:
            return None

    def add_interests(self, person_node: str, person: dict):

        interests = self.safe_get(person, "interests", default=None)

        if not interests:
            return

        # FACEBOOK PAGES
        pages = self.safe_get(person, "interests.pages", default=[])

        for page in pages:

            page_id = self.safe_get(page, "fb_page_id", default=None)

            if not page_id:
                continue

            page_node = f"fb_page:{page_id}"

            picture = self.safe_get(page, "fb_page_profile_photo", default=None)

            node_data = {
                "name": self.safe_get(page, "fb_page_name", default=None),
                "url": self.safe_get(page, "fb_page_url", default=None),
            }

            if picture:
                node_data["picture"] = self.get_presigned_link_picture(picture)

            self.G.add_node(
                page_node,
                type="interest_page",
                platform="facebook",
                **node_data,
            )

            self.G.add_edge(
                person_node,
                page_node,
                relation="likes_page",
            )

        # TELEGRAM GROUPS
        telegram_groups = self.safe_get(
            person,
            "interests.groups.telegram_groups",
            default=[],
        )

        for group in telegram_groups:

            group_id = self.safe_get(group, "telegram_public_group_id", default=None)

            if not group_id:
                continue

            group_node = f"telegram_group:{group_id}"

            self.G.add_node(
                group_node,
                type="interest_group",
                platform="telegram",
                title=self.safe_get(group, "title", default=None),
            )

            self.G.add_edge(
                person_node,
                group_node,
                relation="member_of_group",
            )

        # LINKEDIN INTERESTS
        linkedin_interests = self.safe_get(
            person,
            "interests",
            "linkedin_interests",
            default=[],
        )
        if linkedin_interests:

            for li in linkedin_interests:

                profile_url = self.safe_get(li, "linkedin_profile_url", default=None)

                if not profile_url:
                    continue

                li_node = f"linkedin_interest:{profile_url}"

                self.G.add_node(
                    li_node,
                    type="interest_linkedin",
                    platform="linkedin",
                    name=self.safe_get(li, "linkedin_full_name", default=None),
                    picture=self.get_presigned_link_picture(
                        self.safe_get(li, "linkedin_profile_picture", default=None)
                    ),
                    url=profile_url,
                )

                self.G.add_edge(
                    person_node,
                    li_node,
                    relation="linkedin_interest",
                )

        # =====================================================
        # XING INTERESTS
        # =====================================================
        xing_interests = self.safe_get(
            person,
            "interests.xing_interests",
            default=[],
        )
        if xing_interests:

            for xing in xing_interests:

                if not xing:
                    continue

                xing_node = f"xing_interest:{xing}"

                self.G.add_node(
                    xing_node,
                    type="interest_xing",
                    platform="xing",
                )

                self.G.add_edge(
                    person_node,
                    xing_node,
                    relation="xing_interest",
                )

    def extract_user_ids(self, user_id_obj) -> list[tuple[str, str]]:
        """
        Returns list of (platform, user_id)
        """
        if not user_id_obj:
            return []

        result = []

        for field_name, value in user_id_obj.items():
            if not value:
                continue

            # skip variants
            if field_name == "user_id_variants":
                continue

            if field_name.endswith("_user_id"):
                platform = field_name.replace("_user_id", "")
                result.append((platform, value))

        return result

    def extract_user_ids_matched_profiles(self, matched_profiles) -> list[dict]:
        if not matched_profiles:
            return []

        result = []
        for platform, item in matched_profiles.items():
            if not item:
                continue

            for candidate in (
                self.safe_get(item, "primary_candidate", default={}).values()
                if self.safe_get(item, "primary_candidate", default=None)
                else []
            ):
                candidate_data = {
                    "platform": platform,
                    "profile_id": self.safe_get(candidate, "profile_id", default=None),
                    "profile_username": self.safe_get(
                        candidate, "profile_username", default=None
                    ),
                    "profile_url": self.safe_get(
                        candidate, "profile_url", default=None
                    ),
                    "profile_picture": self.get_presigned_link_picture(
                        self.safe_get(candidate, "profile_picture", default=None)
                    ),
                    "full_name": self.safe_get(candidate, "full_name", default=None),
                }
                result.append(candidate_data)

        return result

    def _get_follow_candidates(self, person_node: str) -> list[str]:
        """Platform-specific candidates with cross-platform fallback."""
        matched_profiles = self.G.nodes[person_node].get("matched_profiles", {})
        platform_matches = [cid for cid in matched_profiles]
        return platform_matches

    def add_connections(self, person_node, person):
        connections = self.safe_get(person, "connections", default={})
        facebook_friends = self.safe_get(connections, "friends.facebook", default=[])
        if facebook_friends:
            data_url = "icon::people"

            connections_node = f"social_connections:{person_node}"

            self.G.add_node(
                connections_node,
                type="social_connections",
                picture=data_url,
                name="social connections",
            )
            self.G.add_edge(
                person_node,
                connections_node,
                relation="has_connections",
            )

        instagram_followers = self.safe_get(
            connections, "followers.instagram", default=[]
        )
        facebook_followers = self.safe_get(
            connections, "followers.facebook", default=[]
        )
        instagram_following = self.safe_get(
            connections, "following.instagram", default=[]
        )
        facebook_following = self.safe_get(
            connections, "following.facebook", default=[]
        )

        # FRIENDS
        if facebook_friends:
            for f in facebook_friends:
                node = f"facebook:{self.safe_get(f, 'facebook_user_id', default=None)}"
                platform = "facebook"
                name = self.safe_get(f, "facebook_full_name", default=None)
                url = self.safe_get(f, "facebook_profile_url", default=None)
                picture = self.get_presigned_link_picture(
                    self.safe_get(f, "facebook_profile_picture", default=None)
                )
                node_data = {
                    "name": name,
                    "url": url,
                }

                if picture:
                    node_data["picture"] = picture
                self.G.add_node(node, type="candidate", platform=platform, **node_data)
                # to support link analysis logic per person
                self.G.add_edge(person_node, node, relation="connection_friend")
                for candidate_id in self._get_follow_candidates(person_node):
                    if self.G.has_node(candidate_id):
                        self.G.add_edge(candidate_id, node, relation="friend")

        # FOLLOWERS
        if instagram_followers:
            for f in instagram_followers:
                node = (
                    f"instagram:{self.safe_get(f, 'instagram_user_id', default=None)}"
                )
                user_name = self.safe_get(f, "instagram_username", default=None)
                url = None
                if user_name:
                    url = f"https://www.instagram.com/{user_name}"

                self.G.add_node(
                    node,
                    type="candidate",
                    platform="instagram",
                    picture=self.get_presigned_link_picture(
                        self.safe_get(f, "instagram_profile_picture", default=None)
                    ),
                    name=self.safe_get(f, "instagram_full_name", default=None),
                    url=url
                )
                for candidate_id in self._get_follow_candidates(person_node):
                    self.G.add_edge(node, candidate_id, relation="follows")

        if facebook_followers:
            for f in facebook_followers:
                node = f"facebook:{self.safe_get(f, 'facebook_user_id', default=None)}"

                self.G.add_node(
                    node,
                    type="candidate",
                    platform="facebook",
                    picture=self.get_presigned_link_picture(
                        self.safe_get(f, "facebook_profile_picture", default=None)
                    ),
                    name=self.safe_get(f, "facebook_full_name", default=None),
                    url=self.safe_get(f, "facebook_profile_url", default=None),
                )
                for candidate_id in self._get_follow_candidates(person_node):
                    self.G.add_edge(node, candidate_id, relation="follows")

        # FOLLOWING — edges are reversed (node → candidate_id) so that when
        # combined with FOLLOWERS edges (candidate_id → node) the bidirectional
        # detection in rewrite_relationships fires correctly for mutual follows.
        if instagram_following:
            for f in instagram_following:
                node = f"instagram:{self.safe_get(f, 'instagram_user_id', default=None)}"
                user_name = self.safe_get(f, "instagram_username", default=None)
                url = None
                if user_name:
                    url = f"https://www.instagram.com/{user_name}"

                self.G.add_node(
                    node,
                    type="candidate",
                    platform="instagram",
                    picture=self.get_presigned_link_picture(
                        self.safe_get(f, "instagram_profile_picture", default=None)
                    ),
                    name=self.safe_get(f, "instagram_full_name", default=None),
                    url=url,
                )
                for candidate_id in self._get_follow_candidates(person_node):
                    if self.G.has_node(candidate_id):
                        self.G.add_edge(candidate_id, node, relation="follows")

        if facebook_following:
            for f in facebook_following:
                node = (
                    f"facebook:{self.safe_get(f, 'facebook_user_id', default=None)}"
                )

                self.G.add_node(
                    node,
                    type="candidate",
                    platform="facebook",
                    picture=self.get_presigned_link_picture(
                        self.safe_get(f, "facebook_profile_picture", default=None)
                    ),
                    name=self.safe_get(f, "facebook_full_name", default=None),
                    url=self.safe_get(f, "facebook_profile_url", default=None),
                )
                for candidate_id in self._get_follow_candidates(person_node):
                    if self.G.has_node(candidate_id):
                        self.G.add_edge(candidate_id, node, relation="follows")

    def add_network_signature(self, person_node: str, person: dict):
        matched_profiles = self.safe_get(
            person, "network_signature", "matched_profiles", default={}
        )

        if not matched_profiles:
            return

        identities = self.extract_user_ids_matched_profiles(matched_profiles)

        for identity in identities:

            platform = self.safe_get(identity, "platform", default=None)
            profile_id = self.safe_get(identity, "profile_id", default=None)

            if not platform or not profile_id:
                continue

            node_id = f"{platform}:{profile_id}"
            name = self.safe_get(identity, "full_name", default=None)
            url = self.safe_get(identity, "profile_url", default=None)
            picture = self.safe_get(identity, "profile_picture", default=None)
            node_data = {
                "name": name,
                "url": url,
            }

            if picture:
                node_data["picture"] = self.get_presigned_link_picture(picture)

            self.G.add_node(
                node_id,
                type="candidate",
                platform=platform,
                **node_data,
                person=person_node,
            )
            if self.G.has_node(person_node):
                if not self.G.nodes[person_node].get("matched_profiles"):
                    self.G.nodes[person_node]["matched_profiles"] = {}
                self.G.nodes[person_node]["matched_profiles"][node_id] = True

            self.G.add_edge(
                person_node, node_id, relation="primary_candidate", platform=platform
            )

    def extract_schools(self, education):
        if not education:
            return []

        result = []
        linkedin_schools = self.safe_get(education, "linkedin_schools", default=[])
        facebook_schools = self.safe_get(education, "facebook_schools", default=[])
        xing_schools = self.safe_get(education, "xing_schools", default=[])
        school_variants = self.safe_get(education, "school_variants", default=[])

        # LinkedIn
        if linkedin_schools:
            for school in linkedin_schools:
                result.append(
                    {
                        "name": self.safe_get(school, "school_name", default=None),
                        "degree": self.safe_get(school, "degree_name", default=None),
                        "field": self.safe_get(school, "education_field", default=None),
                        "period": self.safe_get(school, "period", default=None),
                        "platform": "linkedin",
                        "url": self.safe_get(school, "school_url", default=None),
                        "picture": self.get_presigned_link_picture(
                            self.safe_get(school, "school_logo_url", default=None)
                        ),
                    }
                )

        # Facebook
        if facebook_schools:
            for school in facebook_schools:
                result.append(
                    {
                        "name": self.safe_get(school, "fb_school_name", default=None),
                        "degree": None,
                        "field": self.safe_get(
                            school, "fb_education_field", default=None
                        ),
                        "period": self.safe_get(school, "period", default=None),
                        "platform": "facebook",
                        "url": self.safe_get(school, "fb_school_url", default=None),
                        "picture": self.get_presigned_link_picture(
                            self.safe_get(school, "fb_school_photo", default=None)
                        ),
                    }
                )

        # Xing
        if xing_schools:
            for school in xing_schools:
                result.append(
                    {
                        "name": self.safe_get(school, "school_name", default=None),
                        "degree": self.safe_get(school, "degree_name", default=None),
                        "field": self.safe_get(school, "education_field", default=None),
                        "period": self.safe_get(school, "period", default=None),
                        "platform": "xing",
                        "url": self.safe_get(school, "school_url", default=None),
                        "picture": self.safe_get(
                            school, "school_logo_url", default=None
                        ),
                    }
                )

        # Variants
        if school_variants:
            for school in school_variants:
                result.append(
                    {
                        "name": self.safe_get(school, "school_name", default=None),
                        "degree": self.safe_get(school, "degree_name", default=None),
                        "field": self.safe_get(school, "education_field", default=None),
                        "period": self.safe_get(school, "period", default=None),
                        "platform": "variant",
                        "url": self.safe_get(school, "school_url", default=None),
                        "picture": self.safe_get(
                            school, "school_logo_url", default=None
                        )
                        or self.safe_get(school, "school_photo", default=None),
                    }
                )

        return result

    def extract_work_positions(self, work):
        if not work:
            return []

        result = []
        linkedin_work_positions = self.safe_get(
            work, "linkedin_work.positions", default=[]
        )
        facebook_work = self.safe_get(work, "facebook_work", default=None)
        xing_work = self.safe_get(work, "xing_work", default=None)

        # LinkedIn
        if linkedin_work_positions:
            for pos in linkedin_work_positions:
                result.append(
                    {
                        "company": self.safe_get(pos, "company_name", default=None),
                        "title": self.safe_get(pos, "title", default=None),
                        "period": self.safe_get(pos, "period", default=None),
                        "platform": "linkedin",
                        "url": self.safe_get(pos, "linkedin_company_url", default=None),
                        "picture": self.safe_get(pos, "company_logo_url", default=None),
                    }
                )

        # Facebook
        if facebook_work:
            for fb in facebook_work:
                result.append(
                    {
                        "company": self.safe_get(fb, "fb_workplace_name", default=None),
                        "title": self.safe_get(fb, "fb_work_title", default=None),
                        "period": self.safe_get(fb, "fb_work_period", default=None),
                        "platform": "facebook",
                        "url": self.safe_get(fb, "fb_workplace_url", default=None),
                        "picture": self.safe_get(
                            fb, "fb_workplace_photo_url", default=None
                        ),
                    }
                )

        # Xing
        if xing_work and xing_work.positions:
            for pos in xing_work.positions:
                result.append(
                    {
                        "company": self.safe_get(pos, "company_name", default=None),
                        "title": self.safe_get(pos, "title", default=None),
                        "period": self.safe_get(pos, "period", default=None),
                        "platform": "xing",
                        "url": self.safe_get(pos, "company_url", default=None),
                        "picture": self.safe_get(pos, "company_logo", default=None),
                    }
                )

        return result

    def add_work(self, person_node: str, person: dict):

        positions = self.extract_work_positions(
            self.safe_get(person, "biographic_details.work", default=None)
        )
        work_node = f"work:{person_node}"

        data_url = "icon::work"

        if positions:
            self.G.add_node(
                work_node, type="work", picture=data_url, name="work experience"
            )
            self.G.add_edge(
                person_node,
                work_node,
                relation="has_work",
            )

        for pos in positions:
            company = self.safe_get(pos, "company", default=None)
            if not company:
                continue

            company_node = f"company:{company.strip().lower()}"

            picture = self.get_presigned_link_picture(
                self.safe_get(pos, "picture", default=None)
            )

            node_data = {
                "name": company,
                "url": self.safe_get(pos, "url", default=None),
                "type": "company",
            }

            if picture or data_url:
                node_data["picture"] = str(picture) if picture else data_url

            # Add node only if not exists
            if company_node not in self.G:
                self.G.add_node(company_node, **node_data)
            else:
                # Do not overwrite existing data
                existing = self.G.nodes[company_node]

                if not existing.get("picture") and (picture or data_url):
                    existing["picture"] = str(picture) if picture else data_url

                if not self.safe_get(existing, "url", default=None) and self.safe_get(
                    pos, "url", default=None
                ):
                    existing["url"] = self.safe_get(pos, "url", default=None)

            # Add edge (extra info lives here)
            self.G.add_edge(
                person_node,
                company_node,
                relation="worked_at",
                title=self.safe_get(pos, "title", default=None),
                period=(
                    str(self.safe_get(pos, "period", default=None))
                    if self.safe_get(pos, "period", default=None)
                    else None
                ),
                platform=self.safe_get(pos, "platform", default=None),
            )

    def add_education(self, person_node: str, person: dict):

        schools = self.extract_schools(
            self.safe_get(person, "biographic_details.education", default=None)
        )
        edu_node = f"education:{person_node}"

        data_url ="icon::school"

        if schools:
            self.G.add_node(
                edu_node, type="education", picture=data_url, name="education"
            )
            self.G.add_edge(
                person_node,
                edu_node,
                relation="has_education",
            )

        for school in schools:
            school_name = school.get("name")
            if not school_name:
                continue

            school_node = f"school:{school_name.strip().lower()}"

            picture = self.get_presigned_link_picture(
                self.safe_get(school, "picture", default=None)
            )

            node_data = {
                "name": school_name,
                "url": self.safe_get(school, "url", default=None),
                "type": "school",
            }

            if picture or data_url:
                node_data["picture"] = str(picture) if picture else data_url

            # Add node only if not exists
            if school_node not in self.G:
                self.G.add_node(school_node, **node_data)
            else:
                existing = self.G.nodes[school_node]

                if not existing.get("picture") and picture:
                    existing["picture"] = str(picture)

                if not existing.get("url") and self.safe_get(
                    school, "url", default=None
                ):
                    existing["url"] = self.safe_get(school, "url", default=None)

            # Add edge (relationship metadata)
            self.G.add_edge(
                person_node,
                school_node,
                relation="studied_at",
                degree=self.safe_get(school, "degree", default=None),
                field=self.safe_get(school, "field", default=None),
                period=(
                    str(self.safe_get(school, "period", default=None))
                    if self.safe_get(school, "period", default=None)
                    else None
                ),
                platform=self.safe_get(school, "platform", default=None),
            )

    def extract_check_ins(self, person):
        check_ins = self.safe_get(
            person, "personal_details.location.check_ins.fb_check_ins", default=[]
        )

        if not check_ins:
            return []

        result = []

        for item in check_ins:
            if not item:
                continue

            result.append(
                {
                    "title": self.safe_get(item, "title", default=None),
                    "subtitle": self.safe_get(item, "subtitle", default=None),
                    "url": self.safe_get(item, "url", default=None),
                    "region": self.safe_get(item, "region", default=None),
                    "date": self.safe_get(item, "date", default=None),
                    "picture": self.safe_get(item, "event_image", default=None),
                }
            )

        return result

    def add_check_ins(self, person_node: str, person: dict):

        check_ins = self.extract_check_ins(person)

        if not check_ins:
            return

        checkins_node = f"checkins:{person_node}"

        data_url = "icon::hotel"

        # container node
        self.G.add_node(
            checkins_node, type="check_ins", name="check-ins", picture=data_url
        )

        self.G.add_edge(person_node, checkins_node, relation="has_check_ins")

        # individual check-ins
        for ci in check_ins:

            title = ci.get("title")
            if not title:
                continue

            node_id = f"checkin:{urllib.parse.quote(title)}"

            picture = self.get_presigned_link_picture(ci.get("picture"))

            node_data = {
                "type": "check_in_place",
                "name": title,
                "url": ci.get("url"),
                "region": ci.get("region"),
                "date": ci.get("date"),
            }

            if picture:
                node_data["picture"] = picture

            self.G.add_node(node_id, **node_data)

            self.G.add_edge(person_node, node_id, relation="checked_in")

    def extract_hometown(self, person):

        hometown = self.safe_get(
            person, "personal_details.location.hometown", default=None
        )

        if not hometown:
            return None

        return {
            "name": self.safe_get(hometown, "fb_hometown", default=None),
            "location_id": self.safe_get(hometown, "fb_location_id", default=None),
            "picture": self.safe_get(hometown, "fb_location_picture", default=None),
        }

    def add_hometown(self, person_node: str, person: dict):

        hometown = self.extract_hometown(person)

        if not hometown:
            return

        name = hometown.get("name")

        if not name:
            return

        node_id = f"hometown:{person_node}"
        has_hometown_node_id = f"has_hometown:{person_node}"
        data_url = "icon::home"

        picture = self.get_presigned_link_picture(
            self.safe_get(hometown, "picture", default=None)
        )

        node_data = {
            "type": "hometown",
            "name": name,
        }

        if picture:
            node_data["picture"] = picture

        self.G.add_node(
            has_hometown_node_id, type="has_hometown", picture=data_url, name="hometown"
        )

        self.G.add_edge(person_node, has_hometown_node_id, relation="has_hometown")

        if node_id not in self.G:
            self.G.add_node(node_id, **node_data)

        self.G.add_edge(person_node, node_id, relation="hometown")

    # -----------------------------
    # Add person node
    # -----------------------------
    def add_person(self, person: dict):

        person_id = self.safe_get(person, "id", default=None)
        if not person_id:
            return None
        node = f"person:{person_id}"

        name = self.extract_full_name(person)
        picture = self.extract_profile_picture(person)

        self.G.add_node(
            node,
            type="person",
            name=name,
            picture=picture,
            risk_score=self.safe_get(person, "risk_score", default=None),
            signaight_score=self.safe_get(person, "signaight_score", default=None),
            url=f"/analysis/{person_id}",
        )

        return node

    # Build graph for one person
    def add_person_to_graph(self, person: dict):
        person_node = self.add_person(person)

        if person_node is None:
            return

        self.add_network_signature(person_node, person)

        self.add_connections(person_node, person)

        self.add_interests(person_node, person)

        self.add_work(person_node, person)

        self.add_education(person_node, person)

        self.add_check_ins(person_node, person)

        self.add_hometown(person_node, person)

    # Build graph
    def build(self, persons: list, from_database: bool = False):

        for person in persons:
            person = person if isinstance(person, dict) else person.model_dump()
            if from_database and person.get("connection_graph"):
                try:
                    subgraph = json_graph.node_link_graph(person["connection_graph"])
                    self.G.update(subgraph)
                except Exception as e:
                    print(f"Error loading graph for person {person.get('id')}: {e}")
            else:
                self.add_person_to_graph(person)

        return self.G


FOLLOW_RELATION = "follows"


def _person_edge_exists(H, u, v):
    """Return True if H already has an edge between u and v in either direction."""
    return H.has_edge(u, v) or H.has_edge(v, u)


def _add_bidirectional_edge(H, u, v, label):
    """
    Add (or upgrade) an edge between u and v as bidirectional.
    If an edge already exists in either direction it is replaced with the
    bidirectional one so the pair is never represented twice.
    """
    # Remove the reverse edge if it exists so we end up with a single entry.
    if H.has_edge(v, u) and not H.has_edge(u, v):
        attrs = dict(H[v][u])
        H.remove_edge(v, u)
        H.add_edge(u, v, **attrs)
    H.add_edge(u, v, relation="bidirectional", label=label)


def _resolve_person(G, node):
    return G.nodes[node].get("person") or node


def rewrite_relationships(G, connection_type: List[str] = ["all"], min_degree=2):
    H = nx.DiGraph()
    H.add_nodes_from(G.nodes(data=True))

    bidirectional_nodes = set()

    include_all = "all" in connection_type

    include_bidirectional = include_all or "bidirectional" in connection_type
    include_unidirectional = include_all or "unidirectional" in connection_type
    include_likes = include_all or "likes" in connection_type
    include_groups = include_all or "groups" in connection_type

    processed = set()

    # Build person → all candidate nodes lookup for cross-platform detection
    person_candidates: dict[str, set[str]] = {}
    for node, data in G.nodes(data=True):
        person = data.get("person")
        if person:
            person_candidates.setdefault(person, set()).add(node)
        elif data.get("type") == "person":
            # Person node is its own candidate when it has direct follow edges
            person_candidates.setdefault(node, set()).add(node)

    # ── Detect bidirectional relations ────────────────────────────────────────
    if include_bidirectional:

        for u, v, data in G.edges(data=True):

            if (u, v) in processed:
                continue

            relation = data.get("relation")

            # ── Mutual follow (cross-platform aware) ──────────────────────────
            if relation == "follows":
                person_u = _resolve_person(G, u)
                person_v = _resolve_person(G, v)

                if person_u == person_v or (person_u, person_v) in processed:
                    continue

                # Collect all candidates for each person across all platforms
                candidates_u = person_candidates.get(person_u, {u})
                candidates_v = person_candidates.get(person_v, {v})

                # Mutual if any candidate of person_v follows any candidate of person_u
                mutual = any(
                    G.has_edge(cv, cu) and G[cv][cu].get("relation") == "follows"
                    for cv in candidates_v
                    for cu in candidates_u
                )

                if mutual:
                    _add_bidirectional_edge(H, person_u, person_v, "mutual follow")
                    for cu in candidates_u:
                        for cv in candidates_v:
                            processed.add((cu, cv))
                            processed.add((cv, cu))
                    processed.add((person_u, person_v))
                    processed.add((person_v, person_u))
                    bidirectional_nodes.add(person_u)
                    bidirectional_nodes.add(person_v)
                    continue

            # ── Friendship ────────────────────────────────────────────────────
            if relation == "friend":
                u_person = _resolve_person(G, u)
                v_person = _resolve_person(G, v)
                v_node_data = G.nodes[v]

                if v_node_data.get("person") or G.degree(v) >= min_degree:
                    # Only add if no bidirectional edge already exists between
                    # these two persons (mutual follow takes precedence).
                    if not (
                        H.has_edge(u_person, v_person)
                        and H[u_person][v_person].get("relation") == "bidirectional"
                    ) and not (
                        H.has_edge(v_person, u_person)
                        and H[v_person][u_person].get("relation") == "bidirectional"
                    ):
                        _add_bidirectional_edge(H, u_person, v_person, "friendship")

                    # Prevent these candidate nodes from being processed again
                    for pair in [(u, v), (v, u)]:
                        processed.add(pair)
                    for node in (u, v, u_person, v_person):
                        bidirectional_nodes.add(node)
                    continue

    # ── Add unidirectional relations ──────────────────────────────────────────
    if include_unidirectional:
        for u, v, data in G.edges(data=True):

            if (u, v) in processed:
                continue

            relation = data.get("relation")

            # Skip candidate nodes already consumed for bidirectional edges
            if u in bidirectional_nodes and v in bidirectional_nodes:
                continue

            u = _resolve_person(G, u)
            v = _resolve_person(G, v)

            # Never add a unidirectional edge when a bidirectional one already
            # exists between the same two persons (in either direction).
            if _person_edge_exists(H, u, v):
                continue

            if relation == FOLLOW_RELATION:
                H.add_edge(u, v, relation="unidirectional", label="follow")
            elif relation == "worked_at":
                H.add_edge(u, v, relation="unidirectional", label="work")
            elif relation == "studied_at":
                H.add_edge(u, v, relation="unidirectional", label="study")
            elif relation == "has_work":
                H.add_edge(u, v, relation="unidirectional", label="has_work")
            elif relation == "has_education":
                H.add_edge(u, v, relation="unidirectional", label="has_education")
            elif relation == "social_connections":
                H.add_edge(u, v, relation="unidirectional", label="social_connections")
            elif relation == "has_connections":
                H.add_edge(u, v, relation="unidirectional", label="has_connections")
            elif relation == "connection_friend":
                H.add_edge(u, v, relation="unidirectional", label="friend")
            elif relation == "checked_in":
                H.add_edge(u, v, relation="unidirectional", label="checked in")
            elif relation == "has_check_ins":
                H.add_edge(u, v, relation="unidirectional", label="has check ins")
            elif relation == "hometown":
                H.add_edge(u, v, relation="unidirectional", label="hometown")
            elif relation == "has_hometown":
                H.add_edge(u, v, relation="unidirectional", label="has hometown")

    if include_likes:
        for u, v, data in G.edges(data=True):

            if (u, v) in processed:
                continue

            relation = data.get("relation")

            if u in bidirectional_nodes and v in bidirectional_nodes:
                continue

            u = _resolve_person(G, u)
            v = _resolve_person(G, v)

            if relation == "likes_page":
                H.add_edge(u, v, relation="unidirectional", label="like")

    if include_groups:
        for u, v, data in G.edges(data=True):

            if (u, v) in processed:
                continue

            relation = data.get("relation")

            if u in bidirectional_nodes or v in bidirectional_nodes:
                continue

            u = _resolve_person(G, u)
            v = _resolve_person(G, v)

            if relation == "member_of_group" and not _person_edge_exists(H, u, v):
                H.add_edge(u, v, relation="unidirectional", label="membership")

               
    # Remove unused non-person nodes
    to_remove = [
        n
        for n, d in H.nodes(data=True)
        if d.get("type") != "person" and H.degree(n) == 0
    ]

    H.remove_nodes_from(to_remove)

    nodes_to_keep = set()

    for node, data in H.nodes(data=True):
        node_type = data.get("type")

        if node_type == "person":
            nodes_to_keep.add(node)
            continue

        if H.degree(node) >= min_degree:
            nodes_to_keep.add(node)
    new_graph = H.subgraph(nodes_to_keep).copy()

    return new_graph


def build_dynamic_view(G, node_types, edge_types):
    nodes = {n for n, d in G.nodes(data=True) if d.get("type") in node_types}

    edges = [
        (u, v)
        for u, v, d in G.edges(data=True)
        if (d.get("relation") in edge_types and u in nodes and v in nodes)
    ]

    H = G.edge_subgraph(edges).copy()

    for node, data in G.nodes(data=True):
        if data.get("type") == "person" and node not in H:
            H.add_node(node, **data)

    return H


def nx_to_cytoscape(G):
    elements = []

    # Nodes
    for node, data in G.nodes(data=True):
        elements.append({"data": {"id": node, **data}})

    # Edges
    for u, v, data in G.edges(data=True):
        elements.append(
            {
                "data": {
                    "id": f"{u}-{v}",  # unique edge id required
                    "source": u,
                    "target": v,
                    "type": "edge",
                    **data,
                }
            }
        )

    return elements
