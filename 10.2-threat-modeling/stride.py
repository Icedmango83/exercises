"""STRIDE-per-element: which threats to check for each element of a system model."""
import json
import sys

# Which STRIDE letters apply to each element type.
BASE = {
    "external": {"S", "R"},
    "process": {"S", "T", "R", "I", "D", "E"},
    "store": {"T", "I", "D"},
    "flow": {"T", "I", "D"},
}


def threats_for(element):
    """Return the set of STRIDE letters that apply to one element."""
    kind = element.get("type")
    if kind not in BASE:
        raise ValueError(f"unknown element type: {kind}")
    letters = set(BASE[kind])  # a copy, so the table itself never changes
    if kind == "store" and element.get("holds_logs", False):
        letters.add("R")
    return letters


def prioritize(model):
    """Return element IDs: boundary-crossing flows first, then the rest, in file order."""
    first, rest = [], []
    for element in model["elements"]:
        if element["type"] == "flow" and element.get("crosses_boundary", False):
            first.append(element["id"])
        else:
            rest.append(element["id"])
    return first + rest


def total_checks(model):
    """Count every STRIDE check the team has to do."""
    total = 0
    for element in model["elements"]:
        total = total + len(threats_for(element))
    return total


def format_line(element_id, boundary, letters):
    """One report line: ID, boundary tag, sorted letters, in fixed-width columns."""
    tag = "[boundary]" if boundary else ""
    text = " ".join(sorted(letters))
    return f"{element_id:<5} {tag:<11} {text}"


def main(path):
    with open(path) as f:
        model = json.load(f)
    by_id = {}
    for element in model["elements"]:
        by_id[element["id"]] = element
    for element_id in prioritize(model):
        element = by_id[element_id]
        print(format_line(element_id, element.get("crosses_boundary", False), threats_for(element)))
    print(f"\n{total_checks(model)} checks in total")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python3 stride.py MODEL.json")
    main(sys.argv[1])