# 5.5 冷審包｜MingLi-Bench 雙軌十題

## 必查

1. ASTRO_ON／ASTRO_OFF 是否使用完全相同題目與選項。
2. 兩份盲測題本是否均不含實際答案值。
3. ASTRO_ON 的盤面引用是否鎖定 commit、path、blob SHA 與 case_id。
4. case_1 的 `usa` 粗地點是否維持 WARN。
5. `dataset_ground_truth` 是否與 `reality_truth` 分離。
6. `failure_codes.json` 是否能區分 CHART_ERROR 與 INTERPRETATION_ERROR。
7. 是否有 61 串私有內容或使用者私人命盤進入公開包。
8. manifest SHA-256 是否一致。

## 裁定欄

- PACKAGE_INTEGRITY：PASS／WARN／BLOCK
- INPUT_PARITY：PASS／BLOCK
- CHART_LINKAGE：PASS／WARN／BLOCK
- ANSWER_LEAKAGE：PASS／BLOCK
- ACCURACY_CLAIM_ALLOWED：固定為 BLOCK，直到乾淨執行完成
