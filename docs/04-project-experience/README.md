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

## 五、成本优化项目

### Q4: "你的项目如何降低成本的?具体优化了什么?"

<details>
<summary>💡 STAR回答模板</summary>

**S (Situation):**
> "我们的AI客服系统每月OpenAI API成本高达$8000,主要是GPT-4调用。老板要求在不降低用户体验的前提下,成本降低50%。"

**T (Task):**
> "目标:
> - 月成本从$8000降到$4000 (50%)
> - 用户满意度不低于当前4.2/5
> - 响应速度不超过3秒"

**A (Action):**

### 优化路径1: Token使用优化 (-35%成本)

**1. 上下文压缩**
```python
# Before: 直接把检索到的5个文档全传给LLM
docs = retriever.search(query, k=5)
context = "\n\n".join([doc.content for doc in docs])
# 平均输入: 3500 tokens

prompt = f"""
基于以下文档回答问题:

{context}  # ← 很多无关内容

问题: {query}
"""

# After: LLMLingua压缩上下文
from llmlingua import PromptCompressor

compressor = PromptCompressor()

compressed = compressor.compress_prompt(
    context,
    instruction="保留回答问题所需的关键信息",
    target_token=1000,  # 目标压缩到1000 tokens
    condition_compare=True,
    reorder_context="sort"  # 相关性排序
)

# 压缩后平均: 950 tokens
# Token减少: (3500-950)/3500 = 73%
# 成本节省: 输入token成本 -73%
```

**效果数据:**
```
压缩前: 平均3500 input tokens
压缩后: 平均950 input tokens
准确率: 89% → 87% (下降2%,可接受)
成本节省: $2800/月 (-35%)
```

**2. 会话历史管理**
```python
class ConversationManager:
    def __init__(self, max_history=3):
        self.history = []
        self.summary = ""

    def add_turn(self, user_msg, assistant_msg):
        self.history.append({
            "user": user_msg,
            "assistant": assistant_msg
        })

        # 超过3轮,摘要最早的一轮
        if len(self.history) > 3:
            old_turn = self.history.pop(0)

            # 用GPT-3.5-turbo摘要(便宜)
            turn_summary = gpt35_turbo.summarize(
                f"用户: {old_turn['user']}\n助手: {old_turn['assistant']}"
            )

            self.summary += turn_summary + "\n"

    def get_context(self):
        # 上下文 = 历史摘要 + 最近3轮完整对话
        context = []

        if self.summary:
            context.append(f"历史对话摘要:\n{self.summary}")

        for turn in self.history:
            context.append(f"用户: {turn['user']}")
            context.append(f"助手: {turn['assistant']}")

        return "\n".join(context)

# 效果
# Before: 10轮对话 = 10轮完整历史(约5000 tokens)
# After: 10轮对话 = 摘要(200 tokens) + 最近3轮(1500 tokens)
# Token节省: 70%
```

### 优化路径2: 模型路由 (-25%成本)

**原理: 简单问题用便宜模型,复杂问题用贵模型**

```python
class ModelRouter:
    def __init__(self):
        # 分类器: 判断问题复杂度
        self.classifier = fasttext.load_model("complexity_classifier.bin")

        self.cheap_model = "gpt-3.5-turbo"  # $0.5/1M tokens
        self.expensive_model = "gpt-4"       # $30/1M tokens

    def route(self, query):
        # 分类: simple / medium / complex
        complexity = self.classifier.predict(query)[0][0]

        if complexity == "simple":
            # 60%的问题是简单问题
            # 例: "营业时间?", "怎么退货?"
            return self.cheap_model

        elif complexity == "medium":
            # 30%中等,先试GPT-3.5
            response = gpt35.generate(query)

            # 如果GPT-3.5不确定,升级到GPT-4
            if self.is_uncertain(response):
                return self.expensive_model
            else:
                return self.cheap_model

        else:  # complex
            # 10%复杂问题,直接GPT-4
            # 例: "对比3款产品的性价比"
            return self.expensive_model

    def is_uncertain(self, response):
        # 检测不确定的标志
        uncertain_phrases = [
            "我不确定",
            "可能是",
            "这取决于",
            "抱歉,我无法"
        ]
        return any(phrase in response for phrase in uncertain_phrases)

# 使用
router = ModelRouter()
model = router.route(user_query)
response = llm_pool[model].generate(query)

# 效果数据:
# - 60%请求用GPT-3.5 (省$0.5 vs $30)
# - 30%请求先GPT-3.5,20%升级到GPT-4
# - 10%请求直接GPT-4
#
# 平均成本 = 0.6*$0.5 + 0.3*(0.8*$0.5 + 0.2*$30) + 0.1*$30
#          = $0.3 + $1.92 + $3 = $5.22
# vs 全用GPT-4: $30
# 成本降低: 83%
#
# 考虑质量损失,实际路由策略调整后:
# 成本降低: 25%
```

### 优化路径3: 语义缓存 (-30%成本)

**原理: 相似问题直接返回缓存,不调API**

```python
from langchain.cache import RedisSemanticCache
from langchain.embeddings import OpenAIEmbeddings

class SemanticCache:
    def __init__(self):
        self.redis_client = Redis(host='localhost', port=6379)
        self.embedding_model = OpenAIEmbeddings()
        self.similarity_threshold = 0.85

    def get(self, query):
        """检查缓存"""
        # 1. 计算query的embedding
        query_embedding = self.embedding_model.embed_query(query)

        # 2. 从Redis向量搜索相似query
        similar = self.redis_client.search(
            query_vector=query_embedding,
            k=1,
            similarity_threshold=self.similarity_threshold
        )

        if similar:
            # 命中缓存
            cached_query, cached_response = similar[0]
            print(f"缓存命中: '{query}' ≈ '{cached_query}'")
            return cached_response

        return None

    def set(self, query, response, ttl=86400):
        """存入缓存"""
        query_embedding = self.embedding_model.embed_query(query)

        self.redis_client.set(
            key=query,
            value=response,
            embedding=query_embedding,
            ttl=ttl  # 24小时过期
        )

# 使用
cache = SemanticCache()

def answer_question(query):
    # 先查缓存
    cached = cache.get(query)
    if cached:
        return cached

    # 缓存未命中,调用LLM
    response = llm.generate(query)

    # 存入缓存
    cache.set(query, response)

    return response

# 示例缓存命中:
# Query1: "怎么退货?"
# Query2: "如何申请退款?" ← 相似度0.91,命中缓存
# Query3: "退货流程是什么?" ← 相似度0.88,命中缓存

# 效果数据:
# 缓存命中率: 35%
# 成本节省: 35% API调用
# 延迟降低: 2.5s → 0.1s (缓存响应)
```

**缓存策略优化:**
```python
# 问题: 不是所有问题都适合缓存
# 例: "今天天气怎么样?" - 答案每天变化

class SmartCache:
    def should_cache(self, query, response):
        """判断是否应该缓存"""

        # 1. 静态知识问题 → 缓存
        static_patterns = [
            r".*是什么",
            r".*的定义",
            r".*怎么.*",  # 流程类
        ]

        if any(re.match(p, query) for p in static_patterns):
            return True, 86400*7  # 缓存7天

        # 2. 实时数据问题 → 不缓存
        dynamic_patterns = [
            r".*今天.*",
            r".*现在.*",
            r".*最新.*",
        ]

        if any(re.match(p, query) for p in dynamic_patterns):
            return False, 0

        # 3. 订单查询 → 短时缓存
        if "订单" in query and re.search(r"\d{6,}", query):
            return True, 300  # 缓存5分钟

        # 4. 默认: 缓存24小时
        return True, 86400
```

**R (Result):**
> "经过3个月优化:
> - 月成本从$8000降到**$3600** (**-55%**,超过目标)
> - 用户满意度**4.2/5 → 4.4/5** (提升!)
> - P95响应时间**2.8s → 1.2s** (更快!)
>
> 成本拆解:
> - Token压缩: -$2800 (-35%)
> - 模型路由: -$2000 (-25%)
> - 语义缓存: -$2400 (-30%)
> - 总节省: -$4400 (实际有重叠,最终-55%)
>
> 关键insight:
> 1. 35%缓存命中率带来最大收益
> 2. 60%简单问题用GPT-3.5完全够用
> 3. 上下文压缩73%,准确率只降2%"

**面试追问应对:**

**Q: "语义缓存会不会返回过时信息?"**
> "我们做了3层防护:
> 1. **TTL分级**: 静态知识7天,实时数据不缓存,订单5分钟
> 2. **缓存失效机制**: 产品价格变动时,主动清除相关缓存
> 3. **用户反馈**: 每个缓存答案底部显示'生成于X分钟前',用户可点击'重新生成'
>
> 实测过时率<1%,用户投诉0。"

**Q: "模型路由的分类器怎么训练的?"**
> "我们用FastText训练:
> 1. **数据标注**: 人工标注1000条历史问题为simple/medium/complex
> 2. **特征**: 问题长度、实体数量、是否有比较词('对比','哪个更')
> 3. **训练**: FastText 3分钟训练完,准确率89%
> 4. **持续学习**: 每周用新数据增量训练
>
> 如果分类错误,GPT-3.5会有'不确定'标志,自动升级到GPT-4,兜底策略保证质量。"

**Q: "Token压缩会不会丢失关键信息?"**
> "我们做了评估:
> 1. **AB测试**: 200条问题,人工评分压缩前后答案质量
> 2. **结果**: 压缩到1000 token时,质量从4.5/5降到4.4/5,损失2%
> 3. **阈值选择**: 我们用target_token=1000作为最优平衡点
>
> LLMLingua的reorder_context='sort'会把最相关的内容放前面,LLM优先看到,所以质量损失小。"

</details>

---

## 五、数据与冷启动项目

### Q5: "新产品上线,没有数据怎么办?如何冷启动?"

<details>
<summary>💡 STAR回答模板</summary>

**S (Situation):**
> "我们要上线一个新的AI写作助手,但完全没有用户数据,也没有用户反馈来优化模型。产品经理要求1个月内上线MVP,并在3个月内达到用户留存率30%。"

**T (Task):**
> "挑战:
> - 没有用户历史数据
> - 没有标注数据训练个性化模型
> - 不知道用户真实需求
> - 预算有限,无法大规模标注"

**A (Action):**

### 策略1: 利用开源数据 + 合成数据

**开源数据作为基础**
```python
# 1. 收集开源写作数据集
datasets = [
    "tatsu-lab/alpaca",           # 52K指令数据
    "Anthropic/hh-rlhf",          # 人类偏好数据
    "OpenAssistant/oasst1",       # 多轮对话
    "BELLE-2M-CN",                # 中文指令200万
]

# 2. 过滤与写作相关的数据
from datasets import load_dataset

all_data = []
for dataset_name in datasets:
    ds = load_dataset(dataset_name)

    # 过滤: 只保留写作相关
    writing_keywords = ["写", "撰写", "文章", "博客", "邮件", "报告"]

    filtered = ds.filter(
        lambda x: any(kw in x["instruction"] for kw in writing_keywords)
    )

    all_data.extend(filtered)

# 得到约8万条写作相关数据
print(f"收集到 {len(all_data)} 条写作数据")
```

**合成数据补充**
```python
# 用GPT-4生成领域特定的训练数据
def generate_synthetic_data(seed_examples, num_samples=1000):
    """
    基于种子数据,让GPT-4生成相似的训练样本
    """
    synthetic_data = []

    for _ in range(num_samples):
        # 随机选3个种子示例
        examples = random.sample(seed_examples, 3)

        prompt = f"""
        参考以下写作任务示例:

        示例1:
        指令: {examples[0]["instruction"]}
        输出: {examples[0]["output"]}

        示例2:
        指令: {examples[1]["instruction"]}
        输出: {examples[1]["output"]}

        示例3:
        指令: {examples[2]["instruction"]}
        输出: {examples[2]["output"]}

        请生成1个类似的写作任务和对应的高质量输出。
        要求:
        1. 指令多样化(商业邮件、技术文档、营销文案等)
        2. 输出长度200-500字
        3. 语言流畅专业

        JSON格式输出。
        """

        response = gpt4.generate(prompt, response_format="json")
        synthetic_data.append(response)

    return synthetic_data

# 生成5000条合成数据
synthetic = generate_synthetic_data(all_data[:100], num_samples=5000)

# 总训练数据 = 8万开源 + 5千合成 = 8.5万
```

**效果:**
- 成本: $150 (GPT-4生成5K样本)
- 时间: 2天
- 质量: 人工抽查100条,合格率92%

### 策略2: 引导式数据收集

**产品设计嵌入数据收集**
```python
# 方法1: 首次使用引导
def onboarding_flow(user):
    """新用户注册时收集偏好"""

    # Step 1: 写作场景偏好
    scenes = show_options([
        "商业邮件",
        "技术文档",
        "营销文案",
        "学术论文",
        "社交媒体",
        "创意故事"
    ])
    user.preferences["scenes"] = scenes

    # Step 2: 风格偏好
    styles = show_options([
        "正式专业",
        "轻松幽默",
        "简洁直接",
        "详细严谨"
    ])
    user.preferences["styles"] = styles

    # Step 3: 示例任务
    example_task = "请帮我写一封感谢邮件给合作伙伴"
    ai_draft = generate_draft(example_task)

    # 让用户评分和编辑
    rating = user.rate(ai_draft, scale=5)
    edited = user.edit(ai_draft)

    # 收集首次反馈数据
    save_feedback({
        "task": example_task,
        "draft": ai_draft,
        "rating": rating,
        "edited_version": edited,
        "user_id": user.id
    })

    return user.preferences

# 方法2: 轻量级反馈机制
def show_output_with_feedback(output):
    """每次输出都收集反馈"""

    display(output)

    # 一键反馈(不打断流程)
    feedback_ui = """
    这个答案有用吗? 👍 👎
    [复制] [重新生成] [编辑优化]
    """

    user_action = wait_for_action()

    if user_action == "thumbs_up":
        log_positive_feedback(output)
    elif user_action == "thumbs_down":
        # 追问原因
        reason = ask_reason([
            "不够专业",
            "太啰嗦",
            "偏离主题",
            "其他"
        ])
        log_negative_feedback(output, reason)
    elif user_action == "edit":
        edited = user_edit(output)
        # 收集对比数据: AI版 vs 用户优化版
        log_edit_data(original=output, edited=edited)
```

**数据飞轮启动**
```
Week 1: 100个种子用户
   ↓ 每人平均使用5次
   ↓ 收集500条反馈

Week 2: 用500条反馈微调模型v1.1
   ↓ 质量提升,吸引300新用户
   ↓ 收集2000条反馈

Week 3: 用2500条反馈微调模型v1.2
   ↓ 质量再提升,吸引1000新用户
   ↓ 收集8000条反馈

Week 4: 数据飞轮加速旋转
```

### 策略3: 主动学习优化标注

**问题: 8.5万数据全部人工标注成本太高**

**解决: 主动学习,只标注最有价值的数据**

```python
class ActiveLearningAnnotator:
    def __init__(self, unlabeled_data, budget=1000):
        self.unlabeled_pool = unlabeled_data
        self.labeled_data = []
        self.budget = budget
        self.model = None

    def run(self):
        # Step 1: 随机标注100条作为种子
        seed_samples = random.sample(self.unlabeled_pool, 100)
        self.labeled_data = self.manual_annotate(seed_samples)
        self.unlabeled_pool = [x for x in self.unlabeled_pool if x not in seed_samples]

        # Step 2: 训练初始模型
        self.model = train_model(self.labeled_data)

        # Step 3: 主动学习循环
        while len(self.labeled_data) < self.budget:
            # 找出模型最不确定的样本
            uncertain_samples = self.select_uncertain_samples(k=50)

            # 人工标注这50条
            newly_labeled = self.manual_annotate(uncertain_samples)

            # 加入训练集
            self.labeled_data.extend(newly_labeled)

            # 重新训练
            self.model = train_model(self.labeled_data)

            print(f"已标注: {len(self.labeled_data)}/{self.budget}")

        return self.model

    def select_uncertain_samples(self, k=50):
        """选择最不确定的样本"""
        uncertainties = []

        for sample in self.unlabeled_pool[:5000]:  # 从pool中抽5000条评估
            # 模型预测
            probs = self.model.predict_proba(sample["instruction"])

            # 计算不确定性(熵)
            entropy = -sum(p * np.log(p) for p in probs if p > 0)

            uncertainties.append((sample, entropy))

        # 按不确定性排序,取top-k
        uncertainties.sort(key=lambda x: x[1], reverse=True)

        return [x[0] for x in uncertainties[:k]]

    def manual_annotate(self, samples):
        """人工标注"""
        labeled = []
        for sample in samples:
            # 调用标注平台API
            label = annotation_platform.annotate(
                task=sample["instruction"],
                annotator_id="expert_001"
            )

            sample["label"] = label
            labeled.append(sample)

        return labeled

# 使用主动学习
al = ActiveLearningAnnotator(unlabeled_data=all_data, budget=1000)
optimized_model = al.run()

# 效果对比:
# 随机标注1000条: 准确率75%
# 主动学习标注1000条: 准确率82% (+7%)
# 相当于随机标注1500条的效果,节省33%标注成本
```

### 策略4: 用户分群 + AB测试

**解决冷启动时不知道用户需求的问题**

```python
class ColdStartUserSegmentation:
    def __init__(self):
        self.segments = {
            "business": {
                "keywords": ["商业", "邮件", "报告", "合同"],
                "model_config": {"temperature": 0.3, "style": "formal"}
            },
            "creative": {
                "keywords": ["故事", "小说", "剧本", "创意"],
                "model_config": {"temperature": 0.9, "style": "creative"}
            },
            "tech": {
                "keywords": ["技术", "文档", "API", "代码"],
                "model_config": {"temperature": 0.5, "style": "technical"}
            }
        }

    def assign_segment(self, user_first_query):
        """根据首次查询分群"""
        query = user_first_query.lower()

        for segment_name, config in self.segments.items():
            if any(kw in query for kw in config["keywords"]):
                return segment_name, config["model_config"]

        # 默认分配到"通用"群
        return "general", {"temperature": 0.7, "style": "balanced"}

    def ab_test_variants(self, segment):
        """每个分群内AB测试不同模型配置"""
        variants = {
            "A": {"model": "gpt-3.5-turbo", "prompt_template": "template_v1"},
            "B": {"model": "gpt-4", "prompt_template": "template_v1"},
            "C": {"model": "gpt-3.5-turbo", "prompt_template": "template_v2"}
        }

        # 随机分配
        variant = random.choice(["A", "B", "C"])
        return variants[variant]

# 使用
segmenter = ColdStartUserSegmentation()

def handle_new_user(user):
    # 首次查询
    first_query = user.get_first_query()

    # 分群
    segment, config = segmenter.assign_segment(first_query)
    user.segment = segment

    # AB测试
    variant = segmenter.ab_test_variants(segment)
    user.variant = variant

    # 用对应配置生成
    output = generate_with_config(
        query=first_query,
        **config,
        **variant
    )

    # 记录实验数据
    log_experiment({
        "user_id": user.id,
        "segment": segment,
        "variant": variant,
        "satisfaction": user.rate(output)
    })

# 2周后分析AB测试结果
# Business分群: Variant B (GPT-4 + template_v1) 满意度最高 4.5/5
# Creative分群: Variant C (GPT-3.5 + template_v2) 性价比最高
# Tech分群: Variant A 效果相当,选最便宜的
```

**R (Result):**
> "1个月MVP上线,3个月数据:
> - 累计用户: **3500人**
> - 日活留存: **35%** (超过目标30%)
> - 收集数据: **18000条**用户交互
> - 模型迭代: **v1.0 → v1.5** (5次微调)
> - 用户满意度: **3.2/5 → 4.1/5**
>
> 成本控制:
> - 开源数据: **$0**
> - 合成数据: **$150** (GPT-4)
> - 主动学习标注: **$3000** (1000条 * $3/条)
> - 总成本: **$3150** (远低于全量标注$25万)
>
> 关键成功因素:
> 1. 产品设计嵌入数据收集,用户无感提供反馈
> 2. 主动学习节省67%标注成本
> 3. AB测试快速找到每个分群的最优配置
> 4. 数据飞轮2周开始加速,用户增长带来数据增长"

**面试追问应对:**

**Q: "合成数据质量怎么保证?"**
> "三层质量控制:
> 1. **Prompt工程**: 给GPT-4提供3个高质量示例作为参考,限制输出格式
> 2. **自动过滤**: 用规则过滤明显低质量数据(长度<50字,重复率>30%)
> 3. **人工抽检**: 每生成500条抽检50条,合格率<90%就调整Prompt
>
> 最终5000条合成数据,人工抽查100条,合格率92%,与开源数据质量相当。"

**Q: "主动学习如何选择'最不确定'的样本?"**
> "我们用熵值(Entropy)衡量不确定性:
> ```python
> # 模型预测概率分布
> probs = [0.4, 0.35, 0.25]  # 3个类别
>
> # 计算熵
> entropy = -sum(p * log(p) for p in probs)
> # = 1.57 (高熵 = 不确定)
>
> # 对比:确定的预测
> probs2 = [0.9, 0.05, 0.05]
> entropy2 = 0.47 (低熵 = 确定)
> ```
>
> 选熵值最高的样本标注,因为这些样本最能帮助模型区分边界,性价比最高。实测主动学习1000条,效果等于随机1500条。"

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
| **成本优化** | 成本降低比例 | 语义缓存+模型路由+Token压缩 |
| **冷启动** | 数据收集/留存率 | 开源数据+合成数据+主动学习 |

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

---

## 七、大厂项目架构设计（2026新增）

### Q6: 如果让你设计一个企业级AI客服系统，你会怎么设计？

<details>
<summary>💡 答案要点（STAR框架）</summary>

**S（背景）：** 1000万用户，日活100万，需要7×24小时智能客服

**T（任务）：** 设计一个能处理咨询、售后、投诉等多场景的AI客服系统

**A（行动）——四层架构设计：**

```
┌─────────────────────────────────────────────────────┐
│  接入层：多渠道统一接入                              │
│  微信/APP/网页/电话 → 统一消息格式                  │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  路由层：意图识别 + 路由分发                       │
│  LLM 判断意图 → 转人工/知识库/工单系统             │
└──────────────────┬─────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  能力层：多Agent协作                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │ 知识库Agent│ │ 订单Agent │ │ 投诉Agent │         │
│  └──────────┘ └──────────┘ └──────────┘         │
└──────────────────┬─────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  数据层：会话记忆 + 知识库 + 工单系统               │
└──────────────────────────────────────────────────┘
```

**关键设计点：**

```python
# 意图识别 + 路由
def route(query, session_history):
    intent = llm.judge(f"""
    判断用户意图：
    1=咨询 2=下单 3=售后 4=投诉 5=转人工
    问题：{query}
    历史：{session_history[-3:]}
    """)
    
    if intent == 5 or contains_sensitive词(query):
        return "human_agent"  # 转人工
    elif intent == 1:
        return "knowledge_agent"
    elif intent == 2:
        return "order_agent"
    # ...

# 多轮对话记忆
class ConversationMemory:
    def __init__(self, max_turns=10):
        self.history = []
        self.max_turns = max_turns
    
    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_turns * 2:
            # 压缩：保留关键信息
            self.history = self.summarize_and_compress()
```

**R（结果）：** 客服响应时间从30s→2s，问题解决率85%，人工客服工作量减少60%

</details>

### Q7: 你如何设计一个多模态RAG系统（图文检索）？

<details>
<summary>💡 答案要点</summary>

**多模态RAG架构：**

```
用户上传图片 + 文字问题
         ↓
┌──────────────────────────────────────────┐
│  多模态 Encoder：                        │
│  - 图片 → CLIP 视觉编码 → 向量          │
│  - 文字 → CLIP 文本编码 → 向量          │
│  - 图+文 → 融合向量                     │
└──────────────────┬─────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│  跨模态检索：                            │
│  用户图 vs 文档图：相似度匹配            │
│  用户问题 vs 文档图：图文跨模态匹配      │
└──────────────────┬─────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│  多模态生成：                            │
│  LLaVA 等 VLM 基于图片 + 检索结果生成   │
└──────────────────────────────────────────┘
```

**关键实现代码：**

```python
from sentence_transformers import CLIPModel
import torch

class MultimodalRAG:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    
    def encode_image(self, image):
        with torch.no_grad():
            image_features = self.model.get_image_features(image)
        return image_features.numpy()
    
    def encode_text(self, text):
        with torch.no_grad():
            text_features = self.model.get_text_features(text)
        return text_features.numpy()
    
    def crossmodal_search(self, query_image, query_text, doc_images, top_k=5):
        # 编码
        img_emb = self.encode_image(query_image)
        text_emb = self.encode_text(query_text)
        
        # 融合：图片和文字各50%
        fused_query = 0.5 * img_emb + 0.5 * text_emb
        
        # 在文档图片中检索
        similarities = []
        for doc_img in doc_images:
            doc_emb = self.encode_image(doc_img)
            sim = cosine_similarity(fused_query, doc_emb)
            similarities.append(sim)
        
        return sorted(zip(doc_images, similarities), key=lambda x: -x[1])[:top_k]
```

**面试话术：**
> "多模态RAG的核心是跨模态对齐。我用CLIP做图片和文字的联合编码空间，用户的图片和文字问题都映射到同一个向量空间，直接做相似度匹配。文档端也用CLIP处理产品图片，建立图片向量库。检索时，用户的图+文query和文档图片做跨模态检索，精准找到相关图片。生成阶段用LLaVA读图回答。实测图文混合查询的准确率比纯文字检索提升了35%。"

</details>

### Q8: 如何设计一个企业级AI Agent平台（类似Coze/Dify）？

<details>
<summary>💡 答案要点</summary>

**平台核心架构：**

```
┌─────────────────────────────────────────────────────────┐
│  用户层：可视化编排 / API 调用                          │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  编排层：工作流设计器                                  │
│  - 节点：LLM节点 / 知识库节点 / API节点 / 条件节点    │
│  - 边：数据流 / 条件流                               │
│  - 输出：DSL（领域特定语言）配置文件                  │
└──────────────────────┬───────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  运行时层：工作流引擎                                  │
│  - 执行节点 → 收集输出 → 路由到下一节点             │
│  - 支持条件分支 / 循环 / 并行                        │
└──────────────────────┬───────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  能力层：工具生态                                     │
│  - 内置工具：知识库 / SQL / API / Webhook            │
│  - MCP 集成：扩展工具生态                            │
└──────────────────────────────────────────────────────┘
```

**DSL 工作流配置示例：**

```yaml
workflow:
  name: "智能客服"
  version: "1.0"
  
  nodes:
    - id: "intent"
      type: "llm"
      model: "qwen2.5-14b"
      prompt: "判断用户意图：咨询/下单/售后/投诉"
      output: "user_intent"
    
    - id: "route"
      type: "condition"
      branches:
        - condition: "{{user_intent}} == '咨询'"
          next: "knowledge_base"
        - condition: "{{user_intent}} == '下单'"
          next: "order_agent"
        - condition: "{{user_intent}} == '售后'"
          next: "after_sales"
        default: "human_agent"
    
    - id: "knowledge_base"
      type: "rag"
      knowledge_id: "product_knowledge"
      top_k: 5
      output: "rag_result"
    
    - id: "after_sales"
      type: "api"
      url: "https://api.company.com/order/track"
      params: "{{order_id}}"
      output: "tracking_info"

  edges:
    - from: "intent"
      to: "route"
    - from: "route"
      to: "knowledge_base"
    # ...

  output:
    format: "markdown"
    stream: true
```

**面试话术：**
> "企业级Agent平台的核心是'编排即服务'。我用DSL描述工作流，节点类型包括LLM、知识库、API、HTTP、代码执行等。工作流引擎解析DSL，按拓扑顺序执行节点，支持条件分支、并行、循环。编排层提供可视化画布，用户拖拖拽拽就能搭工作流，生成的DSL存到数据库，运行时引擎执行。平台还接入了MCP协议，工具生态可以无限扩展。"

</details>

