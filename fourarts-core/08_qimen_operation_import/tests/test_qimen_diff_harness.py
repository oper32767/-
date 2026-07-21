#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "qimen_diff_harness.py"
SPEC = importlib.util.spec_from_file_location("qimen_diff_harness", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def sample(adapter: str, ju_number: int = 6) -> dict:
    return {
        "case_id": "CASE-1",
        "engine": {"adapter_id": adapter, "version": "1"},
        "policy": {
            "timezone": "Asia/Taipei",
            "true_solar_time_policy": "CIVIL_TIME",
            "late_zi_hour_mode": "NOT_APPLICABLE",
            "day_boundary": "MIDNIGHT",
            "plate_style": "ROTATING",
            "ju_method": "ZHIRUN",
            "yuan_method": "FU_HEAD",
            "tianqin_lodging": "KUN_2",
            "hidden_stem_method": "METHOD_A"
        },
        "calendar": {
            "datetime": "2026-06-05T16:52:00+08:00",
            "solar_term": "芒種",
            "solar_term_exact_at": None,
            "four_pillars": {
                "year": "丙午",
                "month": "甲午",
                "day": "庚戌",
                "hour": "甲申"
            },
            "xun_head": "甲申庚",
            "void_branches": ["午", "未"]
        },
        "ju": {
            "dun": "YANG",
            "number": ju_number,
            "yuan": "UPPER",
            "zhifu_star": "天任",
            "zhifu_palace": 8,
            "zhishi_door": "生門",
            "zhishi_palace": 8
        },
        "plate": {
            "earth_stems": {"1": "壬"},
            "heaven_stems": {"1": "壬"},
            "stars": {"1": "天蓬"},
            "doors": {"1": "休門"},
            "gods": {"1": "九天"},
            "hidden_stems": {"1": "丙"},
            "void_palaces": [],
            "horse": None
        },
        "anomalies": []
    }


class HarnessTests(unittest.TestCase):
    def test_pass_for_identical_outputs(self) -> None:
        report = MODULE.compare_documents([
            (Path("a.json"), sample("A")),
            (Path("b.json"), sample("B"))
        ])
        self.assertEqual(report["status"], "PASS")
        self.assertIsNone(report["first_divergence"])

    def test_first_divergence_is_ju_number(self) -> None:
        report = MODULE.compare_documents([
            (Path("a.json"), sample("A", 6)),
            (Path("b.json"), sample("B", 3))
        ])
        self.assertEqual(report["status"], "DIVERGED")
        self.assertEqual(report["first_divergence"]["path"], "ju.number")


if __name__ == "__main__":
    unittest.main()
