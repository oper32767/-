# ASTRO_ON × ASTRO_OFF 差異報告｜封存前結構版

## 已完成差異

| 項目 | ASTRO_OFF | ASTRO_ON |
|---|---|---|
| 題目 | 同一固定十題 | 同一固定十題 |
| 選項順序 | 相同 | 相同 |
| 答案 | 不含 | 不含 |
| 出生資料 | 有 | 有 |
| 預排盤 | 無 | 有固定版本摘要與完整盤引用 |
| 主要測量 | 排盤＋解讀的合成能力 | 在指定盤面下的解讀能力 |
| 主要錯誤碼 | CHART_ERROR／INTERPRETATION_ERROR | INTERPRETATION_ERROR／PRECOMPUTED_CHART_MISMATCH_BLOCK |

## 可比較指標

- `accuracy_astro_on`
- `accuracy_astro_off`
- `delta = accuracy_astro_on - accuracy_astro_off`
- `chart_error_count`
- `interpretation_error_count`
- WARN／BLOCK 題數

## 本輪沒有填入成績的原因

包製作者已看過答案鍵，無法再充當乾淨執行模型。為防止答案污染，實際成績欄固定為 `NOT_RUN_CONTAMINATED_BUILDER`。

這不是漏做：封存包、差異契約與錯誤碼均已完成。真正模型執行必須由未接觸答案的新執行環境產生新的 run 記錄，不得修改本封存包。
