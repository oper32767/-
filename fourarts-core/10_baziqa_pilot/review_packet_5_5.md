# 5.5 冷審包｜BaziQA 十題試跑

## 請審查

1. `blind_booklet.json` 是否完全不含實際答案值。
2. 題目是否固定取來源檔前兩位命主、前十題，而非依答案挑題。
3. `manifest.json` 的 SHA-256 是否與檔案或 canonical JSON（標準化 JSON）一致。
4. `source_license_audit.md` 是否正確保留 LICENSE 檔缺失警告。
5. 是否把資料集答案誤稱為現實真相。
6. 是否有任何 61 串私有內容進入本公開包。

## 建議裁定欄

- PACKAGE_INTEGRITY：PASS／WARN／BLOCK
- ANSWER_LEAKAGE：PASS／BLOCK
- LICENSE_PROVENANCE：PASS／WARN／BLOCK
- ACCURACY_CLAIM_ALLOWED：固定為 BLOCK，直到獨立乾淨執行完成
