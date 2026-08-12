<div align="center">

# AI 应用开发工程师面试指南

面向 AI 应用、LLM、RAG 与 Agent 岗位的系统化面试题库。

**最后整理：2026-08-12**

</div>

## 项目定位

本项目帮助候选人完成三件事：

1. 理解 AI 应用开发中的稳定基础知识；
2. 能从质量、延迟、成本、安全和复杂度解释工程取舍；
3. 能用自己的真实项目数据回答追问，而不是背诵虚构经历。

题目质量优先于数量。产品版本、论文数据和性能结论可能随时间变化，使用前应查看题目中的来源和适用条件。

## 学习路线

### AI 应用开发

`LLM 基础 → Prompt → RAG → Agent → 生产部署 → 系统设计`

### RAG 工程

`LLM 基础 → RAG 基础 → 向量检索 → RAG 高级优化 → 安全评估 → 可观测性`

### Agent 工程

`Prompt → Agent 基础 → 规划与反思 → 多 Agent → MCP/Skills → Agent 可观测性`

### 模型训练与推理

`Transformer → 模型训练 → 推理优化 → 推理框架 → 生产部署`

## 题库目录

### 基础与模型

| 模块 | 内容 |
|---|---|
| [01 · LLM 基础](docs/01-basic-concepts/) | Token、解码、Embedding、训练阶段、模型结构基础 |
| [02 · Prompt Engineering](docs/02-prompt-engineering/) | Prompt、上下文设计、结构化输出与评测 |
| [Transformer 架构](docs/04-transformer-architecture/) | Attention、位置编码、归一化与架构演进 |
| [07 · 模型训练](docs/07-model-training/) | LoRA、数据、训练、对齐与评估 |
| [08 · 推理优化](docs/08-inference-optimization/) | KV Cache、量化、批处理与推测解码 |
| [19 · 推理框架](docs/19-inference-frameworks/) | vLLM、SGLang、TensorRT-LLM 与基准方法 |

> `04-project-experience` 与 `04-transformer-architecture` 的历史目录编号重复。为避免破坏已有外部链接，暂时保留目录名，以本页模块名称为准。

### RAG 与检索

| 模块 | 内容 |
|---|---|
| [03 · RAG 系统](docs/03-rag-system/) | 文档处理、检索、生成与常见问题 |
| [06 · 向量索引优化](docs/06-vector-index-optimization/) | ANN 索引、混合检索、Rerank 与调参 |
| [20 · RAG 高级优化](docs/20-rag-advanced-optimization/) | 自适应检索、评估、权限和生产治理 |

### Agent 与协议

| 模块 | 内容 |
|---|---|
| [05 · Agent 基础](docs/05-ai-agent-basics/) | 工具调用、状态、记忆、循环与人工确认 |
| [13 · 多 Agent 系统](docs/13-multi-agent-systems/) | 协作模式、任务分配、通信与故障处理 |
| [14 · MCP 与 Skills](docs/14-mcp-skill-systems/) | MCP 原语、能力发现、授权与协议安全 |
| [22 · Agent 规划与反思](docs/22-agent-planning-reflection/) | 规划、重规划、验证、反思和终止 |
| [23 · Agent 可观测性](docs/23-agent-observability/) | Trace、指标、评估、告警与成本归因 |

### 工程与系统设计

| 模块 | 内容 |
|---|---|
| [04 · 项目经验](docs/04-project-experience/) | 项目说明、指标、取舍和事故复盘 |
| [09 · 安全与评估](docs/09-ai-safety-evaluation/) | 内容安全、Prompt 注入、隐私、红队和评测 |
| [10 · 生产部署](docs/10-production-deployment/) | 网关、限流、流式输出、可靠性与发布 |
| [12 · 框架与工具](docs/12-frameworks-tools/) | 框架抽象、选型、测试和迁移 |
| [24 · Python 工程](docs/24-python-engineering/) | 异步、类型、测试、重试和性能排查 |
| [25 · AI 系统设计](docs/25-system-design-ai/) | 客服、知识库、网关、任务系统和审核系统 |

### 多模态与前沿方向

| 模块 | 内容 |
|---|---|
| [11 · 多模态 AI](docs/11-multimodal-ai/) | 图像、音频、视频与多模态检索 |
| [15 · 高级专题](docs/15-advanced-topics/) | 尚未完全稳定的研究和工程方向 |
| [17 · AI 编程工具](docs/17-ai-coding-tools/) | Coding Agent、代码评测、上下文和团队治理 |
| [21 · 多模态 Agent](docs/21-multimodal-agents/) | GUI、文档、视频和视觉工具调用 |

### 面试准备

| 模块 | 内容 |
|---|---|
| [16 · 简历与面试技巧](docs/16-resume-interview-tips/) | 简历、项目表达、行为面试与追问 |
| [18 · 面试题来源整理](docs/18-big-tech-interview-questions/) | 按公司整理的面试考点；使用时注意来源可信度 |

## 推荐使用方法

学习一道题时，不要直接背完整答案。建议按以下方式练习：

1. 用 30 秒给出结论；
2. 用 2～3 分钟解释原理和取舍；
3. 回答“如何验证”“失败怎么办”“为什么不用另一种方案”；
4. 把示例数字替换成自己的真实项目数据；
5. 对时效性内容检查官方文档或原论文。

## 内容质量与贡献

新增或修改题目前，请阅读 [内容质量规范](CONTENT_QUALITY.md)。本仓库不接受无来源的精确效果数字、虚构的一线面试标签或第一人称项目战绩。

运行内容检查：

```bash
python3 scripts/content_audit.py
```

欢迎通过 [Issue](https://github.com/guocong-bincai/ai-interview-guide/issues) 报告错误，或通过 [Pull Request](https://github.com/guocong-bincai/ai-interview-guide/pulls) 提交修正。对于时效性内容，请优先引用官方文档、标准、论文或可复现的基准测试。

## License

[MIT](LICENSE)
