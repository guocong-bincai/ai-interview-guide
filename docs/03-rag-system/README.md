# 📚 RAG 系统面试题

> **难度：** ⭐⭐⭐⭐
> **考点：** 检索增强生成、向量数据库、Embedding、检索优化

## 📋 目录

1. [基础概念题](#一基础概念题)
2. [架构设计题](#二架构设计题)
3. [优化策略题](#三优化策略题)
4. [高分实战案例](#四高分实战案例)

## 一、基础概念题

### Q1: 什么是 RAG？为什么需要 RAG？

<details>
<summary>💡 答案要点</summary>

**RAG = Retrieval-Augmented Generation（检索增强生成）**

**核心思想：** 先检索相关知识，再让 LLM 基于检索内容回答问题。

**为什么需要 RAG？**

| 问题 | 纯 LLM | RAG |
|------|--------|-----|
| 知识过时 | ❌ 训练数据截止后不知道 | ✅ 可以检索最新数据 |
| 私有数据 | ❌ 不知道公司内部文档 | ✅ 可以检索内部知识库 |
| 幻觉 | ❌ 容易瞎编 | ✅ 基于检索内容，更准确 |
| 可追溯性 | ❌ 不知道答案从哪来 | ✅ 可以给出引用来源 |

**面试话术：**
> "RAG 的核心是解决 LLM 知识过时和幻觉问题。我会用混合检索 + Rerank 提升召回率，用语义缓存降低成本。"

</details>

### Q2: RAG 的完整流程是什么？

<details>
<summary>💡 答案要点</summary>

**两条流水线：**

```
索引流水线（离线）：
文档 → 加载 → 切分 → 向量化 → 存储到向量库

查询流水线（在线）：
用户问题 → 向量化 → 检索 → 生成答案
```

**详细流程：**
```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG 系统全貌                              │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  文档加载器   │ ──→ │  文档切分器   │ ──→ │  Embedding   │
│  (Loader)    │     │  (Splitter)  │     │   (向量化)    │
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
                                                 ↓
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  LLM 生成答案  │ ←── │  检索器      │ ←── │  向量数据库   │
│  (Generator) │     │  (Retriever) │     │  (Vector DB) │
└──────────────┘     └──────────────┘     └──────────────┘
```

**6 个核心步骤：**
1. **加载**：从 PDF/Markdown/网页读取文档
2. **切分**：切成小 chunks（500-1000 tokens）
3. **向量化**：用 Embedding 模型转成向量
4. **存储**：存入向量数据库
5. **检索**：计算相似度，返回 top-k chunks
6. **生成**：LLM 基于检索内容生成答案

</details>

### Q3: 为什么 RAG 要用向量数据库？其他数据库不行吗？

<details>
<summary>💡 高分回答</summary>

**核心区别：检索方式不同**

| 数据库类型 | 检索方式 | 适用场景 |
|------------|----------|----------|
| 传统数据库 | 精确匹配（=、LIKE） | 关键词搜索 |
| 向量数据库 | 语义匹配（相似度） | 语义搜索 |

**性能对比（10 万条数据）：**

| 数据库 | 检索时间 |
|--------|----------|
| MySQL（无索引） | ~5000ms |
| MySQL+pgvector | ~500ms |
| Elasticsearch | ~100ms |
| Milvus/Qdrant | ~10ms |

**为什么向量库快？**
- 内置 ANN 索引（HNSW/IVF）
- 搜索复杂度 O(log N) vs O(N)
- 专为向量检索优化

**面试话术：**
> "向量库是专为'找相似'设计的跑车，传统库是家用轿车。10 万条数据检索差 100-500 倍。但小项目（<1 万条）用 pgvector 就够了。"

</details>

### Q4: Embedding 是什么？1536 维什么意思？

<details>
<summary>💡 答案要点</summary>

**Embedding = 把文本转成向量（一串数字）**

**1536 维 = 用 1536 个特征描述这段文本**

**类比：**
```
描述"张三"这个人：

传统方式：
  "张三，男，30 岁，北京人，程序员，喜欢篮球"

向量方式（简化版）：
  [
    性别：0.9,        // 接近 1 = 男，接近 0 = 女
    年龄：0.3,        // 0-1 归一化，0.3 ≈ 30 岁
    地域：0.8,        // 接近 1 = 北方，接近 0 = 南方
    职业：0.95,       // 接近 1 = 技术岗
    爱好：0.7,        // 接近 1 = 运动型
    ...              // 继续到 1536 维
  ]
```

**余弦相似度：**
- 算两个向量"方向"有多接近
- 1 = 完全同向（语义几乎一样）
- 0 = 垂直（语义无关）
- -1 = 完全反向（语义相反）

**面试话术：**
> "Embedding 是语义的数学表示。我用余弦相似度衡量相关性，用 HNSW 索引加速检索。"

</details>

## 二、架构设计题

### Q5: 设计一个企业级知识库问答系统，你会怎么架构？

<details>
<summary>💡 高分回答</summary>

**1. 架构选型：RAG 是首选，Fine-tuning 是补充**

> "我会优先采用 Advanced RAG 架构而非微调。原因有三：
> 1. 知识库需要频繁更新，RAG 只需更新向量库，而微调成本太高
> 2. RAG 可以提供引用溯源，消除幻觉
> 3. 微调无法处理海量非结构化文档的检索"

**2. 数据清洗与切片**

> "切片不能简单按字符数。我会采用 Markdown 语义切片。对于 PDF 中的表格，我会使用 Unstructured 或 GPT-4o-mini 将表格转为 Markdown 格式，否则向量检索会丢失行列逻辑。"

**进阶提分：**
> "我会给每个 Chunk 增加 Metadata（元数据），比如文件名、页码、所属部门。这样在检索时可以进行 Self-Querying（根据用户权限或范围过滤标签）。"

**3. 检索优化**

> "单次向量检索往往不够。我会引入 Multi-Query Retrieval（将用户问题扩展成多个同义句）和 Hybrid Search（向量检索 + 关键词 BM25 检索）来提升召回率。"

**进阶提分：**
> "我会加入 Rerank（重排序）环节。先从向量库召回 50 个候选片断，再用专门的 Reranker 模型（如 BGE-Reranker）精选出最相关的 Top-5。"

**4. 评估与工程化**

> "我会建立一套 RAGAS 评估体系，重点监控四个维度：忠实度、相关度、上下文精度和召回率。"

**进阶提分：**
> "为了降低 Token 成本和延迟，我会部署 Semantic Cache（语义缓存）。如果两个用户问了语义相似的问题，直接从 Redis 缓存中读取答案，无需再次调用大模型。"

</details>

### Q6: 如何选择 Chunk 大小？有什么影响？

<details>
<summary>💡 答案要点</summary>

**Chunk 大小的权衡：**

| Chunk 大小 | 优点 | 缺点 | 适用场景 |
|------------|------|------|----------|
| 小（256-512） | 检索精确 | 语义不完整 | 技术文档、代码 |
| 中（512-1000） | 平衡 | 平衡 | 通用文档 |
| 大（1000-2000） | 语义完整 | 检索不精确 | 对话数据、文章 |

**经验值：**
- 通用文档：500-1000 tokens
- 技术文档：256-512 tokens
- 对话数据：1024-2048 tokens
- 重叠：chunk_size 的 10-20%

**进阶策略：**
- 父子文档（Parent-Child）：检索小 chunk，返回大文档
- 重叠切分：相邻 chunk 重叠 10-20%
- 语义切分：用 embedding 聚类后切分

</details>

## 三、优化策略题

### Q7: 如何解决检索结果不相关（Recall 质量差）？

<details>
<summary>💡 答案要点</summary>

**解决方案：**

1. **混合检索**
   - 向量检索 + 关键词检索（BM25）
   - 加权融合：Final Score = 0.7 × Vector + 0.3 × BM25

2. **Multi-Query**
   - 用 LLM 生成多个查询变体
   - 合并检索结果，去重

3. **Rerank**
   - 用 Cross-Encoder 重新排序
   - 先从向量库召回 50 个，再精选 Top-5

4. **优化 Embedding**
   - 换更好的模型（如 BGE-M3 中文好）

5. **优化 Chunking**
   - 调整 chunk 大小和重叠

</details>

### Q8: 如何降低 RAG 系统的成本？

<details>
<summary>💡 答案要点</summary>

**成本优化策略：**

1. **语义缓存**
   - 相同/相似问题直接返回缓存
   - 命中率可达 30-50%

2. **Prompt 压缩**
   - 用 LLMLingua 压缩检索结果
   - 减少 40% Context Token

3. **模型路由**
   - 简单问题用小模型（便宜）
   - 复杂问题用大模型（贵但效果好）

4. **优化检索**
   - 减少 k 值（只返回最相关的 2-3 个）
   - 用 Rerank 提升精度，减少无效 token

5. **批量处理**
   - 多个请求合并成一个 LLM 调用
   - 适合离线任务

</details>

## 四、高分实战案例

### 案例：处理复杂 PDF 表格

**背景：** 扫描版 PDF，包含大量跨页表格，直接 OCR 导致文字逻辑错乱。

**解决方案：**

1. **布局分析（Layout Analysis）**
   - 用 Layout-Parser 或 PaddleOCR 的区域检测模型
   - 先识别出文档中的"表格区"、"正文区"

2. **多模态增强**
   - 针对极难处理的表格，用 GPT-4o 直接截取图像进行转换

3. **管道化清洗（Pipeline）**
   - 先用 PyMuPDF 提取可复制文字
   - 对无法识别的图片层启动 OCR
   - 最后通过 Cleaner LLM 修复噪点

**结果：** 财务指标提取准确率从 65% 提升到 94%

### Q11: 什么是Query改写?如何提升检索效果?

<details>
<summary>💡 答案要点</summary>

**Query改写 = 优化用户原始问题,使其更适合检索**

**核心问题:**
```
用户问题往往不够精确:
- "昨天说的那个事" → 缺少上下文
- "怎么办" → 太模糊
- "价格多少" → 缺少主语
```

**改写策略:**

### 1. 补充上下文(多轮对话)
```python
# 对话历史
history = [
    ("什么是RAG?", "RAG是检索增强生成..."),
    ("它有什么优势?", "...")
]

# 用户新问题
user_query = "如何实现它?"

# 改写后
rewritten_query = "如何实现RAG检索增强生成系统?"
```

### 2. 查询扩展
```python
# 原始查询
query = "Python多线程"

# 扩展后
expanded_query = """
Python多线程
Python threading模块
Python GIL全局解释器锁
Python并发编程
"""
# 用扩展后的多个查询检索,合并结果
```

### 3. HyDE(假设性文档嵌入)
```python
# 原始问题
query = "如何优化RAG检索准确率?"

# 让LLM生成假设性答案
hypothetical_doc = llm.generate(f"假设回答: {query}")
# "可以通过混合检索、Rerank、query改写等方法..."

# 用假设性答案的向量去检索(而非原问题)
embedding = embed(hypothetical_doc)
results = vector_db.search(embedding)
```

**HyDE优势**: 答案和文档库中的文档更相似,检索更准

### 4. 多查询生成
```python
# 原始问题
query = "RAG系统慢怎么办?"

# 生成多个视角的查询
sub_queries = llm.generate(f"将问题拆分成3个子问题: {query}")
# 1. "如何提升RAG检索速度?"
# 2. "RAG系统性能瓶颈在哪?"
# 3. "向量数据库优化方法?"

# 分别检索后合并结果
```

**实现示例:**
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Query改写器
def rewrite_query(query, chat_history):
    prompt = f"""
    对话历史: {chat_history}
    当前问题: {query}

    请补充上下文,改写成独立完整的问题。
    """
    return llm.generate(prompt)

# HyDE改写
def hyde_rewrite(query):
    prompt = f"假设你要回答这个问题,你会怎么说: {query}"
    hypothetical_answer = llm.generate(prompt)
    return hypothetical_answer

# 使用
user_query = "如何优化?"
rewritten = rewrite_query(user_query, history)
results = retriever.get_relevant_documents(rewritten)
```

**性能对比:**

| 方法 | Recall@5 | Precision@5 |
|------|----------|-------------|
| 原始查询 | 65% | 58% |
| +上下文补充 | 75% | 68% |
| +HyDE | 82% | 76% |
| +多查询 | 88% | 80% |

**面试话术:**
> "Query改写是RAG的前置优化。用户问题往往模糊或缺上下文,我们用LLM补充完整,或用HyDE生成假设答案去检索。我们项目用HyDE,召回率从67%提升到85%。"

</details>

---

### Q12: 什么是上下文压缩?如何减少无效Token?

<details>
<summary>💡 答案要点</summary>

**上下文压缩 = 从检索结果中提取最相关片段,减少LLM输入**

**问题背景:**
```
检索返回5个文档,每个1000 tokens
→ 总共5000 tokens送给LLM
→ 但只有500 tokens真正有用
→ 浪费4500 tokens,增加成本和延迟
```

**压缩策略:**

### 1. 基于LLM的提取
```python
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)

prompt = """
文档: {document}
问题: {query}

请只提取与问题相关的句子,其他都删除。
"""

# 压缩前: 1000 tokens
# 压缩后: 200 tokens (只保留相关部分)
```

### 2. 基于Embedding的过滤
```python
from langchain.retrievers.document_compressors import EmbeddingsFilter

# 计算每个句子与query的相似度
# 只保留相似度>阈值的句子
embeddings_filter = EmbeddingsFilter(
    embeddings=OpenAIEmbeddings(),
    similarity_threshold=0.76
)
```

### 3. Rerank + Top-K选择
```python
# 先检索50个候选
candidates = vector_db.search(query, top_k=50)

# Rerank重排
reranked = reranker.rerank(query, candidates)

# 只取top-3,并提取关键段落
compressed = []
for doc in reranked[:3]:
    # 从每个文档中提取最相关的3个句子
    relevant_sentences = extract_relevant(doc, query, max_sentences=3)
    compressed.append(relevant_sentences)
```

### 4. Contextual Compression完整流程
```python
from langchain.retrievers import ContextualCompressionRetriever

# 基础检索器
base_retriever = vector_store.as_retriever(search_kwargs={"k": 20})

# 压缩器(LLM提取)
compressor = LLMChainExtractor.from_llm(llm)

# 组合
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# 使用
compressed_docs = compression_retriever.get_relevant_documents(query)
```

**效果对比:**

| 方法 | 输入Tokens | 输出质量 | 成本 | 延迟 |
|------|------------|----------|------|------|
| 无压缩 | 5000 | ⭐⭐⭐⭐ | $0.05 | 3s |
| Embedding过滤 | 2000 | ⭐⭐⭐⭐ | $0.02 | 1.5s |
| LLM提取 | 800 | ⭐⭐⭐⭐⭐ | $0.015 | 2s |
| Rerank+提取 | 500 | ⭐⭐⭐⭐⭐ | $0.01 | 2.5s |

**Late Chunking(晚期分块):**
```python
# 传统chunking: 先切分再embedding
doc = "AI技术正在改变世界。大模型是核心。RAG系统很重要。"
chunks = ["AI技术正在改变世界。", "大模型是核心。", "RAG系统很重要。"]
embeddings = [embed(c) for c in chunks]  # 丢失跨chunk上下文

# Late chunking: 先embedding再切分
full_embedding = embed(doc)  # 保留完整上下文
chunk_embeddings = split_embedding(full_embedding, chunk_boundaries)
```

**优势**: 保留完整文档上下文,提升检索准确率5-10%

**面试话术:**
> "上下文压缩是成本优化的关键。我们用Rerank+LLM提取,从检索的20个文档中精选3个,每个提取3句话,tokens从8000降到600,成本降低92%,质量反而更好。"

</details>

---

## 13. Embedding模型如何选择?

<details>
<summary>💡 答案要点</summary>

### 选择维度

| 维度 | 考虑因素 | 推荐 |
|------|----------|------|
| **1. 语言** | 中文 / 英文 / 多语言 | 中文首选BGE,多语言用M3 |
| **2. 成本** | 闭源API / 开源自部署 | 预算少用开源,省钱 |
| **3. 性能** | MTEB排行榜得分 | 看检索任务NDCG@10指标 |
| **4. 维度** | 256 / 768 / 1024 / 3072 | 大数据集用低维(256),小数据集高维 |
| **5. Token限制** | 512 / 8192 | RAG分块用512够,长文本用8K |
| **6. 部署** | API / 本地推理 | 数据敏感用本地,方便用API |

### 主流模型对比(2024)

#### 闭源API模型

| 模型 | 维度 | 语言 | 价格(百万token) | 优势 | 劣势 |
|------|------|------|-----------------|------|------|
| **text-embedding-3-large** | 256~3072可调 | 多语言 | $0.13 | OpenAI官方,质量稳定 | 贵,数据外传 |
| **text-embedding-3-small** | 512~1536可调 | 多语言 | $0.02 | 便宜,性能够用 | 不如large |
| **Cohere embed-v3** | 1024 | 多语言 | $0.10 | 支持检索/分类双模式 | 小众 |
| **Voyage-2** | 1024 | 英文 | $0.12 | 专为RAG优化 | 只支持英文 |

**选择建议:**
- **预算充足**: text-embedding-3-large (3072维)
- **性价比**: text-embedding-3-small
- **RAG专用**: Voyage-2 (英文) / Cohere (多语言)

#### 开源模型(可本地部署)

| 模型 | 维度 | 语言 | MTEB得分 | 模型大小 | 推荐场景 |
|------|------|------|----------|----------|----------|
| **bge-large-zh-v1.5** | 1024 | 中文⭐ | 64.53 | 1.3GB | 中文RAG首选 |
| **bge-large-en-v1.5** | 1024 | 英文 | 63.98 | 1.3GB | 英文通用 |
| **BGE-M3** | 1024 | 多语言⭐ | 66.12 | 2.2GB | 中英混合,跨语言检索 |
| **gte-large-zh** | 1024 | 中文 | 63.85 | 1.3GB | 备选,阿里出品 |
| **stella-base-zh-v2** | 768 | 中文 | 64.08 | 400MB | 轻量级,速度快 |
| **jina-embeddings-v2** | 768 | 多语言 | 60.38 | 550MB | 支持8K长文本 |
| **E5-large-v2** | 1024 | 英文 | 62.25 | 1.3GB | 微软出品 |

**选择建议:**
- **中文项目**: bge-large-zh-v1.5 (最强) / stella-base-zh-v2 (快)
- **多语言**: BGE-M3
- **长文本**: jina-embeddings-v2 (支持8K tokens)
- **资源受限**: stella-base-zh-v2 (400MB小模型)

### 实战代码

#### 方案1: 闭源API(OpenAI)

```python
from openai import OpenAI

client = OpenAI(api_key="sk-xxx")

def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text,
        dimensions=1024  # 可选256/1024/3072
    )
    return response.data[0].embedding

# 使用
vector = embed_text("什么是RAG系统?")
print(len(vector))  # 1024
```

**优点:** 零部署,调用即用
**缺点:** 每百万token $0.13,数据外传

#### 方案2: 开源本地部署

```python
from sentence_transformers import SentenceTransformer

# 加载模型(首次会下载,约1.3GB)
model = SentenceTransformer('BAAI/bge-large-zh-v1.5')

def embed_text(text):
    # 编码
    embedding = model.encode(
        text,
        normalize_embeddings=True  # 归一化,方便余弦相似度
    )
    return embedding

# 批量处理(更快)
texts = ["什么是RAG?", "如何优化检索?", "向量数据库选择"]
embeddings = model.encode(texts, batch_size=32)
print(embeddings.shape)  # (3, 1024)
```

**优点:** 免费,数据不外传,可微调
**缺点:** 需要GPU(CPU慢10倍),首次下载模型

#### 方案3: 混合策略

```python
class HybridEmbedding:
    def __init__(self):
        # 开源模型处理中文
        self.zh_model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
        # API处理英文
        self.openai_client = OpenAI(api_key="sk-xxx")

    def embed(self, text, language='auto'):
        # 自动检测语言
        if language == 'auto':
            language = 'zh' if contains_chinese(text) else 'en'

        if language == 'zh':
            # 用本地模型(免费)
            return self.zh_model.encode(text)
        else:
            # 用OpenAI(付费但质量好)
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-large",
                input=text
            )
            return response.data[0].embedding

def contains_chinese(text):
    return any('\u4e00' <= char <= '\u9fff' for char in text)
```

**优势:** 中文省钱,英文质量保证

### 性能测试

```python
import time
from sentence_transformers import SentenceTransformer

# 测试embedding速度
model = SentenceTransformer('BAAI/bge-large-zh-v1.5')

texts = ["测试文本"] * 1000

# CPU
start = time.time()
embeddings = model.encode(texts, device='cpu')
cpu_time = time.time() - start
print(f"CPU: {cpu_time:.2f}s, {len(texts)/cpu_time:.1f} texts/s")

# GPU
start = time.time()
embeddings = model.encode(texts, device='cuda')
gpu_time = time.time() - start
print(f"GPU: {gpu_time:.2f}s, {len(texts)/gpu_time:.1f} texts/s")

# 输出示例:
# CPU: 45.23s, 22.1 texts/s
# GPU: 3.12s, 320.5 texts/s
# GPU快14倍!
```

### 微调Embedding模型

**场景:** 通用模型在你的领域(如医疗/法律)效果差

```python
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# 1. 准备训练数据
train_examples = [
    InputExample(
        texts=["患者出现发热症状", "病人体温升高"],
        label=1.0  # 相似
    ),
    InputExample(
        texts=["患者出现发热症状", "今天天气很好"],
        label=0.0  # 不相似
    ),
    # ... 至少1000对
]

# 2. 加载基础模型
model = SentenceTransformer('BAAI/bge-large-zh-v1.5')

# 3. 定义损失函数
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)

# 4. 微调
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3,
    warmup_steps=100,
    output_path='./my-domain-embedding'
)

# 5. 使用微调模型
custom_model = SentenceTransformer('./my-domain-embedding')
embedding = custom_model.encode("医学专业术语")
```

**效果:** 领域适配性+10~20%

### 决策树

```
需要embedding模型?
├─ 中文为主?
│  ├─ 是 → bge-large-zh-v1.5 (开源)
│  └─ 否 → 继续
├─ 多语言/跨语言?
│  ├─ 是 → BGE-M3 (开源) / text-embedding-3-large (付费)
│  └─ 否 → 继续
├─ 预算充足?
│  ├─ 是 → text-embedding-3-large (质量最好)
│  └─ 否 → text-embedding-3-small (性价比)
├─ 数据敏感/不能外传?
│  ├─ 是 → 必须用开源本地部署
│  └─ 否 → API更方便
└─ 需要处理长文本(>512 token)?
   ├─ 是 → jina-embeddings-v2 (8K) / text-embedding-3 (8K)
   └─ 否 → 任意模型
```

**面试话术:**
> "Embedding模型选择看4点:语言(中文用bge)、成本(预算少开源)、性能(看MTEB排行)、部署(敏感数据本地)。我们项目是中文RAG,选了bge-large-zh-v1.5本地部署,1.3GB模型GPU推理每秒300条,免费且效果好。如果是多语言就用BGE-M3,如果不care成本就text-embedding-3-large。"

</details>

---

## 14. GraphRAG是什么？与普通向量RAG的核心区别？何时选择？

<details>
<summary>💡 答案要点</summary>

**GraphRAG = 知识图谱 + RAG，用实体关系图做检索而非纯向量相似度**

### 核心区别

| 维度 | 向量RAG | GraphRAG |
|------|---------|---------|
| **数据组织** | 文本切块→向量 | 实体+关系→图节点/边 |
| **检索方式** | 语义相似度（近似邻居） | 图遍历/Cypher查询 |
| **多跳推理** | ❌ 难以关联多个文档 | ✅ 沿关系路径自然推理 |
| **可解释性** | 低（黑盒相似度） | 高（关系路径可追踪） |
| **构建成本** | 低 | 高（需要NER+关系抽取） |
| **适用场景** | 语义搜索、文档问答 | 复杂关系推理、知识密集 |

### GraphRAG实现流程

**Step 1：知识图谱构建**

```python
from neo4j import GraphDatabase
import spacy

class KnowledgeGraphBuilder:
    def __init__(self, neo4j_uri, user, password):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(user, password))
        self.nlp = spacy.load("zh_core_web_sm")

    def extract_entities_relations(self, text: str):
        """用LLM抽取实体和关系"""
        prompt = f"""
        从以下文本中提取实体和关系，以JSON格式输出：

        文本：{text}

        输出格式：
        {{
            "entities": [
                {{"name": "实体名", "type": "Person/Organization/Product/Location"}}
            ],
            "relations": [
                {{"source": "实体A", "relation": "关系类型", "target": "实体B"}}
            ]
        }}
        """
        result = llm.generate(prompt, temperature=0)
        return json.loads(result)

    def build_graph(self, documents: list):
        """将文档转化为知识图谱"""
        with self.driver.session() as session:
            for doc in documents:
                data = self.extract_entities_relations(doc)

                # 创建实体节点
                for entity in data["entities"]:
                    session.run(
                        "MERGE (e:Entity {name: $name}) SET e.type = $type",
                        name=entity["name"], type=entity["type"]
                    )

                # 创建关系边
                for rel in data["relations"]:
                    session.run("""
                        MATCH (a:Entity {name: $source})
                        MATCH (b:Entity {name: $target})
                        MERGE (a)-[r:RELATION {type: $rel_type}]->(b)
                    """, source=rel["source"],
                         target=rel["target"],
                         rel_type=rel["relation"])

# 示例：构建公司知识图谱
builder = KnowledgeGraphBuilder("bolt://localhost:7687", "neo4j", "password")

docs = [
    "张三是阿里巴巴的CTO，负责技术战略",
    "阿里巴巴旗下有淘宝、天猫、支付宝等产品",
    "支付宝由彭蕾创立，现由韩歆毅担任CEO",
]
builder.build_graph(docs)
```

**Step 2：图检索查询**

```python
class GraphRAGRetriever:
    def __init__(self, driver, llm):
        self.driver = driver
        self.llm = llm

    def query_to_cypher(self, user_query: str) -> str:
        """将自然语言查询转为Cypher图查询"""
        prompt = f"""
        将以下问题转为Neo4j Cypher查询语句：

        问题：{user_query}

        图结构：节点(Entity)有name和type属性，关系(RELATION)有type属性

        只输出Cypher语句，不加解释：
        """
        return self.llm.generate(prompt, temperature=0).strip()

    def retrieve(self, user_query: str) -> list:
        """图检索 + 向量检索混合"""
        results = []

        # 1. 图检索：精确关系查询
        try:
            cypher = self.query_to_cypher(user_query)
            with self.driver.session() as session:
                graph_results = session.run(cypher).data()
                results.extend(graph_results)
        except Exception as e:
            print(f"图查询失败，降级到向量检索：{e}")

        # 2. 向量检索：语义相似度补充
        vector_results = vectordb.search(user_query, k=3)
        results.extend(vector_results)

        return results

    def multi_hop_reasoning(self, query: str, max_hops=3) -> str:
        """多跳推理：沿图关系路径推理"""
        # 提取问题中的实体
        entities = self.extract_entities(query)

        reasoning_chain = []
        for entity in entities:
            # 从实体出发，遍历K跳邻居
            cypher = f"""
            MATCH path = (start:Entity {{name: '{entity}'}})-[*1..{max_hops}]-(end:Entity)
            RETURN path, length(path) as hops
            ORDER BY hops
            LIMIT 20
            """
            with self.driver.session() as session:
                paths = session.run(cypher).data()
                reasoning_chain.extend(paths)

        return reasoning_chain
```

**Step 3：结合LLM生成**

```python
def graphrag_answer(user_query: str):
    retriever = GraphRAGRetriever(driver, llm)

    # 1. 多跳图检索
    graph_context = retriever.multi_hop_reasoning(user_query, max_hops=2)

    # 2. 格式化图上下文
    graph_text = format_graph_paths(graph_context)

    # 3. LLM生成
    prompt = f"""
    基于以下知识图谱信息回答问题：

    图谱信息（实体关系路径）：
    {graph_text}

    问题：{user_query}

    请基于上述关系链条进行推理并回答：
    """

    return llm.generate(prompt)

# 示例
answer = graphrag_answer("支付宝的创始人和阿里巴巴CTO是什么关系？")
# 推理路径：彭蕾 → 创立 → 支付宝 → 归属 → 阿里巴巴 ← 任职 → 张三(CTO)
# 回答："彭蕾创立了支付宝，支付宝隶属于阿里巴巴，张三是阿里巴巴的CTO，所以彭蕾和张三都服务于阿里巴巴体系..."
```

### 选型建议

```
问自己3个问题：

1. 问题需要多跳推理吗？
   例："A的老板的老板是谁？" → 需要 → 选GraphRAG

2. 实体间关系是核心信息吗？
   例：医药、法律、供应链 → 是 → 选GraphRAG

3. 数据是自由文本为主吗？
   例：文章、客服记录 → 是 → 选向量RAG

推荐：生产环境用混合方案（向量召回 + 图精排）
```

**面试话术：**
> "GraphRAG用知识图谱替代纯向量存储，核心优势是多跳推理和可解释性。实现分3步：LLM抽取实体关系建图、自然语言转Cypher图查询、沿关系路径推理生成答案。我用过混合方案：向量检索做宽召回，图遍历做精确关系推理，在医疗知识图谱项目中，多跳问题准确率从向量RAG的45%提升到GraphRAG的82%。代价是构建成本高，需要NER+关系抽取流程。"

</details>

---

## 15. Agentic RAG是什么？与普通RAG的区别？如何实现多跳推理？

<details>
<summary>💡 答案要点</summary>

**Agentic RAG = Agent主动控制检索策略，而非被动执行单次检索**

### 普通RAG vs Agentic RAG

```
普通RAG（被动）：
用户问 → 检索1次 → 固定Top-K → LLM生成
（检索策略固定，不管结果好不好）

Agentic RAG（主动）：
用户问 → Agent分析 → 决定是否检索/检索什么/怎么检索
         → 评估结果 → 决定是否再检索
         → 循环直到信息充分 → 生成
```

### 核心能力

```python
class AgenticRAG:
    """Agent主动控制检索的RAG系统"""

    def __init__(self, llm, vectordb, search_engine):
        self.llm = llm
        self.vectordb = vectordb
        self.search_engine = search_engine
        self.max_retrieval_rounds = 3

    def run(self, user_query: str) -> str:
        context = []
        retrieval_count = 0

        while retrieval_count < self.max_retrieval_rounds:
            # Step 1: Agent分析当前上下文，决定下一步
            decision = self.agent_decide(user_query, context)

            if decision["action"] == "answer":
                # 信息充分，直接回答
                break

            elif decision["action"] == "retrieve_vector":
                # 语义检索
                query = decision["query"]
                docs = self.vectordb.search(query, k=5)
                context.extend(docs)

            elif decision["action"] == "retrieve_web":
                # 实时网络检索
                query = decision["query"]
                docs = self.search_engine.search(query)
                context.extend(docs)

            elif decision["action"] == "decompose":
                # 分解子问题，分别检索
                sub_questions = decision["sub_questions"]
                for sq in sub_questions:
                    docs = self.vectordb.search(sq, k=3)
                    context.extend(docs)

            retrieval_count += 1

        # 最终生成
        return self.generate(user_query, context)

    def agent_decide(self, query: str, context: list) -> dict:
        """Agent决策：下一步做什么"""

        context_text = "\n".join(context[-5:]) if context else "无"

        prompt = f"""
        你是RAG系统的检索策略Agent。

        用户问题：{query}
        当前已检索到的信息：{context_text}

        请判断下一步操作（输出JSON）：

        选项：
        1. {{"action": "answer"}} - 信息已充分，可以回答
        2. {{"action": "retrieve_vector", "query": "检索词"}} - 需要语义检索
        3. {{"action": "retrieve_web", "query": "搜索词"}} - 需要最新网络信息
        4. {{"action": "decompose", "sub_questions": ["子问题1", "子问题2"]}} - 需要分解问题

        判断依据：
        - 当前信息能否回答问题？
        - 是否需要最新数据？
        - 问题是否包含多个子问题？

        输出：
        """

        result = self.llm.generate(prompt, temperature=0)
        return json.loads(result)

    def generate(self, query: str, context: list) -> str:
        """基于收集到的上下文生成最终答案"""
        ctx_text = "\n---\n".join(context)

        prompt = f"""
        基于以下信息回答问题：

        {ctx_text}

        问题：{query}

        请综合所有信息给出完整回答：
        """
        return self.llm.generate(prompt)

# 使用场景示例：复杂多步问题
rag = AgenticRAG(llm, vectordb, search_engine)

result = rag.run("比较GPT-4和Claude 3的价格，哪个更适合做长文档摘要？")

# Agent执行过程：
# 轮次1：retrieve_web("GPT-4最新价格 2024")  → 获取GPT-4价格
# 轮次2：retrieve_web("Claude 3 Opus价格")   → 获取Claude价格
# 轮次3：retrieve_vector("长文档摘要模型对比") → 获取性能对比
# → 信息充分，生成综合对比回答
```

### 多跳推理实现

```python
class MultiHopRAG:
    """多跳推理：每次检索结果作为下一次检索的输入"""

    def multi_hop_retrieve(self, query: str, max_hops=3) -> str:
        reasoning_trace = []
        current_query = query
        accumulated_context = []

        for hop in range(max_hops):
            # 检索当前子问题
            docs = self.vectordb.search(current_query, k=3)
            accumulated_context.extend(docs)

            # 评估是否已有足够信息
            eval_prompt = f"""
            原始问题：{query}
            已收集信息：{" ".join(accumulated_context)}

            判断（JSON）：
            1. 能直接回答原始问题吗？{{"can_answer": true}}
            2. 还需要追问什么？{{"can_answer": false, "next_question": "下一个子问题"}}
            """

            eval_result = json.loads(self.llm.generate(eval_prompt, temperature=0))

            if eval_result["can_answer"]:
                break  # 信息足够，停止检索

            # 继续追问
            current_query = eval_result["next_question"]
            reasoning_trace.append(f"Hop {hop+1}: {current_query}")

        print("推理链：", " → ".join(reasoning_trace))
        return self.generate(query, accumulated_context)

# 示例：
# 问题："参与过阿里投资的公司中，谁的CEO毕业于清华？"
# Hop 1: 检索"阿里巴巴投资的公司" → 找到饿了么、优酷等
# Hop 2: 检索"饿了么CEO教育背景" → 张旭豪复旦大学
# Hop 3: 检索"优酷CEO教育背景" → ...
# 逐步推理找到答案
```

**面试话术：**
> "Agentic RAG让Agent主动决策检索策略，而不是固定执行一次检索。我实现了3种决策：1）信息充分直接回答；2）需要最新信息走实时搜索；3）复杂问题先分解再分别检索。核心是Agent每轮评估'信息是否足够回答问题'，不够就继续检索，最多3轮避免无限循环。实测复杂多跳问题准确率从普通RAG的52%提升到Agentic RAG的78%。"

</details>

---

## 📝 速记卡片

| 概念 | 一句话解释 |
|------|------------|
| **RAG** | 先检索知识，再生成答案 |
| **Embedding** | 文本转语义向量 |
| **Embedding选型** | 中文bge-large-zh,多语言M3,预算足OpenAI |
| **余弦相似度** | 算向量接近程度（-1 到 1） |
| **向量数据库** | 专为"找相似"设计的数据库 |
| **Chunking** | 把长文档切成小块 |
| **混合检索** | 向量 + 关键词一起搜 |
| **GraphRAG** | 知识图谱+图遍历，多跳推理准确率+37% |
| **Agentic RAG** | Agent主动控制检索策略，动态多轮检索 |
| **Rerank** | 对检索结果重新排序 |
| **ANN** | 近似最近邻搜索，加速检索 |
| **Query改写** | 优化问题,补充上下文,HyDE生成假设答案 |
| **上下文压缩** | 提取相关片段,减少无效Token,降成本 |
| **Late Chunking** | 先embedding再切分,保留完整上下文 |
| **幻觉优化** | RAG提供证据+低Temperature+CoT推理，幻觉率<5% |
| **RAG效果提升** | 混合检索+Rerank+Query重写+上下文压缩四步走 |

---

## 高频追问：RAG 效果如何提升？出现幻觉怎么办？

### Q: RAG 效果不好如何排查和提升？

<details>
<summary>💡 答案要点</summary>

**效果问题诊断流程：**

```
RAG回答不好
    ├── 检索没找到相关内容（召回问题）
    │       ├── Embedding 模型不够好 → 换 bge-large-zh
    │       ├── Chunk 切分太大/太小 → 调整 chunk_size
    │       ├── 查询和文档表达不一致 → 加 Query 改写
    │       └── 只用向量检索 → 改混合检索（BM25 + 向量）
    │
    ├── 找到了但排序靠后（排序问题）
    │       └── 加 Rerank（BGE-Reranker/Cohere）
    │
    └── 找到了但模型没用上（生成问题）
            ├── Context 太长模型忽略 → 上下文压缩
            ├── Prompt 没引导好 → 优化 Prompt
            └── 模型能力不足 → 换更强模型
```

**四步优化组合拳：**

```python
# Step 1: Query 改写（解决表达不一致）
rewritten_query = await query_rewriter.rewrite(
    query=user_query,
    history=conversation_history
)

# Step 2: 混合检索（提升召回率）
vector_results = vector_db.search(rewritten_query, top_k=20)
bm25_results   = bm25_index.search(rewritten_query, top_k=20)
merged_results = rrf_merge(vector_results, bm25_results)  # RRF 融合

# Step 3: Rerank 精排（提升相关性）
reranked = reranker.rerank(
    query=rewritten_query,
    docs=merged_results,
    top_k=5  # 精选 top5
)

# Step 4: 上下文压缩（避免 Lost in Middle）
compressed = context_compressor.compress(
    query=rewritten_query,
    docs=reranked,
    max_tokens=2000
)

# 生成
answer = await llm.generate(query=user_query, context=compressed)
```

**各优化手段效果量化：**

| 优化手段 | 召回率提升 | 准确率提升 | 成本影响 |
|---------|-----------|-----------|---------|
| 混合检索（BM25+向量） | +20-30% | +15% | +10% |
| Query 改写 | +15-25% | +20% | +5% |
| Rerank | - | +25-35% | +15% |
| 上下文压缩 | - | +10-15% | -30% |
| **组合使用** | **+40%** | **+50%** | **+0%** |

**面试话术：**
> "RAG 效果优化我分三层诊断：召回层（混合检索+Query改写）、排序层（BGE-Reranker精排）、生成层（上下文压缩+Prompt优化）。实际项目中组合使用后准确率从 65% 提升到 88%，成本基本持平（压缩节省的抵消了Rerank的开销）。"

</details>

### Q: RAG 出现幻觉怎么办？

<details>
<summary>💡 答案要点</summary>

**幻觉来源分类：**

| 幻觉类型 | 原因 | 示例 |
|---------|------|------|
| **检索幻觉** | 检索内容不相关，模型自行编造 | 问A知识，找到B知识，模型混用 |
| **融合幻觉** | 多个 chunk 信息矛盾，模型错误融合 | 文档A说10%，文档B说20%，模型说15% |
| **过度推断幻觉** | 模型超出检索内容范围推断 | 文档说"可能"，模型断言"一定" |
| **记忆幻觉** | 模型用训练记忆覆盖检索内容 | 检索到最新数据，模型仍用旧知识 |

**对应解决方案：**

```python
class HallucinationGuard:
    """幻觉防护三层体系"""

    # Layer 1: 预防 - 让模型只能基于检索内容回答
    SYSTEM_PROMPT = """
    你只能根据提供的<context>内容回答问题。
    如果context中没有相关信息，回答"根据现有资料无法回答该问题"。
    不要推断或补充context中没有的信息。
    每个关键论断必须引用对应的context片段。
    """

    # Layer 2: 检测 - 答案与来源的一致性验证
    async def check_faithfulness(
        self, answer: str, sources: list[str]
    ) -> float:
        """RAGAS Faithfulness 评估：答案有多少来自检索内容"""
        prompt = f"""
        判断以下答案中的每个陈述是否能从来源文本中找到依据。
        答案：{answer}
        来源：{sources}
        输出 JSON: {{"faithful_score": 0.0-1.0, "unsupported_claims": []}}
        """
        result = await llm.complete(prompt)
        return result["faithful_score"]

    # Layer 3: 兜底 - 低置信度转人工
    async def safe_answer(self, query: str, context: list) -> str:
        answer = await llm.generate(query, context)
        score = await self.check_faithfulness(answer, context)

        if score < 0.7:
            # 置信度低 → 明确告知不确定
            return f"基于现有资料，{answer}（注：该回答置信度较低，建议人工核实）"
        return answer
```

**实际指标目标：**
```
幻觉率（Faithfulness < 0.7 的比例）：< 5%
RAGAS Faithfulness 均值：> 0.85
无法回答率（主动拒答）：5-15%（合理范围，优于编造）
```

**面试话术：**
> "RAG 幻觉我用三层防护：1) Prompt 层约束模型只能引用 context 内容，未找到时主动说'无法回答'；2) 低 Temperature（0.1-0.2）让模型保守生成；3) RAGAS Faithfulness 指标持续监控，评分<0.7 的回答标记为低置信度并转人工审核。生产环境幻觉率控制在 3% 以内。"

</details>

### Q9: RAG 系统的语义缓存（Semantic Cache）如何实现？有哪些关键问题？

<details>
<summary>💡 答案要点</summary>

**语义缓存 = 用语义相似度判断是否命中缓存**

**问题背景：**
- 传统缓存：精确匹配（相同问题 → 相同答案）
- 语义缓存：语义相似 → 相同答案

```
用户问题 A："如何优化 Python 代码性能？"
用户问题 B："Python 性能优化方法有哪些？"
→ 语义相似 → 命中缓存

用户问题 C："如何优化 Python 代码性能？"
用户问题 C 再次问："如何优化 Python 代码性能？"
→ 完全相同 → 精确命中
```

**核心挑战：**

| 挑战 | 说明 | 解决方案 |
|------|------|----------|
| **相似度阈值** | 设太高 → 命中率低；设太低 → 答案不相关 | 线上 A/B 测试调参 |
| **向量检索开销** | 每次请求都要做向量检索 | 粗排 + 精排 |
| **缓存失效** | 知识库更新后，缓存可能过期 | TTL + 版本号 |
| **多租户** | 不同用户看到不同答案 | 用户级缓存隔离 |

**实现架构：**
```
用户问题
    ↓
┌─────────────┐
│ Query 向量化 │ → embedding
└─────────────┘
    ↓
┌─────────────┐
│ 缓存命中判断 │ → 向量数据库检索 top-k
└─────────────┘
    ↓
命中？ → 是 → 返回缓存答案
    ↓ 否
┌─────────────┐
│ 正常 RAG 流程 │ → 执行检索 + 生成
└─────────────┘
    ↓
┌─────────────┐
│ 写入缓存    │ → 新问题 + 答案 → 向量存入
└─────────────┘
```

**实现示例：**
```python
import numpy as np

class SemanticCache:
    def __init__(self, threshold=0.85, ttl=3600):
        self.cache = []  # [(embedding, question, answer, timestamp)]
        self.threshold = threshold
        self.ttl = ttl
    
    def get(self, question, embedding):
        # 1. 向量检索
        scores = [cosine(e1, embedding) for e1, _, _, _ in self.cache]
        
        # 2. 找最佳匹配
        if not scores:
            return None
        
        best_idx = np.argmax(scores)
        best_score = scores[best_idx]
        
        # 3. 检查阈值和 TTL
        if best_score >= self.threshold:
            _, _, answer, timestamp = self.cache[best_idx]
            if time.time() - timestamp < self.ttl:
                return answer
        
        return None
    
    def set(self, question, embedding, answer):
        # 检查缓存大小，超限时淘汰最旧的
        if len(self.cache) > 10000:
            self.cache.pop(0)
        self.cache.append((embedding, question, answer, time.time()))
```

**性能对比：**

| 方案 | 命中率 | 延迟 | 成本 |
|------|--------|------|------|
| 无缓存 | 0% | 500ms | ¥0.01/次 |
| 精确缓存 | 10-20% | 10ms | ¥0.002/次 |
| **语义缓存** | **30-50%** | **50ms** | **¥0.005/次** |

**面试话术：**
> "语义缓存是 RAG 成本优化的杀手级功能。我实测命中率 30-50%，配合向量数据库（如 Qdrant）的 ANN 索引，缓存检索只要 50ms，比直接调用 LLM 快 10 倍。关键是相似度阈值要调好，我一般设 0.85——太高容易漏命中，太低答案不相关。"

</details>

---

**上一模块：** [Prompt 工程](../02-prompt-engineering/)
**下一模块：** [Transformer 架构](../04-transformer-architecture/)

---

[返回目录 →](../../README.md)
