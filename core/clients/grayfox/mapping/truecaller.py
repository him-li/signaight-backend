from glom import T, Coalesce, SKIP

def _norm_str(s):
    return s.strip() if isinstance(s, str) and s.strip() else None

def _norm_cc(cc):
    cc = _norm_str(cc)
    return cc.upper() if cc else None

def truecaller_block(root):
    data = root.get("data", {}) if isinstance(root, dict) else {}
    profiles = data.get("profiles", []) or []
    locations = data.get("locations", []) or []

    tc_profile = next(
        (p for p in profiles if isinstance(p, dict) and p.get("source") == "truecaller"),
        None,
    )
    if not tc_profile:
        return None

    # Prefer country code from profile, else first truecaller location with a non-empty country_code
    cc = _norm_cc(tc_profile.get("country_code"))
    if not cc:
        for loc in locations:
            if isinstance(loc, dict) and loc.get("source") == "truecaller":
                cc = _norm_cc(loc.get("country_code"))
                if cc:
                    break

    return {
        "personal_details": {
            "name": {
                "first_name": {
                    "truecaller_f_name": _norm_str(tc_profile.get("firstname"))
                },
                "last_name": {
                    "truecaller_l_name": _norm_str(tc_profile.get("lastname"))
                },
            },
            "visuals": {
                "profile_photo": {
                    "truecaller_profile_picture": (
                        pic if isinstance((pic := tc_profile.get("profile_pic")), str)
                        and (pic.startswith("http") or pic.startswith("data:image"))
                        else None
                    )
                }
            },
            "gender": {"truecaller_gender": tc_profile.get("gender")},
            "location": {"truecaller_country_code": cc},
            "birth_year_birthday": {
                "birthday": {"truecaller_birthday": tc_profile.get("birthday")}
            },
        },
        "network_signature": {
            "username": {
                "truecaller_username": _norm_str(tc_profile.get("username"))
            }
        },
        "source": tc_profile.get("source"),
    }
