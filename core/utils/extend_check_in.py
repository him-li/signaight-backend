import pendulum


def extend_check_in(check_in, subtitle):
    if "\n" in subtitle:
        subtitle_list = subtitle.split("\n")
        check_in["region"] = subtitle_list[0]
    if "Visited on" in subtitle:
        subtitle_list = subtitle.split("Visited on")
        visit_date = pendulum.parse(
            subtitle_list[1],
            strict=False).to_date_string()
        check_in["date"] = visit_date
    return check_in
