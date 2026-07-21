#!/usr/bin/env python3
"""驗證奇門外部候選搬回包。

本工具只檢查治理、來源、結構與差分施工條件。
它不裁決術數正誤。
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
    "qimen_internal_mainline_profile_v0.1.json",
    "qimen_engine_output_schema_v0.1.json",
    "qimen_differential_case_set_v0.1.json",
]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"缺少檔案：{path.name}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON（結構化資料）格式錯誤：{path.name}: {exc}") from exc


def validate_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        return ["來源登記表沒有來源"]
    for index, source in enumerate(sources):
        prefix = f"sources[{index}]"
        for key in ("source_id", "kind", "license", "roles", "use_mode"):
            if not source.get(key):
                errors.append(f"{prefix} 缺少 {key}")
        if source.get("kind") == "GITHUB_REPOSITORY":
            if not source.get("repository"):
                errors.append(f"{prefix} 缺少 repository（倉庫）")
            if not source.get("commit"):
                errors.append(f"{prefix} 缺少 commit（提交碼）")
        if source.get("upstream_lineage") and source.get("independent_evidence") is True:
            errors.append(f"{prefix} 同源資料不得標成獨立證據")
    return errors


def validate_benchmarks(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    vectors = data.get("vectors")
    if not isinstance(vectors, list) or not vectors:
        return ["基準盤集合沒有向量"]
    seen: set[str] = set()
    for index, vector in enumerate(vectors):
        prefix = f"vectors[{index}]"
        vector_id = vector.get("vector_id")
        if not vector_id:
            errors.append(f"{prefix} 缺少 vector_id（向量編號）")
        elif vector_id in seen:
            errors.append(f"{prefix} 重複 vector_id（向量編號）：{vector_id}")
        else:
            seen.add(vector_id)
        for key in ("datetime_local", "timezone", "expected"):
            if key not in vector:
                errors.append(f"{prefix} 缺少 {key}")
        if vector.get("timezone") == "UNSPECIFIED_RUNTIME_LOCAL":
            if data.get("status") != "EXTERNAL_BENCHMARK_CANDIDATE_NOT_FORMAL_TRUTH":
                errors.append(f"{prefix} 時區未明不得進正式狀態")
    return errors


def validate_method_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = data.get("required_declarations")
    if not isinstance(required, list) or not required:
        errors.append("方法登記表沒有必要聲明欄位")
        return errors
    adapters = data.get("adapters")
    if not isinstance(adapters, list) or not adapters:
        return ["方法登記表沒有適配器"]
    internal_found = False
    for index, adapter in enumerate(adapters):
        prefix = f"adapters[{index}]"
        for key in ("adapter_id", "role", "status"):
            if not adapter.get(key):
                errors.append(f"{prefix} 缺少 {key}")
        if adapter.get("adapter_id") == "INTERNAL_SIXTY_ONE_ROTATING":
            internal_found = True
            for key in required:
                if key not in adapter:
                    errors.append(f"{prefix} 內部主鏈缺少必要口徑 {key}")
            if adapter.get("ju_method") != "ZHIRUN":
                errors.append(f"{prefix} 內部主鏈必須明示置閏")
            if adapter.get("plate_style") != "ROTATING":
                errors.append(f"{prefix} 內部主鏈必須明示轉盤")
    if not internal_found:
        errors.append("方法登記表缺少內部六十一串主鏈")
    return errors


def validate_internal_profile(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("profile_id") != "YUNLONG_QIMEN_INTERNAL_MAINLINE_V0_1":
        errors.append("內部主鏈 profile_id（設定編號）錯誤")
    if not data.get("source_basis"):
        errors.append("內部主鏈沒有來源")
    scope = data.get("scope", {})
    if scope.get("plate_style") != "ROTATING":
        errors.append("內部主鏈未鎖轉盤")
    if scope.get("primary_ju_method") != "ZHIRUN":
        errors.append("內部主鏈未鎖置閏")
    if scope.get("orientation") != "SOUTH_TOP_NORTH_BOTTOM":
        errors.append("內部主鏈未鎖下北上南")
    hidden = data.get("hidden_stems", {})
    if hidden.get("hard_stop_if_undeclared") is not True:
        errors.append("暗干法別未聲明時必須停機")
    return errors


def validate_case_set(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < 2:
        return ["差分案例不足"]
    ids: set[str] = set()
    for index, case in enumerate(cases):
        case_id = case.get("case_id")
        if not case_id:
            errors.append(f"cases[{index}] 缺少 case_id（案例編號）")
        elif case_id in ids:
            errors.append(f"重複案例編號：{case_id}")
        else:
            ids.add(case_id)
        if not case.get("datetime"):
            errors.append(f"cases[{index}] 缺少 datetime（時間）")
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
        errors.extend(validate_internal_profile(loaded["qimen_internal_mainline_profile_v0.1.json"]))
        errors.extend(validate_case_set(loaded["qimen_differential_case_set_v0.1.json"]))
    if errors:
        print("FAIL（失敗）")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS（通過）")
    print(f"- 已驗證 {len(REQUIRED_FILES)} 個 JSON（結構化資料）檔案")
    print("- 來源、源流與獨立證據檢查通過")
    print("- 內部六十一串主鏈口徑檢查通過")
    print("- 外部基準盤安全限制通過")
    print("- 差分案例與方法適配器檢查通過")
    return 0


if __name__ == "__main__":
    sys.exit(main())
