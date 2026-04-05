# 🚀 RAG 高级优化面试题（GraphRAG / HyDE / Semantic Chunking）

> **难度：** ⭐⭐⭐⭐
> **更新：** 2026-04-03
> **考点：** GraphRAG、HyDE、Semantic Chunking、Context Cliff、混合检索、Rerank、LLMLingua

## 📋 目录

1. [RAG 优化进阶概念](#一rag-优化进阶概念)
2. [语义分块与文档处理](#二语义分块与文档处理)
3. [GraphRAG 知识图谱增强](#三graphrag-知识图谱增强)
4. [检索结果重排序与压缩](#四检索结果重排序与压缩)
5. [RAG 评估与调优](#五rag-评估与调优)

## 一、RAG 优化进阶概念

### Q1: 什么是 RAG-Fusion？它解决了传统 RAG 的什么问题？

<details>
<summary>💡 答案要点</summary>

**传统 RAG 的问题：**

1. **语义孤岛**：用户查询和文档的语义可能存在偏差
2. **召回单一**：仅靠向量相似度，可能遗漏相关内容
3. **缺乏全局理解**：无法回答需要多文档汇总的问题

**RAG-Fusion 解决方案：**

```
用户查询: "2026年Q1季度营收增长原因"

Step 1: Query Rewriting（查询改写）
→ 生成多个相关查询：
  - "2026年Q1营收数据"
  - "营收增长驱动因素"
  - "季度财务分析"

Step 2: Multi-Query Retrieval（多查询检索）
→ 对每个查询独立检索 Top-K 文档

Step 3: Reciprocal Rank Fusion (RRF)
→ RRF = Σ(1/(k+rank_i))，融合多查询结果
→ 最终排序：综合多查询视角的结果

Step 4: 输出
→ 生成综合多文档的答案
```

**RRF 公式：**
```python
def reciprocal_rank_fusion(results_list, k=60):
    """k is a constant, typically 60"""
    fused_scores = {}
    for results in results_list:
        for rank, doc in enumerate(results):
            doc_id = doc['id']
            fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(fused_scores.items(), key=lambda x: -x[1])
```

**面试话术：**
> "RAG-Fusion 解决了传统 RAG 的语义孤岛问题。核心思路是：用户问一个问题，我生成 N 个相关查询，每个查询独立检索，再通过 RRF 算法融合排序。这样能召回更多样的文档，特别是需要多文档汇总的问题。实现上用 Reciprocal Rank Fusion，简单但有效。"

</details>

### Q2: 什么是 HyDE（Hypothetical Document Embeddings）？它的原理是什么？

<details>
<summary>💡 答案要点</summary>

**核心思想：让 LLM 先写"假答案"，再用假答案去检索**

**为什么需要 HyDE？**
- 用户查询是短文本，语义信息有限
- 直接检索可能无法准确匹配相关文档
- HyDE 用 LLM 生成"假设性答案"，答案更接近文档风格

**HyDE 工作流程：**
```
用户查询: "Transformer为何能并行计算？"

Step 1: LLM 生成假设性答案（不真实，但风格类似文档）
假设性答案: "Transformer并行计算的核心在于Self-Attention机制..."
         → 这个答案的embedding更接近真实技术文档

Step 2: 用假设性答案的向量去检索
检索: cosine_similarity(假设答案_emb, 文档_emb)

Step 3: 检索出真实文档
返回: ["Attention is all you need论文...", "BERT技术解读..."]

Step 4: 用真实文档 + 用户原始问题 → 最终生成答案
```

**代码实现：**
```python
def hyde_retrieve(query, vector_db, llm, k=5):
    # Step 1: LLM生成假设性答案
    hypothetical_doc = llm.generate(
        f"请用技术文档的风格回答以下问题，不需要真实：{query}"
    )
    
    # Step 2: 用假设答案检索
    query_emb = embed(hypothetical_doc)
    results = vector_db.search(query_emb, k=k)
    
    return results
```

**适用场景：**
- 查询与文档风格差异大（如口语问 vs 学术文档）
- 需要深层语义理解的问题
- 简单关键词匹配效果不好的场景

**面试话术：**
> "HyDE 的核心思想很巧妙：先用 LLM 生成一个'假答案'，这个假答案的风格更接近真实文档，用它去检索效果反而更好。因为用户的问题是短文本，直接检索容易语义漂移，而 LLM 生成的回答是长文本，embedding 更稳定。实测在学术问答场景，HyDE 能提升召回率 15-20%。"

</details>

### Q3: RAG 与 SFT（监督微调）如何选择？什么时候该用 RAG 而不是 SFT？

<details>
<summary>💡 答案要点</summary>

**选择决策框架：**

| 维度 | RAG | SFT |
|------|-----|-----|
| **知识时效性** | ✅ 高（可实时更新） | ❌ 低（需重新训练） |
| **知识容量** | ✅ 海量知识 | ❌ 受模型参数限制 |
| **推理成本** | ❌ 每次检索有延迟 | ✅ 推理更快 |
| **定制风格** | △ 受 prompt 控制 | ✅ 深度定制 |
| **幻觉问题** | ✅ 答案可溯源 | ❌ 幻觉难以避免 |
| **训练成本** | ✅ 低 | ❌ 高（需要数据） |

**选型决策树：**
```
知识是否频繁变化？
    ├── 是 → RAG（实时更新知识库）
    ↓ 否
知识是否超出模型参数容量？
    ├── 是 → RAG（知识库 > 7B参数容量）
    ↓ 否
需要深度定制回答风格/格式？
    ├── 是 → SFT（需要大量标注数据）
    ↓ 否
对答案准确性/可溯源性要求高？
    → RAG（答案可溯源到文档）
```

**混合方案（RAG + SFT）：**
```python
# 实际生产环境中，RAG + SFT 混合使用
class HybridRAGWithSFT:
    def __init__(self, vector_db, fine_tuned_model):
        self.vector_db = vector_db
        self.model = fine_tuned_model  # 微调过的模型
    
    def answer(self, query):
        # 1. RAG 检索相关文档
        docs = self.vector_db.search(query, k=5)
        
        # 2. 用微调模型生成（微调模型已学会特定风格）
        context = "\n".join([d['content'] for d in docs])
        answer = self.model.generate(
            prompt=f"基于以下上下文回答：{context}\n\n问题：{query}"
        )
        return answer

# SFT负责风格（如医疗报告格式）
# RAG负责知识实时性（如最新药品信息）
```

**面试话术：**
> "我的经验是：知识频繁变化选 RAG，需要特定风格选 SFT，数据量小先 RAG，效果不够再 SFT。实际项目里通常是 RAG + SFT 混合——RAG 保证知识实时性，SFT 微调模型输出风格。我在之前的短剧平台项目里就是混合方案：RAG 检索最新剧情热度，SFT 控制回复风格。"

</details>

## 二、语义分块与文档处理

### Q4: 什么是 Semantic Chunking？它和固定分块有什么区别？2026年有什么新发现？

<details>
<summary>💡 答案要点</summary>

**传统固定分块的问题：**
```python
# 固定分块（Fixed Chunking）
text = "这是一篇关于机器学习的文章..."
chunks = []
for i in range(0, len(text), 500):  # 每500字符一分
    chunks.append(text[i:i+500])
# 问题：可能在句子中间截断，语义不完整
```

**Semantic Chunking（语义分块）：**
```python
# 语义分块：用嵌入相似度判断何时"切"
def semantic_chunking(text, similarity_threshold=0.7):
    sentences = split_sentences(text)  # 先按句子分割
    chunks = [[sentences[0]]]
    
    for sent in sentences[1:]:
        # 比较当前句子与上一个chunk的相似度
        similarity = cosine_sim(embed(sent), embed(chunks[-1]))
        
        if similarity > similarity_threshold:
            chunks[-1].append(sent)  # 继续属于当前chunk
        else:
            chunks.append([sent])    # 开始新chunk
    
    return [" ".join(c) for c in chunks]
```

**2026年新发现——Context Cliff：**

| 分块策略 | 平均大小 | 问答准确率 | 问题 |
|----------|----------|-----------|------|
| 固定分块（500字符） | ~200 tokens | 72% | 可能截断语义 |
| 语义分块（自动） | ~43 tokens | 54% | **chunk 太小，上下文不足！** |
| 语义分块（优化后） | ~512 tokens | 81% | 最佳平衡点 |
| **Context Cliff** | >2,500 tokens | 质量骤降 | **关键发现！** |

**Context Cliff 现象（2026年1月发现）：**
```
Token数量增加
    ↑
100%│                      ┌─ 稳定区
    │                      │
 80%│  ┌───────────────────┘
    │  │
 60%│  │
    │  └───── Context Cliff（~2500 tokens）
 40%│        质量急剧下降
    │  
  0%└─────────────────────────────→
    0    1000   2500   4000   tokens
```

**面试话术：**
> "Semantic Chunking 的关键是'相似就合并，不相似就切开'，用句子级别的嵌入相似度驱动分块，比固定字符数更智能。但 2026 年的新发现是 Context Cliff——chunk 太大（>2500 tokens）反而质量下降，因为有效信息被稀释了。最佳实践是控制 chunk 在 500-1000 tokens，既保留足够上下文，又不超过 Context Cliff。"

</details>

### Q5: 如何解决 RAG 的"丢失中间信息"问题（Lost in the Middle）？

<details>
<summary>💡 答案要点</summary>

**Lost in the Middle 问题：**

```
Prompt结构：
[重要-开头] [不重要] [重要-中间!] [不重要] [重要-结尾]

LLM关注度：
★★★★★         ★☆☆☆☆    ★★★     ★☆☆☆☆    ★★★★★
  ↑                          ↑
  └────── 容易被LLM忽略 ──────┘

→ 中间部分的信息容易被LLM"忘记"
```

**解决方案：**

### 方案1：逆向序列化（Reverse Process）
```python
# 将重要信息放在开头或结尾（LLM更关注的位置）
def reverse_context_window(docs, max_tokens=3000):
    """把检索结果逆序排列，中间放不太重要的"""
    if len(docs) <= 3:
        return docs
    
    # 按相关性排序：最高放开头，最低放中间，次高放结尾
    sorted_docs = sorted(docs, key=lambda x: x['score'], reverse=True)
    
    # 构建上下文：最高 → 最低 → 次高
    context = [
        sorted_docs[0],      # 最高相关性放开头
        sorted_docs[-1],     # 最低放中间（最容易被忽略）
        sorted_docs[1]       # 次高放结尾
    ]
    return context
```

### 方案2：上下文压缩（Context Compression）
```python
# 使用 LLMLingua 等工具压缩上下文
from llmlingua import PromptCompressor

compressor = PromptCompressor()
compressed = compressor.compress(
    prompt=full_context,
    instruction="回答用户关于X的问题",
    target_token=2000  # 压缩到2000 tokens
)
# 保留关键信息，去除冗余
```

### 方案3：滑动窗口 + 重叠分块
```python
# 重叠分块确保关键信息不被截断
def sliding_window_chunk(text, chunk_size=500, overlap=100):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks
# 重叠100 tokens，防止关键信息被切断
```

### 方案4：Big Bird（稀疏注意力）
```python
# Big Bird 的三种注意力机制：
# 1. 全局注意力（开头/结尾token）
# 2. 随机注意力（随机采样一些token）
# 3. 滑动窗口注意力（局部上下文）
# → 确保中间信息被关注
```

**面试话术：**
> "Lost in the Middle 是 RAG 的经典问题——LLM 对上下文中间部分关注度最低。我的解法是：先把检索结果逆序排列（最高相关→最低→次高），让重要信息尽量靠前或靠后；其次用 LLMLingua 做上下文压缩，去掉冗余保留关键；还有滑动窗口重叠分块，防止信息在 chunk 边界被切断。"

</details>

## 三、GraphRAG 知识图谱增强

### Q6: 什么是 GraphRAG？它和传统向量 RAG 有什么区别？

<details>
<summary>💡 答案要点</summary>

**传统向量 RAG 的问题：**

```
用户问题："苹果公司CEO都做了哪些环保措施？"

向量检索：找与"苹果CEO环保"语义最相似的文档
→ 可能返回多篇关于Tim Cook、环保政策、苹果公司的独立文章
→ 难以关联"CEO"和"环保措施"之间的关系
→ 无法回答需要多跳推理的问题
```

**GraphRAG 解决方案：**

```python
# 知识图谱结构：
# (苹果公司) --[CEO]--> (Tim Cook) --[推动]--> (环保政策)
# (苹果公司) --[总部]--> (加州) --[气候]--> (清洁能源)

# 用户问题 → 拆解为子问题：
# 1. Tim Cook是谁？→ (苹果公司CEO)
# 2. 他推动了哪些环保措施？→ 查询 (Tim Cook) --[推动]--> (?)

# GraphRAG 返回的不是文档，而是知识图谱子图
subgraph = {
    "nodes": ["Tim Cook", "苹果公司", "环保措施A", "环保措施B"],
    "edges": [
        ("Tim Cook", "CEO", "苹果公司"),
        ("Tim Cook", "推动", "环保措施A"),
        ("Tim Cook", "推动", "环保措施B")
    ]
}
```

**GraphRAG vs 向量 RAG 对比：**

| 维度 | 向量 RAG | GraphRAG |
|------|----------|----------|
| **检索单元** | 文档片段 | 知识图谱子图 |
| **关系理解** | ❌ 弱（靠语义相似） | ✅ 强（图结构显式关系） |
| **多跳推理** | ❌ 差（一跳问询） | ✅ 好（多跳关联） |
| **复杂问题** | 一般 | ✅ 优秀（理解问题结构） |
| **实现复杂度** | 低 | 高（需要构建知识图谱） |
| **构建成本** | 低（直接切分文档） | 高（需要NLP提取实体关系） |

**GraphRAG 适用场景：**

| 场景 | 向量 RAG | GraphRAG |
|------|----------|----------|
| "查找苹果公司的环保报告" | ✅ | ✅ |
| "Tim Cook 推动了什么环保政策？" | ✅ | ✅ |
| "苹果公司CEO和谷歌CEO谁更关注环保？" | ❌ | ✅ |
| "过去5年科技公司CEO环保措施对比" | ❌ | ✅ |

**面试话术：**
> "GraphRAG 的核心是知识图谱——把文档里的实体（人物、公司、地点）和关系（CEO、推动、合作）抽出来构成图。检索时不是找相似文档，而是找图里的子路径。比如问'苹果和谷歌CEO的环保对比'，向量 RAG 只能各自召回文章，GraphRAG 能关联出两个人的具体环保举措。缺点是构建成本高，需要 NLP 提取实体关系。"

</details>

### Q7: 如何构建知识图谱用于 GraphRAG？

<details>
<summary>💡 答案要点</summary>

**知识图谱构建流程：**

```
原始文档
    ↓
① 实体抽取（Named Entity Recognition）
    → 人名、地名、机构名、事件...
    ↓
② 关系抽取（Relation Extraction）
    → CEO、成立于、投资、竞争...
    ↓
③ 实体链接（Entity Linking）
    → "苹果" → Apple Inc.（消歧）
    ↓
④ 图谱存储（Neo4j / 图数据库）
    → (实体) --[关系]--> (实体)
```

**实体抽取代码示例：**
```python
from transformers import pipeline

ner_pipeline = pipeline("ner", model="bert-base-chinese")

def extract_entities(text):
    entities = ner_pipeline(text)
    # 返回：[{'word': '苹果', 'entity': 'ORG'}, {'word': 'Tim Cook', 'entity': 'PER'}]
    return entities
```

**关系分类代码示例：**
```python
def extract_relations(sentence, entities):
    prompt = f"""
    从以下句子中抽取关系：
    句子："{sentence}"
    实体：{entities}
    
    关系类型：CEO、成立于、投资、收购、竞争、合作
    以(json)格式返回：{{"subject": "", "relation": "", "object": ""}}
    """
    result = llm.generate(prompt)
    return json.parse(result)
```

**知识图谱存储：**
```python
# Neo4j 示例
from neo4j import GraphDatabase

def add_triple(tx, subject, relation, obj):
    tx.run("""
        MERGE (s:Entity {name: $subject})
        MERGE (o:Entity {name: $object})
        MERGE (s)-[r:RELATION {type: $relation}]->(o)
    """, subject=subject, relation=relation, object=obj)

# 查询示例：Tim Cook 的所有关系
def query_graph(tx, entity):
    result = tx.run("""
        MATCH (e:Entity {name: $entity})-[r]-(other)
        RETURN e.name, type(r), other.name
    """, entity=entity)
    return list(result)
```

**面试话术：**
> "GraphRAG 的核心是构建知识图谱。流程是：先用 NER 抽实体（人名/地名/机构），再用关系分类抽关系（CEO/收购/合作），然后存到 Neo4j 图数据库。构建成本确实高，但收益是：对多跳问题（'A和B什么关系'）效果远超向量 RAG。我在项目里用 SpaCy 做中文 NER，用 LLM 做关系抽取，实测抽取出 80%+ 准确率。"

</details>

## 四、检索结果重排序与压缩

### Q8: 什么是 Rerank？为什么向量检索后还需要重排序？

<details>
<summary>💡 答案要点</summary>

**两阶段检索架构：**

```
用户查询
    ↓
① 向量检索（BiEncoder，快速召回）
    → 从百万文档中快速召回 Top-100 候选
    → 用 cosine similarity 排序
    ↓
② Rerank（CrossEncoder，精排）
    → 对 Top-100 候选逐一打分
    → 输出最终 Top-10
```

**BiEncoder vs CrossEncoder：**

| 维度 | BiEncoder（向量检索） | CrossEncoder（重排序） |
|------|---------------------|----------------------|
| **速度** | 快（一次 embedding） | 慢（需逐个计算注意力） |
| **精度** | 中等 | 高（考虑query-doc交互） |
| **适用阶段** | 粗召回（Top-100） | 精排序（Top-10） |
| **硬件需求** | 低 | 高 |

**Rerank 模型示例：**
```python
from sentence_transformers import CrossEncoder

# 使用交叉编码器重排序
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, documents, top_k=10):
    # 输入：[query, doc] 对
    pairs = [[query, doc] for doc in documents]
    
    # 获取相关性分数
    scores = cross_encoder.predict(pairs)
    
    # 按分数排序
    ranked_indices = np.argsort(scores)[::-1][:top_k]
    
    return [documents[i] for i in ranked_indices]
```

**为什么需要 Rerank？**
```python
# 向量检索的问题：语义相似 ≠ 相关
query = "如何减肥"
doc1 = "减肥药广告：神奇减肥，一周瘦10斤"  # 向量相似度高，但质量差
doc2 = "健康饮食与运动减肥的科学方法"       # 向量相似度一般，但更相关

# CrossEncoder 能捕捉细粒度相关性问题
# 它会注意："减肥"和"健康饮食"虽然字不相似，但实际高度相关
```

**面试话术：**
> "向量检索是 BiEncoder，能快速从海量文档里召回候选，但精度有限。Rerank 用 CrossEncoder，对每个 query-doc 对计算交叉注意力，打分更精准。生产级 RAG 系统通常是两阶段：向量检索 Top-100 → CrossEncoder 重排 Top-10。BiEncoder 快但粗，CrossEncoder 慢但准，两者结合是工程最优解。"

</details>

### Q9: 什么是 LLMLingua？它如何实现 Prompt/上下文压缩？

<details>
<summary>💡 答案要点</summary>

**LLMLingua 核心思想：**

- 用小模型（如 GPT-2）识别 Prompt 中的"关键token"
- 压缩掉不重要但消耗 token 的内容
- 保留对最终答案贡献大的信息

**为什么需要上下文压缩？**
```
LLM上下文窗口：32K tokens
用户输入：1K tokens
检索文档：30K tokens（100个文档）
↓
总输入：31K tokens → 刚好卡在边界，可能被截断

LLMLingua 压缩后：
压缩文档：8K tokens（去掉冗余）
总输入：9K tokens → 流畅处理
```

**LLMLingua 工作原理：**
```python
from llmlingua import PromptCompressor

compressor = PromptCompressor(
    model_name="WeMix-4/llmlingua2-bert-base-multilingual-cased-gsm8k-对话",
    rate=0.5  # 压缩到50%
)

def compress_context(context, instruction):
    compressed = compressor.compress(
        prompt=context,
        instruction=instruction,  # "回答用户关于X的问题"
        target_token=2000
    )
    return compressed

# 示例
original = """
苹果公司（Apple Inc.）是一家美国跨国科技公司...
总部位于加利福尼亚州库比蒂诺...
史蒂夫·乔布斯于1976年4月1日创立...
"""
instruction = "总结苹果公司的关键信息"

compressed = compress_context(original, instruction)
# 输出：压缩后的关键信息，token数减少60-70%
```

**压缩效果对比：**

| 方法 | Token数 | 答案准确率 | 保留率 |
|------|---------|-----------|--------|
| 不压缩 | 3000 | 85% | 100% |
| LLMLingua | 900 | 83% | ~97%语义 |
| Random Cut | 900 | 71% | ~75%语义 |

**面试话术：**
> "LLMLingua 是上下文压缩利器。传统压缩会丢失语义，它用小模型识别哪些 token 对答案贡献大，只压缩低贡献部分。我在长文档 RAG 场景用过，压缩 60-70% 的 token 量，准确率只下降 2-3%。特别适合上下文窗口紧张但检索文档很多的情况。"

</details>

## 五、RAG 评估与调优

### Q10: 如何系统性评估一个 RAG 系统？有哪些关键指标？

<details>
<summary>💡 答案要点</summary>

**RAG 评估框架（RAGAS）：**

```python
# RAGAS 三大核心指标
from ragas import evaluate
from datasets import Dataset

# 准备评估数据
eval_data = Dataset.from_dict({
    "user_input": ["问题1", "问题2", ...],
    "retrieved_contexts": [["文档1", "文档2"], ...],
    "response": ["答案1", "答案2", ...],
    "reference": ["标准答案1", "标准答案2", ...]
})

# 计算指标
result = evaluate(eval_data, metrics=[
    faithfulness,      # 答案是否忠于检索内容
    answer_relevancy,   # 答案是否切题
    context_recall,     # 检索内容是否完整
    context_precision   # 检索内容是否精确
])
```

**四大核心指标详解：**

| 指标 | 含义 | 目标值 | 测量方式 |
|------|------|--------|----------|
| **Faithfulness** | 答案事实是否来自检索内容 | >0.9 | LLM判断答案中有多少陈述被检索内容支持 |
| **Answer Relevancy** | 答案和问题相关程度 | >0.8 | LLM生成反问，看与原问题的语义相似度 |
| **Context Recall** | 检索内容覆盖标准答案的程度 | >0.85 | 比较检索内容 vs 标准答案的实体重叠 |
| **Context Precision** | 检索内容中噪音比例 | >0.9 | 计算 Top-K 中相关文档的比例 |

**Context Precision 计算：**
```python
def context_precision(retrieved_docs, relevant_docs, k=10):
    """Context Precision@K"""
    hits = 0
    for i, doc in enumerate(retrieved_docs[:k]):
        if doc in relevant_docs:
            hits += 1
    return hits / min(k, len(relevant_docs))
```

**实际调优案例：**

```python
# 调优前：Faithfulness=0.72
# 问题：模型有时候会"自己发挥"，脱离检索内容

# 调优方案：添加 prompt 约束
improved_prompt = """
你是一个严格基于给定上下文回答的助手。
规则：
1. 只使用上下文中的信息，不要添加外部知识
2. 如果上下文中没有相关信息，直接回答"我不知道"
3. 回答时引用上下文中的具体内容

上下文：{context}
问题：{question}
"""

# 调优后：Faithfulness=0.91
```

**面试话术：**
> "RAG 评估用 RAGAS 框架，核心看四个指标：Faithfulness（答案是否忠于检索内容）、Answer Relevancy（答案是否切题）、Context Recall（检索是否完整）、Context Precision（检索是否精确）。生产环境我会用 RAGAS 配合人工抽检，每周跑一次评估看板。Faithfulness 最关键，低于 0.9 就得优化 Prompt 或检索质量。"

</details>

### Q11: 如何优化 RAG 系统的召回率和准确率？

<details>
<summary>💡 答案要点</summary>

**召回率 vs 准确率的两难：**

```
召回率↑ = 多召回文档 = 更容易包含正确答案 BUT 更多噪音
准确率↑ = 严格筛选 = 更少噪音 BUT 可能漏掉正确答案
```

**召回率优化（Recall）：**

```python
# 1. Query Expansion（查询扩展）
def query_expansion(query, llm):
    """生成多个相关查询，每个独立检索"""
    expanded_queries = llm.generate(
        f"为这个问题生成3个不同的表述：{query}"
    )
    all_docs = []
    for q in expanded_queries:
        docs = vector_db.search(q, k=10)
        all_docs.extend(docs)
    # 用 RRF 融合
    return rrf_fusion(all_docs)

# 2. HyDE（前面讲过）

# 3. 混合检索（稀疏 + 稠密）
def hybrid_search(query, vector_db, bm25_index):
    # 稠密向量检索
    dense_results = vector_db.search(embed(query), k=20)
    # 稀疏 BM25 检索
    sparse_results = bm25_index.search(query, k=20)
    # RRF 融合
    return rrf_fusion([dense_results, sparse_results])
```

**准确率优化（Precision）：**

```python
# 1. Rerank（前面讲过）

# 2. 元数据过滤
def search_with_metadata_filter(query, vector_db, filters):
    """支持按时间、类型、来源等过滤"""
    results = vector_db.search(
        query_emb,
        k=50,
        filter={"category": "技术文档", "date": {"$gte": "2024-01-01"}}
    )
    return rerank(query, results, top_k=10)

# 3. 上下文窗口优化（前面讲过的 Lost in the Middle 解法）
```

**综合调优策略：**

| 阶段 | 优化方法 | 效果 |
|------|----------|------|
| **召回** | Query Expansion、HyDE、混合检索 | 召回率 +15-20% |
| **排序** | CrossEncoder Rerank | Precision +25% |
| **生成** | Faithfulness Prompt、引用追踪 | Faithfulness +10% |
| **压缩** | LLMLingua | 上下文利用率 +40% |

**A/B 测试框架：**
```python
# 生产环境 A/B 测试不同配置
def ab_test(query, config_a, config_b):
    result_a = rag_pipeline(query, **config_a)
    result_b = rag_pipeline(query, **config_b)
    
    # 记录到评估数据集
    log_to_eval({"query": query, "config": "A", "result": result_a})
    log_to_eval({"query": query, "config": "B", "result": result_b})
    
    return result_a, result_b
```

**面试话术：**
> "RAG 调优核心是平衡召回和准确。我的策略是：先用 Query Expansion + HyDE 提升召回，再用 CrossEncoder Rerank 保证准确。生成阶段加 Faithfulness 约束 prompt，强制模型只引用检索内容。生产环境每周跑 RAGAS 评估，Faithfulness <0.9 就预警。"

</details>

---

## 六、2026年RAG评估新趋势（新增考点）

### Q12: 什么是self-RAG和CRAG？和传统RAG有什么区别？

<details>
<summary>💡 答案要点</summary>

**self-RAG = Self-Retrieval-Augmented Generation（自检索增强生成）**

**传统RAG的问题：**
- 不管查询是否需要检索，都强制检索
- 检索结果质量差时，模型仍然基于错误上下文生成
- 无法判断检索是否必要

**self-RAG的核心创新：**
- 模型自主判断"需不需要检索"
- 模型自主评估检索结果的质量
- 质量差时主动修正或忽略错误上下文

**self-RAG流程：**
```
用户Query → 模型判断：是否需要检索？
  ├── 不需要 → 直接生成答案
  └── 需要 → 检索文档
              ↓
      模型判断：文档是否相关？
        ├── 不相关 → 忽略，用内部知识
        └── 相关 → 生成答案 + 引用
```

**CRAG = Corrective RAG（纠错型RAG）**
```python
# CRAG的自我纠错流程
class CorrectiveRAG:
    def generate(self, query):
        docs = retriever.retrieve(query)

        # 评估检索质量
        relevance = assessor.evaluate(query, docs)

        if relevance > 0.8:
            # 高相关：直接生成
            return llm.generate(query, docs)
        elif relevance > 0.3:
            # 中相关：知识精炼后生成
            refined = knowledge_refiner.refine(query, docs)
            return llm.generate(query, refined)
        else:
            # 低相关：忽略检索，用内部知识
            return llm.generate(query, [])  # 无上下文
```

**对比：**

| 方案 | 检索触发 | 质量控制 | 适用场景 |
|------|----------|----------|----------|
| **传统RAG** | 100%触发 | 无 | 简单问答 |
| **self-RAG** | 模型自主决定 | 反思token评估 | 复杂推理任务 |
| **CRAG** | 100%触发 | 三级质量过滤 | 高精度要求场景 |

**面试话术：**
> "self-RAG的突破是让模型'知道自己什么时候该查资料、查到的资料靠不靠谱'。CRAG则是'先查再审，不行就换'。生产环境中，我用CRAG做金融问答，检索质量<0.3的直接走内部知识，幻觉率从15%降到3%。"

</details>

### Q13: DeepEval是什么？和RAGAS、TruLens有什么区别？

<details>
<summary>💡 答案要点</summary>

**DeepEval = Python-first RAG评估框架（by confident-ai）**

**三大评估工具对比：**

| 工具 | 定位 | 核心优势 | 适用阶段 |
|------|------|----------|----------|
| **RAGAS** | 指标探索 | RAG专属指标全，信仰度/相关性/召回率 | 离线评估 |
| **TruLens** | 实验看板 | 实时可观测，RAG三元素追踪 | 开发调试 |
| **DeepEval** | CI/CD集成 | Pytest风格，流水线自动化 | 回归测试 |

**DeepEval核心特点：**
```python
# Pytest风格的评估（DeepEval特色）
from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric

# 定义测试用例
test_cases = [
    "什么是RAG系统",
    "self-RAG和CRAG的区别",
]

# 用装饰器评估
@evaluate(version=1)
def test_rag_accuracy():
    metric = FaithfulnessMetric(threshold=0.8)
    result = rag_pipeline.run(test_cases[0])
    metric.measure(test_cases[0], result.answer, result.context)
    assert metric.score > 0.8
```

**DeepEval的独特功能：**

| 功能 | 说明 |
|------|------|
| **Pytest集成** | 用单元测试的思路评估RAG，无缝接入CI/CD |
| **红绿对比** | 评估结果直观（通过/失败），适合团队协作 |
| **自定义指标** | 支持用LLM-as-Judge自定义评估维度 |
| **幻觉检测** | 内置幻觉检测，发现"答非所问" |

**2026年评估工具选型决策树：**
```python
def select_eval_tool(scenario):
    if scenario == "快速探索指标":
        return "RAGAS"  # 指标最全
    elif scenario == "开发调试看过程":
        return "TruLens"  # 实时追踪
    elif scenario == "CI/CD自动化":
        return "DeepEval"  # Pytest风格
    elif scenario == "生产监控看板":
        return "TruLens + RAGAS"  # 组合使用
```

**面试话术：**
> "DeepEval是2026年CI/CD集成的首选。它的Pytest风格让评估变成'测试用例'，每次代码变更自动跑评估，Faithfulness<0.8就阻止上线。我用它做RAG系统的回归测试，配合GitHub Actions，检索质量波动超过5%自动告警。"

</details>

### Q14: 什么是state-aware retrieval和agentic retrieval？2026年检索新趋势？

<details>
<summary>💡 答案要点</summary>

**传统检索的问题：**
- 静态top-k检索，不考虑用户意图的动态变化
- 不考虑对话上下文（多轮对话场景）
- 缺乏时效性控制和多样性控制

**state-aware retrieval（状态感知检索）：**
```python
# 传统检索 vs 状态感知检索
# 传统：
static_docs = vector_db.top_k(query, k=5)

# 状态感知：
def state_aware_retrieve(query, user_context, conversation_history):
    # 1. 提取用户真实意图
    intent = intent_extractor.parse(query)

    # 2. 应用元数据过滤器
    filtered_docs = apply_filters(intent.metadata_constraints)

    # 3. 时效性权重（近期文档优先）
    recency_boost(intent.requires_fresh_docs, filtered_docs)

    # 4. 多样性控制（避免重复主题）
    diversified = diversify(filtered_docs, conversation_history)

    return diversified
```

**agentic retrieval（智能体式检索）：**
```python
# Azure AI Search的agentic retrieval示例
"""
用户复杂查询："对比Q1和Q2季度营收，分析增长原因"
→ 分解为多个子查询：
  子查询1: Q1季度营收数据
  子查询2: Q2季度营收数据
  子查询3: 季度增长原因分析
→ 并行执行 → 结果融合 → 结构化响应
"""

# 核心流程：
class AgenticRetriever:
    def retrieve(self, complex_query):
        # 1. 查询分解
        sub_queries = self.query_decomposer.split(complex_query)

        # 2. 并行检索
        results = parallel_retrieve(sub_queries)

        # 3. 结果融合
        fused = self.fusion_engine.merge(results)

        # 4. 返回结构化响应（优化给LLM）
        return structured_response(fused)
```

**2026年检索新趋势：**

| 趋势 | 技术 | 效果 |
|------|------|------|
| **状态感知 | 对话上下文+意图识别 | 多轮场景召回+25% |
| **agentic检索 | 查询分解+并行检索 | 复杂问题准确+30% |
| **动态chunk | 根据查询动态调整块大小 | 上下文利用率+40% |
| **多跳推理 | 跨文档关联推理 | 推理型问题准确+35% |

**面试话术：**
> "state-aware retrieval解决的是'用户问了一半的问题，系统不知道在聊什么'的问题。agentic retrieval则是让检索本身变成一个Agent——自动分解复杂查询、并行检索、融合结果。我在金融分析场景用agentic retrieval，用户问'对比去年和今年利润'，系统自动拆解成4个子查询并发生成，复杂问题准确率提升30%。"

</details>

---

*版本: v2.6 | 更新: 2026-04-05 | by 二狗子 🐕*
