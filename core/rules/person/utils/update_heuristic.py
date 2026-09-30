from core.models.alerts import Alert


def update_heuristics_score(self_key, heuristic):
    try:
        if isinstance(self_key, dict):
            for i, _heuristic in enumerate(self_key.get("heuristics", [])):
                if _heuristic.get("title") == heuristic.get('title', ''):
                    del self_key.get("heuristics", [])[i]
            if not self_key.get("heuristics"):
                self_key.setdefault("heuristics", [])
            self_key["heuristics"].append(heuristic)
            max_score = max(heuristic.get("score") for heuristic in
                            self_key.get("heuristics"))
            self_key["score"] = max_score
        else:
            self_key = self_key.model_dump()
            for i, _heuristic in enumerate(self_key.get("heuristics", [])):
                if _heuristic.get("title") == heuristic.get('title', ''):
                    del self_key.get("heuristics", [])[i]
            if not self_key.get("heuristics"):
                self_key.setdefault("heuristics", [])
            self_key["heuristics"].append(heuristic)
            max_score = max(heuristic.get("score") for heuristic in
                            self_key.get("heuristics"))
            self_key["score"] = max_score

    except AttributeError:
        self_key = {
            "heuristics": [heuristic],
            "score": heuristic.get('score')
        }

    return Alert(**self_key)
