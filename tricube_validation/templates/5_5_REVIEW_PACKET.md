# 5.5 總司獨立驗收包

## 1. 批次識別

- batch_id:
- domain:
- source_id:
- branch_or_commit:
- executor: GPT-5.6
- rule_set_version:
- prompt_sha256:
- booklet_sha256:
- answer_key_sha256:

## 2. 執行前 Gate

- [ ] 題本與答案鍵已分離
- [ ] 執行席未讀答案鍵
- [ ] 來源授權與檔案 hash 已記錄
- [ ] 題目可客觀評分
- [ ] WARN 題不計正式準度
- [ ] 未封板規則不得進主判

## 3. 結果摘要

- 有效題數:
- PASS:
- WARN:
- BLOCK:
- 機械正確率:
- 棄答／停機率:
- 排盤錯誤數:
- 規則違反數:

## 4. 5.6 自報失敗類型

| failure_code | 件數 | 代表案例 | 是否需回補規則 |
|---|---:|---|---|
| | | | |

## 5. 總司必查

1. 是否存在答案或選項位置污染？
2. 是否把模糊描述算成命中？
3. Dataset ground truth 是否有內部矛盾？
4. 有無跳過 rule_id、旺衰／調候、命身／三方四正等封板主鏈？
5. 有無資料不足卻未停機？
6. 結果是否可由另一模型重跑？
7. 哪些題必須送雲龍終裁或 Claude 冷審？

## 6. 5.5 裁決

- review_result: PASS / WARN / BLOCK
- 可計入正式樣本數:
- 排除案例:
- 必修問題:
- 是否准下一批:
- 是否需 Claude:

## 7. 雲龍終裁

- final_result:
- 封板內容:
- 不採用內容:
- 下一批範圍:
