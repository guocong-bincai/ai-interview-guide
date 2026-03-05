# 🚀 AI 应用开发工程师面试宝典

> **版本：** v2.0
> **最后更新：** 2026-03-05
> **作者：** 二狗子 🐕
> **适用岗位：** AI Application Developer / LLM Engineer / AI Agent 开发工程师

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/guocong-bincai/ai-interview-guide?style=flat)](https://github.com/guocong-bincai/ai-interview-guide)
[![Last Commit](https://img.shields.io/github/last-commit/guocong-bincai/ai-interview-guide?style=flat)](https://github.com/guocong-bincai/ai-interview-guide/commits/main)

---

## 📖 简介

本仓库是 **AI 应用开发工程师** 的面试备考指南，专注于帮助传统后端开发者转型 AI 应用开发领域。

**内容涵盖：**
- ✅ RAG 系统设计与实战
- ✅ AI Agent 开发模式
- ✅ LLM 应用架构与工程化
- ✅ 向量数据库与 Embedding
- ✅ Prompt Engineering 进阶
- ✅ 成本优化与性能调优
- ✅ **MCP 协议与 Skill 系统**（2026 热点）
- ✅ **AI 安全与评估**（2026 热点）
- ✅ **AI 应用开发高级专题**（2026 热点）
- ✅ **90+ 高频面试题 + 高分回答**

---

## 📚 目录

### 一、面试题库（130+ 道题）

| 分类 | 内容 | 难度 | 题数 |
|------|------|------|------|
| 🟢 **基础概念** | LLM 原理、Token、Context Window、Temperature 等 | ⭐⭐ | 14 道 |
| 🟡 **RAG 系统** | 检索增强生成、向量数据库、Embedding、Rerank | ⭐⭐⭐ | 10 道 |
| 🟠 **Agent 开发** | ReAct、Function Calling、多智能体协作 | ⭐⭐⭐⭐ | 8 道 |
| 🔴 **工程架构** | 成本控制、性能优化、监控评估、生产部署 | ⭐⭐⭐⭐⭐ | 20 道 |
| 🟣 **MCP & Skill** | MCP 协议、Skill 系统设计、动态加载、安全隔离 | ⭐⭐⭐⭐⭐ | 11 道 |
| 🔵 **AI 安全与评估** | 内容安全、PII 保护、RAGAS 评估、回归测试 | ⭐⭐⭐⭐⭐ | 10 道 |
| 🟤 **高级专题** | 多模态、自主 Agent、产品思维、调试优化、前沿技术 | ⭐⭐⭐⭐⭐ | 10 道 |
| 🎓 **模型微调与训练** | LoRA、RLHF、DPO、微调策略、训练优化 | ⭐⭐⭐⭐ | 11 道 |
| ⚡ **推理优化** | KV Cache、量化、FlashAttention、推理加速 | ⭐⭐⭐⭐⭐ | 10 道 |
| 🎨 **多模态应用** | CLIP、BLIP、图文检索、多模态RAG | ⭐⭐⭐⭐ | 8 道 |

### 二、核心知识点

```
AI 应用开发知识体系
├── 📌 LLM 基础
│   ├── Token 与上下文管理
│   ├── 温度/Top-P/Top-K 调参
│   └── 模型选型（OpenAI vs 开源）
│
├── 📌 RAG 系统
│   ├── 文档加载与切分
│   ├── Embedding 向量化
│   ├── 向量数据库（Milvus/Qdrant/pgvector）
│   ├── 检索优化（混合检索/Rerank）
│   └── 引用溯源与幻觉控制
│
├── 📌 AI Agent
│   ├── ReAct 模式
│   ├── Function Calling
│   ├── 规划与反思
│   └── 多智能体协作
│
├── 📌 工程化
│   ├── 流式输出（SSE）
│   ├── 语义缓存
│   ├── 成本优化（模型路由/Prompt 压缩）
│   └── 监控评估（RAGAS/Tracing）
│
└── 📌 数据处理
    ├── PDF 解析与表格提取
    ├── OCR 与布局分析
    └── 数据清洗 Pipeline
```

### 三、高分实战案例

1. **处理脏数据** - 复杂 PDF 表格解析（准确率 65% → 94%）
2. **成本优化** - 模型路由 + 语义缓存（成本降低 35%）
3. **生产部署** - 解决并发与流式卡顿（200 QPS 稳定运行）

---

## 🎯 使用指南

### 快速开始

1. **基础薄弱？** 从 [基础概念题](docs/01-basic.md) 开始
2. **备战面试？** 直接刷 [面试题库](docs/interview-questions.md)
3. **深入实战？** 看 [高分案例](docs/case-studies.md)

### 学习路线

```
第 1 周：LLM 基础 + Prompt Engineering
第 2 周：RAG 系统原理与实战
第 3 周：AI Agent 设计模式
第 4 周：工程化与成本优化
第 5-6 周：刷题 + 模拟面试
```

---

## 📝 内容预览

### 什么是 RAG？

> RAG = Retrieval-Augmented Generation（检索增强生成）
>
> **核心思想：** 先检索相关知识，再让 LLM 基于检索内容回答问题。
>
> **为什么需要 RAG？**
> - ✅ 解决知识过时问题
> - ✅ 支持私有数据检索
> - ✅ 减少幻觉，提供引用溯源

[查看详细讲解 →](docs/02-rag.md)

---

### 什么是 Embedding？

> Embedding 是把文本的"语义"编码成一串数字（向量）。
>
> **类比：** 描述一个人
> - 传统方式："张三，男，30 岁，北京人，程序员"
> - 向量方式：[0.9, 0.3, 0.8, 0.95, ...]（1536 维）
>
> **语义相似的文本 → 向量接近**

[查看详细讲解 →](docs/03-embedding.md)

---

## 📦 仓库结构

```
ai-interview-guide/
├── README.md              # 本文件
├── docs/                  # 详细文档
│   ├── 01-basic.md        # 基础概念
│   ├── 02-rag.md          # RAG 系统
│   ├── 03-embedding.md    # Embedding 与向量
│   ├── 04-agent.md        # AI Agent
│   ├── 05-engineering.md  # 工程化
│   ├── 06-advanced-questions/  # 进阶问题
│   ├── 07-hot-questions/       # 高频面试题
│   ├── 08-framework-ops/       # 框架与运维
│   ├── 09-vector-index-deep-dive/  # 向量索引深入
│   ├── 10-mcp-skill/      # MCP & Skill 系统
│   ├── 11-ai-safety-eval/ # AI 安全与评估
│   ├── 12-advanced-topics/ # AI 应用开发高级专题
│   ├── 13-model-training/  # 大模型微调与训练（新增）
│   ├── 14-inference-optimization/ # LLM 推理优化（新增）
│   └── 15-multimodal/     # 多模态大模型（新增）
├── questions/             # 面试题库
│   ├── basic.md           # 基础题
│   ├── rag.md             # RAG 题
│   ├── agent.md           # Agent 题
│   └── engineering.md     # 工程题
├── cases/                 # 实战案例
│   ├── pdf-parsing.md     # PDF 解析
│   ├── cost-optimization.md # 成本优化
│   └── production.md      # 生产部署
└── resume/                # 简历模板
    ├── resume-ai.md       # AI 简历
    └── resume-go.md       # Go 简历
```

---

## 🌟 特色

- **📖 系统化** - 从基础到进阶，完整知识体系（**15 个模块**）
- **💡 实战导向** - 每个知识点配实战案例
- **🎯 面试友好** - **130+ 高频题** + 高分回答模板
- **🔥 最新内容** - MCP 协议、Skill 系统、AI 安全评估、模型微调、推理优化、多模态（2026 热点）
- **🔄 持续更新** - 跟随 AI 领域最新发展

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

- 发现错误？[提交 Issue](https://github.com/guocong-bincai/ai-interview-guide/issues)
- 有好题分享？[提交 PR](https://github.com/guocong-bincai/ai-interview-guide/pulls)

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🔗 相关链接

- **作者 GitHub：** https://github.com/guocong-bincai
- **私有仓库：** https://github.com/guocong-bincai/openclaw-workspace
- **VoicePaper 项目：** https://github.com/guocong-bincai/VoicePaper

---

<div align="center">

**👍 如果对你有帮助，请给个 Star！**

Made with ❤️ by 二狗子 🐕

</div>
