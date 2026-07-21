#!/usr/bin/env python3
"""奇門多引擎差分工具。

用途：
1. 讀取多個已標準化的奇門排盤 JSON（結構化資料）。
2. 依固定層級找出第一個分歧。
3. 輸出差異報告，但不裁決哪個術數口徑正確。

本工具不執行排盤，也不做解盤。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

COMPARE_PATHS: list[tuple[str, ...]] = [
    ("policy", "timezone"),
    ("policy", "true_solar_time_policy"),
    ("policy", "late_zi_hour_mode"),
    ("policy", "day_boundary"),
    ("policy", "plate_style"),
    ("policy", "ju_method"),
    ("policy", "yuan_method"),
    ("policy", "tianqin_lodging"),
    ("policy", "hidden_stem_method"),
    ("calendar", "solar_term"),
    ("calendar", "solar_term_exact_at"),
    ("calendar", "four_pillars"),
    ("calendar", "xun_head"),
    ("calendar", "void_branches"),
    ("ju", "dun"),
    ("ju", "number"),
    ("ju", "yuan"),
    ("plate", "earth_stems"),
    ("ju", "zhifu_star"),
    ("ju", "zhifu_palace"),
    ("ju", "zhishi_door"),
    ("ju", "zhishi_palace"),
    ("plate", "heaven_stems"),
    ("plate", "stars"),
    ("plate", "doors"),
    ("plate", "gods"),
    ("plate", "hidden_stems"),
    ("plate", "void_palaces"),
    ("plate", "horse"),
    ("anomalies",),
]

REQUIRED_TOP_LEVEL = {"case_id", "engine", "policy", "calendar", "ju", "plate", "anomalies"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"找不到檔案：{path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON（結構化資料）格式錯誤：{path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"最上層必須是物件：{path}")
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise ValueError(f"{path} 缺少必要欄位：{', '.join(missing)}")
    return data


def get_path(data: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return {"__missing__": True}
        current = current[key]
    return current


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def engine_label(data: dict[str, Any], fallback: str) -> str:
    engine = data.get("engine", {})
    adapter = engine.get("adapter_id")
    version = engine.get("version")
    if adapter and version:
        return f"{adapter}@{version}"
    return fallback


def compare_documents(documents: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    case_ids = {data.get("case_id") for _, data in documents}
    report: dict[str, Any] = {
        "status": "PASS",
        "case_ids": sorted(str(x) for x in case_ids),
        "engine_count": len(documents),
        "first_divergence": None,
        "differences": [],
        "warnings": [],
        "description_zh_tw": "PASS（通過）只代表輸出一致；不代表術數規則正確。",
    }
    if len(case_ids) != 1:
        report["status"] = "FAIL"
        report["warnings"].append("輸入檔案的 case_id（案例編號）不一致。")
        return report

    labels = [engine_label(data, path.name) for path, data in documents]
    for path_tuple in COMPARE_PATHS:
        values = [get_path(data, path_tuple) for _, data in documents]
        normalized = [canonical(value) for value in values]
        if len(set(normalized)) > 1:
            item = {
                "path": ".".join(path_tuple),
                "values": {labels[i]: values[i] for i in range(len(values))},
            }
            report["differences"].append(item)
            if report["first_divergence"] is None:
                report["first_divergence"] = item
                report["status"] = "DIVERGED"

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="比較多個奇門引擎的標準化輸出。")
    parser.add_argument("inputs", nargs="+", help="兩個以上標準化 JSON（結構化資料）檔案")
    parser.add_argument("--output", help="差分報告輸出路徑；省略時印到畫面")
    args = parser.parse_args()

    if len(args.inputs) < 2:
        print("FAIL（失敗）：至少需要兩個輸入檔案。", file=sys.stderr)
        return 2

    documents: list[tuple[Path, dict[str, Any]]] = []
    try:
        for raw in args.inputs:
            path = Path(raw)
            documents.append((path, load_json(path)))
    except ValueError as exc:
        print(f"FAIL（失敗）：{exc}", file=sys.stderr)
        return 2

    report = compare_documents(documents)
    output_text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        Path(args.output).write_text(output_text, encoding="utf-8")
    else:
        print(output_text, end="")

    return 0 if report["status"] in {"PASS", "DIVERGED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
