from business_rules.variables import boolean_rule_variable

from ..base import PersonBaseVariables


class InterestsVariables(PersonBaseVariables):

    @boolean_rule_variable()
    def person_with_pages(self):
        try:
            if interests := self.person.interests:
                if pages := interests.pages:
                    if any(page.fb_page_name or page.fb_page_id for
                           page in pages):
                        return True
        except Exception:
            pass
        return False
