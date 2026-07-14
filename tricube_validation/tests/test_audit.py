import json
import tempfile
import unittest
from pathlib import Path

from tricube_validation.audit import (
    audit_questions,
    iter_baziqa,
    iter_mingli,
    split_blind_package,
)


class AuditTests(unittest.TestCase):
    def test_baziqa_adapter_and_sealing(self) -> None:
        raw = [
            {"contest_id": "demo", "total_questions": 1},
            {
                "person_id": "p1",
                "profile": {
                    "birth": {"year": 2000, "month": 1, "day": 2, "hour": 3},
                    "gender": "male",
                },
                "questions": [
                    {
                        "question_id": "q1",
                        "question": "Demo?",
                        "options": ["A. One", "B. Two", "C. Three", "D. Four"],
                        "answer": "B",
                    }
                ],
            },
        ]
        questions = list(iter_baziqa(raw, "demo.json"))
        summary, findings = audit_questions(questions)
        self.assertEqual(summary["question_count"], 1)
        self.assertEqual(summary["case_count"], 1)
        self.assertFalse(any(item.severity == "BLOCK" for item in findings))

        with tempfile.TemporaryDirectory() as temp_dir:
            paths = split_blind_package(questions, Path(temp_dir), 10)
            booklet = json.loads(Path(paths["booklet"]).read_text(encoding="utf-8"))
            key = json.loads(Path(paths["answer_key"]).read_text(encoding="utf-8"))
            self.assertNotIn("answer", booklet[0])
            self.assertEqual(key[0]["answer"], "B")

    def test_mingli_adapter(self) -> None:
        raw = {
            "questions": [
                {
                    "id": "ftb_1",
                    "case_id": "case_1",
                    "birth_info": {
                        "gender": "男",
                        "year": 1974,
                        "month": 4,
                        "day": 28,
                        "hour": 16,
                    },
                    "question": "What happened?",
                    "options": [
                        {"letter": "A", "text": "a"},
                        {"letter": "B", "text": "b"},
                        {"letter": "C", "text": "c"},
                        {"letter": "D", "text": "d"},
                    ],
                    "answer": "C",
                    "category": "健康",
                }
            ]
        }
        questions = list(iter_mingli(raw, "data.json"))
        summary, findings = audit_questions(questions)
        self.assertEqual(summary["category_counts"], {"健康": 1})
        self.assertFalse(any(item.severity == "BLOCK" for item in findings))

    def test_invalid_answer_blocks(self) -> None:
        raw = {
            "questions": [
                {
                    "id": "bad",
                    "case_id": "case_bad",
                    "birth_info": {"year": 2000, "month": 1, "day": 1, "hour": 0},
                    "question": "Bad answer",
                    "options": [
                        {"letter": "A", "text": "a"},
                        {"letter": "B", "text": "b"},
                        {"letter": "C", "text": "c"},
                        {"letter": "D", "text": "d"},
                    ],
                    "answer": "E",
                }
            ]
        }
        questions = list(iter_mingli(raw, "bad.json"))
        _, findings = audit_questions(questions)
        codes = {item.code for item in findings if item.severity == "BLOCK"}
        self.assertIn("INVALID_ANSWER", codes)
        self.assertIn("ANSWER_NOT_IN_OPTIONS", codes)


if __name__ == "__main__":
    unittest.main()
