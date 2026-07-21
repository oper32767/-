# 奇門排盤・解盤・運籌候選施工包 v0.3

> 狀態：`EXTERNAL_CANDIDATE`（外部候選）＋`INTERNAL_MAINLINE_MAPPING`（內部主鏈映射）  
> 日期：2026-07-22  
> 適用倉庫：全術數 60+1 主線總控倉庫

## 0. 定位

本目錄只搬回可驗證、可重跑、可審計的工程方法、測試向量與公版來源導航，並把六十一串奇門主鏈轉成機器可讀設定。

本包不修改：

- 《四術算法依據庫 v1.0》；
- 六十一串既有封板；
- 任何正式 `rule_id`（規則編號）；
- 主分支上的正式奇門結果。

## 1. 來源源流

經雲龍依自身學習來源確認：

- 陰盤奇門普遍所稱「四害」為擊刑、入墓、門迫、空亡；
- 荀爽 YouTube（影音平台）教學另形成「六害」口徑：四害加白虎、庚；
- 六十一串與 `skyfiredao/qmenpowers` 的六害、化氣陣內容屬同一上游源流；
- 同源資料不得重複計票；
- 外部倉庫可提供獨立工程實作，但不構成獨立術數驗證。

## 2. v0.3 已完成施工

### 2.1 六十一串內部主鏈接入

新增 `qimen_internal_mainline_profile_v0.1.json`，鎖定：

- 時家、轉盤、置閏主鏈；
- 九宮下北上南；
- 排盤從零重建；
- 中五寄坤，寄星與寄干同步；
- 暗干先聲明法別；
- 異常摘要先於解盤；
- 日干看求測人、時干看問事；
- 用神落宮整包；
- 排盤、解盤、運籌分鏈。

### 2.2 多引擎統一輸出

新增 `qimen_engine_output_schema_v0.1.json`，規定每個引擎都要輸出：

- 時間與方法政策；
- 節氣、四柱、旬首；
- 陰陽遁、局數、三元；
- 值符、值使；
- 天地盤、九星、八門、八神；
- 暗干、空亡、馬星；
- 擊刑、入墓、門迫等異常。

### 2.3 固定差分案例

新增 `qimen_differential_case_set_v0.1.json`：

- 六組外部基準盤回放；
- 晚子時同日／次日雙政策測試；
- 節氣邊界測試標記。

外部基準未明示時區者只作回放候選，不進正式答案。

### 2.4 可執行差分工具

新增 `tools/qimen_diff_harness.py`。

`harness`（測試支架）會：

1. 讀取兩個以上標準化 JSON（結構化資料）；
2. 按時間政策、曆法、定局、天地盤、星門神、暗干、異常的順序比較；
3. 回報第一個分歧；
4. 保留全部差異；
5. 不裁決哪一方正確。

### 2.5 工具自身測試

新增 `tests/test_qimen_diff_harness.py`，至少驗證：

- 相同結果輸出 `PASS`（通過）；
- 局數不同時，第一差異能指向 `ju.number`（局數欄位）。

### 2.6 GitHub Actions（GitHub 自動化工作流程）

新增 `.github/workflows/qimen-import-check.yml`，每次相關檔案變更會自動執行：

- 候選包結構驗證；
- 六十一串內部主鏈口徑驗證；
- 差分工具單元測試。

## 3. 主要檔案

| 檔案 | 用途 |
|---|---|
| `qimen_internal_mainline_profile_v0.1.json` | 六十一串內部奇門主鏈機器設定 |
| `qimen_method_adapter_registry_v0.1.json` | 內外引擎方法、版本、源流與缺口登記 |
| `qimen_engine_output_schema_v0.1.json` | 多引擎統一輸出格式 |
| `qimen_differential_case_set_v0.1.json` | 固定回放與邊界案例 |
| `tools/qimen_diff_harness.py` | 找出多引擎第一分歧 |
| `tests/test_qimen_diff_harness.py` | 驗證差分工具本身 |
| `qimen_mainline_integration_and_diff_guide_v0.1.md` | 說明各零件的用途 |
| `qimen_operation_candidate_contract_v0.1.json` | 運籌輸入、證據、輸出與停機契約 |
| `qimen_operation_gate_candidate_v0.1.md` | 運籌前置 Gate（閘門） |
| `qimen_timing_candidate_scoring_v0.1.md` | 擇時候選排序框架 |
| `qimen_external_source_registry_v0.2.json` | 外部來源、授權、提交碼與源流 |
| `qimen_calendar_snapshot_schema_v0.1.json` | 標準化曆法快照 |
| `qimen_plate_differential_harness_spec_v0.1.md` | 分層差分規格 |
| `qimen_interpretation_evidence_contract_v0.1.json` | 解盤規則證據契約 |
| `qimen_classical_source_map_v0.1.md` | 公版古籍來源導航 |
| `tools/validate_qimen_import_package.py` | 候選包結構驗證器 |

## 4. 使用方式

### 驗證整個候選包

```bash
python3 tools/validate_qimen_import_package.py
```

### 測試差分工具

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

### 比較兩個以上引擎輸出

```bash
python3 tools/qimen_diff_harness.py engine_a.json engine_b.json --output diff_report.json
```

其中：

- `engine_a.json`、`engine_b.json` 是不同引擎的標準化輸出；
- `diff_report.json` 是差分報告；
- 檔名可保留英文，內容用途如上。

## 5. 明確不搬回

- 外部無來源的用神、格局與固定斷語；
- 「六害最少就是最佳時間」；
- 生日局處理所有事件；
- 指定物件必然改變現實；
- 固定三個月起效；
- 同源資料當獨立證據；
- 程式能跑等於術式有效；
- 未經授權直接複製 GPL-3.0（GNU 通用公共授權第三版）或 MPL-2.0（Mozilla 公共授權第二版）程式碼；
- 高干預運籌直接用於真人案例。

## 6. 目前能力邊界

目前已能：

- 把六十一串主鏈變成可檢查設定；
- 強制各引擎聲明方法；
- 接收標準化排盤結果；
- 自動找第一差異；
- 防止暗干、晚子時、寄宮等口徑被偷偷混用。

目前仍不能：

- 只輸入日期便由內部六十一串算法自動排出完整盤；
- 自動裁決哪個外部引擎一定正確；
- 自動把外部解盤或運籌內容升為正式規則。

下一階段是把內部置閏轉盤排盤核心程式化，先完成曆法、定局、地盤、符使，再逐層補天盤、星門神、暗干與異常。
