# MingLi-Bench 來源與授權審計｜v1.0

## 來源鎖定

- repository（倉庫）：`DestinyLinker/MingLi-Bench`
- commit（提交版本）：`b7433280fd86d7a7c27debbc47d0303c218f0bfd`
- question file（題目檔）：`data/data.json`
- question blob SHA：`6543b077fe4b76ab0a9f4d8e32959b4144ae6fa0`
- astro file（預排盤檔）：`data/fortune_api_results.json`
- astro blob SHA：`bf128852622cd0b4775c53bb256a63b959bcbce9`

## 授權

倉庫包含完整 MIT License（MIT 授權）檔，版權標示為 2026 MingLi-Bench Contributors。重用時需保留授權與版權聲明。

## 上游宣告

README 宣告：
- 2022–2025；
- 160 題；
- `data.json` 為正規化題目；
- `fortune_api_results.json` 為依 `case_id` 連接的預先八字／紫微盤。

## 固定十題解析

- 題目：10
- 案例：2
- 每題四選一：10/10
- `has_answer=true`：10/10
- 答案 A/B/C/D：10/10
- 題號重複：0
- 類別：健康、婚姻、家庭、學業、子女、外貌

## 預排盤連接核對

### case_1
- 題目出生資料與預排盤出生資料：MATCH
- 八字：甲寅 戊辰 己亥 壬申
- 時辰：申時
- 狀態：WARN；地點只有 `usa`，過於粗略，且未明示時區。

### case_2
- 題目出生資料與預排盤出生資料：MATCH
- 八字：辛酉 癸巳 甲辰 乙丑
- 時辰：丑時
- 狀態：WARN；地點為香港，但未明示 IANA 時區與換日規則。

本輪只確認「題目出生欄位與預排盤紀錄連接一致」，沒有用獨立排盤器重新證明 iztro 計算正確。

## Gate（閘門）

- 地點只有國家／大區：WARN
- 預排盤與出生欄位不一致：BLOCK
- 執行模型接觸答案：BLOCK
- 資料集答案：僅為 `dataset_ground_truth`
