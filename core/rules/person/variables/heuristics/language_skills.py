from business_rules.variables import boolean_rule_variable

from ..base import PersonBaseVariables


class LanguageSkillsVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label=('Person has high proficiency languages')
    )
    def person_with_multiple_languages(self):
        try:
            languages = self.person.personal_details.languages
            if li_languages := languages.li_languages:
                pass
            else:
                li_languages = []
            if xing_languages := languages.xing_languages:
                pass
            else:
                xing_languages = []
            languages = [*li_languages, *xing_languages]
        except AttributeError:
            languages = {}

        return True if languages else False
