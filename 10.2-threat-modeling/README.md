<img src="assets/banner.svg" alt="10.2 Threat modeling: STRIDE-per-element engine" width="100%">

[![tests](https://github.com/Icedmango83/exercises/actions/workflows/tests.yml/badge.svg)](https://github.com/Icedmango83/exercises/actions/workflows/tests.yml)
![area](https://img.shields.io/badge/area-10.2%20Threat%20modeling-4BDE81?labelColor=0b2216)
![python](https://img.shields.io/badge/python-3.12-4BDE81?labelColor=0b2216)
![tests](https://img.shields.io/badge/tests-10-4BDE81?labelColor=0b2216)

# STRIDE-per-element engine

A small threat-modeling tool. It reads a system's **data-flow diagram** as JSON, decides which **STRIDE** threats must be checked for every element, and prints a checklist with the **flows that cross a trust boundary first**, because that's where most threats live.

```
$ python3 stride.py clinicbook.json
DF1   [boundary]  D I T
DF4   [boundary]  D I T
E1                R S
E2                R S
P1                D E I R S T
D2                D I T
D3                D I R T
DF6               D I T

26 checks in total
```

## The system it models

`clinicbook.json` describes **ClinicBook**, a fictional clinic booking app:

```mermaid
flowchart LR
  subgraph TB1["internet (untrusted)"]
    E1["E1 · Patient browser"]
    E2["E2 · Clinic SSO"]
  end
  subgraph APP["application"]
    P1(("P1 · ClinicBook API"))
  end
  subgraph TB2["data"]
    D2[("D2 · Visit notes")]
    D3[("D3 · Audit log")]
  end
  E1 -- DF1 · crosses boundary --> P1
  P1 -- DF4 · crosses boundary --> D2
  P1 --> D3
  P1 -- DF6 --> P2["P2 · Notification worker"]
```

## The rule it applies: STRIDE-per-element

Each type of diagram element can only suffer certain threats:

| Element type | Letters | Why |
|---|---|---|
| External entity | **S R** | someone can pretend to be it, or it can deny an action |
| Process | **S T R I D E** | code that acts can be attacked in every way |
| Data store | **T I D** (+ **R** if it holds logs) | data at rest can be changed, read or made unavailable |
| Data flow | **T I D** | data in transit can be changed, read or blocked |

STRIDE = **S**poofing · **T**ampering · **R**epudiation · **I**nformation disclosure · **D**enial of service · **E**levation of privilege.

## How it's built

| Function | Job |
|---|---|
| `threats_for(element)` | letters for one element; copies the rule table and raises `ValueError` on unknown types |
| `prioritize(model)` | element IDs, boundary-crossing flows first, file order kept |
| `format_line(id, boundary, letters)` | one fixed-width report line |
| `total_checks(model)` | how many checks the whole system needs |
| `main(path)` | loads the JSON and prints the report (only when run directly) |

## Two bug classes it guards against

1. **Shared state.** Adding `R` to the rule table itself (instead of a copy) would silently give every later store an `R`. Guarded by `test_store_order_does_not_leak`.
2. **Presence vs value.** `"holds_logs" in element` is true even for `"holds_logs": false`. The tool reads the value with `.get("holds_logs", False)`. Guarded by `test_holds_logs_false_means_no_r`.

## Run it

```bash
python3 stride.py clinicbook.json
python3 -m pytest
```

Requires Python 3.10+ (no dependencies) and `pytest` for the tests.
