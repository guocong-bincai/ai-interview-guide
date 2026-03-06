# 💼 AI项目实战经验面试题

> **难度：** ⭐⭐⭐⭐⭐
> **更新：** 2026-03-05
> **考点：** 项目描述、技术选型、难点突破、性能优化

## 📋 目录

1. [RAG系统项目](#一rag系统项目)
2. [AI Agent项目](#二ai-agent项目)
3. [LLM应用项目](#三llm应用项目)
4. [多模态项目](#四多模态项目)
5. [优化类项目](#五优化类项目)
6. [项目回答技巧](#六项目回答技巧)

---

## 一、RAG系统项目

### Q1: "请介绍一下你做过的RAG系统项目"

<details>
<summary>💡 STAR回答模板</summary>

**S (Situation - 背景):**
> "我在xx公司负责开发一个企业级知识库问答系统,主要服务内部员工查询公司文档、政策、技术文档等。知识库包含5000+文档,总计200万字,涵盖HR、技术、产品等多个领域。"

**T (Task - 任务):**
> "项目目标是实现:
> 1. 准确率>85% (用户满意度)
> 2. 平均响应时间<2秒
> 3. 成本可控(月<$500)
> 4. 支持中英文混合查询"

**A (Action - 行动):**

**1. 技术架构设计**
```python
# 技术栈选择
向量数据库: Qdrant (开源,支持混合检索)
Embedding模型: bge-large-zh-v1.5 (中文效果好)
LLM: GPT-3.5-turbo (成本平衡)
框架: LangChain

# 核心流程
用户提问 → Query改写(补充上下文)
         → 混合检索(BM25 + 语义)
         → Rerank精排(BGE-Reranker)
         → 上下文压缩(LLMLingua)
         → LLM生成答案
         → 引用来源标注
```

**2. 关键优化点**

**(1) 分块策略优化**
```python
# 问题: 固定512 token分块效果差
# 原因: 切断了语义完整性

# 解决: 语义分块 + 重叠
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,           # 略大,保留更多上下文
    chunk_overlap=200,        # 20%重叠,避免边界问题
    separators=["\n\n", "\n", "。", ".", " "],  # 优先按段落
)

# 效果: 召回率 68% → 79%
```

**(2) 混合检索实现**
```python
def hybrid_search(query, top_k=20):
    # BM25检索
    bm25_results = bm25_retriever.search(query, k=top_k)

    # 向量检索
    vector_results = vector_db.search(
        embedding_model.encode(query),
        k=top_k
    )

    # RRF融合
    final_results = reciprocal_rank_fusion(
        [bm25_results, vector_results],
        k=60
    )

    return final_results[:10]  # 取top-10

# 效果: 召回率 79% → 87%
```

**(3) Rerank精排**
```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('BAAI/bge-reranker-large')

def rerank(query, candidates):
    # 计算query与每个candidate的相关性分数
    scores = reranker.predict([
        [query, doc.content] for doc in candidates
    ])

    # 按分数排序
    ranked = sorted(
        zip(candidates, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked[:5]]

# 效果: 精确率 73% → 89%
```

**(4) 成本优化 - 语义缓存**
```python
from langchain.cache import RedisSemanticCache

# 相似问题直接返回缓存答案
cache = RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=embedding_model,
    score_threshold=0.85  # 相似度>0.85命中缓存
)

# 缓存命中率: 35%
# 成本节省: 35% API调用
```

**R (Result - 结果):**
> "项目上线后:
> - 准确率达到**89%** (超过目标85%)
> - P95响应时间**1.8秒** (目标<2秒)
> - 月成本**$320** (节省36%,目标$500)
> - 日均处理**2000+**次查询
> - 用户满意度**4.3/5**
>
> 核心突破点:
> 1. 混合检索+Rerank,召回率提升19%
> 2. 语义缓存,成本降低35%
> 3. 语义分块,召回率提升11%"

**面试追问应对:**

**Q: "为什么选择Qdrant而不是Pinecone/Milvus?"**
> "我们对比了3个方案:
> - Pinecone: 云服务,易用但贵($70/月起)
> - Milvus: 功能强大但部署复杂,需要K8s
> - **Qdrant: 开源免费,Docker部署简单,支持混合检索⭐**
>
> 我们团队规模小,选Qdrant自部署,成本$0,功能够用。"

**Q: "遇到的最大难点是什么?怎么解决的?"**
> "最大难点是**长文档检索不准**。
>
> **问题现象:**
> - 用户问'请假流程',检索到的chunk是'考勤制度第3章',但答案在第5章
> - 召回率只有68%
>
> **分析原因:**
> - 固定512 token分块,切断了语义
> - 标题和正文分离,丢失了上下文
>
> **解决方案:**
> 1. 语义分块: 按段落/标题层级切分
> 2. 增加chunk_overlap: 200 token重叠
> 3. Parent-Child索引: 检索时返回父chunk
>
> **效果:** 召回率68%→79%,提升16%"

**Q: "如果让你重新设计,会怎么改进?"**
> "3个改进方向:
>
> 1. **引入HyDE (假设性文档嵌入)**
>    - 当前: 直接用用户问题检索
>    - 改进: 先让LLM生成假设答案,用假设答案检索
>    - 预期: 召回率+5%
>
> 2. **多路召回+学习排序**
>    - 当前: BM25 + Vector 两路
>    - 改进: + 时间相关性 + 用户历史偏好
>    - 预期: 个性化提升
>
> 3. **Fine-tune Embedding模型**
>    - 当前: 通用bge模型
>    - 改进: 在企业文档上微调
>    - 预期: 领域适配性+10%"

</details>

---

### Q2: "RAG系统中遇到的召回率低问题,怎么解决的?"

<details>
<summary>💡 答案要点</summary>

**问题分析:**
```
召回率低 = 相关文档没检索到

可能原因:
1. 分块策略不合理
2. Embedding模型不适配
3. 只用单一检索方式
4. Query表达不清晰
```

**诊断步骤:**

**Step 1: 建立评估数据集**
```python
# 构建100条标准问答对
test_dataset = [
    {
        "question": "员工请假超过3天需要什么审批?",
        "ground_truth_docs": ["doc_123", "doc_456"],  # 应该检索到的文档ID
        "ideal_answer": "超过3天需要部门经理+HR审批"
    },
    # ... 100条
]

# 计算Recall@K
def evaluate_recall(retriever, dataset, k=5):
    total_recall = 0
    for item in dataset:
        retrieved = retriever.search(item["question"], k=k)
        retrieved_ids = [doc.id for doc in retrieved]

        # 计算召回了多少ground_truth
        hits = len(set(retrieved_ids) & set(item["ground_truth_docs"]))
        recall = hits / len(item["ground_truth_docs"])
        total_recall += recall

    return total_recall / len(dataset)

# 基线: Recall@5 = 0.68
```

**Step 2: 逐项优化**

**(1) 优化分块 (+11% Recall)**
```python
# Before: 固定长度
splitter_old = RecursiveCharacterTextSplitter(chunk_size=512)

# After: 语义分块 + 元数据
from langchain.text_splitter import MarkdownTextSplitter

splitter_new = MarkdownTextSplitter(
    chunk_size=800,
    chunk_overlap=200,
    # 保留标题层级
    add_start_index=True
)

# 添加元数据
for chunk in chunks:
    chunk.metadata = {
        "source": doc.source,
        "title": extract_title(chunk),
        "section": extract_section(chunk),
        "page": chunk.page
    }

# Recall: 0.68 → 0.79 (+11%)
```

**(2) 混合检索 (+8% Recall)**
```python
# Before: 只用向量检索
vector_results = vector_db.search(query)

# After: BM25 + Vector + RRF
def hybrid_retrieval(query, k=20):
    # BM25擅长关键词
    bm25_results = bm25.search(query, k=k)

    # Vector擅长语义
    vector_results = vector_db.search(
        embed(query), k=k
    )

    # RRF融合
    return rrf_fusion([bm25_results, vector_results], k=60)

# Recall: 0.79 → 0.87 (+8%)
```

**(3) Query改写 (+5% Recall)**
```python
# Before: 直接用用户原始问题
query = "请假流程"  # 太简短,语义不明

# After: LLM扩展query
def expand_query(query):
    prompt = f"""
    原始问题: {query}

    请生成3个相关的扩展查询,帮助检索:
    1. 同义词替换
    2. 补充上下文
    3. 细化问题

    示例:
    原始: "请假流程"
    扩展:
    1. "员工请假审批流程"
    2. "如何申请休假"
    3. "请假需要哪些步骤"
    """

    expanded = llm.generate(prompt)
    return [query] + expanded  # 返回原始+扩展

# 用多个query检索,合并结果
all_results = []
for q in expand_query(query):
    all_results.extend(hybrid_retrieval(q, k=10))

# 去重+排序
final = deduplicate_and_rerank(all_results)

# Recall: 0.87 → 0.92 (+5%)
```

**(4) Rerank精排 (+3% 保持top-5质量)**
```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('BAAI/bge-reranker-large')

# 先召回20个候选
candidates = hybrid_retrieval(query, k=20)

# Rerank精选top-5
scores = reranker.predict([
    [query, doc.content] for doc in candidates
])

top5 = sorted(
    zip(candidates, scores),
    key=lambda x: x[1],
    reverse=True
)[:5]

# Precision@5: 0.73 → 0.89 (+16%)
```

**最终效果:**
```
优化路径:
基线 (0.68)
→ 语义分块 (0.79, +11%)
→ 混合检索 (0.87, +8%)
→ Query扩展 (0.92, +5%)
→ Rerank (精确率+16%)

总提升: Recall@5 从 68% → 92% (+24个百分点)
```

**成本分析:**
```
优化成本:
- 语义分块: 0 (只是代码改动)
- 混合检索: +100ms延迟, $0成本
- Query扩展: +$0.002/次 (LLM调用)
- Rerank: +200ms延迟, $0成本

投入产出比: 极高
```

**面试话术:**
> "召回率低我先建立评估数据集量化问题,然后逐项优化:语义分块+11%,混合检索+8%,Query扩展+5%,Rerank保证精确率。最终Recall@5从68%提升到92%,代价只是+300ms延迟和每次$0.002的Query扩展成本。"

</details>

---

## 二、AI Agent项目

### Q3: "介绍一下你做过的AI Agent项目"

<details>
<summary>💡 STAR回答模板</summary>

**S (Situation):**
> "我在xx公司开发了一个**客服Agent**,自动处理用户咨询、订单查询、退换货等问题。原来完全靠人工,客服团队10人,日均处理500个工单,响应慢、成本高。"

**T (Task):**
> "目标是:
> - 自动化率>70% (Agent独立解决)
> - 准确率>90%
> - 平均响应时间<10秒
> - 降低人力成本50%"

**A (Action):**

**1. Agent架构设计**
```
用户输入 → 意图识别 → 工具路由 → 工具执行 → 结果整合 → 回复用户
               ↓
         [ReAct循环]
   Thought → Action → Observation → 继续或结束
```

**2. 工具设计**
```python
tools = [
    # 工具1: 订单查询
    {
        "name": "query_order",
        "description": "查询用户订单信息,需要订单号",
        "parameters": {
            "order_id": "string"
        },
        "function": query_order_from_db
    },

    # 工具2: 知识库检索
    {
        "name": "search_faq",
        "description": "搜索常见问题FAQ",
        "parameters": {
            "question": "string"
        },
        "function": search_rag_system
    },

    # 工具3: 退货流程
    {
        "name": "process_refund",
        "description": "处理退货申请,需要订单号和原因",
        "parameters": {
            "order_id": "string",
            "reason": "string"
        },
        "function": create_refund_ticket
    },

    # 工具4: 转人工
    {
        "name": "transfer_to_human",
        "description": "复杂问题转人工客服",
        "parameters": {},
        "function": create_human_ticket
    }
]
```

**3. ReAct实现**
```python
from langchain.agents import create_react_agent

agent = create_react_agent(
    llm=ChatOpenAI(model="gpt-4"),
    tools=tools,
    prompt=f"""
    你是智能客服Agent。

    可用工具:
    {tools_description}

    工作流程:
    1. 理解用户问题
    2. 选择合适的工具
    3. 根据工具结果继续思考或给出答案
    4. 如果3次调用未解决,转人工

    格式:
    Thought: 我需要...
    Action: tool_name
    Action Input: {{"param": "value"}}
    Observation: tool返回结果
    ... (重复)
    Final Answer: 最终答案
    """
)

# 执行
result = agent.run("我的订单123456什么时候发货?")
```

**4. 关键优化**

**(1) 意图识别提前**
```python
# 问题: 每次都从ReAct开始,浪费token

# 优化: 先快速分类
def classify_intent(query):
    prompt = f"""
    分类用户意图(只返回类别):
    1. order_query - 订单查询
    2. refund - 退换货
    3. faq - 常见问题
    4. other - 其他

    用户: {query}
    类别:
    """
    intent = llm_fast.generate(prompt, max_tokens=10)
    return intent.strip()

# 根据意图直接调工具
intent = classify_intent(query)
if intent == "order_query":
    order_id = extract_order_id(query)
    result = query_order(order_id)
    # 省去ReAct推理,快速返回

# 效果: 延迟 8s → 2s, 成本 -60%
```

**(2) 防止死循环**
```python
class SafeAgent:
    def __init__(self, max_iterations=5):
        self.max_iterations = max_iterations

    def run(self, query):
        iteration = 0
        while iteration < self.max_iterations:
            thought = self.think(query)
            action = self.act(thought)
            observation = self.execute(action)

            # 检查是否完成
            if self.is_done(observation):
                return observation

            iteration += 1

        # 超过最大迭代,转人工
        return self.transfer_to_human(query)
```

**(3) 工具调用失败处理**
```python
def execute_tool_with_retry(tool, params, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = tool.function(**params)
            return {"success": True, "data": result}

        except DatabaseTimeout:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
                continue
            return {"success": False, "error": "数据库超时"}

        except InvalidParameter as e:
            # 参数错误不重试,让LLM修正
            return {
                "success": False,
                "error": f"参数错误: {str(e)}",
                "suggestion": "请检查并修正参数"
            }
```

**R (Result):**
> "项目上线3个月后:
> - 自动化率达到**78%** (超过目标70%)
> - 准确率**92%** (目标90%)
> - 平均响应时间**3.5秒** (目标<10秒)
> - 人力成本降低**65%** (5个客服缩减到2个)
> - 用户满意度**4.2/5** → **4.6/5**
>
> 关键成果:
> - 日均自动处理**390个**工单(总500个)
> - 人工客服只处理**110个**复杂问题
> - 夜间无人值守,24小时服务"

**面试追问应对:**

**Q: "Agent出错怎么办?"**
> "3层防护:
> 1. **意图识别层**: 提前分类,简单问题直接返回,不走Agent
> 2. **迭代限制层**: 最多5次工具调用,超过转人工
> 3. **异常捕获层**: 工具调用失败重试3次,失败则转人工
>
> 实际上线后,Agent失败率<3%,都能优雅降级到人工。"

**Q: "如何评估Agent质量?"**
> "4个维度:
> 1. **自动化率**: 成功独立解决的比例 (78%)
> 2. **准确率**: 人工抽查100条,答案正确的比例 (92%)
> 3. **用户满意度**: 对话结束后评分 (4.6/5)
> 4. **工具调用效率**: 平均调用次数 (1.8次,目标<3)
>
> 每周生成评估报告,发现问题及时调整Prompt。"

</details>

---

## 六、项目回答技巧

### 回答框架: STAR法则

**S (Situation) - 项目背景 (20秒)**
- 公司/团队规模
- 业务场景
- 遇到的问题

**T (Task) - 任务目标 (20秒)**
- 具体指标(量化)
- 技术要求
- 时间限制

**A (Action) - 具体行动 (60秒) ⭐核心**
- 技术选型 + 理由
- 架构设计
- 关键优化点
- 遇到的坑 + 解决方案

**R (Result) - 最终结果 (20秒)**
- 量化数据(对比)
- 业务价值
- 技术亮点

### 通用话术模板

**项目介绍:**
> "我在xx公司负责**[项目名]**,主要解决**[业务痛点]**。技术栈选用**[核心技术]**,实现了**[核心功能]**。最终**[关键指标]**从**[优化前]**提升到**[优化后]**,**[业务价值]**。"

**技术选型:**
> "我们对比了**[方案A]**和**[方案B]**,最终选择**[方案B]**,主要因为**[核心优势]**。虽然**[方案A]**在**[某方面]**更好,但考虑到**[实际约束]**,**[方案B]**更适合。"

**难点突破:**
> "最大的难点是**[具体问题]**。表现是**[现象]**,分析发现原因是**[根因]**。我们尝试了**[方案1]**,但**[问题]**。最终用**[最终方案]**解决,效果是**[数据对比]**。"

**如果重新设计:**
> "如果重新设计,我会改进**3点**:
> 1. **[技术点1]**: 当前**[现状]**,改进后**[预期]**
> 2. **[技术点2]**: ...(同上)
> 3. **[技术点3]**: ..."

---

## 📝 速记卡片

| 项目类型 | 核心考点 | 回答重点 |
|---------|---------|----------|
| **RAG系统** | 召回率/准确率 | 混合检索+Rerank+语义分块 |
| **AI Agent** | 自动化率/鲁棒性 | ReAct+工具设计+失败处理 |
| **成本优化** | 成本降低比例 | 语义缓存+模型路由+Prompt压缩 |

### 面试万能公式

```
项目 = 业务价值 + 技术亮点 + 量化数据

业务价值: 解决了什么问题,带来什么收益
技术亮点: 用了什么技术,为什么这么选
量化数据: 从x提升到y,提升了z%
```

---

**上一模块:** [RAG系统](../03-rag-system/)
**下一模块:** [Transformer架构](../05-transformer-architecture/)

---

[返回目录 →](../../README.md)
