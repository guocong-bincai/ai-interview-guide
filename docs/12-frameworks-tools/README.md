# 🛠️ AI 框架与运维面试题

> **难度：** ⭐⭐⭐⭐
> **更新：** 2026-03-02
> **考点：** LangChain、向量数据库、测试评估、部署运维

## 📋 目录

1. [框架使用题](#一框架使用题)
2. [向量数据库题](#二向量数据库题)
3. [测试评估题](#三测试评估题)
4. [部署运维题](#四部署运维题)

## 一、框架使用题

### Q1: LangChain 的核心组件有哪些？如何使用 Chain？

<details>
<summary>💡 答案要点</summary>

**LangChain 核心组件：**

| 组件 | 作用 | 示例 |
|------|------|------|
| **LLM** | 模型抽象层 | ChatOpenAI、ChatAnthropic |
| **Prompt** | 提示词模板 | ChatPromptTemplate |
| **Chain** | 任务编排 | LLMChain、SequentialChain |
| **Agent** | 自主决策 | AgentExecutor |
| **Memory** | 对话记忆 | ConversationBufferMemory |
| **Retriever** | 文档检索 | VectorStoreRetriever |
| **VectorStore** | 向量存储 | Chroma、Milvus、FAISS |

**Chain 使用示例：**
```python
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

# 1. 定义 Prompt 模板
prompt = ChatPromptTemplate.from_template(
    "你是一个{role}。请回答以下问题：{question}"
)

# 2. 创建 LLMChain
chain = LLMChain(
    llm=ChatOpenAI(model="gpt-4o"),
    prompt=prompt
)

# 3. 执行
result = chain.run(role="客服助手", question="如何退款？")
print(result)
```

**面试话术：**
> "LangChain 的核心价值是抽象和编排。我用 LLMChain 封装了 Prompt + LLM，用 SequentialChain 编排多步任务，用 AgentExecutor 实现自主决策。这样代码更模块化，容易测试和维护。"

</details>

### Q2: LangGraph 和 LangChain 有什么区别？什么时候用 LangGraph？

<details>
<summary>💡 答案要点</summary>

**区别对比：**

| 特性 | LangChain | LangGraph |
|------|-----------|-----------|
| **执行模式** | 线性链式 | 图结构（有环） |
| **适用场景** | 简单任务流 | 复杂多轮对话 |
| **状态管理** | 简单 | 强状态管理 |
| **循环支持** | 不支持 | 支持（StateGraph） |

**LangGraph 适用场景：**
1. 多轮对话（需要记住状态）
2. 条件分支（根据结果走不同路径）
3. 循环执行（直到满足条件）
4. 多 Agent 协作

**LangGraph 示例：**
```python
from langgraph.graph import StateGraph, END

# 1. 定义状态
class State(TypedDict):
    messages: list
    current_step: str

# 2. 创建图
graph = StateGraph(State)

# 3. 添加节点
graph.add_node("research", research_agent)
graph.add_node("write", writer_agent)
graph.add_node("review", reviewer_agent)

# 4. 添加边
graph.add_edge("research", "write")
graph.add_edge("write", "review")
graph.add_conditional_edges(
    "review",
    lambda s: "write" if s["needs_revision"] else END
)

# 5. 编译
app = graph.compile()
```

**面试话术：**
> "LangChain 适合线性任务流，LangGraph 适合复杂的多轮对话和多 Agent 协作。我在项目中用 LangGraph 实现了内容创作系统：Researcher 搜索→Writer 写作→Reviewer 审核，如果审核不通过就返回 Writer 修改，形成闭环。"

</details>

### Q3: 如何使用 LlamaIndex 构建 RAG 系统？和 LangChain 有什么区别？

<details>
<summary>💡 答案要点</summary>

**LlamaIndex 核心概念：**

| 概念 | 作用 | 对应 LangChain |
|------|------|----------------|
| **Document** | 文档对象 | Document |
| **Node** | 文档节点（Chunk） | Document |
| **Index** | 索引结构 | VectorStore |
| **QueryEngine** | 查询引擎 | Retriever + Chain |

**LlamaIndex 构建 RAG：**
```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings
)
from llama_index.llms.openai import OpenAI

# 1. 设置 LLM
Settings.llm = OpenAI(model="gpt-4o")

# 2. 加载文档
documents = SimpleDirectoryReader("./docs").load_data()

# 3. 创建索引
index = VectorStoreIndex.from_documents(documents)

# 4. 创建查询引擎
query_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="compact"
)

# 5. 查询
response = query_engine.query("什么是 RAG？")
print(response)
```

**和 LangChain 的区别：**

| 维度 | LlamaIndex | LangChain |
|------|------------|-----------|
| **定位** | 专注于 RAG | 通用 AI 应用框架 |
| **索引** | 丰富（向量、关键词、层次） | 主要是向量 |
| **查询** | 灵活（多阶段查询） | 相对简单 |
| **生态** | 较小 | 更大 |

**面试话术：**
> "LlamaIndex 专注于 RAG，索引和查询更灵活；LangChain 是通用框架，生态更大。我在项目中用 LlamaIndex 做 RAG，因为它支持多阶段查询（先检索摘要，再检索具体段落），检索精度更高。"

</details>

## 二、向量数据库题

### Q4: 向量数据库的索引类型有哪些？怎么选？

<details>
<summary>💡 答案要点</summary>

**主流索引类型：**

| 索引 | 原理 | 速度 | 精度 | 内存 | 适用场景 |
|------|------|------|------|------|----------|
| **HNSW** | 多层图结构 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 高 | 追求速度，内存充足 |
| **IVF** | 先聚类再搜索 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 中 | 数据量大，可接受精度损失 |
| **LSH** | 局部敏感哈希 | ⭐⭐⭐⭐ | ⭐⭐ | 低 | 超大规模，近似即可 |
| **PQ** | 乘积量化 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 低 | 内存受限场景 |

**选型建议：**

| 场景 | 推荐索引 |
|------|----------|
| **<100 万条** | HNSW（速度快） |
| **100 万 -1000 万** | IVF + PQ（平衡） |
| **>1000 万** | IVF 或 LSH（节省内存） |
| **实时插入** | HNSW（索引更新快） |
| **离线批量** | IVF（批量构建快） |

**面试话术：**
> "我在项目中用 HNSW 索引，因为数据量在 50 万条左右，内存充足，追求检索速度。HNSW 的检索延迟在 10ms 以内，比 IVF 快 10 倍。如果数据量增长到千万级，我会考虑 IVF+PQ 的组合。"

</details>

### Q5: 如何优化向量检索的精度和速度？

<details>
<summary>💡 答案要点</summary>

**精度优化：**

| 方案 | 说明 | 效果 |
|------|------|------|
| **Rerank** | 用 Cross-Encoder 重新排序 | 精度提升 10-20% |
| **混合检索** | 向量 + 关键词（BM25） | 召回率提升 15% |
| **Multi-Query** | 生成多个查询变体 | 召回率提升 10% |
| **更好的 Embedding** | BGE-M3、text-embedding-3 | 精度提升 5-10% |

**速度优化：**

| 方案 | 说明 | 效果 |
|------|------|------|
| **HNSW 索引** | 图结构索引 | 100ms → 10ms |
| **减少 k 值** | 只返回 top-3 | 延迟降低 30% |
| **量化** | 向量压缩（FP32→INT8） | 内存减少 4 倍 |
| **GPU 加速** | 并行计算 | 速度提升 5-10 倍 |

**面试话术：**
> "我用了组合优化：1）混合检索（向量+BM25）提升召回率；2）Rerank 精选 Top-5，精度提升 15%；3）HNSW 索引加速检索，延迟从 100ms 降到 10ms。综合下来，检索精度和速度都满足了生产要求。"

</details>

### Q6: 向量数据库的 Metadata 过滤怎么用？有什么应用场景？

<details>
<summary>💡 答案要点</summary>

**Metadata 过滤示例：**
```python
# Chroma 示例
results = collection.query(
    query_embeddings=[...],
    filter={
        "tenant_id": "company_a",
        "department": {"$in": ["hr", "finance"]},
        "created_at": {"$gte": "2025-01-01"},
        "access_level": {"$lte": 3}
    },
    n_results=5
)

# Milvus 示例
results = collection.search(
    data=[...],
    filter="tenant_id == 'company_a' and created_at > '2025-01-01'",
    limit=5
)
```

**应用场景：**

| 场景 | Metadata 字段 | 过滤条件 |
|------|--------------|----------|
| **多租户** | tenant_id | tenant_id == "xxx" |
| **权限控制** | access_level | access_level <= user_level |
| **时间范围** | created_at | created_at >= "2025-01-01" |
| **部门隔离** | department | department in ["hr", "finance"] |
| **文档类型** | doc_type | doc_type == "policy" |

**面试话术：**
> "我在多租户系统中，用 Metadata 实现了数据隔离和权限控制。每个 Chunk 都有 tenant_id、department、access_level 等字段。检索时自动过滤，确保用户只能访问授权的知识。这样不需要物理隔离多个向量库，成本降低了 80%。"

</details>

## 三、测试评估题

### Q7: 如何测试 AI 应用的质量？有哪些评估指标？

<details>
<summary>💡 答案要点</summary>

**评估指标体系：**

| 类别 | 指标 | 说明 | 合格线 |
|------|------|------|--------|
| **准确性** | Faithfulness | 答案是否基于检索内容 | > 0.7 |
| **准确性** | Answer Relevance | 答案是否回答问题 | > 0.8 |
| **检索质量** | Context Relevance | 检索内容是否有用 | > 0.8 |
| **检索质量** | Context Recall | 是否检索到正确答案 | > 0.8 |
| **用户体验** | 点赞率 | 用户满意的比例 | > 80% |
| **用户体验** | 重新生成率 | 用户重新生成的比例 | < 15% |

**测试方法：**

| 方法 | 说明 | 优缺点 |
|------|------|--------|
| **人工评估** | 人工给答案打分 | 准确，但成本高 |
| **自动评估** | RAGAS、TruLens | 快速，但不够准确 |
| **A/B 测试** | 对比不同策略 | 真实，但需要流量 |
| **回归测试** | 固定测试集定期跑 | 防止退化 |

**面试话术：**
> "我建立了三层评估体系：1）自动评估（RAGAS）每次上线前跑；2）人工抽检（每周 5%）；3）A/B 测试（新策略灰度发布）。有一次 RAGAS 指标正常，但人工评估发现答案质量下降，原来是检索策略改变了，及时调整了回来。"

</details>

### Q8: 如何构建 AI 应用的测试集？

<details>
<summary>💡 答案要点</summary>

**测试集构建流程：**

```
1. 收集问题 → 2. 标注标准答案 → 3. 分类整理 → 4. 定期更新
```

**问题分类：**

| 类别 | 说明 | 占比 |
|------|------|------|
| **简单问题** | FAQ、事实查询 | 40% |
| **中等问题** | 需要推理 | 40% |
| **复杂问题** | 多步推理、计算 | 15% |
| **边界问题** | 模糊、无答案 | 5% |

**测试集规模：**
- **最小可用**：50-100 题
- **推荐**：200-500 题
- **生产级**：1000+ 题

**维护策略：**
1. **每周新增**：从用户反馈中收集新问题
2. **每月审核**：删除过时问题，更新答案
3. **每季度回归**：跑一遍测试集，确保质量不下降

**面试话术：**
> "我维护了一个 300 题的测试集，覆盖简单/中等/复杂三种难度。每次上线前跑一遍，Faithfulness 低于 0.7 就阻断发布。同时每周从用户反馈中收集 10-20 个新问题，持续扩充测试集。"

</details>

## 四、部署运维题

### Q9: 如何部署 LLM 应用到生产环境？需要注意什么？

<details>
<summary>💡 答案要点</summary>

**部署架构：**
```
用户 → CDN → 负载均衡 → API Gateway → 服务集群 → LLM API
                                    ↓
                              Redis 缓存
                                    ↓
                              监控告警
```

**关键注意事项：**

| 方面 | 注意点 | 解决方案 |
|------|--------|----------|
| **延迟** | LLM 响应慢 | 流式输出、缓存 |
| **成本** | Token 费用高 | 模型路由、压缩 |
| **稳定性** | API 可能失败 | 重试、降级、多 Key 轮询 |
| **安全** | Prompt Injection | 输入过滤、输出审核 |
| **监控** | 难以追踪问题 | 完整链路日志、RAGAS 监控 |

**部署清单：**
- [ ] 限流配置（令牌桶）
- [ ] 缓存策略（语义缓存）
- [ ] 超时设置（首字<5s）
- [ ] 降级方案（LLM 挂了返回预设答案）
- [ ] 监控告警（成本、延迟、错误率）
- [ ] 日志记录（完整请求链路）

**面试话术：**
> "我部署 AI 应用时，核心是稳定性。LLM API 可能失败，我设计了多 Key 轮询 + 重试 + 降级三层防护。同时用流式输出降低首字延迟，用语义缓存降低成本。监控方面，我追踪每个请求的完整链路，一旦成本或延迟异常就告警。"

</details>

### Q10: 如何监控 AI 应用的成本？如何优化？

<details>
<summary>💡 答案要点</summary>

**成本组成：**
```
总成本 = LLM 调用成本 + 向量数据库成本 + 服务器成本
       (70%)           (20%)            (10%)
```

**监控指标：**

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| **每日 Token 消耗** | 输入 + 输出 | 超过预算 20% |
| **单次调用成本** | 平均每次请求的费用 | > $0.01 |
| **缓存命中率** | 缓存命中的比例 | < 30% |
| **模型分布** | 各模型调用比例 | 大模型占比过高 |

**优化策略：**

| 策略 | 说明 | 节省比例 |
|------|------|----------|
| **语义缓存** | 相似问题直接返回 | 30-50% |
| **模型路由** | 简单问题用小模型 | 30-40% |
| **Prompt 压缩** | LLMLingua 压缩 | 40-90% |
| **批量处理** | 多个请求合并 | 10-20% |

**面试话术：**
> "我搭建了成本监控看板，实时追踪 Token 消耗和费用。有一次发现成本突增，通过追踪发现是一个 Prompt 泄露了系统指令，导致模型输出了大量无效内容。修复后，我加入了 Prompt 长度限制和输出审核，成本稳定在预算内。"

</details>

## 9. Coze平台如何搭建AI应用?与传统开发的区别?

<details>
<summary>💡 答案要点</summary>

**Coze = 字节跳动的低代码AI应用开发平台**

### Coze核心能力

| 能力 | 说明 | 优势 |
|------|------|------|
| **Bot构建** | 可视化配置AI助手 | 零代码快速上线 |
| **Workflow** | 拖拽式工作流设计 | 复杂逻辑可视化 |
| **插件系统** | 丰富的预制插件 | 快速集成第三方服务 |
| **知识库** | 文档上传+向量检索 | RAG开箱即用 |
| **多模态** | 支持图文/语音/视频 | 全场景覆盖 |

### Coze工作流设计

**场景: 客服机器人**

```
Coze可视化流程:

┌──────────┐
│ 用户输入 │
└────┬─────┘
     │
     ▼
┌──────────┐     ┌──────────┐
│ 意图识别 │────→│ 知识库   │
└────┬─────┘     │ 检索     │
     │           └────┬─────┘
     │ (商品咨询)      │
     ▼                ▼
┌──────────┐     ┌──────────┐
│ 调用API  │     │ LLM生成  │
│ 查库存   │     │ 回答     │
└────┬─────┘     └────┬─────┘
     │                │
     └────────┬───────┘
              ▼
         ┌──────────┐
         │ 返回用户 │
         └──────────┘

传统代码实现需要100+行
Coze可视化配置:5分钟完成
```

**配置示例:**

```yaml
# Coze Workflow配置(伪代码)
workflow:
  name: "客服Bot"

  nodes:
    - id: "intent"
      type: "intent_classifier"
      config:
        intents:
          - "商品咨询"
          - "退换货"
          - "投诉"

    - id: "knowledge_base"
      type: "knowledge_retrieval"
      config:
        kb_id: "kb_12345"
        top_k: 3

    - id: "api_call"
      type: "http_request"
      config:
        url: "https://api.example.com/inventory"
        method: "GET"

    - id: "llm_response"
      type: "llm_generation"
      config:
        model: "gpt-4o-mini"
        prompt: "基于以下信息回答用户:\n知识库: {{knowledge_base.output}}\n库存: {{api_call.response}}"

  edges:
    - from: "intent"
      to: "knowledge_base"
      condition: "intent == '商品咨询'"

    - from: "knowledge_base"
      to: "llm_response"
```

### Coze vs 传统开发

| 维度 | Coze平台 | 传统代码 | 差距 |
|------|---------|---------|------|
| **开发速度** | 5分钟 | 2-3天 | **100倍** |
| **技术门槛** | 产品经理可用 | 需AI工程师 | **大幅降低** |
| **RAG集成** | 拖拽配置 | 50+行代码 | **10倍效率** |
| **工作流可视化** | ✅ | ❌ | **易维护** |
| **模型切换** | 一键切换 | 改代码+测试 | **即时** |
| **成本** | 按调用付费 | 服务器+人力 | **灵活** |

### Coze高级功能

**1. 插件系统**

```javascript
// Coze预制插件
plugins:
  - "web_search"      // 网页搜索
  - "image_gen"       // 图片生成
  - "code_interpreter" // 代码执行
  - "weather_api"     // 天气查询
  - "database_query"  // 数据库查询

// 自定义插件(JavaScript)
function myPlugin(input) {
  // 调用第三方API
  const result = fetch("https://api.example.com", {
    body: JSON.stringify(input)
  });

  return result.data;
}
```

**2. 变量管理**

```python
# Coze支持的变量类型
variables:
  - user_id: "{{user.id}}"           # 用户变量
  - session_id: "{{session.id}}"     # 会话变量
  - kb_result: "{{knowledge.output}}" # 节点输出
  - config.api_key: "sk-xxx"         # 环境变量
```

**3. 条件分支**

```
IF 用户意图 == "退货"
  THEN
    → 检查订单状态
    → IF 可退货
        THEN 生成退货链接
        ELSE 告知不可退货原因
ELSE IF 用户意图 == "商品咨询"
  THEN
    → 知识库检索
    → LLM生成回答
```

### Coze实战案例

**案例: 招聘面试助手**

```yaml
workflow:
  # 1. 简历解析
  - node: "resume_parser"
    input: "{{user_upload.file}}"
    output: "parsed_resume"

  # 2. 岗位匹配
  - node: "job_matching"
    input: "{{parsed_resume}}"
    prompt: "分析候选人是否适合XX岗位"
    output: "match_score"

  # 3. 面试问题生成
  - node: "question_generator"
    condition: "{{match_score}} > 60"
    prompt: "根据简历生成5个面试问题:\n{{parsed_resume}}"
    output: "questions"

  # 4. 面试对话
  - node: "interview_bot"
    input: "{{questions}}"
    memory: true  # 记录对话历史
    output: "interview_record"

  # 5. 评估报告
  - node: "evaluation"
    input: "{{interview_record}}"
    prompt: "生成面试评估报告"
    output: "final_report"
```

**效果:**
- 开发时间: 1小时 (传统开发需1周)
- 测试调整: 实时预览,立即修改
- 部署上线: 一键发布,无需运维

### Coze vs Dify vs FastGPT

| 平台 | 定位 | 优势 | 劣势 |
|------|------|------|------|
| **Coze** | 商业平台,字节出品 | UI最美,插件丰富,稳定 | 闭源,国内限制 |
| **Dify** | 开源平台 | 可本地部署,自主可控 | UI稍弱,需运维 |
| **FastGPT** | 开源RAG平台 | 专注知识库,轻量 | 功能单一 |

**选型建议:**
- **快速验证:** Coze (5分钟上线)
- **企业私有化:** Dify (数据安全)
- **纯知识库:** FastGPT (简单场景)

**面试话术:**
> "我用Coze快速搭建过客服Bot,5分钟完成传统开发需2天的工作。Coze的优势是可视化工作流+开箱即用的RAG,非常适合快速验证。但生产环境我们用Dify,因为需要本地部署保证数据安全。Coze的插件生态很强,像代码执行、图片生成都是预制的,但灵活性不如代码开发。我会根据场景选择:原型验证用Coze,生产系统用Dify+代码混合。"

</details>

---

## 10. Dify本地部署与性能优化实战?

<details>
<summary>💡 答案要点</summary>

**Dify = 开源的LLM应用开发平台**

### Dify架构

```
┌─────────────────────────────────────────────────┐
│                   Dify 架构                      │
├─────────────────────────────────────────────────┤
│  前端 (Next.js)                                  │
│    ↓                                             │
│  API服务 (Flask)                                 │
│    ↓                                             │
│  ┌─────────┬─────────┬─────────┬─────────┐      │
│  │ LLM层   │ 知识库  │ 工作流  │ 插件    │      │
│  └─────────┴─────────┴─────────┴─────────┘      │
│    ↓         ↓         ↓         ↓              │
│  ┌──────────────────────────────────────┐       │
│  │ 数据层: PostgreSQL + Redis + Milvus  │       │
│  └──────────────────────────────────────┘       │
└─────────────────────────────────────────────────┘
```

### 本地部署流程

**方式1: Docker Compose (推荐)**

```bash
# 1. 克隆仓库
git clone https://github.com/langgenius/dify.git
cd dify/docker

# 2. 配置环境变量
cp .env.example .env

# 编辑 .env
vim .env
# 修改:
# SECRET_KEY=your-secret-key
# OPENAI_API_KEY=sk-xxx
# DB_PASSWORD=strong-password

# 3. 启动服务
docker-compose up -d

# 4. 检查服务
docker-compose ps

# 输出:
# dify-api        running   0.0.0.0:5001->5001/tcp
# dify-web        running   0.0.0.0:3000->3000/tcp
# dify-worker     running
# postgres        running   5432/tcp
# redis           running   6379/tcp
# milvus          running   19530/tcp

# 5. 访问
# http://localhost:3000
```

**方式2: K8s部署 (生产环境)**

```yaml
# dify-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dify-api
spec:
  replicas: 3  # 高可用
  selector:
    matchLabels:
      app: dify-api
  template:
    metadata:
      labels:
        app: dify-api
    spec:
      containers:
      - name: api
        image: langgenius/dify-api:latest
        env:
        - name: DB_HOST
          value: "postgres-service"
        - name: REDIS_HOST
          value: "redis-service"
        - name: VECTOR_STORE
          value: "milvus"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        readinessProbe:
          httpGet:
            path: /health
            port: 5001
          initialDelaySeconds: 30
          periodSeconds: 10
```

### 性能优化实战

**优化1: 数据库连接池**

```python
# docker/.env 配置
# Before: 默认连接池小
SQLALCHEMY_POOL_SIZE=10

# After: 根据并发调整
SQLALCHEMY_POOL_SIZE=50          # 连接池大小
SQLALCHEMY_MAX_OVERFLOW=100      # 最大溢出
SQLALCHEMY_POOL_TIMEOUT=30       # 超时时间
SQLALCHEMY_POOL_RECYCLE=3600     # 连接回收

# 效果: 并发从100 QPS → 500 QPS
```

**优化2: Redis缓存策略**

```python
# api/core/redis.py
class CacheManager:
    def __init__(self):
        self.redis = Redis(
            host=os.getenv("REDIS_HOST"),
            decode_responses=True,
            max_connections=100  # 连接池
        )

    def cache_llm_response(self, prompt_hash, response, ttl=3600):
        """缓存LLM响应"""
        key = f"llm:cache:{prompt_hash}"
        self.redis.setex(key, ttl, json.dumps(response))

    def get_cached_response(self, prompt_hash):
        """获取缓存"""
        key = f"llm:cache:{prompt_hash}"
        cached = self.redis.get(key)
        return json.loads(cached) if cached else None

# 使用
cache = CacheManager()

# Before: 每次都调LLM
response = llm.generate(prompt)  # 2秒

# After: 命中缓存
prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
cached = cache.get_cached_response(prompt_hash)
if cached:
    return cached  # 10ms ⚡
else:
    response = llm.generate(prompt)
    cache.cache_llm_response(prompt_hash, response)

# 效果: 缓存命中率30%,平均响应时间 -600ms
```

**优化3: 向量检索优化**

```python
# api/core/vector_store.py

# Before: 向量检索慢
results = milvus.search(
    collection_name="documents",
    query_vectors=[embedding],
    top_k=10
)  # 500ms

# After: 优化索引+预过滤
# 1. 创建HNSW索引
milvus.create_index(
    collection_name="documents",
    field_name="embedding",
    index_params={
        "index_type": "HNSW",
        "metric_type": "COSINE",
        "params": {"M": 16, "efConstruction": 256}
    }
)

# 2. 分区存储(按租户)
milvus.create_partition(
    collection_name="documents",
    partition_name=f"tenant_{tenant_id}"
)

# 3. 检索时预过滤
results = milvus.search(
    collection_name="documents",
    partition_names=[f"tenant_{tenant_id}"],  # 只搜索该租户
    query_vectors=[embedding],
    top_k=10,
    expr="created_at > 1704067200"  # 过滤时间
)  # 50ms ⚡ (优化10倍)

# 效果: 检索时间 500ms → 50ms
```

**优化4: 异步任务队列**

```python
# api/core/celery_app.py
from celery import Celery

celery = Celery(
    "dify",
    broker=os.getenv("CELERY_BROKER"),
    backend=os.getenv("CELERY_BACKEND")
)

@celery.task
def async_embedding_task(document_id, text):
    """异步Embedding"""
    embedding = embedding_model.encode(text)
    milvus.insert(document_id, embedding)

# 使用
# Before: 同步处理,阻塞用户
for doc in documents:
    embedding = embedding_model.encode(doc.text)  # 阻塞1秒
    milvus.insert(doc.id, embedding)
# 10个文档 = 10秒

# After: 异步处理
for doc in documents:
    async_embedding_task.delay(doc.id, doc.text)
# 立即返回,后台处理 ⚡

# 效果: 用户等待时间 10秒 → 100ms
```

**优化5: API限流**

```python
# api/middleware/rate_limit.py
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.headers.get("X-User-ID"),
    storage_uri=f"redis://{os.getenv('REDIS_HOST')}:6379"
)

# 应用限流
@app.route("/api/chat", methods=["POST"])
@limiter.limit("60/minute")  # 每分钟60次
def chat():
    pass

# 不同用户等级不同限流
@limiter.limit("100/minute", key_func=lambda: f"premium:{get_user_id()}")
@limiter.limit("20/minute", key_func=lambda: f"free:{get_user_id()}")
def tiered_chat():
    pass

# 效果: 防止恶意攻击,保护系统稳定
```

### 监控与告警

```python
# api/core/monitoring.py
import prometheus_client as prom

# 定义指标
llm_request_duration = prom.Histogram(
    "llm_request_duration_seconds",
    "LLM请求耗时",
    buckets=[0.1, 0.5, 1, 2, 5, 10]
)

llm_request_total = prom.Counter(
    "llm_request_total",
    "LLM请求总数",
    ["model", "status"]
)

cache_hit_rate = prom.Gauge(
    "cache_hit_rate",
    "缓存命中率"
)

# 记录指标
with llm_request_duration.time():
    response = llm.generate(prompt)

llm_request_total.labels(model="gpt-4", status="success").inc()

# Grafana看板
# http://localhost:3000/dashboards
# - LLM请求QPS
# - 平均响应时间
# - 缓存命中率
# - 错误率
```

### 生产环境清单

```yaml
# 部署清单
infrastructure:
  - ✅ K8s集群 (至少3节点)
  - ✅ PostgreSQL (主从复制)
  - ✅ Redis (哨兵模式)
  - ✅ Milvus (分布式)
  - ✅ 负载均衡 (Nginx)

performance:
  - ✅ 数据库连接池优化
  - ✅ Redis缓存策略
  - ✅ 向量检索索引
  - ✅ 异步任务队列
  - ✅ API限流

monitoring:
  - ✅ Prometheus监控
  - ✅ Grafana看板
  - ✅ 日志聚合(ELK)
  - ✅ 告警通知(钉钉/企微)

security:
  - ✅ HTTPS证书
  - ✅ 密钥管理(Vault)
  - ✅ 权限控制(RBAC)
  - ✅ 数据加密
```

**面试话术:**
> "我本地部署过Dify,用Docker Compose快速启动,生产用K8s 3副本高可用。核心优化4点:1)数据库连接池50+溢出100,并发从100→500QPS;2)Redis缓存LLM响应,命中率30%省600ms;3)Milvus用HNSW索引+分区存储,检索从500ms→50ms快10倍;4)Embedding异步处理,用户等待10秒→100ms。部署后Prometheus+Grafana监控,设置P99<2秒告警。整体系统稳定支撑1000+用户。"

</details>

---

## 📝 速记卡片

| 话题 | 核心要点 |
|------|----------|
| **LangChain** | LLM+Prompt+Chain+Agent+Memory+Retriever |
| **LangGraph** | 图结构，支持循环和多 Agent 协作 |
| **LlamaIndex** | 专注 RAG，索引和查询更灵活 |
| **向量索引** | HNSW（快）、IVF（大）、LSH（超大） |
| **检索优化** | Rerank + 混合检索 + Multi-Query |
| **Metadata 过滤** | 多租户、权限、时间、部门 |
| **评估指标** | Faithfulness、Relevance、Recall |
| **测试集** | 50-100 题最小，300 题推荐，1000+ 生产级 |
| **部署清单** | 限流、缓存、超时、降级、监控、日志 |
| **成本优化** | 缓存 30-50% + 路由 30-40% + 压缩 40-90% |
| **Coze平台** | 字节低代码平台,5分钟搭Bot,插件丰富 |
| **Dify部署** | Docker Compose快速/K8s生产,优化4点(连接池/缓存/索引/异步) |

## 📊 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-03-02 | 新增 10 道框架与运维面试题 |


---

**上一模块：** [多模态 AI](../11-multimodal-ai/)
**下一模块：** [多智能体系统](../13-multi-agent-systems/)

---

[返回目录 →](../../README.md)
