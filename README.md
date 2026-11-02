# Security exercises

[![tests](https://github.com/Icedmango83/exercises/actions/workflows/tests.yml/badge.svg)](https://github.com/Icedmango83/exercises/actions/workflows/tests.yml)

Small, tested security tools from my AI-security learning plan. Each folder is one sub-subject, named by its number and colored by its area.

| # | Exercise | What it does |
|---|---|---|
| ![10.2](https://img.shields.io/badge/10.2-4BDE81?labelColor=0b2216) | [Threat modeling: STRIDE-per-element engine](10.2-threat-modeling/) | Reads a data-flow diagram as JSON and prints the STRIDE threats to check per element, boundary-crossing flows first |

Run any exercise's tests from its folder with `python3 -m pytest`. Every push runs all of them in GitHub Actions.
