from pairwise import generate_pairwise_tests


def test_generate_pairwise_binary_parameters():
    params = {
        "a": [0, 1],
        "b": [0, 1],
        "c": [0, 1],
    }
    cases = generate_pairwise_tests(params)

    # Ensure all pairs are covered
    seen_pairs = set()
    names = list(params)
    for case in cases:
        for i, p1 in enumerate(names):
            for p2 in names[i + 1 :]:
                pair = frozenset(((p1, case[p1]), (p2, case[p2])))
                seen_pairs.add(pair)

    expected_pairs = set()
    for i, p1 in enumerate(names):
        for p2 in names[i + 1 :]:
            for v1 in params[p1]:
                for v2 in params[p2]:
                    expected_pairs.add(frozenset(((p1, v1), (p2, v2))))

    assert seen_pairs == expected_pairs
