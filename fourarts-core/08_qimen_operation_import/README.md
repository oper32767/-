# 奇門差分測試與來源治理底盤 v0.1

> 狀態：`ENGINEERING_BASELINE`（工程底盤）  
> 日期：2026-07-22

## 定位

本目錄只提供：

- 標準化曆法輸入與多引擎輸出格式；
- 外部排盤引擎的方法、版本、授權與源流登記；
- 分層差分工具與單元測試；
- 解盤規則的證據欄位契約；
- 公版古籍來源導航。

本底盤不修改《四術算法依據庫 v1.0》，不新增正式 `rule_id`（規則編號），也不裁決哪一套奇門算法正確。

## 已合併範圍

- `qimen_calendar_snapshot_schema_v0.1.json`：曆法與時間政策輸入格式。
- `qimen_engine_output_schema_v0.1.json`：不同引擎的統一輸出格式。
- `qimen_method_adapter_registry_v0.1.json`：外部引擎方法與缺口登記。
- `qimen_differential_case_set_v0.1.json`：固定回放及邊界案例。
- `tools/qimen_diff_harness.py`：找出第一個分歧與全部差異。
- `tests/test_qimen_diff_harness.py`：檢查差分工具本身。
- `tools/validate_qimen_import_package.py`：檢查來源、結構與方法聲明。
- `qimen_interpretation_evidence_contract_v0.1.json`：解盤規則證據契約。
- `qimen_external_source_registry_v0.2.json`：來源、提交碼、授權與同源關係。
- `qimen_classical_source_map_v0.1.md`：公版古籍來源導航。

## 未合併範圍

以下仍留在候選 PR（合併請求）#15，不進主分支：

- 六十一串內部主鏈機器設定；
- 時區未鎖定的外部基準盤；
- 運籌輸入輸出契約；
- 運籌外部候選地圖；
- 運籌 Gate（閘門）候選；
- 擇時評分候選。

## 使用方式

```bash
cd fourarts-core/08_qimen_operation_import
python3 tools/validate_qimen_import_package.py
python3 -m unittest discover -s tests -p "test_*.py" -v
```

比較兩個以上已標準化的引擎輸出：

```bash
python3 tools/qimen_diff_harness.py engine_a.json engine_b.json --output diff_report.json
```

`engine_a.json`、`engine_b.json` 為引擎輸出檔；`diff_report.json` 為差分報告。

## 邊界

自動檢查通過只代表檔案與程式結構正常，不代表術數規則已被證明，也不代表外部引擎可以覆蓋六十一串主線。
