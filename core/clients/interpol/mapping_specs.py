import pendulum
from glom import Coalesce, SKIP, T
from urllib.parse import urlunparse
from datetime import datetime, date
from iso639 import Lang
from isocodes import countries

EYE_COLOR = {
        "BLA": "Black",
        "BLU": "Blue",
        "BLUL": "Light blue ",
        "BRO": "Brown",
        "BROD": "Dark brown",
        "BROH": "Hazel",
        "BROL": "Light brown",
        "GRE": "Green",
        "GRY": "Grey",
        "OTHC": "Eyes of different colours",
        "OTHD": "Dark",
        "OTHL": "Light"
        }

HAIR_COLOR = {
            "BLA": "Black",
            "BRO": "Brown",
            "BROF": "Fair",
            "GRY": "Grey",
            "GRYG": "Greying",
            "HAIB": "Bald",
            "HAID": "Dyed",
            "OTHD": "Dark",
            "RED": "Red",
            "REDA": "Auburn",
            "WHI": "White",
            "YELB": "Blond"
        }

class InterpolSpecs:

    format_date = lambda date: datetime.strptime(date, r'%Y/%m/%d').strftime(r'%d-%m-%Y')

    def parse_country_code(country_code):
        country = countries.get(alpha_2=country_code.upper())
        return country.get('name') if country else 'Unknown'
    
    def get_language_name(language_code):
        try:
            language = Lang(language_code.lower())
            return language.name
        except KeyError:
            return 'Unknown'
        
    def combine_birth_info(data):
        place_of_birth = data.get('place_of_birth')
        country_of_birth_id = data.get('country_of_birth_id')
        country_name = InterpolSpecs.parse_country_code(country_of_birth_id)
        
        if place_of_birth and country_name:
            return f"{place_of_birth}, {country_name}"
        elif place_of_birth:
            return place_of_birth
        elif country_name:
            return country_name
        else:
            return None      

    
    search_specs = (Coalesce('_embedded.notices', default=[]), [
        {
            'personal_details' : {
                'name' : {
                    'last_name' : {
                        'interpol_l_name' : Coalesce('name', default=None),
                    },
                    'first_name' : {
                        'interpol_f_name' : Coalesce('forename', default=None),
                    },
                    'full_name' : {
                        'interpol_full_name' : Coalesce(T['forename'] + " " + T['name'], default=None),
                    }
                },
                'birth_year_birthday' : {
                    'birthday' : {
                        'interpol_birthday' : Coalesce((T['date_of_birth'], format_date), default=None),
                    }
                },
                'nationality' : {
                    'interpol_nationalities' : Coalesce((T['nationalities'], [parse_country_code]), default=[]),
                },
                'visuals' : {
                    'profile_photo' : {
                        'interpol_profile_picture' : Coalesce('_links.thumbnail.href', default=None),
                    }
                }
            },
            'network_signature' : {
                'user_id' : {
                    'interpol_entity_id' : Coalesce(lambda t: '-'.join(t['entity_id'].split('/')), default=None)
                },
                'url' : {
                    'interpol_profile_url' : Coalesce((T['entity_id'], lambda id: urlunparse(('https', 'www.interpol.int', '/en/How-we-work/Notices/Red-Notices/View-Red-Notices', '', '', '-'.join(id.split('/'))))))
                }
            },
        }
    ])


    enrich_specs = {
        'personal_details' : {
            'name' : {
                'last_name' : {
                    'interpol_l_name' : Coalesce('name', default=None),
                },
                'first_name' : {
                    'interpol_f_name' : Coalesce('forename', default=None),
                },
                'full_name' : {
                    'interpol_full_name' : Coalesce(T['forename'] + " " + T['name'], default=None),
                }
            },
            'gender' : {
                'interpol_gender' : Coalesce((T['sex_id'], lambda sex: 'MALE' if sex == 'M' else 'FEMALE'), default=None),
            },
            'birth_year_birthday' : {
                'birthday' : {
                    'interpol_birthday' : Coalesce((T['date_of_birth'], format_date), default=None),
                }
            },
            'nationality' : {
                'interpol_nationalities' : Coalesce((T['nationalities'], [parse_country_code]), default=[]),
            },
            'visuals' : {
                'profile_photo' : {
                    'interpol_profile_picture' : Coalesce('_links.thumbnail.href', default=None),
                }
            },
            'location' : {
                'interpol_birthplace' : Coalesce(lambda t: InterpolSpecs.combine_birth_info(t), default=None),
            },
            'languages' : {
                'interpol_languages' : Coalesce(('languages_spoken_ids', [{'language' : get_language_name}]), default=[]),
            },
            'additional_details' : {
                'interpol_details' : {
                    'arrest_warrants' : Coalesce((T['arrest_warrants'], [{
                        'charge': Coalesce('charge', default=None),
                        'issuing_country': Coalesce(('issuing_country_id', parse_country_code), default=None),
                        'charge_translation' : Coalesce('charge_translation', default=None),
                    }]), default=[]),
                    'interpol_entity_id' : Coalesce(lambda t: '-'.join(t['entity_id'].split('/')), default=None)
                },
                'physical_identifiers' : {
                    'height' : {
                        'interpol_height' : Coalesce(('height', str), default=None),
                    },
                    'weight' : {
                        'interpol_weight' : Coalesce(('weight', str), default=None),
                    },
                    'eye_color' : {
                        'interpol_eye_color' : Coalesce(('eyes_colors_id', lambda colors: [EYE_COLOR.get(color) for color in colors] if colors else None), default=None),
                    },
                    'hair_color' : {
                        'interpol_hair_color' : Coalesce(('hairs_id', lambda colors: [HAIR_COLOR.get(color) for color in colors] if colors else None), default=None),
                    },
                    'identfiers' : {
                        'interpol_identifiers' : Coalesce('distinguishing_marks', default=None),
                    }
                }
            },
        },
        'network_signature' : {
            'url' : {
                'interpol_profile_url' : Coalesce((T['entity_id'], lambda id: urlunparse(('https', 'www.interpol.int', '/en/How-we-work/Notices/Red-Notices/View-Red-Notices', '', '', '-'.join(id.split('/'))))))
            }
        },  
    } 

    
    images_specs = {
        'personal_details' : {
            'visuals' : {
                'interpol_photos' : Coalesce((T['_embedded']['images'], ['_links.self.href']), default=[]),
            }
        }
    }              
