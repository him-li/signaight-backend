from ..utils import Utils


class BioDetails:

    def __init__(self):
        self.utils = Utils()
        # Map for BiographicDetails class
        self.biographic_details_map = {
            'biographic_details.description_bio_intro': 'create_dict_for_path',
            'biographic_details.volunteer_experience': 'create_dict_for_path',
            'biographic_details.marital_status_relatives':
            'update_list_attribute',
            'biographic_details.education': 'create_dict_for_path',
            'biographic_details.work': 'create_dict_for_path',
        }

        # Map for Work class
        self.work_map = {
            'biographic_details.work.linkedin_work': 'create_dict_for_path',
            'biographic_details.work.facebook_work': 'update_list_attribute',
        }

        # Map for Education class
        self.education_map = {
            'biographic_details.education.linkedin_schools':
            'update_list_attribute',
            'biographic_details.education.facebook_schools':
            'update_list_attribute',
        }

        # Map for VolunteerExperience class
        self.volunteer_experience_map = {
            'biographic_details.volunteer_experience.volunteer_experience':
            'update_list_attribute',
            ('biographic_details.volunteer_experience.'
             'linkedin_volunteering_experiences'):
            'create_dict_for_path',
            'biographic_details.volunteer_experience.certificates':
            'update_list_attribute',
            'biographic_details.volunteer_experience.role':
            'update_list_attribute',
            'biographic_details.volunteer_experience.cause':
            'update_list_attribute',
        }

        # Map for DescriptionBioIntro class
        self.description_bio_intro_map = {
            'biographic_details.description_bio_intro.introduction':
            'update_attribute',
            'biographic_details.description_bio_intro.linkedin_headline':
            'update_attribute',
            'biographic_details.description_bio_intro.instagram_bio':
            'update_attribute',
            'biographic_details.description_bio_intro.biography_with_entities':
            'update_list_attribute',
            'biographic_details.description_bio_intro.instagram_bio_links':
            'update_list_attribute',
            ('biographic_details.description_bio_intro.'
             'instagram_fb_link_on_profile'):
            'update_attribute',
        }

        # Combine all the individual maps into a single map
        self.combined_map = {
            **self.biographic_details_map,
            **self.work_map,
            **self.education_map,
            **self.volunteer_experience_map,
            **self.description_bio_intro_map,
        }

    def update_bio_details(self, person, candidate):
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
