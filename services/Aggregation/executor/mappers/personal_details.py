from ..utils import Utils


class PersonalDetails:

    def __init__(self):
        self.utils = Utils()
        self.update_map = {
            # Name attributes
            'personal_details.name.first_name.{source}_f_name':
            'update_attribute',
            'personal_details.name.last_name.{source}_l_name':
            'update_attribute',
            'personal_details.name.full_name.{source}_full_name':
            'update_attribute',
            'personal_details.name.middle_name': 'update_attribute',
            'personal_details.name.middle_name.{source}_middle_name':
            'update_attribute',
            'personal_details.name.nickname': 'create_dict_for_path',
            'personal_details.name.nickname.fb_nicknames': 'update_attribute',
            'personal_details.name.nickname.fb_other_names':
            'update_attribute',
            'personal_details.name.nickname.other_names':
            'update_list_attribute',

            # Phone attributes
            'personal_details.phone': 'create_dict_for_path',
            'personal_details.phone.phones': 'update_list_attribute',
            'personal_details.phone.fb_phone': 'update_attribute',
            'personal_details.phone.fb_phones': 'update_list_attribute',
            'personal_details.phone.fb_phones_in_whatsapp': 'update_attribute',
            'personal_details.phone.linkedin_phone_numbers':
            'update_attribute',

            # Gender attribute
            'personal_details.gender': 'create_dict_for_path',
            'personal_details.gender.gender': 'update_attribute',
            'personal_details.gender.fb_gender': 'update_attribute',

            # Visuals attributes
            'personal_details.visuals': 'create_dict_for_path',
            'personal_details.visuals.background_image': 'update_attribute',
            'personal_details.visuals.fb_cover_photo': 'update_attribute',
            'personal_details.visuals.profile_photo': 'create_dict_for_path',
            'personal_details.visuals.profile_photo.{source}_profile_picture':
            'update_attribute',

            # Additional details attributes
            'personal_details.additional_details':
            'create_dict_for_path',
            'personal_details.additional_details.additional_person_details':
            'update_attribute',
            'personal_details.additional_details.fb_interested_in':
            'update_attribute',
            'personal_details.additional_details.fb_political_views':
            'update_attribute',
            'personal_details.additional_details.fb_religious_views':
            'update_attribute',

            # Email attributes
            'personal_details.email.email_address': 'update_list_attribute',
            'personal_details.email.fb_email_address': 'update_attribute',
            'personal_details.email.linkedin_email_address':
            'update_attribute',

            # Birthday attributes
            'personal_details.birth_year_birthday':
            'create_dict_for_path',
            'personal_details.birth_year_birthday.birthday':
            'create_dict_for_path',
            'personal_details.birth_year_birthday.birthday.birthday':
            'update_attribute',
            'personal_details.birth_year_birthday.birthday.linkedin_birthday':
            'update_attribute',
            'personal_details.birth_year_birthday.birthday.fb_birthday':
            'update_attribute',
            'personal_details.birth_year_birthday.year_of_birth':
            'create_dict_for_path',
            'personal_details.birth_year_birthday.year_of_birth.birthyear':
            'update_attribute',

            # Websites attributes
            'personal_details.websites': 'create_dict_for_path',
            'personal_details.websites.websites': 'update_list_attribute',
            'personal_details.websites.linkedin_websites':
            'update_list_attribute',

            # Languages attributes
            'personal_details.languages': 'create_dict_for_path',
            'personal_details.languages.languages': 'update_list_attribute',
            'personal_details.languages.fb_languages': 'update_list_attribute',

            # Location attributes
            'personal_details.location': 'create_dict_for_path',
            'personal_details.location.location': 'update_attribute',
            ('personal_details.location.current_city_region_country.'
             'linkedin_search_location'): 'update_attribute',
            ('personal_details.location.current_city_region_country.'
             'linkedin_location'): 'update_attribute',
            ('personal_details.location.current_location.'
             'linkedin_location_epieos'): 'update_attribute',
            'personal_details.location.current_location.fb_lives_in_url':
            'update_attribute',
            'personal_details.location.current_city.fb_current_city':
            'update_attribute',
            ('personal_details.location.current_country.'
             'linkedin_location_country'): 'update_attribute',
            'personal_details.location.current_region': 'update_attribute',
            'personal_details.location.check_ins.fb_check_ins':
            'update_list_attribute',
            'personal_details.location.current_lat_long.fb_lives_in_lat':
            'update_attribute',
            'personal_details.location.current_lat_long.fb_lives_in_long':
            'update_attribute',
            'personal_details.location.hometown.fb_hometown':
            'update_attribute',
        }

    def update_personal_details(self, person, candidate):
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
