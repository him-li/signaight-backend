from langsearch.models.matcher_results import UnifiedPerson
from collections import Counter
from typing import List
from langsearch.models.matcher_results import ValueRanking


def value_counter(values: List[str]) -> List[ValueRanking]:
    values_counter = dict(Counter(values))
    values_counter = [
        ValueRanking(value=i[0], probability=round(i[1] / len(values), 3), ranking=j, count=i[1])
        for i, j in zip(values_counter.items(), range(1, len(values_counter) + 1))
    ]
    return values_counter


def merge_value_rankings(value_rankings: List[ValueRanking], new_value_rankings: List[ValueRanking]) -> List[ValueRanking]:
    values_to_remove = []
    for new_value_ranking in new_value_rankings:
        for value_ranking in value_rankings:
            if value_ranking.default:
                continue
            if new_value_ranking.value == value_ranking.value:
                new_value_ranking.count += value_ranking.count
                values_to_remove.append(value_ranking)
                break

    value_rankings = [value_ranking for value_ranking in value_rankings if value_ranking not in values_to_remove]

    return update_value_rankings(new_value_rankings + value_rankings)


def update_value_rankings(value_rankings: List[ValueRanking]) -> List[ValueRanking]:
    total_count = sum(value_ranking.count for value_ranking in value_rankings)

    for value_ranking in value_rankings:
        if value_ranking.default:
            continue
        value_ranking.probability = round(value_ranking.count / total_count, 3)

    value_rankings = sorted(value_rankings, key=lambda x: x.probability if not x.default else x.default, reverse=True)

    for i, value_ranking in zip(range(1, len(value_rankings)), value_rankings):
        if value_ranking.default:
            continue
        value_ranking.ranking = i

    return value_rankings
