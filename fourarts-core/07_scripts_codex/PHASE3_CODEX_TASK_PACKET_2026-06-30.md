# Phase 3 Codex Task Packet｜2026-06-30

Codex（程式代理）只負責機械檢查與批量處理，不做術數正誤裁決。

## Inputs

- `FourArts_Phase3_VERIFIED_RULE_review_100rows_20260630.csv`
- `FourArts_Phase3_Risk_Gate_review_25rows_20260630.csv`
- `FourArts_Phase3_Case_Regression_round1_plan_40rows_20260630.csv`
- `FourArts_Phase3_Codex_Tasklist_20260630.csv`

## Tasks

1. `validate_phase3_columns`：欄位完整性檢查。
2. `validate_line_ranges`：來源檔名與行號格式檢查。
3. `dedupe_rule_candidates`：候選規則去重。
4. `qimen_platecheck_template`：奇門排盤校驗模板。
5. `case_regression_readiness`：案例回歸準備度檢查。

## Expected Outputs

- `missing_columns_report.csv`
- `bad_line_refs_report.csv`
- `duplicate_groups.csv`
- `qimen_platecheck_report.csv`
- `case_missing_fields_report.csv`

## Hard Rules

- `[A]`（AI 推論）不得單獨升 VERIFIED_RULE（核定規則）。
- `[U?]`（使用者疑似裁決）必須雲龍或冷審確認。
- 奇門需先 plate-check validation（排盤校驗）。
- Codex 不得做封板裁決。
