from business_rules.actions import rule_action
from iso639 import Lang

from core.rules.person.utils import update_evaluation_factors

from ..base import PersonBaseActions

langs = [Lang("en"), Lang("he")]


class LanguageSkillsActions(PersonBaseActions):

    @rule_action()
    def set_lang_proficiency(self):
        HIGH_PROFICIENCY_MULTIPLIER = 2.0
        LOW_PROFICIENCY_MULTIPLIER = 1.0
        POSITION_MULTIPLIERS = [0, 3, 2, 1]
        high_proficiency = ["native or bilingual proficiency",
                            "full professional proficiency",
                            "professional working proficiency",
                            "good", "fluent", "first language"]
        low_proficiency = ["basic", "elementary proficiency",
                           "limited working proficiency"]

        try:
            languages = self.person.personal_details.languages
            li_languages = languages.li_languages or []
            xing_languages = languages.xing_languages or []
        except AttributeError:
            languages = {}
        if isinstance(li_languages, list) or isinstance(xing_languages, list):
            languages = [*li_languages, *xing_languages]
            score = 0
            language_summary = []
            for i, item in enumerate(languages):
                language_name = item.language or "Unknown Language"
                proficiency = (item.proficiency.lower()
                               if item.proficiency else "")
                if proficiency in high_proficiency:
                    level = "High Proficiency"
                elif proficiency in low_proficiency:
                    level = "Low Proficiency"
                elif proficiency:
                    level = "Other Proficiency"
                else:
                    level = "Proficiency level not specified"

                language_summary.append(f"● {language_name} - {level}")

                if i == 0:
                    continue
                position_multiplier = POSITION_MULTIPLIERS[min(i, 3)]
                proficiency_multiplier = (HIGH_PROFICIENCY_MULTIPLIER if
                                          item.proficiency and
                                          item.proficiency.lower() in
                                          high_proficiency else
                                          LOW_PROFICIENCY_MULTIPLIER)
                score += position_multiplier * proficiency_multiplier

            score = round(min(score, 10), 1) if score else 0

        if language_summary and score:
            factor = {
                "title": self._format_language_note(language_summary),
                "score": score
            }
            self.evaluation.language_skills = update_evaluation_factors(
                self.evaluation.language_skills, factor)

    def _format_language_note(self, language_summary: list[str]) -> str:
        name = self.get_person_name()
        summary = "\n".join(language_summary)
        return f"{name} has the following language skills:\n{summary}"
