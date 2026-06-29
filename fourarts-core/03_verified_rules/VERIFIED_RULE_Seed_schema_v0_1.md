# VERIFIED_RULE_Seed Schema v0.1｜核定規則首批欄位規格

## 定位

`VERIFIED_RULE_Seed`（核定規則種子表）用於承接 61 串教學提取成果與 Drive 既有規則庫，產出第一批可送雲龍／冷審封板的核心規則。

## 狀態定義

- `VERIFIED_CANDIDATE`（核定候選）：來源清楚，可送封板。
- `NEEDS_REVIEW`（待審）：有價值，但來源、污染、版本或語義仍待核。
- `BLOCKED_POLLUTION`（污染封鎖）：疑似污染，不得進規則庫。
- `REJECTED`（否決）：已裁定不可用。

## 欄位

| 欄位 | 中文說明 | 必填 |
|---|---|---|
| rule_id | 規則 ID | 是 |
| category | 術數分類：八字／紫微／六壬／奇門／四術整合／污染 Gate | 是 |
| rule_type | 規則類型：排盤／解盤／用神／流月／案例／禁令 | 是 |
| source_file | 來源檔名 | 是 |
| line_range | 行號範圍 | 是 |
| raw_quote | 原文摘錄 | 是 |
| extracted_rule | 萃取規則 | 是 |
| source_tag | 來源標籤：[U]/[R]/[A]/[?] | 是 |
| pollution_risk | 污染風險：NONE/LOW/MID/HIGH | 是 |
| version_status | 版本狀態：current/historical/conflict/unknown | 是 |
| case_link | 對應案例 ID | 否 |
| gate_link | 對應 Gate ID | 否 |
| status | 狀態 | 是 |
| reviewer | 雲龍／冷審／外部工具 | 否 |
| decision | PASS/PASS-/WARN/BLOCK/FAIL | 否 |
| notes | 備註 | 否 |

## 硬限制

1. `[A]`（AI 推論）不得單獨升 `VERIFIED_RULE`。
2. 缺檔名或行號者不得封板。
3. 疑似污染未排除者不得封板。
4. 奇門真盤需 APP／外部工具／雲龍核盤。
5. 紫微盤底衝突未處理前不得封細節。
