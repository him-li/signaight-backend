from business_rules.variables import boolean_rule_variable

from ..base import PersonBaseVariables


class PostsVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label='Person has posts'
    )
    def person_with_posts(self):
        person = self.person

        if person.posts:
            return True
        else:
            return False
