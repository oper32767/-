from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable


REQUIRED_BIRTH_FIELDS = ("year", "month", "day", "hour")
VALID_ANSWERS = {"A", "B", "C", "D"}


@dataclass
class AuditFinding:
    severity: str
    code: str
    item_id: str
    message: str


@dataclass
class NormalizedQuestion:
    question_id: str
    case_id: str
    category: str
    birth: dict[str, Any]
    question: str
    options: list[dict[str, str]]
    answer: str
    source_file: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_options(raw: Any) -> list[dict[str, str]]:
    if not isinstance(raw, list):
        return []
    options: list[dict[str, str]] = []
    for index, item in enumerate(raw):
        fallback_letter = chr(ord("A") + index)
        if isinstance(item, dict):
            letter = str(item.get("letter", fallback_letter)).strip().upper()
            text = str(item.get("text", "")).strip()
        else:
            text = str(item).strip()
            letter = fallback_letter
            if len(text) >= 2 and text[0].upper() in VALID_ANSWERS and text[1] in {".", "、", ")", "：", ":"}:
                letter = text[0].upper()
                text = text[2:].strip()
        options.append({"letter": letter, "text": text})
    return options


def iter_baziqa(data: Any, source_file: str) -> Iterable[NormalizedQuestion]:
    if not isinstance(data, list):
        raise ValueError("BaziQA input must be a JSON list")
    for person in data:
        if not isinstance(person, dict) or "questions" not in person:
            continue
        profile = person.get("profile") or {}
        birth = (profile.get("birth") or {}) if isinstance(profile, dict) else {}
        case_id = str(person.get("person_id") or person.get("name") or "unknown_case")
        categories = person.get("categories") or {}
        question_category: dict[str, str] = {}
        if isinstance(categories, dict):
            for category, events in categories.items():
                if isinstance(events, list):
                    for event in events:
                        question_category[str(event)] = str(category)
        for question in person.get("questions") or []:
            if not isinstance(question, dict):
                continue
            yield NormalizedQuestion(
                question_id=str(question.get("question_id") or ""),
                case_id=case_id,
                category=str(question.get("category") or "unclassified"),
                birth=dict(birth),
                question=str(question.get("question") or "").strip(),
                options=normalize_options(question.get("options")),
                answer=str(question.get("answer") or "").strip().upper(),
                source_file=source_file,
            )


def iter_mingli(data: Any, source_file: str) -> Iterable[NormalizedQuestion]:
    if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
        raise ValueError("MingLi-Bench input must contain a questions list")
    for question in data["questions"]:
        if not isinstance(question, dict):
            continue
        yield NormalizedQuestion(
            question_id=str(question.get("id") or ""),
            case_id=str(question.get("case_id") or "unknown_case"),
            category=str(question.get("category") or "unclassified"),
            birth=dict(question.get("birth_info") or {}),
            question=str(question.get("question") or "").strip(),
            options=normalize_options(question.get("options")),
            answer=str(question.get("answer") or "").strip().upper(),
            source_file=source_file,
        )


def audit_questions(questions: list[NormalizedQuestion]) -> tuple[dict[str, Any], list[AuditFinding]]:
    findings: list[AuditFinding] = []
    seen_ids: set[str] = set()
    category_counts: Counter[str] = Counter()
    case_counts: Counter[str] = Counter()

    for item in questions:
        category_counts[item.category] += 1
        case_counts[item.case_id] += 1
        item_id = item.question_id or "<missing>"

        if not item.question_id:
            findings.append(AuditFinding("BLOCK", "MISSING_QUESTION_ID", item_id, "Question id is empty"))
        elif item.question_id in seen_ids:
            findings.append(AuditFinding("BLOCK", "DUPLICATE_QUESTION_ID", item_id, "Question id is duplicated"))
        seen_ids.add(item.question_id)

        missing_birth = [field for field in REQUIRED_BIRTH_FIELDS if item.birth.get(field) in (None, "")]
        if missing_birth:
            findings.append(
                AuditFinding(
                    "WARN",
                    "INCOMPLETE_BIRTH",
                    item_id,
                    f"Missing birth fields: {', '.join(missing_birth)}",
                )
            )

        if item.answer not in VALID_ANSWERS:
            findings.append(AuditFinding("BLOCK", "INVALID_ANSWER", item_id, f"Answer is {item.answer!r}"))

        option_letters = [option.get("letter") for option in item.options]
        if len(item.options) != 4 or set(option_letters) != VALID_ANSWERS:
            findings.append(
                AuditFinding(
                    "WARN",
                    "NONSTANDARD_OPTIONS",
                    item_id,
                    f"Expected A-D exactly; found {option_letters}",
                )
            )

        if not item.question:
            findings.append(AuditFinding("BLOCK", "EMPTY_QUESTION", item_id, "Question text is empty"))

        if item.answer and item.answer not in option_letters:
            findings.append(
                AuditFinding(
                    "BLOCK",
                    "ANSWER_NOT_IN_OPTIONS",
                    item_id,
                    "Answer key does not exist in options",
                )
            )

        # A dataset can be internally consistent and still lack independent provenance.
        # This is intentionally WARN rather than PASS: source evidence must be audited separately.
        if not item.birth.get("source") and not item.birth.get("reliability"):
            findings.append(
                AuditFinding(
                    "WARN",
                    "NO_BIRTH_PROVENANCE",
                    item_id,
                    "No independent birth source or reliability grade is embedded",
                )
            )

    severity_counts = Counter(finding.severity for finding in findings)
    summary = {
        "question_count": len(questions),
        "case_count": len(case_counts),
        "category_counts": dict(sorted(category_counts.items())),
        "severity_counts": dict(sorted(severity_counts.items())),
        "ready_for_blind_pilot": severity_counts.get("BLOCK", 0) == 0 and len(questions) > 0,
    }
    return summary, findings


def split_blind_package(
    questions: list[NormalizedQuestion], output_dir: Path, sample_size: int
) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    selected = questions[:sample_size] if sample_size > 0 else questions

    booklet = []
    answer_key = []
    for item in selected:
        public_item = asdict(item)
        answer = public_item.pop("answer")
        booklet.append(public_item)
        answer_key.append({"question_id": item.question_id, "answer": answer})

    booklet_path = output_dir / "blind_booklet.json"
    key_path = output_dir / "sealed_answer_key.json"
    manifest_path = output_dir / "manifest.json"

    booklet_path.write_text(json.dumps(booklet, ensure_ascii=False, indent=2), encoding="utf-8")
    key_path.write_text(json.dumps(answer_key, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {
        "booklet_sha256": sha256_file(booklet_path),
        "answer_key_sha256": sha256_file(key_path),
        "question_count": len(selected),
        "warning": "Keep the sealed answer key away from the execution model.",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"booklet": str(booklet_path), "answer_key": str(key_path), "manifest": str(manifest_path)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a public fortune-telling benchmark before blind evaluation")
    parser.add_argument("--adapter", required=True, choices=("baziqa", "mingli"))
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--sample-size", type=int, default=10)
    args = parser.parse_args()

    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        iterator = iter_baziqa(raw, args.input.name) if args.adapter == "baziqa" else iter_mingli(raw, args.input.name)
        questions = list(iterator)
        summary, findings = audit_questions(questions)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        report = {
            "source_file": str(args.input),
            "source_sha256": sha256_file(args.input),
            "adapter": args.adapter,
            "summary": summary,
            "findings": [asdict(finding) for finding in findings],
        }
        report_path = args.output_dir / "audit_report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        package = split_blind_package(questions, args.output_dir / "pilot", args.sample_size)
        print(json.dumps({"audit_report": str(report_path), "pilot": package, "summary": summary}, ensure_ascii=False, indent=2))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"audit failed: {exc}") from exc


if __name__ == "__main__":
    main()
