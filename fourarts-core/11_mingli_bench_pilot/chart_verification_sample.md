# 預排盤抽樣核對｜case_1 與 case_2

| case_id | 出生欄位連接 | API success | 八字 | 時辰 | 地點 Gate |
|---|---|---|---|---|---|
| case_1 | MATCH | true | 甲寅 戊辰 己亥 壬申 | 申時 | WARN：僅 usa |
| case_2 | MATCH | true | 辛酉 癸巳 甲辰 乙丑 | 丑時 | WARN：未明示時區 |

結論：抽樣兩案沒有發現 `PRECOMPUTED_CHART_MISMATCH_BLOCK`。  
限制：未用第二套曆法／排盤引擎獨立重算，因此不可把此表寫成排盤正確性封板。
