from difflib import SequenceMatcher

def compare_names_data(person_name: str, candidate_name: str):
    ratio = SequenceMatcher(None, person_name.lower() if person_name else "", candidate_name.lower()).ratio()
    print('ratio', ratio, 'person_name', person_name, 'candidate_name', candidate_name)
    name_match = ratio > 0.8
    return name_match, ratio
