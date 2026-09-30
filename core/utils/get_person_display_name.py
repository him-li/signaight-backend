def get_person_display_name(person) -> str:
    name = getattr(person.personal_details, "name", None)

    if name:
        if name.full_name and name.full_name.full_name:
            return name.full_name.full_name
        if name.first_name or name.last_name:
            name_chunks = []
            if name.first_name.f_name:
                name_chunks.append(name.first_name.f_name)
            if name.last_name.l_name:
                name_chunks.append(name.last_name.l_name)
            if len(name_chunks) > 0:
                return " ".join(name_chunks)

    return "No name"

