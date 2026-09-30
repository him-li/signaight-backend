import pendulum
from typing import List, Dict
from glom import glom
from mergedeep import merge, Strategy
from functools import reduce

from core.clients.vetric.linkedin import api, VtLISpecs
from core.documents import (
    SearchRequestDoc,
    SearchResponseDoc,
    EnrichRequestDoc,
    EnrichResponseDoc
)
from core.dotty_dictionary import dotty
from core.logging import logger
from core.utils import parse_vtrc_li_period
from ..config import settings


class VetricLinkedinAPI():

    resource = "vetric"

    async def search(
            self,
            doc: SearchRequestDoc
    ) -> List[SearchResponseDoc]:
        params = {"firstName": doc.f_name,
                  "lastName": doc.l_name,
                  "keywords": doc.name if doc.name else "*"
                  }
        docs = []
        mapped_results = []
        cursor = None
        has_more_results = True
        while (has_more_results and
               (len(mapped_results) <
                settings.VETRIC_LINKEDIN_CANDIDATES_LIMIT)):
            try:
                if cursor:
                    params['cursor'] = cursor
                response = await api.async_search.people(params=params)
                response_body = response.body
            except Exception as e:
                logger.error(f"VetricLinkedinApin search error: {str(e)}")
                return docs

            spec = VtLISpecs.search_spec
            search_results = glom(response_body, spec)
            mapped_results.extend(search_results)
            cursor = response_body.get("cursor")
            total_matches = response_body.get("total_matches")
            if not cursor or len(mapped_results) >= total_matches:
                has_more_results = False
                break

        try:
            for result in mapped_results:
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
                            "linkedin_full_name": result.get(
                                "personal_details").get("name").get(
                                    "full_name").get("linkedin_full_name")
                        }
                    },
                    "email": {
                        "email_address": ([doc.email_address] if
                                          doc.email_address else None)
                    },
                    "visuals": {
                        "profile_photo": {
                            "linkedin_profile_picture": result.get(
                                "personal_details").get("visuals").get(
                                    "profile_photo").get(
                                        "linkedin_profile_picture")
                        }
                    },
                    "location": {
                        "current_city_region_country": {
                            "linkedin_search_location": result.get(
                                "personal_details").get("location").get(
                                    "current_city_region_country").get(
                                        "linkedin_search_location")
                        }
                    }
                }
                result["personal_details"] = personal_details
                headline = result.get(
                    "biographic_details").get(
                        "description_bio_intro").get("linkedin_headline")
                if "|" in headline:
                    headline = headline.split("|")[0]
                if "at" in headline:
                    index = headline.index("at")
                    title = headline[:index].strip()
                    company_name = headline[index+2:].strip()
                    position = {
                        "title": title,
                        "company_name": company_name
                    }
                    bio_details = result.get("biographic_details")
                    bio_details = {
                        "biographic_details": {**bio_details, "work": {
                            "linkedin_work": {"positions": [position]}}}}
                    result.update(bio_details)
                elif "@" in headline:
                    index = headline.index("@")
                    title = headline[:index].strip()
                    company_name = headline[index+1:].strip()
                    position = {
                        "title": title,
                        "company_name": company_name
                    }
                    bio_details = result.get("biographic_details")
                    bio_details = {
                        "biographic_details": {**bio_details, "work": {
                            "linkedin_work": {"positions": [position]}}}}
                    result.update(bio_details)
                else:
                    pass
                result["resource"] = self.resource
                result["urn"] = doc.urn
                result["search_id"] = doc.search_id
                _doc = SearchResponseDoc(**result)
                docs.append(_doc)
        except Exception as e:
            print(e)
            pass
        return docs

    async def enrich(self, doc: EnrichRequestDoc) -> EnrichResponseDoc:
        if doc.source_id is None:
            doc.source_id = await self._resolve_URL(doc.profile_url)
        in_docs = []
        funcs = [
            '_enrich_overview',
            '_enrich_experience',
            '_enrich_skills',
            '_enrich_education',
            '_enrich_recommendations_received',
            '_enrich_contact_info',
            '_enrich_licences_certifications',
            '_enrich_volunteering',
            '_enrich_honors_awards',
            '_enrich_activity',
            '_enrich_courses',
            '_enrich_publications',
            '_enrich_projects',
            '_enrich_interests_influencers',
            '_enrich_test_scores',
            '_enrich_languages',
        ]

        for _func in funcs:
            try:
                func = getattr(self, _func)
                if result := await func(doc):
                    in_docs.append(result)
                logger.debug(f"{_func} done")
            except Exception as e:
                logger.error(f"{_func}: {str(e)}")
        if not in_docs:
            return
        _doc = merge(*in_docs, strategy=Strategy.REPLACE)
        _doc['urn'] = doc.urn
        _doc['source'] = 'linkedin'
        _doc = EnrichResponseDoc(**_doc)
        return _doc

    async def _resolve_URL(
            self,
            profile_url) -> str:
        try:
            params = {"url": profile_url}
            response = await api.async_profile.resolve_url(params=params)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.url_resolver_spec
        urn = glom(response_body, spec)

        return urn

    async def _enrich_overview(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.overview(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return
        spec = VtLISpecs.overview_spec
        mapped = dotty(glom(response_body, spec, default={}))
        if top_position := mapped.pop("biographic_details.work"
                                      ".linkedin_work.positions", {}):
            if period := top_position.get("period"):
                top_position['period'] = parse_vtrc_li_period(period)
            mapped["biographic_details.work"
                   ".linkedin_work.positions"] = [top_position]

        if education := mapped.pop(
                "biographic_details.education.linkedin_schools"):
            mapped["biographic_details.education.linkedin_schools"] = [
                education]
        # dotty dictionary should be turned into regular dictionary
        return mapped.to_dict() if mapped else None

    async def _enrich_experience(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.experience(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.experience_spec
        mapped = dotty(glom(response_body, spec, default={}))

        experiences = []
        skills = []
        companies = mapped.get("biographic_details.work"
                               ".linkedin_work.positions")
        for company in companies:
            company_info = {
                "company_name": company.get("company_name"),
                "location": company.get("location"),
                "company_logo_url": company.get("company_logo_url"),
                "linkedin_company_url": company.get("linkedin_company_url")
            }
            positions = company.get("positions", [])
            for position in positions:
                period = parse_vtrc_li_period(position.get("period", {}))
                experiences.append({
                    **company_info,
                    **{
                        "title": position.get("title"),
                        "employment_type": position.get("employment_type"),
                        "description": position.get("description"),
                        "period": period,
                        "duration": period.get("duration")
                    }
                })
                position_skills = position.get("skills", [])
                if position_skills:
                    skills.extend(position_skills)
        # make skills unique
        skills = reduce(
            lambda re, x: re+[x] if x not in re else re, skills, [])

        biographic_details = dotty()
        if experiences:
            biographic_details["biographic_details"
                               ".work.linkedin_work.positions"] = experiences
        if skills:
            biographic_details["biographic_details"
                               ".work.linkedin_work.skills"] = skills
        # dotty dictionary should be turned into regular dictionary
        return biographic_details.to_dict() if biographic_details else None

    async def _enrich_skills(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.skills(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.skills_spec
        mapped = dotty(glom(response_body, spec, default={}))

        for skill in mapped.get("biographic_details.work"
                                ".linkedin_work.skills", []):
            endorser_count = skill.get("endorser_count")
            if not endorser_count:
                pass
            elif "+" in endorser_count:
                skill["endorser_count"] = 99
            else:
                try:
                    skill["endorser_count"] = int(endorser_count)
                except Exception:
                    skill["endorser_count"] = None
        return mapped.to_dict() if mapped else None

    async def _enrich_education(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.education(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return
        spec = VtLISpecs.education_spec
        mapped = dotty(glom(response_body, spec, default=None))

        for education in mapped.get("biographic_details.education"
                                    ".linkedin_schools", []):
            education['period'] = parse_vtrc_li_period(
                education.get("period", {}))

        return mapped.to_dict() if mapped else None

    async def _enrich_recommendations_received(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.recommendations_received(
                source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.recommendations_received_spec
        return glom(response_body, spec, default=None)

    async def _enrich_contact_info(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.contact_info(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.contact_info_spec
        return glom(response_body, spec, default=None)

    async def _enrich_courses(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.courses(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.courses_spec
        return glom(response_body, spec, default=None)

    async def _enrich_activity(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        docs = {}
        try:
            posts_res = await self._enrich_activity_posts(doc)
            if posts_res:
                docs = merge(docs, posts_res, strategy=Strategy.ADDITIVE)
        except Exception as e:
            print(str(e))
        try:
            reactions_res = await self._enrich_activity_reactions(doc)
            if reactions_res:
                docs = merge(docs, reactions_res, strategy=Strategy.ADDITIVE)
        except Exception as e:
            print(str(e))

        return docs

    async def _enrich_activity_posts(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.activity_posts(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.activity_posts_spec
        return glom(response_body, spec)

    async def _enrich_activity_reactions(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.activity_reactions(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.activity_reactions_spec
        return glom(response_body, spec)

    async def _enrich_languages(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.languages(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.languages_spec
        return glom(response_body, spec, default=None)

    # NOTE: release buggy dates
    async def _enrich_licences_certifications(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.licences_certifications(
                source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.licences_certifications_spec
        mapped = dotty(glom(response_body, spec, default={}))

        for item in mapped.get("biographic_details.work"
                               ".linkedin_work.licences_certifications", []):
            for datefield in ["issue_date", "expiration_date"]:
                if datefield_value := item.pop(datefield, None):
                    if not datefield_value.get("year"):
                        continue
                    if year := datefield_value.get('year'):
                        item[datefield] = pendulum.datetime(
                            year,
                            (datefield_value.get('month', '1')
                             if datefield_value.get('month') else 1),
                            (datefield_value.get('day', '1')
                             if datefield_value.get('day') else 1),
                        ).to_date_string()
                        pass

        return mapped.to_dict() if mapped else None

    async def _enrich_volunteering(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.volunteering(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.volunteering_spec
        mapped = dotty(glom(response_body, spec, default={}))

        for item in mapped.get("biographic_details.work"
                               ".linkedin_work.volunteering_experiences", []):
            for datefield in ["start_month_year", "end_month_year"]:
                if datefield_value := item.pop(datefield):
                    if year := datefield_value.get('year'):
                        item[datefield] = pendulum.datetime(
                            year,
                            (datefield_value.get('month', '1')
                             if datefield_value.get('month') else 1),
                            (datefield_value.get('day', '1')
                             if datefield_value.get('day') else 1),
                        ).to_date_string()
                        pass

        return mapped.to_dict() if mapped else None

    async def _enrich_honors_awards(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.honors_awards(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.honors_awards_spec
        mapped = dotty(glom(response_body, spec, default={}))

        for item in mapped.get("biographic_details.work"
                               ".linkedin_work.honors", []):
            if issue_date := item.pop("issue_date", None):
                try:
                    item["issue_date"] = pendulum.parse(
                        f"1 {issue_date}",
                        strict=False).to_date_string()
                except Exception:
                    pass

        return mapped.to_dict() if mapped else None

    async def _enrich_publications(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.publications(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.publications_spec
        return glom(response_body, spec, default=None)

    async def _enrich_projects(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.projects(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.projects_spec
        mapped = dotty(glom(response_body, spec, default={}))

        for item in mapped.get("biographic_details.work"
                               ".linkedin_work.projects", []):
            if start_month_year := item.pop("start_month_year"):
                start_month_year = start_month_year.split("-")
                try:
                    item["start_month_year"] = pendulum.parse(
                        start_month_year[0].strip(),
                        strict=False).to_date_string()
                except Exception:
                    pass

            if end_month_year := item.pop("end_month_year"):
                end_month_year = end_month_year.split("-")
                try:
                    if "Present" not in end_month_year[1].strip():
                        item["end_month_year"] = pendulum.parse(
                            start_month_year[0].strip(),
                            strict=False).to_date_string()
                except Exception:
                    pass

        return mapped.to_dict() if mapped else None

    async def _enrich_interests_influencers(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.interests_influencers(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.interests_influencers_spec
        mapped = dotty(glom(response_body, spec, default={}))

        for item in mapped.get("interests.linkedin_interests"):
            linkedin_is_influencer = item.get("linkedin_is_influencer")
            item["linkedin_is_influencer"] = (
                True if linkedin_is_influencer == "influencer" else False)

        return mapped.to_dict() if mapped else None

    async def _enrich_test_scores(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        source_id = doc.source_id
        try:
            response = await api.async_profile.test_scores(source_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            return

        spec = VtLISpecs.test_scores_spec
        mapped = dotty(glom(response_body, spec, default={}))

        for item in mapped.get("biographic_details.work"
                               ".linkedin_work.test_scores", []):
            try:
                item["score"] = item.get("score", "").split(
                    " · ")[0].split(":")[1].strip()
            except Exception:
                pass
            try:
                item["date"] = pendulum.parse(
                    item.pop("date", "").split(" · ")[1].strip(),
                    strict=False).to_date_string()
            except Exception:
                pass

        return mapped.to_dict() if mapped else None
