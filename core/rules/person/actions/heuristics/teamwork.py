import pendulum
from business_rules.actions import rule_action

from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import (
    create_positions_list_additive, update_evaluation_factors_weighted_average,
    build_post_photo_text_list)
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseActions


class TeamworkActions(PersonBaseActions):
    @rule_action()
    def set_person_has_teamwork_experience(self):
        positions = create_positions_list_additive(self.person)

        if positions:
            teamwork_positions = []
            work_experience = {
                "hash": str(positions),
                "work_experience": positions
            }
            logger.debug('Rules engine: TeamworkVariables'
                         ' teamwork for positions')
            try:
                ds_response = ds_app_api.ds_request.team_work_experience(
                    body=work_experience,
                    headers={
                        'x-remote-context': build_person_urn(self.person.id)
                    }
                )
                ds_response_body = ds_response.body
            except Exception:
                ds_response_body = {}
            if ds_response_body:
                if teamwork_experience := ds_response_body.get(
                        "teamwork_experience"):
                    for i, position in enumerate(teamwork_experience):
                        if position.get("has_teamwork_experience"):
                            try:
                                position_info = positions[i]
                                teamwork_positions.append(position_info)
                            except Exception:
                                continue

            try:
                teamwork_positions_ratio = len(
                    teamwork_positions) / len(positions)
            except Exception:
                teamwork_positions_ratio = 0

            teamwork_duration = 0
            try:
                for position in teamwork_positions:
                    if duration := position.get("duration"):
                        if duration.get("months") or duration.get("years"):
                            if years := duration.get("years"):
                                teamwork_duration += years
                            if months := duration.get("months"):
                                teamwork_duration += months / 12

                    elif period := position.get("period"):
                        current_date = pendulum.now().start_of('month')
                        start = pendulum.parse(
                            period.get("date_from"),
                            strict=False).start_of('month')
                        try:
                            end = (pendulum.parse(
                                period.get("date_to"),
                                strict=False).start_of('month') if
                                period.get("date_to") else current_date)
                        except Exception:
                            end = pendulum.now().start_of("month")
                        duration = end.diff(start).in_years()
                        teamwork_duration += duration
            except Exception:
                pass

            if teamwork_positions_ratio or teamwork_duration:
                score = ((teamwork_positions_ratio*0.1) +
                         (teamwork_duration/9)*0.9) * 10
                if score:
                    if score > 10:
                        score = 10
                    score = round(score, 1)
                    factor = {
                        "title": ("{}'s experience shows teamwork").format(
                            self.get_person_name()),
                        "score": score,
                        "weight": 3

                    }
                    self.evaluation.teamwork = (
                        update_evaluation_factors_weighted_average(
                            self.evaluation.teamwork, factor))

    @rule_action()
    def set_teamwork_team_related_activities_posts(self):
        posts = self.person.posts
        posts_list = build_post_photo_text_list(posts)
        for post in posts_list["posts_list"]:
            del post["hash"]
        req_body = {
            "hash": str(posts),
            "posts": posts_list["posts_list"]
        }
        if posts_list["posts_list"]:
            try:
                ds_response = ds_app_api.ds_request.team_related_activities(
                    body=req_body,
                    headers={
                        'x-remote-context': build_person_urn(self.person.id)
                    }
                )
                ds_response_body = ds_response.body
            except Exception:
                ds_response_body = {}
            team_related = 0
            posts_res = ds_response_body.get("posts")
            score = 0
            if posts_res:
                for post in posts_res:
                    if post.get("is_team_related"):
                        team_related += 1
                if team_related:
                    if team_related >= 1 and team_related <= 3:
                        score = 5
                    if team_related >= 4 and team_related <= 5:
                        score = 7
                    if team_related >= 6 and team_related <= 7:
                        score = 8
                    if team_related >= 8 and team_related <= 9:
                        score = 9
                    if team_related >= 10:
                        score = 10
                    if score:
                        factor = {
                            "title": ("{}'s posts show team related activities"
                                      ).format(
                                self.get_person_name()),
                            "score": score,
                            "weight": 10
                        }
                        self.evaluation.teamwork = (
                            update_evaluation_factors_weighted_average(
                                self.evaluation.teamwork, factor))

    @rule_action()
    def set_teamwork_team_related_activities_reactions(self):
        posts = self.person.posts
        posts_list = build_post_photo_text_list(posts, "reaction")
        for post in posts_list["posts_list"]:
            del post["hash"]
        req_body = {
            "hash": str(posts),
            "posts": posts_list["posts_list"]
        }
        if posts_list["posts_list"]:
            try:
                ds_response = ds_app_api.ds_request.team_related_activities(
                    body=req_body,
                    headers={
                        'x-remote-context': build_person_urn(self.person.id)
                    }
                )
                ds_response_body = ds_response.body
            except Exception:
                ds_response_body = {}
            team_related = 0
            posts_res = ds_response_body.get("posts")
            score = 0
            if posts_res:
                for post in posts_res:
                    if post.get("is_team_related"):
                        team_related += 1
                if team_related:
                    if team_related >= 1 and team_related <= 5:
                        score = 5
                    if team_related >= 6 and team_related <= 10:
                        score = 6
                    if team_related >= 11 and team_related <= 15:
                        score = 7
                    if team_related >= 16 and team_related <= 20:
                        score = 8
                    if team_related >= 21 and team_related <= 24:
                        score = 9
                    if team_related >= 25:
                        score = 10
                    if score:
                        factor = {
                            "title": ("{}'s post reactions show team related "
                                      "activities").format(
                                self.get_person_name()),
                            "score": score,
                            "weight": 1
                        }
                        self.evaluation.teamwork = (
                            update_evaluation_factors_weighted_average(
                                self.evaluation.teamwork, factor))
