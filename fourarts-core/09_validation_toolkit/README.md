# Validation Toolkit｜驗證工具包 v1.0

## 定位

本目錄提供四模組驗證工程所需的最小正式模板。只處理工程結構、來源、狀態、審查與未知項，不進行術數主判，也不宣稱準度。

## 檔案

- `case_schema.json`：案例資料的 JSON Schema（JSON 結構規格）。
- `gate_schema.json`：Gate（閘門）資料的 JSON Schema（JSON 結構規格）。
- `validation_matrix.csv`：靜態／動態案例共用矩陣模板。
- `unknown_list.csv`：未知與缺口清單。
- `run_log.csv`：每次執行、結果、阻擋與審查紀錄。

## 狀態規則

- `PASS`：必要資料齊全，允許進入指定階段。
- `WARN`：可保留或試跑，但不得計入正式準度。
- `BLOCK`：禁止進入下一階段。
- 未知資料必須留在 `unknowns` 或 `unknown_list.csv`，不得自行補寫。

## 靜態與動態分離

- `STATIC（靜態）`：八字、紫微等固定命盤案例。
- `DYNAMIC（動態）`：六壬、奇門等依問題時間起課／起局案例。
- 每筆案例均須填 `case_layer`，不得混用。

## 最小操作流程

1. 依 `case_schema.json` 建立案例。
2. 將缺口登記到 `unknown_list.csv`。
3. 套用 `gate_schema.json` 定義的閘門。
4. 將案例寫入 `validation_matrix.csv`。
5. 每次執行寫入 `run_log.csv`。
6. 由指定審查者確認結果；AI（人工智慧）不得自行升格規則或批准案例。

## 驗收結論

本工具包已覆蓋 Issue #6 要求的六項交付物，並保留來源、審查者、狀態、結果與未知欄位。模板中的 `TEMPLATE-*`／`UNK-TEMPLATE-*`／`RUN-TEMPLATE-*` 只作欄位示範，正式使用前須替換或刪除。
