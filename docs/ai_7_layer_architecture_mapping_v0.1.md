# AI 七層架構對照表 v0.1

日期：2026-06-17

## 1. 來源定位

本文件根據使用者提供的「AI 七層架構」整理，並對照 OpenAI 官方工具線。

使用者原始七層：

```text
Token（詞元／最小符號單位）
Prompt（提示詞）
Context（上下文）
Agent（智能體／代理程式）
Harness（流程框架／外層控制架構）
MCP（Model Context Protocol，模型上下文協定／連接層）
Skills（技能沉澱）
```

---

## 2. 七層架構與本專案對應

| 層級 | 英文術語＋中文標示 | 原始意思 | 本專案對應 |
|---|---|---|---|
| 1 | Token（詞元／最小符號單位） | AI 處理文字的底層單位 | 文字、Markdown（純文字文件格式）、CSV（逗號分隔表格）、XLSX（Excel 試算表）等資料切片 |
| 2 | Prompt（提示詞） | 使用者給 AI 的指令 | v4.0 打包提示詞、Skill（技能）啟動口令、NotebookLM（Google 筆記型 AI 工具）更新指令 |
| 3 | Context（上下文） | 短期記憶與外部資料 | 60 串原文、第 61 串、核心表、糾正鏈、NotebookLM 資料庫 |
| 4 | Agent（智能體／代理程式） | 可拆任務、調工具、執行流程的 AI 工作單元 | Source Agent（來源蒐集員）、Gate Agent（檢核員）、Static Agent（靜態運算員）、Dynamic Agent（動態運算員） |
| 5 | Harness（流程框架／外層控制架構） | 控制任務順序、條件與多步驟流程 | HumanMachine_Harness、Trace_Log（追蹤紀錄）、Ratchet_Log（防回退紀錄）、Gate（檢核閘門） |
| 6 | MCP（模型上下文協定／連接層） | 讓 AI 接外部工具與資料 | Google Drive（雲端硬碟）、GitHub（版本控制／程式碼倉庫）、Gmail、Calendar、外部 API（應用程式介面） |
| 7 | Skills（技能沉澱） | 可複用的流程、規則、模板 | 八字紫微 Skill（技能）、四術整合 Skill（技能）、靜態／動態樣本策略、Gate 規則 |

---

## 3. OpenAI 官方工具對照

| OpenAI 工具 | 中文標示 | 對應層級 | 本專案用途 |
|---|---|---|---|
| Responses API | 回應 API | 第 3～6 層 | 新工程若要用 OpenAI API，應優先以 Responses API 作統一入口 |
| Agents SDK | 代理程式開發套件 | 第 4 層 | 後續若要把 Source／Gate／Static／Dynamic Agent 程式化，可用 Agents SDK |
| MCP and Connectors | MCP（模型上下文協定）與連接器 | 第 6 層 | 連 Google Drive、GitHub、外部資料源 |
| Skills | 技能 | 第 7 層 | 把四術流程、Gate、樣本策略做成可複用技能 |
| Realtime API | 即時 API | 第 4～6 層 | 暫不列第一優先；可作語音、即時互動或即時工具調用研究 |
| Agent Builder | 代理程式建構器 | 第 4～5 層 | 暫列候選；需再確認實際可用性、權限、是否適合本案 |

---

## 4. 本專案採用裁定

```text
短期不先做商業化或完整 Agent 平台。
先做 GitHub + NotebookLM + Skill + 樣本庫 + Gate。
```

第一階段落地順序：

1. Context（上下文）：60+1 原文庫與核心表整理。
2. Skills（技能）：八字紫微 Skill、四術整合 Skill。
3. Harness（流程框架）：主線總控表、Gate、Trace、Ratchet。
4. MCP／Connector（連接層）：GitHub、Google Drive、NotebookLM。
5. Agent（代理程式）：先文件化分工，不急著全自動。
6. Validation Samples（驗證樣本）：靜態 10 筆、動態 10 筆。

---

## 5. 對四術 MVP 的對應

| 四術工程 | 對應七層 |
|---|---|
| 60 串原文與第 61 串 | Context（上下文） |
| 八字紫微靜態層 Skill | Skills（技能） |
| 六壬奇門動態層 SOP | Skills（技能） |
| 樣本 Gate | Harness（流程框架） |
| GitHub 倉庫 | MCP／Connector（連接層）與版本控制 |
| NotebookLM | Context（上下文）與檢索輔助 |
| Agent 分工 | Agent（代理程式） |

---

## 6. 禁止誤用

1. 不得把 Prompt（提示詞）當成完整系統。
2. 不得只有 Context（上下文）就宣稱會算。
3. 不得只有 Agent（代理程式）名稱，沒有 Gate（檢核閘門）與樣本驗證。
4. 不得把 MCP（連接層）當萬能；連接器只負責接資料，不負責判斷正確。
5. 不得把 Skills（技能）當封板；技能只是可複用規則，仍需測試。
6. 不得用商業變現敘事壓過四術 MVP 準度驗證。

---

## 7. 下一步

1. 建立 `samples/static_cases_seed_v0.1.csv`。
2. 建立 `samples/dynamic_cases_seed_v0.1.csv`。
3. 建立 `schemas/static_case.schema.json`。
4. 建立 `schemas/dynamic_case.schema.json`。
5. 將 AI 七層架構納入主線總控表。
