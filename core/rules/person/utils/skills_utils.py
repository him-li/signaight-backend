from typing import List

from core.models.skill import Skill


def calculate_skill_score(skill, skill_model: Skill):
    endorser_count = 0
    if skill_model.endorser_count:
        endorser_count = skill_model.endorser_count

    score = 5
    if skill.lower() == 'teamwork':
        if endorser_count >= 1:
            score = 6
        if endorser_count >= 2:
            score = 8
        if endorser_count >= 4:
            score = 9
        if endorser_count >= 6:
            score = 10
    elif skill.lower() == 'decision making':
        if endorser_count:
            score += endorser_count

    if score > 10:
        score = 10

    return score


def calculate_skill_score_and_check(skills: List[Skill],
                                    threshold):
    for skill_model in skills:
        if skill_model.name.lower() == 'interpersonal skills':
            return True
        elif skill_model.name.lower() == 'teamwork':
            teamwork_score = calculate_skill_score('teamwork', skill_model)
            if teamwork_score >= threshold:
                return True
    return False
