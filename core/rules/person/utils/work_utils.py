from core.models.work import Position
from core.models import Person


def create_positions_list_unique(person: Person):
    positions = []
    linkedin_work = {}
    xing_work = {}
    facebook_work = []

    try:
        if linkedin_work := (person.biographic_details.work.
                             linkedin_work):
            linkedin_work = linkedin_work.model_dump()
            _ = (positions.extend(linkedin_work.get("positions", []))
                 if linkedin_work.get("positions") else [])
    except Exception:
        pass
    try:
        if ((xing_work := person.biographic_details.work.xing_work) and
                not linkedin_work):
            xing_work = xing_work.model_dump()
            _ = (positions.extend(xing_work.get("positions", []))
                 if xing_work.get("positions") else positions)
    except Exception:
        pass
    try:
        if ((facebook_work := person.biographic_details.work.facebook_work) and
                not linkedin_work and not xing_work):
            facebook_work = [work.model_dump() for work in facebook_work]
            _ = (positions.extend(facebook_work)
                 if facebook_work else [])
    except Exception:
        pass
    for position in positions:
        try:
            if company_logo_url := position.get("company_logo_url"):
                position['company_logo_url'] = str(company_logo_url)
            if linkedin_company_url := position.get(
                    "linkedin_company_url"):
                position['linkedin_company_url'] = str(
                    linkedin_company_url)
            if xing_company_url := position.get("xing_company_url"):
                position['xing_company_url'] = str(xing_company_url)
        except Exception:
            pass
        if (position.get("fb_workplace_name") or
            position.get("fb_work_title") or
                position.get("fb_work_period")):
            position['company_name'] = position.get('fb_workplace_name')
            position['title'] = position.get('fb_work_title')
            position['period'] = position.get('fb_work_period')
            position['location'] = position.get('fb_workplace_location')

    return positions


def create_positions_list_additive(person: Person):
    positions = []
    try:
        if linkedin_work := (person.biographic_details.work.
                             linkedin_work):
            linkedin_work = linkedin_work.model_dump()
            _ = (positions.extend(linkedin_work.get("positions", []))
                 if linkedin_work.get("positions") else [])
    except Exception:
        pass
    try:
        if xing_work := person.biographic_details.work.xing_work:
            xing_work = xing_work.model_dump()
            _ = (positions.extend(xing_work.get("positions", []))
                 if xing_work.get("positions") else positions)
    except Exception:
        pass
    try:
        if facebook_work := person.biographic_details.work.facebook_work:
            facebook_work = [work.model_dump() for work in facebook_work]
            _ = (positions.extend(facebook_work)
                 if facebook_work else [])
    except Exception:
        pass
    for position in positions:
        try:
            if company_logo_url := position.get("company_logo_url"):
                position['company_logo_url'] = str(company_logo_url)
            if linkedin_company_url := position.get(
                    "linkedin_company_url"):
                position['linkedin_company_url'] = str(
                    linkedin_company_url)
            if xing_company_url := position.get("xing_company_url"):
                position['xing_company_url'] = str(xing_company_url)
        except Exception:
            pass
        if (position.get("fb_workplace_name") or
            position.get("fb_work_title") or
                position.get("fb_work_period")):
            position['company_name'] = position.get('fb_workplace_name')
            position['title'] = position.get('fb_work_title')
            position['period'] = position.get('fb_work_period')
            position['location'] = position.get('fb_workplace_location')

    return positions


def create_position_model_list_unique(person: Person):
    positions = []
    linkedin_work = {}
    xing_work = {}
    facebook_work = []

    try:
        if linkedin_work := person.biographic_details.work.linkedin_work:
            _ = (positions.extend(linkedin_work.positions)
                 if hasattr(linkedin_work, "positions") else [])
    except Exception:
        pass
    try:
        if ((xing_work := person.biographic_details.work.xing_work) and
                not linkedin_work):
            _ = (positions.extend(xing_work.positions)
                 if hasattr(xing_work, "positions") else [])
    except Exception:
        pass
    try:
        if ((facebook_work := person.biographic_details.work.facebook_work) and
                not linkedin_work and not xing_work):
            _ = (positions.extend(facebook_work)
                 if facebook_work else [])
    except Exception:
        pass
    reviewed_positions = []
    for position in positions:
        try:
            if hasattr(position, "company_logo_url"):
                position.company_logo_url = str(
                    position.company_logo_url
                ) if position.company_logo_url else None
            if hasattr(position, "linkedin_company_url"):
                position.linkedin_company_url = str(
                    position.linkedin_company_url
                ) if position.linkedin_company_url else None
            if hasattr(position, "xing_company_url"):
                position.xing_company_url = str(
                    position.xing_company_url
                ) if position.xing_company_url else None
        except Exception:
            pass
        if (hasattr(position, "fb_workplace_name") or
            hasattr(position, "fb_work_title") or
                hasattr(position, "fb_work_period")):
            position_dict = position.model_dump()
            position_dict['company_name'] = position_dict.get(
                'fb_workplace_name')
            position_dict['title'] = position_dict.get('fb_work_title')
            position_dict['period'] = position_dict.get('fb_work_period')
            position_dict['location'] = position_dict.get(
                'fb_workplace_location')
            position_model = Position(**position_dict)
            reviewed_positions.append(position_model)

    positions = reviewed_positions if reviewed_positions else positions
    try:
        positions.sort(key=lambda position: position.period.date_from)
        positions.reverse()
    except Exception:
        pass

    return positions


def create_position_model_list_additive(person: Person):
    positions = []
    try:
        if linkedin_work := person.biographic_details.work.linkedin_work:
            _ = (positions.extend(linkedin_work.positions)
                 if hasattr(linkedin_work, "positions") else [])
    except Exception:
        pass
    try:
        if xing_work := person.biographic_details.work.xing_work:
            _ = (positions.extend(xing_work.positions)
                 if hasattr(xing_work, "positions") else [])
    except Exception:
        pass
    try:
        if facebook_work := person.biographic_details.work.facebook_work:
            _ = (positions.extend(facebook_work)
                 if facebook_work else [])
    except Exception:
        pass
    reviewed_positions = []
    for position in positions:
        try:
            if hasattr(position, "company_logo_url"):
                position.company_logo_url = str(
                    position.company_logo_url
                ) if position.company_logo_url else None
            if hasattr(position, "linkedin_company_url"):
                position.linkedin_company_url = str(
                    position.linkedin_company_url
                ) if position.linkedin_company_url else None
            if hasattr(position, "xing_company_url"):
                position.xing_company_url = str(
                    position.xing_company_url
                ) if position.xing_company_url else None
        except Exception:
            pass
        if (hasattr(position, "fb_workplace_name") or
            hasattr(position, "fb_work_title") or
                hasattr(position, "fb_work_period")):
            position_dict = position.model_dump()
            position_dict['company_name'] = position_dict.get(
                'fb_workplace_name')
            position_dict['title'] = position_dict.get('fb_work_title')
            position_dict['period'] = position_dict.get('fb_work_period')
            position_dict['location'] = position_dict.get(
                'fb_workplace_location')
            position_model = Position(**position_dict)
            reviewed_positions.append(position_model)

    positions = reviewed_positions if reviewed_positions else positions
    try:
        positions.sort(key=lambda position: position.period.date_from)
        positions.reverse()
    except Exception:
        pass

    return positions


def create_skills_model_list(person: Person):
    skills = []

    # Extract LinkedIn skills
    try:
        linkedin_work = getattr(
            person.biographic_details.work, 'linkedin_work', None)
        if linkedin_work and hasattr(linkedin_work, 'skills'):
            skills.extend(
                linkedin_work.skills) if linkedin_work.skills else []
    except Exception:
        pass

    # Extract Xing skills
    try:
        xing_work = getattr(person.biographic_details.work, 'xing_work', None)
        if xing_work and hasattr(xing_work, 'skills'):
            xing_skills = xing_work.skills
            if hasattr(xing_skills, 'hard_skills'):
                skills.extend(
                    xing_skills.hard_skills) if xing_skills.hard_skills else []
            if hasattr(xing_skills, 'top_skills'):
                skills.extend(
                    xing_skills.top_skills) if xing_skills.top_skills else []
            if hasattr(xing_skills, 'soft_skills'):
                skills.extend(
                    xing_skills.soft_skills) if xing_skills.soft_skills else []
    except Exception:
        pass

    return skills
