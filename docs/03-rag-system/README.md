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
| **Rerank** | 对检索结果重新排序 |
| **ANN** | 近似最近邻搜索，加速检索 |
| **Query改写** | 优化问题,补充上下文,HyDE生成假设答案 |
| **上下文压缩** | 提取相关片段,减少无效Token,降成本 |
| **Late Chunking** | 先embedding再切分,保留完整上下文 |


---

**上一模块：** [Prompt 工程](../02-prompt-engineering/)
**下一模块：** [Transformer 架构](../04-transformer-architecture/)

---

[返回目录 →](../../README.md)
