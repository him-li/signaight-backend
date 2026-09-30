def extract_specific_rules(ruleset, labels_to_extract):
    extracted_rules = []
    for rule in ruleset:
        if rule['label'] in labels_to_extract:
            extracted_rules.append(rule)
    return extracted_rules


def extract_score_compatibility_rules(person_ruleset):
    labels_of_interest = [
        "Calculate person signaight_score",
        "Calculate person compatibility",
        "Calculate Person Risk Score if there are Red Flags"
    ]

    return extract_specific_rules(person_ruleset, labels_of_interest)
