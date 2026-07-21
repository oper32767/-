# 奇門多引擎差分使用說明 v0.1

## 0. 目的

本文件只說明如何比較不同排盤引擎，不把任何外部引擎設為真相源，也不把六十一串主鏈改寫成程式規則。

差分流程用來回答：

1. 兩個結果最早從哪一層開始不同；
2. 差異是時間、曆法、定局、寄宮、暗干或下游盤面造成；
3. 哪一個欄位需要回到六十一串或原典人工裁決。

## 1. 方法登記

`qimen_method_adapter_registry_v0.1.json` 記錄外部引擎採用的：

- 排盤層級與盤式；
- 置閏、拆補、茅山或其他定局法；
- 晚子時與換日政策；
- 節氣來源與精度；
- 天禽寄宮；
- 暗干、空亡與馬星算法。

必要口徑未聲明時，只能標記缺口，不能直接把不同結果判成程式錯誤。

## 2. 統一輸出

`qimen_engine_output_schema_v0.1.json` 要求引擎輸出相同欄位，包括：

- 時間與方法政策；
- 節氣、四柱與旬首；
- 陰陽遁、局數與三元；
- 地盤、值符與值使；
- 天盤、九星、八門與八神；
- 暗干、空亡、馬星與異常。

## 3. 第一分歧工具

`tools/qimen_diff_harness.py` 依固定順序逐欄比較，輸出：

- `PASS`（通過）：目前比較欄位一致；
- `DIVERGED`（已分歧）：找到第一個分歧與全部差異；
- `FAIL`（失敗）：輸入缺漏或案例不相容。

工具不裁決哪個引擎正確。

## 4. 固定案例

`qimen_differential_case_set_v0.1.json` 保存回放與邊界案例。每次修改轉接器或差分工具後，應重跑同一批案例，確認沒有產生非預期變化。

## 5. 驗證指令

```bash
cd fourarts-core/08_qimen_operation_import
python3 tools/validate_qimen_import_package.py
python3 -m unittest discover -s tests -p "test_*.py" -v
```

比較引擎輸出：

```bash
python3 tools/qimen_diff_harness.py engine_a.json engine_b.json --output diff_report.json
```

## 6. 邊界

- 差分一致不代表術數正確；多個引擎可能同源。
- 差分不一致不代表某一方有程式錯誤；可能只是方法口徑不同。
- 任何正式裁決仍需回到六十一串、原典、案例及人工審核。
