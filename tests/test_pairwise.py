from pathlib import Path
import json
import subprocess
import sys

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


def test_cli_invocation_generates_cases():
    script = Path(__file__).resolve().parent.parent / "pairwise.py"
    cmd = [sys.executable, str(script)]
    user_input = "a\n0,1\nb\n0,1\ndone\n"
    result = subprocess.run(
        cmd, input=user_input, capture_output=True, text=True, check=True
    )

    cases = [
        json.loads(line)
        for line in result.stdout.splitlines()
        if line.startswith("{")
    ]
    seen_pairs = {
        frozenset((("a", case["a"]), ("b", case["b"])))
        for case in cases
    }

    expected_pairs = {
        frozenset((("a", a), ("b", b)))
        for a in ["0", "1"]
        for b in ["0", "1"]
    }
    assert seen_pairs == expected_pairs
