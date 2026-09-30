def get_result_messages_by_source(result_set, messages):
    need = {k: len(v) for k, v in result_set.items()}
    total_need = sum(need.values())

    # take only the latest messages that will be consumed
    pool = messages[-total_need:] if total_need else []

    assigned = dict()
    i = 0
    for k in result_set.keys():
        n = need[k]
        assigned[k] = pool[i:i+n]
        i += n
    
    return assigned
