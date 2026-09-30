from ..utils import Utils


class Posts:

    def __init__(self):
        self.utils = Utils()
        self.posts_map = {
            'posts': 'update_list_attribute'
        }
        # Combine all the individual maps into a single map
        self.combined_map = {
            **self.posts_map,
        }

    def update_posts(self, person, candidate):
        for attribute, update_method in self.combined_map.items():
            if update_method == 'update_attribute':
                person = self.utils.update_attribute(
                    person,
                    candidate,
                    attribute)
            elif update_method == 'update_list_attribute':
                person = self.utils.update_list_attribute(
                    person,
                    candidate,
                    attribute)
            elif update_method == 'create_dict_for_path':
                person = self.utils.create_dict_for_path(
                    person,
                    attribute)
            # Add more update methods here if needed

        return person
