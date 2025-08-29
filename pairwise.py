#!/usr/bin/env python3
"""Command-line tool for generating pairwise test cases.

This module provides a function :func:`generate_pairwise_tests` implementing a
near-optimal greedy algorithm for pairwise combinatorial testing.  When run as a
script it prompts the user for parameters and values and outputs the resulting
suite as comma separated values so it can easily be copied into spreadsheet
software such as Excel.

The script is platform independent and works on Windows, macOS and Linux.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import sys
from typing import Dict, List


def generate_pairwise_tests(parameters: Dict[str, List[str]]) -> List[Dict[str, str]]:
    """Generate a near-optimal set of pairwise test cases using a greedy algorithm.

    Args:
        parameters: Mapping of parameter name to a list of its possible values.

    Returns:
        A list of dictionaries where each dictionary represents a single test
        case.  Keys are parameter names and values are the selected value for
        that test case.
    """
    # --- 1. Handle Edge Cases ---
    if not parameters or len(parameters) < 2:
        if len(parameters) == 1:
            param_name = next(iter(parameters))
            return [{param_name: value} for value in parameters[param_name]]
        return []

    # --- 2. Generate the Master Set of All Pairs to Be Covered ---
    uncovered_pairs = set()
    param_names = list(parameters.keys())
    for p1_name, p2_name in itertools.combinations(param_names, 2):
        for v1 in parameters[p1_name]:
            for v2 in parameters[p2_name]:
                pair = tuple(sorted(((p1_name, v1), (p2_name, v2))))
                uncovered_pairs.add(pair)

    # --- 3. Iteratively Build Test Cases ---
    test_cases: List[Dict[str, str]] = []
    sorted_params = sorted(parameters, key=lambda p: len(parameters[p]), reverse=True)

    while uncovered_pairs:
        current_test_case: Dict[str, str] = {}
        for param_name in sorted_params:
            best_value = None
            max_covered = -1
            for value in parameters[param_name]:
                newly_covered_count = 0
                for existing_param, existing_value in current_test_case.items():
                    pair_to_check = tuple(sorted(((param_name, value), (existing_param, existing_value))))
                    if pair_to_check in uncovered_pairs:
                        newly_covered_count += 1
                if newly_covered_count > max_covered:
                    max_covered = newly_covered_count
                    best_value = value
            if best_value is None:
                best_value = parameters[param_name][0]
            current_test_case[param_name] = best_value
        test_cases.append(current_test_case)
        pairs_in_new_case = set()
        for p1_name, p2_name in itertools.combinations(current_test_case, 2):
            pair = tuple(sorted(((p1_name, current_test_case[p1_name]), (p2_name, current_test_case[p2_name]))))
            pairs_in_new_case.add(pair)
        uncovered_pairs -= pairs_in_new_case
    return test_cases


def collect_parameters() -> Dict[str, List[str]]:
    """Interactively collect parameters and their values from the user."""
    params: Dict[str, List[str]] = {}
    print("Enter parameters for pairwise testing. Type 'done' when finished.\n")
    while True:
        name = input("Parameter name (or 'done'): ").strip()
        if not name:
            continue
        if name.lower() == "done":
            break
        values_input = input(f"Values for '{name}' separated by commas: ").strip()
        values = [v.strip() for v in values_input.split(',') if v.strip()]
        if not values:
            print("No values entered, parameter ignored.\n")
            continue
        params[name] = values
    return params


def output_csv(test_cases: List[Dict[str, str]], fieldnames: List[str], out_file: str | None) -> None:
    """Write the test cases as CSV either to a file or to stdout."""
    if out_file:
        with open(out_file, 'w', newline='', encoding='utf-8') as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(test_cases)
        print(f"Wrote {len(test_cases)} test cases to '{out_file}'.")
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(test_cases)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate pairwise test cases.")
    parser.add_argument('-o', '--output', help='Optional path to CSV file for saving the results.')
    args = parser.parse_args(argv)

    parameters = collect_parameters()
    if not parameters:
        print("No parameters entered. Exiting.")
        return 1
    test_cases = generate_pairwise_tests(parameters)
    output_csv(test_cases, list(parameters.keys()), args.output)
    return 0


if __name__ == '__main__':  # pragma: no cover - CLI entry point
    raise SystemExit(main())
