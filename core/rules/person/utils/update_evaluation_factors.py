import string

from core.models.evaluation import EvaluationCategory


def update_evaluation_factors(self_key, factor):
    try:
        if isinstance(self_key, dict):
            for i, _factor in enumerate(self_key.get("factors", [])):
                if _normalize_text(
                        _factor.get("title")) == _normalize_text(
                            factor.get('title', '')):
                    del self_key.get("factors", [])[i]
            if not self_key.get("factors"):
                self_key.setdefault("factors", [])
            self_key["factors"].append(factor)
            max_score = max(factor.get("score") for factor in
                            self_key.get("factors"))
            self_key["score"] = max_score
        else:
            self_key = self_key.model_dump()
            for i, _factor in enumerate(self_key.get("factors", [])):
                if _normalize_text(
                        _factor.get("title")) == _normalize_text(
                            factor.get('title', '')):
                    del self_key.get("factors", [])[i]
            if not self_key.get("factors"):
                self_key.setdefault("factors", [])
            self_key["factors"].append(factor)
            max_score = max(factor.get("score") for factor in
                            self_key.get("factors"))
            self_key["score"] = max_score

    except AttributeError:
        self_key = {
            "factors": [factor],
            "score": factor.get('score')
        }

    return EvaluationCategory(**self_key)


def update_evaluation_factors_weighted_average(self_key, factor):
    try:
        if isinstance(self_key, dict):
            for i, _factor in enumerate(self_key.get("factors", [])):
                if _normalize_text(
                        _factor.get("title")) == _normalize_text(
                            factor.get('title', '')):
                    del self_key.get("factors", [])[i]
            if not self_key.get("factors"):
                self_key.setdefault("factors", [])
            self_key["factors"].append(factor)
            total_score = sum(factor.get("score") * factor.get("weight", 1)
                              for factor in self_key.get("factors"))
            total_weight = sum(factor.get("weight", 1)
                               for factor in self_key.get("factors"))
            self_key["score"] = total_score / total_weight
        else:
            self_key = self_key.model_dump()
            for i, _factor in enumerate(self_key.get("factors", [])):
                if _normalize_text(
                        _factor.get("title")) == _normalize_text(
                            factor.get('title', '')):
                    del self_key.get("factors", [])[i]
            if not self_key.get("factors"):
                self_key.setdefault("factors", [])
            self_key["factors"].append(factor)
            total_score = sum(factor.get("score") * factor.get("weight", 1)
                              for factor in self_key.get("factors"))
            total_weight = sum(factor.get("weight", 1)
                               for factor in self_key.get("factors"))
            self_key["score"] = total_score / total_weight

    except AttributeError:
        self_key = {
            "factors": [factor],
            "score": factor.get('score')
        }

    return EvaluationCategory(**self_key)


def _normalize_text(text):
    return text.translate(str.maketrans('', '', string.punctuation)).lower()
