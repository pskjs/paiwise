from __future__ import annotations

from itertools import combinations
from typing import Dict, Iterable, List, Tuple, FrozenSet


Pair = FrozenSet[Tuple[str, object]]


def _pair_key(p1: str, v1, p2: str, v2) -> Pair:
    """Return a canonical representation for a pair of parameter values."""
    return frozenset(((p1, v1), (p2, v2)))


def generate_pairwise_tests(parameters: Dict[str, Iterable[object]]) -> List[Dict[str, object]]:
    """Generate a set of test cases that provides pairwise coverage.

    Parameters
    ----------
    parameters:
        Mapping of parameter names to iterables of possible values.

    Returns
    -------
    List[Dict[str, object]]
        A list of dictionaries representing test cases.

    Raises
    ------
    ValueError
        If no progress can be made towards covering new pairs, which would
        otherwise result in an infinite loop.
    """

    param_names = list(parameters)
    # Build the set of all pairs that must be covered
    uncovered_pairs: set[Pair] = set()
    for p1, p2 in combinations(param_names, 2):
        for v1 in parameters[p1]:
            for v2 in parameters[p2]:
                uncovered_pairs.add(_pair_key(p1, v1, p2, v2))

    tests: List[Dict[str, object]] = []
    while uncovered_pairs:
        test_case: Dict[str, object] = {}
        # Choose a value for each parameter greedily based on remaining coverage
        for param in param_names:
            best_value = None
            best_score = -1
            for value in parameters[param]:
                score = 0
                for other in param_names:
                    if other == param:
                        continue
                    if other in test_case:
                        pair = _pair_key(param, value, other, test_case[other])
                        if pair in uncovered_pairs:
                            score += 1
                    else:
                        for ov in parameters[other]:
                            pair = _pair_key(param, value, other, ov)
                            if pair in uncovered_pairs:
                                score += 1
                if score > best_score:
                    best_value, best_score = value, score
            test_case[param] = best_value

        # Determine which uncovered pairs are exercised by this test case
        pairs_in_new_case = set()
        for p1, p2 in combinations(param_names, 2):
            pair = _pair_key(p1, test_case[p1], p2, test_case[p2])
            pairs_in_new_case.add(pair)

        newly_covered = pairs_in_new_case & uncovered_pairs
        if not newly_covered:
            raise ValueError(
                "Generated test case does not cover any new pairs; algorithm stalled"
            )

        tests.append(test_case)
        uncovered_pairs -= newly_covered

    return tests
