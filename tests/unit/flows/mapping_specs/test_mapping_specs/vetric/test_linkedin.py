from glom import glom
from datetime import date, datetime
from faker import Faker

from core.models import BiographicDetails, NetworkSignature
from core.models.visuals import Visuals
from core.models.position import Position
from core.models.skill import Skill
from core.models.education import LinkedinSchool
from core.models.recommendation import Recommendation
from core.models.course import Course
from core.models.post import Post
from core.models.language import Language
from core.models.licence_certification import LicenceCertification
from core.models.volunteering_experience import VolunteeringExperience
from core.models.honor import Honor
from core.models.publication import Publication
from core.models.project_part_of import ProjectPartOf
from core.models.interests import (
    LinkedinInfluencers,
)
from core.models.test_score import TestScore as Score
from core.utils import parse_vtrc_li_period
from core.models.company import Company

from core.clients.vetric.linkedin import VtLISpecs

from core.dotty_dictionary import dotty

from tests.unit.flows.mapping_specs.mapping_targets import Targets

fake = Faker()


class TestMappingsSpecs:
    def test_vetric_linkedin_search(self):
        target = Targets.vtrc_li_search
        spec = VtLISpecs.search_spec
        result = glom(target, spec)
        assert result
        assert isinstance(result, list)
        for person in result:
            headline = person.get(
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
                bio_details = person.get("biographic_details")
                bio_details = {"biographic_details": {**bio_details, "work": {
                    "linkedin_work": {"positions": [position]}}}}
                person.update(bio_details)
            elif "@" in headline:
                index = headline.index("@")
                title = headline[:index].strip()
                company_name = headline[index+1:].strip()
                position = {
                    "title": title,
                    "company_name": company_name
                }
                bio_details = person.get("biographic_details")
                bio_details = {"biographic_details": {**bio_details, "work": {
                    "linkedin_work": {"positions": [position]}}}}
                person.update(bio_details)
            else:
                pass

        linkedin_name = result[0].get("personal_details").get("name").get(
            "full_name").get("linkedin_full_name")
        assert isinstance(linkedin_name, str)

    def test_vetric_linkedin_new_search(self):
        target = Targets.vtrc_li_search
        spec = VtLISpecs.new_search_spec
        result = glom(target, spec)
        assert result
        assert isinstance(result, list)
        for person in result:
            person = dotty(person)
            assert person.get("source") == "linkedin"
            assert person.get("resource") == "vetric"
            assert person.get(
                "personal_details.name.full_name.linkedin_full_name")
            if person.get(
                    "personal_details.visuals.profile_photo."
                    "linkedin_profile_picture"):
                assert person.get(
                    "personal_details.visuals.profile_photo."
                    "linkedin_profile_picture")
            assert person.get(
                "personal_details.location.current_city_region_country."
                "linkedin_search_location")
            assert person.get(
                "biographic_details.description_bio_intro.linkedin_headline")
            assert person.get(
                "biographic_details.work.linkedin_work.positions") is not None
            if person.get("biographic_details.work.linkedin_work.positions"):
                for position in person.get("biographic_details.work."
                                           "linkedin_work.positions"):
                    assert position.get("title")
                    assert position.get("company_name")
            assert person.get("network_signature.user_id.linkedin_user_id")
            assert person.get("network_signature.url.linkedin_profile_url")

    def test_vetric_linkedin_resolve_url(self):
        target = Targets.vtrc_li_resolve_url
        spec = VtLISpecs.url_resolver_spec
        result = glom(target, spec)
        assert result
        assert isinstance(result, str)

    def test_vetric_linkedin_overview(self):
        target = Targets.vtrc_li_overview
        spec = VtLISpecs.overview_spec
        result = glom(target, spec)
        assert result

        position_dict = result.get("biographic_details").get(
            "work").get("linkedin_work").get("positions")

        if position_dict:
            period = position_dict.get("period")
            period = parse_vtrc_li_period(period)
            positions = []
            positions.append(position_dict)
            result["biographic_details"]["work"]["linkedin_work"][
                "positions"] = positions

        education = []
        education.append(
            result["biographic_details"]["education"]["linkedin_schools"])
        result["biographic_details"]["education"][
            "linkedin_schools"] = education

        assert result["personal_details"]
        assert result["biographic_details"]
        assert result["network_signature"]
        bio_details = BiographicDetails(**result["biographic_details"])
        assert isinstance(bio_details, BiographicDetails)
        network_signature = NetworkSignature(**result["network_signature"])
        assert isinstance(network_signature, NetworkSignature)
        visuals = Visuals(**result["personal_details"]["visuals"])
        assert isinstance(visuals, Visuals)

    def test_vetric_linkedin_experience(self):
        target = Targets.vtrc_li_experience
        spec = VtLISpecs.experience_spec
        result = glom(target, spec)
        assert result

        experiences = []
        skills = []
        experiences = result.get("biographic_details").get(
            "work").get("linkedin_work").get("positions")
        for company in experiences:
            positions = company.get("positions")
            if positions:
                for position in positions:
                    period = position.get("period")
                    period = parse_vtrc_li_period(period)

                    position_dict = {
                        "company_name": company.get("company_name"),
                        "location": company.get("location"),
                        "company_logo_url": company.get("company_logo_url"),
                        "linkedin_company_url": company.get(
                            "linkedin_company_url"),
                        "title": position.get("title"),
                        "employment_type": position.get("employment_type"),
                        "description": position.get("description"),
                        "period": position.get("period")
                    }
                    experiences.append(position_dict)
                    position_skills = position.get("skills")
                    if position_skills:
                        skills.extend(position_skills)
                position_entity = Position(**position_dict)
                assert isinstance(position_entity, Position)

        bio_details = {
            "work": {
                "linkedin_work:": {
                    "positions": experiences,
                    "skills": skills
                }
            }
        }

        work = BiographicDetails(**bio_details)
        assert isinstance(work, BiographicDetails)

    def test_vetric_linkedin_skills(self):
        target = Targets.vtrc_li_skills
        spec = VtLISpecs.skills_spec
        result = glom(target, spec)
        assert result
        for skill in result.get("biographic_details").get(
                "work").get("linkedin_work").get("skills"):
            if "+" in skill["endorser_count"]:
                skill["endorser_count"] = 99
            else:
                skill["endorser_count"] = int(skill["endorser_count"])
        skill_obj = Skill(**skill)
        assert isinstance(skill_obj, Skill)

    def test_vetric_linkedin_education(self):
        target = Targets.vtrc_li_education
        spec = VtLISpecs.education_spec
        result = glom(target, spec)
        assert result

        for school in result.get("biographic_details").get(
                "education").get("linkedin_schools"):
            school['period'] = parse_vtrc_li_period(school.get("period", {}))
            li_school = LinkedinSchool(**school)
            assert isinstance(li_school, LinkedinSchool)

    def test_vetric_linkedin_recommendations_received(self):
        target = Targets.vtrc_li_recommendations_received
        spec = VtLISpecs.recommendations_received_spec
        result = glom(target, spec)
        assert result

        for recommendation in result.get("biographic_details").get(
                "work").get("linkedin_work").get("recommendations"):
            rec_obj = Recommendation(**recommendation)
            assert isinstance(rec_obj, Recommendation)

    def test_vetric_linkedin_contact_info(self):
        target = Targets.vtrc_li_contact_info
        spec = VtLISpecs.contact_info_spec
        result = glom(target, spec)
        assert result
        dot_result = dotty(result)
        assert dot_result.get(
            "personal_details.name.first_name.linkedin_f_name")
        assert dot_result.get(
            "personal_details.name.last_name.linkedin_l_name")
        assert dot_result.get(
            "personal_details.email.linkedin_email_address")
        assert dot_result.get(
            "personal_details.websites.linkedin_websites.0.url")
        assert dot_result.get(
            "personal_details.websites.linkedin_websites.0.category"
        )
        assert dot_result.get(
            "network_signature.username.linkedin_username")

    def test_vetric_linkedin_courses(self):
        target = Targets.vtrc_li_courses
        spec = VtLISpecs.courses_spec
        result = glom(target, spec)
        assert result
        dot_result = dotty(result)
        for course in dot_result.get(
                "biographic_details.work.linkedin_work.courses"):
            course_obj = Course(**course)
            assert isinstance(course_obj, Course)

    def test_vetric_linkedin_activity_posts(self):
        target = Targets.vtrc_li_activity_posts
        spec = VtLISpecs.activity_posts_spec
        result = glom(target, spec)
        assert result
        for post in result.get("posts"):
            post = dotty(post)
            assert post.get("linkedin_post_text")
            assert post.get("linkedin_post_publishment_date")
            assert post.get("linkedin_post_comments_count") != None  # noqa
            assert post.get("linkedin_post_likes_count") != None  # noqa
            assert post.get("linkedin_post_shares_count") != None  # noqa
            assert post.get("linkedin_post_url")
            reactions = post.get("reactions")
            assert reactions
            if len(reactions) > 0:
                for reaction in reactions:
                    assert reaction.get(
                        "linkedin_post_reaction_type")
                    assert reaction.get(
                        "linkedin_post_reaction_type_count")
            assert post.get("post_author")
            assert post.get("post_author.linkedin_f_name")
            assert post.get("post_author.linkedin_l_name")
            assert post.get("post_author.title")
            assert post.get("post_author.linkedin_profile_picture")
            assert post.get("post_author.linkedin_profile_url")
            if post.get("shared_post"):
                shared_author = post.get("shared_post.post_author")
                if shared_author:
                    shared_author = dotty(shared_author)
                    assert shared_author.get(
                        "post_author.linkedin_f_name")
                    assert shared_author.get(
                        "post_author.linkedin_l_name")
                    assert shared_author.get("post_author.title")
                    assert shared_author.get(
                        "post_author.linkedin_profile_picture")
                    assert shared_author.get(
                        "post_author.linkedin_profile_url")

            tagged = post.get("tagged_profiles")
            assert tagged != None  # noqa
            if len(tagged) > 0:
                for person in tagged:
                    assert person.get("linkedin_f_name")
                    assert person.get("linkedin_l_name")
                    assert person.get("title")
                    assert person.get("linkedin_profile_url")
        for post in result.get("posts")[:5]:
            post_obj = Post(**post)
            assert isinstance(post_obj, Post)

    def test_vetric_linkedin_activity_reactions(self):
        target = Targets.vtrc_li_activity_reactions
        spec = VtLISpecs.activity_reactions_spec
        result = glom(target, spec)
        assert result
        for post in result.get("posts"):
            post = dotty(post)
            assert post.get("post_reaction")
            assert post.get("post_reaction.reaction_type")
            assert post.get("post_reaction.reaction_target")
            assert post.get("activity_type") == 'reaction'
        target = Targets.vtrc_li_activity_reactions_2
        spec = VtLISpecs.activity_reactions_spec
        result = glom(target, spec)
        assert result
        for post in result.get("posts"):
            post = dotty(post)
            assert post.get("post_reaction")
            assert post.get("post_reaction.reaction_type")
            assert post.get("post_reaction.reaction_target")
            assert post.get("activity_type") == 'reaction'
        target = Targets.vtrc_li_activity_reactions_3
        spec = VtLISpecs.activity_reactions_spec
        result = glom(target, spec)
        assert result
        for post in result.get("posts"):
            post = dotty(post)
            assert post.get("post_reaction")
            assert post.get("post_reaction.reaction_type")
            assert post.get("post_reaction.reaction_target")
            assert post.get("activity_type") == 'reaction'
        for post in result.get("posts")[:5]:
            post_obj = Post(**post)
            assert isinstance(post_obj, Post)

    def test_vetric_linkedin_languages(self):
        target = Targets.vtrc_li_languages
        spec = VtLISpecs.languages_spec
        result = glom(target, spec)
        assert result
        result = dotty(result)

        for language in result.get(
                "personal_details.languages.li_languages"):
            lang_obj = Language(**language)
            assert isinstance(lang_obj, Language)

    def test_vetric_linkedin_licences_certifications(self):
        target = Targets.vtrc_li_licences_certifications
        spec = VtLISpecs.licences_certifications_spec
        result = glom(target, spec)
        assert result
        result = dotty(result)

        for item in result.get("biographic_details.work.linkedin_work.licences_certifications"):  # noqa
            assert item.get("name")
            assert item.get("issuer")
            assert item.get("issuer_photo")
            assert item.get("issuer_url")
            issue_date = item.get("issue_date")
            assert issue_date
            if issue_date.get("year"):
                year = issue_date.get('year')
                month = issue_date.get(
                    'month') if issue_date.get('month') else 1
                day = issue_date.get(
                    'day') if issue_date.get('day') else 1
                item["issue_date"] = date(year, month, day)
            else:
                del item["issue_date"]
            certif_obj = LicenceCertification(**item)
            assert isinstance(certif_obj, LicenceCertification)

    def test_vetric_linkedin_volunteering(self):
        target = Targets.vtrc_li_volunteering
        spec = VtLISpecs.volunteering_spec
        result = glom(target, spec)
        assert result
        result = dotty(result)

        for item in result.get("biographic_details.work.linkedin_work.volunteering_experiences"):  # noqa
            assert item.get("role")
            is_current = item.get("is_current")
            assert is_current != None  # noqa
            assert isinstance(is_current, bool)
            company = item.get("company_name")
            if company:
                assert isinstance(company, str)
            description = item.get("description")
            if description:
                assert isinstance(description, str)
            assert item.get("duration")
            start_date = item.get("start_month_year")
            assert start_date
            if start_date.get("year"):
                year = start_date.get('year')
                month = start_date.get(
                    'month') if start_date.get('month') else 1
                day = start_date.get(
                    'day') if start_date.get('day') else 1
                item["start_month_year"] = date(year, month, day)
            else:
                del item["start_month_year"]
            end_date = item.get("end_month_year")
            assert end_date
            if end_date.get("year"):
                year = end_date.get('year')
                month = end_date.get(
                    'month') if end_date.get('month') else 1
                day = end_date.get(
                    'day') if end_date.get('day') else 1
                item["end_month_year"] = date(year, month, day)
            else:
                del item["end_month_year"]
            volunteering_obj = VolunteeringExperience(**item)
            assert isinstance(volunteering_obj, VolunteeringExperience)

    def test_vetric_linkedin_honors_awards(self):
        target = Targets.vtrc_li_honors_awards
        spec = VtLISpecs.honors_awards_spec
        result = glom(target, spec)
        assert result
        result = dotty(result)

        for item in result.get("biographic_details.work.linkedin_work.honors"):  # noqa
            assert item.get("title")
            association = item.get("associated_with")
            if association:
                assert isinstance(association, str)
            issue_date = item.get("issue_date")
            if issue_date:
                datetime_obj = datetime.strptime(issue_date, "%b %Y")
                item["issue_date"] = datetime_obj.date()

            honor = Honor(**item)
            assert isinstance(honor, Honor)

    def test_vetric_linkedin_publications(self):
        target = Targets.vtrc_li_publications
        spec = VtLISpecs.publications_spec
        result = glom(target, spec)
        assert result
        result = dotty(result)

        for item in result.get("biographic_details.work.linkedin_work.publications"):  # noqa
            assert item.get("description")
            assert item.get("name")
            assert item.get("publisher")
            assert item.get("url")
            publication = Publication(**item)
            assert isinstance(publication, Publication)

    def test_vetric_linkedin_projects(self):
        target = Targets.vtrc_li_projects
        spec = VtLISpecs.projects_spec
        result = glom(target, spec)
        assert result
        result = dotty(result)

        for item in result.get("biographic_details.work.linkedin_work.projects"):  # noqa
            assert item.get("description")
            assert item.get("title")
            start_month_year = item.get("start_month_year")
            assert start_month_year
            if start_month_year:
                start_month_year = start_month_year.split("-")
                datetime_obj = datetime.strptime(
                    start_month_year[0].strip(), "%b %Y")
                item["start_month_year"] = datetime_obj.date()
            end_month_year = item.get("end_month_year")
            assert item.get("end_month_year")
            if end_month_year:
                end_month_year = end_month_year.split("-")
                if "Present" not in end_month_year[1].strip():
                    datetime_obj = datetime.strptime(
                        end_month_year[1].strip(), "%b %Y")
                    item["end_month_year"] = datetime_obj.date()
                else:
                    del item["end_month_year"]
            project = ProjectPartOf(**item)
            assert isinstance(project, ProjectPartOf)

    def test_vetric_linkedin_interests_influencers(self):
        target = Targets.vtrc_li_interests_influencers
        spec = VtLISpecs.interests_influencers_spec
        result = glom(target, spec)
        assert result
        result = dotty(result)

        for item in result.get("interests.linkedin_interests"):
            assert item.get("linkedin_full_name")
            assert item.get("linkedin_headline")
            assert item.get("linkedin_followers_count")
            assert item.get("linkedin_profile_url")
            assert item.get("linkedin_profile_picture")
            linkedin_is_influencer = item.get("linkedin_is_influencer")
            assert item.get("linkedin_is_influencer")
            if linkedin_is_influencer == "influencer":
                item["linkedin_is_influencer"] = True
            else:
                item["linkedin_is_influencer"] = False

            influencer = LinkedinInfluencers(**item)
            assert isinstance(influencer, LinkedinInfluencers)

    def test_vetric_linkedin_test_scores(self):
        target = Targets.vtrc_li_test_scores
        spec = VtLISpecs.test_scores_spec
        result = glom(target, spec)
        assert result
        result = dotty(result)

        for item in result.get("biographic_details.work.linkedin_work.test_scores"):  # noqa
            assert item.get("test_name")
            assert item.get("score")
            assert item.get("date")
            item["score"] = item.get("score").split(
                " · ")[0].split(":")[1].strip()
            date_str = item.get("date").split(" · ")[1].strip()
            datetime_obj = datetime.strptime(date_str, "%b %Y")
            item["date"] = datetime_obj.date()

            assert isinstance(item.get("date"), date)
            test_score = Score(**item)
            assert isinstance(test_score, Score)

    def test_vetric_companies_search(self):
        target = Targets.vtrc_li_company_search
        spec = VtLISpecs.companies_search_spec
        result = glom(target, spec)
        assert result
        for company in result:
            company_model = Company(**company)
            assert company_model

    def test_vetric_company_details(self):
        target = Targets.vtrc_li_company_details
        spec = VtLISpecs.company_details_spec
        result = glom(target, spec)
        assert result
        company_model = Company(**result)
        assert company_model
