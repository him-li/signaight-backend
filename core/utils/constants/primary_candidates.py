COMMON_PRIMARY_CANDIDATE_SOURCES = [
    {
        "when": {
            "candidate.resource": "grayfox",
            "candidate.source:not_in": ["web", "deepweb", "darkweb"],
            "flow_step:not": "linkage_accuracy",
        },
        "set": {
            "primary": True,
            "ds_filter": True,
        },
    },
]

LINKAGE_ACCURACY_CANDIDATE_SOURCES = [
    {
        "when": {
            "candidate.resource": "grayfox",
            "candidate.source:not_in": ["web", "deepweb", "darkweb"],
            "flow_step": "linkage_accuracy",
        },
        "set": {
            "primary": True,
            "ds_filter": True,
        },
    },
]

SIGNAIGHT_PHONE_FLOW_PRIMARY_CANDIDATE_SOURCES = [
    {
        "when": {
            "candidate.resource": "grayfox",
            "candidate.source:not_in": ["web", "deepweb", "darkweb"],
            "candidate.source:in": ["whatsapp", "truecaller", "telegram_groups", "telegram", "eyecon", "truecaller_email"],
            "flow_step:not": "linkage_accuracy",
        },
        "set": {
            "primary": True,
            "ds_filter": True,
        },
    }
]


SIGNAIGHT_APP_CONTEXT = "7505d64a54e061b7acd54ccd58b49dc43500b635"
