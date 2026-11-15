# ECON 847 PS3 — Bathroom tissue: Python logit, version 1

这是可复现的第一版清洗与需求估计，不是最终识别结果，也尚未进行 merger simulation。
代码不限制价格系数符号，不按照估计符号挑选样本。

## 快速运行

在解压后的 `ps3_v1` 文件夹中：

```bash
python -m pip install -r requirements.txt
python src/check_estimator.py
python src/run_logit.py --estimate-only
```

最后一行直接使用本包附带的清洗表，重新生成估计结果；不需要原始数据，也不需要 SAS / Stata。

从原始数据开始完整复现：

```bash
python src/run_logit.py --data-dir "/Users/wenhanli/Desktop/847/PS 3/Data/Dominick"
```

其他电脑修改 `--data-dir` 即可。需要原始 `wtti.csv`、`ccount.dta`、`demo.dta`。
官方 `upctti.csv` 已放在 `inputs/`。旧版 `UPCTTI.SD2` 不用于计算。
Stata 文件通过 `pandas.read_stata` 直接读取，不需要安装 Stata。

## 主要输出

| 文件 | 内容 |
|---|---|
| `results/summary_zh.md` | 本轮结果与局限的中文说明 |
| `results/estimates.csv` | 每个模型的系数、标准误、弹性、样本和 first-stage 诊断 |
| `results/coefficients_and_first_stages.csv` | 价格、促销及第一阶段的完整系数表 |
| `results/clean_upc_store_week.csv.gz` | 主要清洗表；gzip 压缩 CSV，pandas 可直接读取 |
| `results/clean_brand_pack_variant_store_week.csv.gz` | 产品聚合的敏感性检查表 |
| `results/reported_zero_sales_records.csv.gz` | 原始零销量记录另行保留，不加 epsilon、不填价格 |
| `results/cleaning_audit.csv` | 各步筛选记录数 |
| `results/upc_catalog.csv` | 商品描述、包装规格、品牌初步分类和非卷纸排除标记 |
| `results/weekly_traffic.csv` | 通过日期核对且有七个有效购物日的 store-week 客流 |
| `results/flagged_price_records.csv` | 超出预设宽价格区间的原始记录 |
| `results/flagged_invalid_share_markets.csv` | 包装销量不少于客流等导致 outside share 无效的市场 |
| `results/zero_sales_by_upc.csv` | 清洗后正价记录数及客流匹配前的原始零销量记录数；二者口径不同 |
| `results/demographics.csv` | 从 Stata 转出的门店人口特征；本轮未用于估计 |
| `inputs/source_manifest.json` | 原始输入大小和 SHA-256，用于确认版本 |
| `results/run.log` | 完整清洗和估计日志 |

## 当前估计方程

市场为 store-week；主要产品定义为 UPC；数量是包装数，价格为美元/包装。

\[
\log s_{jst}-\log s_{0st}=\mu_{js}+\tau_t+\beta_p p_{jst}+\gamma Deal_{jst}+\xi_{jst}.
\]

`beta_price` 直接乘价格，因此合理的向下倾斜需求对应 **beta_price < 0**。
若用课堂的 `-alpha * price` 记法，则 alpha = -beta_price > 0。

- `mu_js` 是 store × UPC 固定效应，同时控制商品长期质量和门店长期偏好。
- `tau_t` 是具体周的固定效应，不只是 week-of-year。
- 额外规格用 store × week 固定效应取代 week 固定效应，吸收门店每周共同需求变化。
- 价格是 `PRICE / QTY`；QTY 表示促销捆绑件数，不是包装内卷数。
- `market_size` 是七个有效日期的 CUSTCOUN 合计；份额是包装销量 / 客流。
- outside quantity 为客流减去纳入模型的有效卷纸包装销量。它包含不买这些商品的购物机会，不能解释成所有未在 Dominick's 买纸的居民。
- `DEAL` 表示有非空官方促销代码，不等同于完整观测到的促销状态。
- 自价格弹性为 `beta_price * price_pack * (1 - share)`。

OLS 和两组候选 IV 都报告。AAC 为 `price_pack * (1 - PROFIT/100)`。
负的零售毛利可能是真实的促销亏损，不自动删除；AAC 必须为有限正数。
第二组候选 IV 是同 UPC 同周其他至少五家门店的简单平均价格。
所有 IV 都是有待论证排除限制的候选，不能把第一阶段强等同于有效。

标准误按 store 和 week 双向聚类（Cameron–Gelbach–Miller 包含减去交叉项），
第一阶段报告相同聚类方式下的 Wald chi-square 和 partial R²。
`first_stage_wald_per_iv` 是 Wald/q；它不是 KP 统计量，也不能套用 Stock–Yogo 临界值。
固定效应用 alternating projections 吸收；双向 FE 的秩由二部图连通分量计算。

## 清洗规则与尚未解决的问题

1. UPC 和 movement 一对多匹配，检查唯一键和匹配覆盖率。
2. 剔除湿巾、48-count 擦拭产品、175-count 盒装纸等非卷纸。该分类是对描述和规格的初步判读，目录供人工复核。
3. 保留 OK=1、QTY>0、MOVE>=0、有效周号；不填补不存在的 product-market 记录。
4. 原始零价格/零销量行单独保存。当前原始数据的零销量记录没有可用的正价格，因此反演回归只能用正销量记录。
   **这是明确的结果选择问题，不是证明商品不可得。不能说零销量偏误已解决。**
5. 宽价格筛选预先设为 $0.10–$60 / pack；另报告 $0.25–$20 的敏感性结果，未按系数符号调整边界。
6. 日期按 YYMMDD 解析，用官方周起点 1989-09-14（week 1）独立核对 week。
   客流要求来自样本门店、日期周号一致、正整数计数；无重复 store-date。
7. 只保留有七个有效客流日期的 store-week。这是保守的覆盖筛选，可能剔除关店日/节假日周；不是声称这些周必然错误。
8. 计算总包装数后，移除 outside share 不在 (0,1) 的市场；不把份额截断成合法值。
9. 同 store-week 中部分 OK=0/无效 UPC 记录未恢复。这些缺失销量不能被当作确切的不购买；第一版 outside share 仍是基于可用有效记录的近似。
10. 旧 UPC 的最新规格/描述可能不完全对应所有历史年份。UPC FE 可吸收长期差异，不能纠正包装变更或编码错误。

当前品牌聚合敏感性定义为 brand × 包装卷数 × 描述中的 roll variant，合并不同颜色等 UPC。
这不是 SSS 的七品牌定义，品牌和 variant 分类尚需人工复核。
聚合价格使用全样本固定 UPC 销量权重，对当期有价格的 UPC 重新归一化；这样避免直接使用当期销量权重，
但仍受 UPC 构成变化影响，而且权重来自本样本，并非外生/预定的工具变量。
该规格仅作敏感性检查，不作为已验证的主模型。

此外，简单静态 logit 忽略囤货、一次多包装购买和选店；市场规模近似也不能凭份额小于 1 获得验证。
候选 AAC 工具包含零售价且可能反映促销和库存，其他店价格可能共享品牌需求冲击和连锁促销。
固定效应不能自动解决这些内生性问题。

## 文献使用范围

- Gandhi, Lu & Shi (2012), *Demand Estimation for Differentiated Products: The Many Markets Case*, early working paper, section 5.
  直接使用 bathroom tissue、UPC-store-week、Customer Count 和简单 logit；也用毛利推算采购成本作为 IV。
  **这是早期版本**。2023 年正式论文已改为 tuna 实证，不能把其 toilet-tissue 设定说成正式版结果。
  https://www.princeton.edu/~erp/erp%20seminar%20pdfs/Spring%20PDF%202012/shi.pdf
- Gandhi, Lu & Shi (2023), *Estimating demand for differentiated products with zeroes in market share data*, Quantitative Economics.
  主要借鉴零销量选择问题的诊断，不在本轮复现其 moment-inequality 估计器。
  https://doi.org/10.3982/QE1593
- Romeo (2005), *Estimating Discrete Joint Probability Distributions for Demographic Characteristics at the Store Level Given Store Level Marginal Distributions and a City-Wide Joint Distribution*, QME 3, 71–93.
  用 Dominick's bathroom tissue、UPC-store-week 及 mixed logit，并明确保留 outside good；更适合后续异质性阶段。
  https://citeseerx.ist.psu.edu/document?doi=e25ee5663e3b02d3f98b1498fc7cdeaa63317da7&repid=rep1&type=pdf
- Hausman & Leonard (2002), *The Competitive Effects of a New Product Introduction: A Case Study*, JIE 50, 237–263.
  bathroom tissue 的竞争和福利分析；使用 Nielsen 数据，不是 Dominick's。
  提供零售商固定加价假设下将制造商 FOC 与零售数据连接的讨论。
  https://doi.org/10.1111/1467-6451.00176
  Public earlier version: https://users.nber.org/~confer/2000/si2000/hausman.pdf
- Shi, Shum & Song (2018), Econometrica，section 6.2：品牌聚合和 store-week 的参考，
  不直接照搬 cyclic-monotonicity 方法来做 merger。

Data source and acknowledgement: Kilts Center for Marketing at the University of Chicago Booth School of Business.
https://www.chicagobooth.edu/research/kilts/research-data/dominicks

## 已做验证

- 清洗中的键唯一性、UPC 匹配、日期、正 outside share 等检查。
- 自编 absorbed OLS/2SLS 与显式 dummy 回归的系数逐项比较。
- OLS 的双向聚类标准误与 statsmodels 的独立实现比较。
- 第一阶段、产品聚合、时间样本、促销控制、固定效应和价格筛选的敏感性结果。

没有运行合并模拟：负价格系数只是必要的初步检查，不能替代识别与供给侧合理性检查。
