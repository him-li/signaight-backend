from ..utils import Utils


class NetworkSignature:

    def __init__(self):
        self.utils = Utils()
        self.update_map = {
            # Username attributes
            'network_signature.username': 'create_dict_for_path',
            'network_signature.username.{source}_username': 'update_attribute',
            'network_signature.username.linkedin_twitter_aliases':
            'update_list_attribute',

            # URL attributes
            'network_signature.url': 'create_dict_for_path',
            'network_signature.url.{source}_profile_url': 'update_attribute',

            # UserId attributes
            'network_signature.user_id': 'create_dict_for_path',
            'network_signature.user_id.{source}_user_id': 'update_attribute',

            # OnlineSignature attributes
            'network_signature.online_signature':
            'create_dict_for_path',
            'network_signature.online_signature.instagram_followers_count':
            'update_attribute',
            'network_signature.online_signature.instagram_following_count':
            'update_attribute',
            'network_signature.online_signature.instagram_following_tag_count':
            'update_attribute',
            'network_signature.online_signature.instagram_posts_count':
            'update_attribute',
            'network_signature.online_signature.fb_followers':
            'update_attribute',
            'network_signature.online_signature.linkedin_connections_count':
            'update_attribute',
            'network_signature.online_signature.linkedin_followers_count':
            'update_attribute',
            'network_signature.online_signature.linkedin_joined':
            'update_attribute',

            # NetworkMisc attributes
            'network_signature.misc': 'create_dict_for_path',
            'network_signature.misc.instagram_is_verified': 'update_attribute',
            'network_signature.misc.instagram_is_business': 'update_attribute',
            'network_signature.misc.instagram_is_private': 'update_attribute',
        }

    def update_network_signature(self, person, candidate):
        for attribute, update_method in self.update_map.items():
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
