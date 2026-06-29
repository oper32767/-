# FourArts Core｜四術工程版本庫

本倉庫用於承接雲龍四術工程的版本控管。

## 定位

- `RAW_SOURCE`（原始來源）：61 串原始對話與行號語料仍以私域封版包保存，不直接放入 public repo（公開倉庫）。
- `TEACHING_EXTRACTION`（教學提取）：只放欄位結構、索引說明與封版聲明，不放未匿名全文。
- `VERIFIED_RULE`（核定規則）：只收經雲龍或冷審確認的規則。
- `CASE_REGRESSION`（案例回歸）：只收可驗證、已匿名、可追溯案例。
- `POLLUTION_GATE`（污染閘門）：收 AI 失敗樣本與禁止再犯規則。
- `SKILL`（技能規格）：收可給模型／代理／Codex 執行的規格。

## 目前狀態｜2026-06-30

- 61 串來源與術數教學提取分類已暫時封版。
- Drive 內已有：高承重糾正鏈、現行規則庫與錯誤 Gate、四術準度封板衝刺表、HumanMachine Harness。
- GitHub 目前作為版本庫骨架，不承載私人原文。

## 下一步

1. 建立 `VERIFIED_RULE_Seed_v0.1`（首批 200 條）。
2. 建立 `Pollution_Gate_Seed_v0.1`（首批 50 條）。
3. 建立 `Case_Regression_v0.1`（四術 40 案）。
4. 建立 `Codex_Tasklist_v0.1`（批量去重、欄位檢查、行號校驗）。

雲龍為最終裁決者；AI／代理／Codex 只負責整理、檢查、產出候選，不得自行封板術數正誤。
