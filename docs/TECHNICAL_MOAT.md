# 技術資產與護城河審查 — 2026-10-07

## 結論與證據等級
目前有可重用的工程資產，但尚未證明有競爭護城河。不得宣稱比其他 Agent 更強、獨有、可專利或難以複製。
本文件是架構審查與可否證的建造策略，不是已完成的比較實驗或智慧財產權意見。
12 項軟體測試與單筆欄位對照，證明部分程式行為；不證明科學預測能力、商業價值或比較優勢。

## 現有資產盤點
| 資產 | 已實作 | 資產價值 | 現階段防禦性 |
|---|---|---|---|
| 公開快照下載、checksum、來源 manifest | 是 | 可重現 ingestion | 通用且容易重做；公開資料非獨占資產 |
| retrieved / derived / inferred / unknown 欄位隔離 | 是 | 科學證據介面與錯誤防線 | 基本可靠性要求，不應當作獨有創新 |
| 原始記錄、ID、版本與單筆 reference 對照 | 是 | 可追溯回歸驗證 | 測試範圍小，未形成領域案例庫 |
| formation-energy 排序基線 | 是 | 比較起點 | 弱基線，未證明 stability discrimination |
| 半導體 early-warning、calibration、SPC/ML 比較 | 否 | 潛在領域技術資產 | 尚無證據 |
| 獨立 hull、文獻交叉驗證、實驗選擇與回饋學習 | 否 | 潛在驗證/決策資產 | 尚無證據 |

## 建議的競爭切口：領域約束下的科學決策品質
不是「Agent 比較多」，而是「固定資料、錯誤率與預算下，做出更可靠、更值得驗證的領域決策」。這是策略假說，必須用測量支持。
Merck 2027 是使用者目標，不代表已確認競賽規則或需求。材料案例先建立證據方法；半導體 QA 是既定 observation 主線，不另開題目。

可累積的四種資產：
1. 領域問題與評測資產：已審核標籤、困難案例、反例、資料分割與版本。Synthetic 能控制機制，但不能替代真實外部驗證；公開 benchmark 本身也不構成資料獨占。
2. 驗證資產：能量 reference/單位/來源相容性檢查、可重現獨立計算與錯誤診斷；避免只驗證轉錄正確。
3. 決策資產：可測試的 abstention、risk calibration、成本約束排序與人工批准規則。未校準的 score 不得標成 probability。
4. 經審核的回饋資產：成功與失敗案例、規則版本、修正理由、跨版本回歸。記錄 feedback 不等於已完成 active learning；只有用 feedback 改進後通過獨立留出集，才有改善證據。

核心模組必須在移除 LLM 後仍能執行與測試；更換模型不應遺失案例庫、驗證器或評估歷史。LLM 是提案/工具呼叫介面，不是科學真值來源。

## 目標架構（未全面實作）
Domain observation / candidate → evidence contract → compatible-domain verifier → calibrated decision policy → frozen evaluator → human-reviewed feedback.
Agent adapters 僅連接這些核心，不能繞過 evidence contract 或改寫 evaluator。
目前只具備部分 evidence contract、CSV ingestion 與 mapping regression；沒有完整 verifier、calibrated policy 或閉環。
下一階段先集中材料 evidence integrity，而非同時擴張所有模組。

## 分兩階段證明，不混淆指標
### 第一階段：證據可靠性
下一個最小建造項目是版本化、離線可跑的 evidence-integrity challenge set。
包含正常記錄、缺值、錯誤單位、不同 reference hull、來源衝突、不存在 ID，以及把推論冒充原值的案例。標籤由明確規則與人工審核支持；fixture 的人工擾動必須標 synthetic，不能冒充真實資料衝突。
每案有 source/hash、輸入、禁止洩漏的答案、預期接受/拒答行為、案例理由與錯誤成本。
以純規則 mapper 作起點；之後比較 plain LLM、相同工具的 LLM 和我們的 verifier-assisted workflow。尚未跑過任何 LLM head-to-head。
報告 supported-claim rate、unsupported numerical claims、錯誤拒絕率、正常案例 coverage、可重放率與執行成本。只拒答全部問題不算成功。
停止條件：freeze 前訂好必要安全案例與正常案例 coverage 標準；不得見結果才調標準。這一階段只能支持「測試集上的可靠性差異」。

### 第二階段：科學決策效益
Materials：混合類別且能量相容的 group/temporal holdout；同一結構/化學族洩漏檢查；budgeted precision@k、recall、calibration、每次有效候選的驗證成本。
Semiconductor：固定 seed、A/B/C scenarios；固定 false alarms/100 lots 下的 lead time、event recall、precision 與 calibration；SPC 閾值只用 training/validation 決定。
公平比較固定可用資料、工具、基底模型、計算/呼叫預算與重試政策，記錄 latency/cost，重複多 seed；對相關資料採 composition/group 或 episode 等適當單位估計區間，不能把相鄰 lots 當獨立樣本。
執行無 verifier、無 uncertainty policy、無 feedback 的 ablations。若移除核心也一樣好，不應宣稱它是優勢來源。
在預先定義的主要指標、留出測試與不惡化的安全指標上出現可重現改善，才能宣稱相對指定 baseline 的技術優勢。不能推廣成「勝過所有 Agent」。

## 累積與保護
所有結論連到資料版本、方法版本、命令與結果；保留負結果。公開來源、工具 wrapper、prompt 與架構名稱不當作獨占資產。
未來合作資料只能在取得使用/衍生/公開授權後納入；GNoME 資料的 CC BY-NC 條件不得假設商用或競賽已清除。專利或保密策略需另行專業審查，本次不作判斷。
開源有助可驗證性但也降低複製門檻；可持續差異更可能來自領域案例品質、外部驗證、長期維護與合法取得的合作回饋。這是合理策略推論，不是保證。

## 審查來源
本地實作：skills/materials_discovery/{retrieve,evaluate,provenance}.py、tests/、experiments/retrospective_validation/MATERIALS_V01.md。
競品能力以 [一手資料盤點](AGENT_LANDSCAPE.md) 為準，不用宣傳頁面推算對方在我們 benchmark 上的分數。
Materials Project 將 Matbench Discovery 描述為材料發現 ML 模型的評測框架：[官方文件](https://docs.materialsproject.org/services/ml-and-ai-applications/matbench-discovery)。
其論文指出 formation energy 與 thermodynamic stability、以及 retrospective/prospective 評估之間的差異；這支持任務導向評估，不證明我們的方法有效：[原論文](https://arxiv.org/abs/2308.14920)。

## 下一步的決策
先建立 evidence-integrity challenge set 與凍結評估協議，不增加 orchestration 框架或新頂層專案。
本次只完成資產/競爭審查與建造門檻文件，未實作上述新 benchmark 或宣稱護城河已成立。
