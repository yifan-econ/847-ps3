# PS3：外部成本 IV 与两种包装样本（v2）

运行日期：2026-11-14。代码和结果已实际运行；原始数据保持不变。

## 核心结论

所有包装 OLS 价格系数复现为 −1.293247；仅多卷装重新计算 outside share 并重新估计后，OLS 为 −1.229548 左右，非弹性约 2.95%。这不是沿用旧系数删除行的结果。
外部纸浆成本 IV 在这套固定效应和暴露代理下偏弱，不能确认为可靠的主 IV。仅多卷装纸浆 IV 出现正价格系数且标准误很大，这是弱识别警讯，不能解释成需求向上。纸浆与塑料联合 IV 也没有建立有效性。AAC 结果作为比较保留，不能仅凭其较强第一阶段认定排除限制成立。

## 目录与复现

项目根目录：`/Users/wenhanli/Desktop/847/PS 3/`。
- `Data/`：原有原始数据，未修改。
- `Paper/`：已有论文与从旧压缩包恢复的三份 PDF；没有将旧公开版冒充正式版。
- `Archive/ps3_v1/`：完整恢复第一版压缩包。
- `Archive/ps3_reference_update/`：完整恢复诊断与参考文献压缩包。
- `Analysis/cost_iv_v2/src/`：估计、诊断和报告代码。
- `Analysis/cost_iv_v2/data/raw/`：FRED 原始成本 CSV、下载来源和 SHA256。
- `Analysis/cost_iv_v2/data/processed/`：月度成本及两个版本的估计面板。
- `Analysis/cost_iv_v2/results/`：14 个规格、第一阶段、过度识别检验、样本审计、验证和日志。

在项目目录安装 requirements.txt 中的依赖后运行：

```sh
python Analysis/cost_iv_v2/src/run_analysis.py
python Analysis/cost_iv_v2/src/check_overidentification.py
python Analysis/cost_iv_v2/src/write_report.py
```

本轮使用已恢复的 v1 清洗面板作为输入，并重新构造多卷装份额、成本 IV 和所有回归；没有声称重新从原始 movement 重做全部清洗。v1 原始清洗代码、UPC 表和原始零记录输出均在 Archive 中。

## 零销量处理

412,611 条原始零销量记录的价格都为零（旧诊断结果）。这些记录保留在原始数据及 `Archive/ps3_v1/results/reported_zero_sales_records.csv.gz`，不参与当前正份额 logit 反演。不填价格、不加 epsilon，也不因该条件自动认定商品不可得。
本轮回归样本等价于沿用 v1 正价格正销量的筛选；这是一种有选择限制的初步估计，并不是解决零销量选择偏误的方法。构建真实 choice set、BLP 商品数 IV 和合并预测时，仍需要单独研究可售状态。

## 成本数据与工具构造

来源：美国 BLS，经 FRED 下载，月度、未季调。下载范围请求 1988–1998 年，实际序列范围和非缺失月数见 manifest.json。
- 木浆 PPI：WPU0911，https://fred.stlouisfed.org/series/WPU0911
- 塑料薄膜、片材及其他形状 PPI：WPU072205，https://fred.stlouisfed.org/series/WPU072205
周按该周起始日所在月份匹配月度指数，不进行周度线性插值。两者都是名义指数；价格也保持名义美元/包装。指数除以 100 仅改变 IV 尺度。
全国共同成本序列本身被 week FE 吸收，因此使用：
`z_pulp_rolls = (木浆PPI/100) × pack_count`
`z_plastic_surface = (塑料PPI/100) × pack_count^(2/3)`
木浆暴露的卷数代理忽略每卷纸张数量、尺寸、层数和再生纸占比。塑料暴露以相似几何形状下表面积随体积的 2/3 次方变化作为粗略代理；它不是观测到的包装重量，只作探索性规格，不能称为已经验证的投入系数。没有根据估计符号调节该指数。
塑料序列在 1989 年至 1991 年上半年缺失；本轮共同样本从 1991 年 7 月开始，不补齐缺失。为了区分换样本与换 IV，报告同样本 OLS 和纸浆单 IV。
Villas-Boas (2007) §5.2、Table 3 是投入价格与产品差异交互的文献先例，但不直接证明我们的两个暴露代理有效。文献：https://academic.oup.com/restud/article-abstract/74/2/625/1576967

## 模型、样本与推断

模型：`log(s_jst)-log(s_0st) = store×UPC FE + week FE + beta*price_pack + gamma*deal + error`。无价格符号约束。
两个样本都保留原始购物客流作为 market size。多卷装样本剔除所有单卷 UPC，其购买计入 outside option；重新计算 inside quantity、outside share 和因变量，未将多卷装份额重新归一化为 1。
OLS 不解决价格内生性。AAC=price_pack×(1-profit/100) 为候选成本代理，作为比较。
标准误按门店和月份双向聚类，适应月度成本共同变化。这使标准误不同于旧版的门店和周聚类，OLS 点估计应相同。双向聚类仍不能解决跨月份的任意共同序列相关，推断应保守解读。
包装组线性趋势敏感性规格，控制各包装组随时间线性变化的需求差异；保留门店×UPC 与周固定效应。

## 全部估计结果

第一阶段 Wald/q 是双向聚类排除工具 Wald 统计量除以工具数量，不是 KP、Stock–Yogo 或有效 F；不能简单用大于 10 宣布不存在弱工具。

| 规格 | N | 价格系数 | 聚类SE | 中位自价格弹性 | 非弹性% | 向上倾斜% | Wald/q | partial R² |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all_packs__OLS | 946,237 | -1.2932 | 0.0789 | -1.747 | 21.10 | 0.00 | — | — |
| all_packs__AAC_IV | 946,237 | -1.1636 | 0.1918 | -1.572 | 21.91 | 0.00 | 23.975 | 0.06573 |
| all_packs__PULP_IV | 946,237 | -0.5228 | 0.4582 | -0.706 | 58.85 | 0.00 | 4.474 | 0.00346 |
| all_packs__OLS_joint_sample | 748,035 | -1.1910 | 0.0873 | -1.604 | 19.93 | 0.00 | — | — |
| all_packs__PULP_IV_joint_sample | 748,035 | -1.1241 | 1.5092 | -1.514 | 22.11 | 0.00 | 0.939 | 0.00064 |
| all_packs__PULP_PLASTIC_IV | 748,035 | -0.7343 | 0.4116 | -0.989 | 50.60 | 0.00 | 3.034 | 0.00667 |
| all_packs__PULP_IV_pack_trends | 946,237 | -0.8908 | 0.6051 | -1.204 | 34.66 | 0.00 | 3.395 | 0.00293 |
| multi_packs__OLS | 764,960 | -1.2295 | 0.0860 | -2.372 | 2.95 | 0.00 | — | — |
| multi_packs__AAC_IV | 764,960 | -1.4086 | 0.2632 | -2.717 | 1.56 | 0.00 | 18.562 | 0.04635 |
| multi_packs__PULP_IV | 764,960 | 6.0298 | 19.4780 | 11.630 | 0.00 | 100.00 | 0.106 | 0.00005 |
| multi_packs__OLS_joint_sample | 614,278 | -1.0990 | 0.0872 | -2.184 | 5.42 | 0.00 | — | — |
| multi_packs__PULP_IV_joint_sample | 614,278 | -9.5421 | 67.3698 | -18.962 | 0.00 | 0.00 | 0.019 | 0.00001 |
| multi_packs__PULP_PLASTIC_IV | 614,278 | -0.5585 | 0.2738 | -1.110 | 44.76 | 0.00 | 13.041 | 0.01752 |
| multi_packs__PULP_IV_pack_trends | 764,960 | -4.4988 | 13.9721 | -8.677 | 0.00 | 0.00 | 0.095 | 0.00005 |

非弹性按 |elasticity|<1 统计；正价格系数即使非弹性比例为 0%，也不是合格模型，必须结合向上倾斜比例判断。

## IV 诊断如何解释

每个 IV 规格报告第一阶段 partial R²、聚类 Wald 检验和对 beta_price=0 的 Anderson–Rubin 排除工具检验。AR 的 p 值是指定零假设的检验，不是 IV 有效性检验，也不是完整的弱工具稳健置信区间。

两个成本 IV 的联合规格还执行 nuisance-estimation-orthogonal overidentifying moment Wald 检验（门店×月份双向聚类）：
- all_packs: chi²(1)=0.0890, p=0.7654。
- multi_packs: chi²(1)=0.9895, p=0.3199。

未拒绝过度识别限制不能证明 IV 有效：两个 IV 可同时违反排除限制，弱识别还会降低检验能力。由于这些是产品规模×共同时间成本，若包装组需求趋势、促销或产品调整与成本同步变化，仍可能违背排除限制。包装组趋势敏感性也没有使纸浆 IV 可靠。

## 当前建议与下一步

保留所有包装和仅多卷装两个版本。当前不将外部纸浆或纸浆+塑料规格当成最终主估计，不据此进入合并模拟。OLS 与 AAC-IV 可作为清楚标注局限的比较结果；AAC 的第一阶段较强不等于外生。
优先补充更可信的纸张总量/重量、再生纸及制造商生产地暴露，或核对 AAC 采购成本的行业机制。若仍只有卷数，必须承认外部 IV 识别有限，不能靠删规格或强制负系数解决。

## 核验

检查通过：产品市场键唯一；价格和销量为正；每市场 inside shares + outside share = 1；多卷装样本不含单卷商品；所有包装 OLS 点估计与 v1 一致（差异 <1e-7）；14 个规格正常收敛；回归协方差对角线无负值；原始数据未改写。
详细文件：validation.json、sample_audit.csv、coefficients_first_stages.csv、overidentification.csv、run.log。
