#!/usr/bin/env python3
"""Validate the Qimen external import candidate package.

This script checks governance and schema-level invariants only.
It does not decide metaphysical correctness.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_FILES = [
    "qimen_external_source_registry_v0.2.json",
    "qimen_calendar_snapshot_schema_v0.1.json",
    "qimen_method_adapter_registry_v0.1.json",
    "qimen_external_benchmark_vectors_qfdk_v0.1.json",
    "qimen_interpretation_evidence_contract_v0.1.json",
]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path.name}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {path.name}: {exc}") from exc


def validate_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        return ["source registry has no sources"]

    for index, source in enumerate(sources):
        prefix = f"sources[{index}]"
        for key in ("source_id", "kind", "license", "roles", "use_mode"):
            if not source.get(key):
                errors.append(f"{prefix} missing {key}")

        if source.get("kind") == "GITHUB_REPOSITORY":
            if not source.get("repository"):
                errors.append(f"{prefix} missing repository")
            if not source.get("commit"):
                errors.append(f"{prefix} missing commit")

        if source.get("upstream_lineage") and source.get("independent_evidence") is True:
            errors.append(f"{prefix} same-lineage source cannot be independent evidence")

    return errors


def validate_benchmarks(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    vectors = data.get("vectors")
    if not isinstance(vectors, list) or not vectors:
        return ["benchmark set has no vectors"]

    seen: set[str] = set()
    for index, vector in enumerate(vectors):
        prefix = f"vectors[{index}]"
        vector_id = vector.get("vector_id")
        if not vector_id:
            errors.append(f"{prefix} missing vector_id")
        elif vector_id in seen:
            errors.append(f"{prefix} duplicate vector_id: {vector_id}")
        else:
            seen.add(vector_id)

        for key in ("datetime_local", "timezone", "expected"):
            if key not in vector:
                errors.append(f"{prefix} missing {key}")

        if vector.get("timezone") == "UNSPECIFIED_RUNTIME_LOCAL":
            if data.get("status") != "EXTERNAL_BENCHMARK_CANDIDATE_NOT_FORMAL_TRUTH":
                errors.append(f"{prefix} unspecified timezone cannot enter formal status")

    return errors


def validate_method_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = data.get("required_declarations")
    if not isinstance(required, list) or not required:
        errors.append("method registry has no required declarations")

    adapters = data.get("adapters")
    if not isinstance(adapters, list) or not adapters:
        errors.append("method registry has no adapters")
        return errors

    for index, adapter in enumerate(adapters):
        prefix = f"adapters[{index}]"
        for key in ("adapter_id", "role", "status"):
            if not adapter.get(key):
                errors.append(f"{prefix} missing {key}")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    loaded: dict[str, Any] = {}

    for name in REQUIRED_FILES:
        try:
            loaded[name] = load_json(root / name)
        except ValueError as exc:
            errors.append(str(exc))

    if not errors:
        errors.extend(validate_registry(loaded["qimen_external_source_registry_v0.2.json"]))
        errors.extend(validate_benchmarks(loaded["qimen_external_benchmark_vectors_qfdk_v0.1.json"]))
        errors.extend(validate_method_registry(loaded["qimen_method_adapter_registry_v0.1.json"]))

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    print(f"- validated {len(REQUIRED_FILES)} JSON files")
    print("- source lineage and independent-evidence checks passed")
    print("- benchmark candidate safeguards passed")
    print("- method adapter registry checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
