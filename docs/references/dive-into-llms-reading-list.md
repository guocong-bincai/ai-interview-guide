# 《动手学大模型》课件与实验阅读索引

> 本页整理 [Lordog/dive-into-llms](https://github.com/Lordog/dive-into-llms) 中与本面试指南互补的 PDF、README 和 Notebook，方便按题目继续动手验证。

## 使用与版权说明

截至 2026-08-25，目标仓库根目录未见明确的开源许可证文件，README 也声明材料来自贡献者经验、互联网资料和科研积累。本仓库已按学习资料归档 11 份 PDF，并明确保留来源和权利说明；这些课件不应理解为适用本项目的 MIT 许可证。Notebook 和代码仍链接到原仓库，面试答案继续基于原论文、官方项目和独立表述编写。

使用这些材料时建议遵循：

1. README 和 PDF 用于建立实验背景；
2. Notebook 用于理解最小实现，不直接视为生产代码；
3. 结论、指标和方法回到论文或官方项目核验；
4. 依赖版本、模型许可、数据许可和硬件条件以实际复现环境为准；
5. 安全实验只在授权模型、隔离环境和受控数据上运行。

## 1. 微调与部署（已有覆盖，按需阅读）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter1)
- [本仓库 PDF](../../ai-books-online/01-finetuning-and-deployment.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter1/dive-into-llm.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter1/dive-tuning.ipynb)
- 对应主答案：[07 · 模型训练](../07-model-training/)

该实验以 Transformers 文本分类和 Gradio 部署为主，适合理解训练、验证、推理和 Demo 发布的最小链路。示例模型与依赖较早，不应直接当作当前生产选型。

## 2. Prompt 与思维链（已有覆盖，按需阅读）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter2)
- [本仓库 PDF](../../ai-books-online/02-prompting-and-cot.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter2/dive-into-prompting.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter2/dive-prompting.ipynb)
- 对应主答案：[02 · Prompt Engineering](../02-prompt-engineering/)

## 3. 知识编辑（高优先级）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter3)
- [本仓库 PDF](../../ai-books-online/03-knowledge-editing.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter3/dive_edit_0410.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter3/dive_edit.ipynb)
- 对应主答案：[07 · 模型训练 Q21-Q23](../07-model-training/#q21-什么是大模型知识编辑它和微调rag机器遗忘有什么区别)

建议复现重点：单条事实编辑、改写泛化、邻近事实局部性和编辑前后能力回归。不要只验证原始 Prompt 是否命中新答案。

## 4. 数学推理蒸馏（高优先级）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter4)
- [本仓库 PDF](../../ai-books-online/04-math-reasoning.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter4/math.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter4/sft_math.ipynb)
- 对应主答案：[07 · 模型训练 Q24](../07-model-training/#q24-如何把强推理模型的能力蒸馏到小模型为什么不能只收集长思维链做-sft)

建议复现重点：数据清洗、答案验证、语义去重、SFT、盲测，以及答案正确率与过程质量的分离评估。

## 5. 模型水印（高优先级）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter5)
- [本仓库 PDF](../../ai-books-online/05-text-watermark.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter5/watermark.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter5/watermark.ipynb)
- 对应主答案：[09 · 安全与评估 Q25-Q26](../09-ai-safety-evaluation/#q25-llm-文本水印如何嵌入和检测kgw-与语义水印有什么区别)

建议复现重点：KGW 嵌入与统计检测、不同长度文本、固定假阳性率下的召回，以及改写和翻译后的水印残留。

## 6. 越狱攻击与防御评测（高优先级）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter6)
- [本仓库 PDF](../../ai-books-online/06-jailbreak.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter6/dive-Jailbreak.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter6/dive-jailbreak.ipynb)
- 对应主答案：[09 · 安全与评估 Q27](../09-ai-safety-evaluation/#q27-如何把零散越狱样本变成可持续运行的自动化红队-harness)

建议复现重点：Selector、Mutator、Constraint、Evaluator 的编排与评估器校准。不要在无授权外部服务上运行攻击测试，也不要把攻击载荷提交到公开 Issue 或日志。

## 7. LLM 文本隐写（选修）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter7)
- [本仓库 PDF](../../ai-books-online/07-text-steganography.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter7/stega.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter7/llm_stega.ipynb)
- 对应主答案：[09 · 安全与评估 Q26](../09-ai-safety-evaluation/#q26-如何评估文本水印为什么能检测出来还不够)

该实验用 Huffman Coding 和 Fixed Length Coding 控制 token 选择以隐藏消息。面试重点是区分水印与隐写，以及容量、自然度、可恢复性和可检测性的取舍。

## 8. 多模态大模型（已有覆盖，按需阅读）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter8)
- [本仓库 PDF](../../ai-books-online/08-multimodal-llms.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter8/mllms.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter8/mllms.ipynb)
- 对应主答案：[11 · 多模态 AI](../11-multimodal-ai/)

## 9. GUI Agent 构建（高优先级）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter9)
- [本仓库 PDF](../../ai-books-online/09-gui-agent.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter9/GUIagent.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter9/GUIagent.ipynb)
- 对应主答案：[21 · 多模态 Agent Q16](../21-multimodal-agents/#q16-如何构建-gui-agent-的训练数据动作空间和评测闭环什么时候必须请求人工接管)

建议复现重点：截图、任务、历史动作与下一动作的数据对齐；坐标归一化；异常页面；以及低置信或高风险动作的人工接管。

## 10. Agent 安全评测（高优先级）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter10)
- [本仓库 PDF](../../ai-books-online/10-agent-safety.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter10/dive-into-safety.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter10/agent.ipynb)
- 对应主答案：[28 · Test Harness Q15](../28-test-harness-evaluation/#q15-agent-类应用会调工具的怎么评测最前沿答出来直接拉开差距)

建议复现重点：把任务完成与行为安全拆成两个标签，记录完整交互轨迹、风险类型、危险步骤和可阻断策略。

## 11. RLHF 实验（已有覆盖，按需阅读）

- [章节 README](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter11)
- [本仓库 PDF](../../ai-books-online/11-rlhf.pdf) · [上游原件](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter11/RLHF.pdf)
- [Notebook](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter11/RLHF.ipynb)
- 对应主答案：[07 · 模型训练 Q7-Q9](../07-model-training/#三对齐技术rlhf与dpo)

该实验用情感分类器作为奖励信号演示 PPO。复现时应额外观察 KL、奖励黑客、输出多样性和通用能力回归，不能只看奖励分数上升。

## 推荐学习顺序

1. 知识编辑：建立“可靠性、泛化、局部性、可移植性”的评测意识；
2. 文本水印：理解可检测性、质量、鲁棒性和安全性的多目标取舍；
3. 推理蒸馏：走完数据生成、验证、训练和盲测链路；
4. 自动化越狱红队：只在授权环境中搭建迭代评测 Harness；
5. GUI Agent 与 Agent 安全：把任务轨迹、安全副作用和人工接管纳入统一评测。
