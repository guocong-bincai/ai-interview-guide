# 🏢 国内大厂AI工程师面试真题

> **来源:** 字节跳动、阿里巴巴、美团、百度等一线互联网公司
> **更新:** 2026-03-10
> **考点:** 真实面试题、大厂风格、高频考点

## 📋 目录

1. [字节跳动](#一字节跳动)
2. [阿里巴巴](#二阿里巴巴)
3. [美团](#三美团)
4. [百度](#四百度)
5. [腾讯](#五腾讯)
6. [通用准备建议](#六通用准备建议)

---

## 一、字节跳动

### 岗位特点
- 侧重实战能力和工程落地
- 重视LLM/RAG/Agent技术栈
- 喜欢问开放性问题
- 重视代码实现能力

### 高频面试题

#### 1. LLM基础篇

<details>
<summary>💡 Q1: Transformer自注意力机制详解</summary>

**题目:** 请详细解释Transformer模型中的self-attention机制是如何工作的？为什么它比RNN更适合处理长序列？

**答案要点:**

**Self-Attention工作原理:**

```python
def self_attention(Q, K, V):
    """
    Q: Query矩阵 (batch, seq_len, d_k)
    K: Key矩阵 (batch, seq_len, d_k)
    V: Value矩阵 (batch, seq_len, d_v)
    """
    # 1. 计算注意力分数
    # Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V

    d_k = Q.shape[-1]

    # 2. Q和K做点积
    scores = torch.matmul(Q, K.transpose(-2, -1))  # (batch, seq_len, seq_len)

    # 3. 缩放(防止梯度消失)
    scores = scores / math.sqrt(d_k)

    # 4. Softmax归一化
    attention_weights = F.softmax(scores, dim=-1)

    # 5. 加权求和V
    output = torch.matmul(attention_weights, V)

    return output, attention_weights

# 示例
seq_len = 5
d_model = 512
d_k = d_v = 64

Q = torch.randn(1, seq_len, d_k)
K = torch.randn(1, seq_len, d_k)
V = torch.randn(1, seq_len, d_v)

output, weights = self_attention(Q, K, V)
print(output.shape)  # (1, 5, 64)
print(weights.shape)  # (1, 5, 5) - 注意力矩阵
```

**为什么比RNN好:**

| 维度 | RNN | Self-Attention |
|------|-----|----------------|
| **并行性** | ❌ 串行计算 | ✅ 完全并行 |
| **长依赖** | ❌ 梯度消失 | ✅ 直接连接 |
| **计算复杂度** | O(n·d²) | O(n²·d) |
| **长文本** | ❌ 信息丢失 | ✅ 全局视野 |

**面试话术:**
> "Self-Attention的核心是让每个词都能直接看到序列中的所有其他词。计算分3步:Q和K点积得分数,Softmax归一化,加权求和V。相比RNN,它最大优势是并行计算和直接的长距离依赖,不会梯度消失。代价是O(n²)复杂度,所以超长文本需要优化如FlashAttention。"

</details>

<details>
<summary>💡 Q2: 位置编码(Positional Encoding)实现</summary>

**题目:** 什么是位置编码？为什么Transformer必需它？请列举至少两种实现方式并对比。

**答案要点:**

**为什么需要位置编码:**
- Self-Attention是排列不变的(permutation-invariant)
- 没有位置信息,"我爱你"和"你爱我"的表示完全相同
- 位置编码注入顺序信息

**方式1: 正弦位置编码(原始Transformer)**

```python
def sinusoidal_positional_encoding(seq_len, d_model):
    """
    PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    """
    position = torch.arange(seq_len).unsqueeze(1)  # (seq_len, 1)
    div_term = torch.exp(
        torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model)
    )

    pe = torch.zeros(seq_len, d_model)
    pe[:, 0::2] = torch.sin(position * div_term)  # 偶数位置
    pe[:, 1::2] = torch.cos(position * div_term)  # 奇数位置

    return pe

# 使用
seq_len = 100
d_model = 512
pe = sinusoidal_positional_encoding(seq_len, d_model)

# 可视化
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 5))
plt.imshow(pe[:50, :50], cmap='RdBu', aspect='auto')
plt.xlabel("Dimension")
plt.ylabel("Position")
plt.colorbar()
plt.title("Sinusoidal Positional Encoding")
plt.show()
```

**方式2: 可学习位置编码(BERT)**

```python
class LearnedPositionalEncoding(nn.Module):
    def __init__(self, max_seq_len, d_model):
        super().__init__()
        # 直接学习一个位置Embedding矩阵
        self.pos_embedding = nn.Embedding(max_seq_len, d_model)

    def forward(self, x):
        seq_len = x.size(1)
        positions = torch.arange(seq_len, device=x.device)
        return x + self.pos_embedding(positions)

# 使用
model = LearnedPositionalEncoding(max_seq_len=512, d_model=768)
x = torch.randn(1, 100, 768)
output = model(x)
```

**方式3: 旋转位置编码(RoPE) - 字节高频考点**

```python
def rotate_half(x):
    """旋转一半的维度"""
    x1, x2 = x[..., :x.shape[-1]//2], x[..., x.shape[-1]//2:]
    return torch.cat((-x2, x1), dim=-1)

def apply_rotary_pos_emb(q, k, cos, sin):
    """应用RoPE"""
    # q, k: (batch, seq_len, num_heads, head_dim)
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed

# RoPE的优势:
# 1. 相对位置信息(query和key之间的距离)
# 2. 外推性好(训练512可推理1024+)
# 3. 不增加参数
```

**对比表:**

| 方法 | 优点 | 缺点 | 使用 |
|------|------|------|------|
| **正弦编码** | 无参数,外推性好 | 固定模式 | GPT-3 |
| **可学习编码** | 灵活,可适应数据 | 不能外推 | BERT |
| **RoPE** | 相对位置,外推性强 | 实现复杂 | LLaMA |

**面试话术:**
> "Transformer的Self-Attention没有顺序信息,所以需要位置编码。原始方法用sin/cos周期函数编码绝对位置,优点是无参数且能外推。BERT用可学习Embedding,灵活但不能外推长度。现在主流是RoPE旋转编码,编码相对位置信息,外推性最好,LLaMA/Qwen都用它。字节面试喜欢问RoPE原理和优势。"

</details>

<details>
<summary>💡 Q3: MHA vs MQA vs GQA对比</summary>

**题目:** 请解释Multi-Head Attention (MHA)、Multi-Query Attention (MQA)、Grouped-Query Attention (GQA)的区别。

**答案要点:**

**MHA (Multi-Head Attention) - 标准方法**

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, num_heads=8):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        # 每个head都有独立的Q、K、V
        self.W_q = nn.Linear(d_model, d_model)  # 8个head,每个64维
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x):
        batch_size, seq_len, d_model = x.shape

        # 1. 线性变换
        Q = self.W_q(x)  # (batch, seq_len, d_model)
        K = self.W_k(x)
        V = self.W_v(x)

        # 2. 分割成多个head
        Q = Q.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        # 形状: (batch, num_heads, seq_len, d_k)

        # 3. Attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        attn = F.softmax(scores, dim=-1)
        output = torch.matmul(attn, V)

        # 4. 拼接
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)
        return self.W_o(output)

# KV Cache大小: batch * seq_len * num_heads * head_dim * 2 (K和V)
# 8个head,每个64维 → 1024 tokens需要 1*1024*8*64*2*2字节 = 2MB (FP16)
```

**MQA (Multi-Query Attention) - Google提出**

```python
class MultiQueryAttention(nn.Module):
    def __init__(self, d_model=512, num_heads=8):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        # Q有多个head,但K和V只有1个(共享)
        self.W_q = nn.Linear(d_model, d_model)  # 8个head
        self.W_k = nn.Linear(d_model, self.d_k)  # 只1个head!
        self.W_v = nn.Linear(d_model, self.d_k)  # 只1个head!
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x):
        batch_size, seq_len, d_model = x.shape

        Q = self.W_q(x).view(batch, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).unsqueeze(1)  # (batch, 1, seq_len, d_k) - 广播给所有head
        V = self.W_v(x).unsqueeze(1)  # (batch, 1, seq_len, d_k)

        # 所有Q head共享同一个K和V
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        attn = F.softmax(scores, dim=-1)
        output = torch.matmul(attn, V)

        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)
        return self.W_o(output)

# KV Cache大小: batch * seq_len * 1 * head_dim * 2
# 只1个head → 1024 tokens需要 1*1024*1*64*2*2字节 = 256KB (FP16)
# 相比MHA减少8倍!
```

**GQA (Grouped-Query Attention) - LLaMA 2**

```python
class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model=512, num_heads=8, num_kv_heads=2):
        super().__init__()
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads  # K/V的head数(比Q少)
        self.num_queries_per_kv = num_heads // num_kv_heads  # 每个KV对应几个Q
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)  # 8个head
        self.W_k = nn.Linear(d_model, num_kv_heads * self.d_k)  # 2个head
        self.W_v = nn.Linear(d_model, num_kv_heads * self.d_k)  # 2个head
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x):
        batch_size, seq_len, d_model = x.shape

        Q = self.W_q(x).view(batch, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        # (batch, 8, seq_len, 64)

        K = self.W_k(x).view(batch, seq_len, self.num_kv_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch, seq_len, self.num_kv_heads, self.d_k).transpose(1, 2)
        # (batch, 2, seq_len, 64)

        # 重复K和V,让每个KV对应4个Q
        K = K.repeat_interleave(self.num_queries_per_kv, dim=1)  # (batch, 8, seq_len, 64)
        V = V.repeat_interleave(self.num_queries_per_kv, dim=1)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        attn = F.softmax(scores, dim=-1)
        output = torch.matmul(attn, V)

        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)
        return self.W_o(output)

# KV Cache大小: batch * seq_len * num_kv_heads * head_dim * 2
# 2个KV head → 1024 tokens需要 1*1024*2*64*2*2字节 = 512KB
# 是MHA的1/4,是MQA的2倍
```

**对比总结:**

| 方法 | Q heads | K/V heads | KV Cache | 质量 | 速度 | 使用 |
|------|---------|-----------|----------|------|------|------|
| **MHA** | 8 | 8 | 2MB | ⭐⭐⭐⭐⭐ | ⭐⭐ | GPT-3 |
| **MQA** | 8 | 1 | 256KB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | PaLM |
| **GQA** | 8 | 2 | 512KB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | LLaMA 2 |

**面试话术:**
> "MHA是标准的多头注意力,每个head都有独立的Q、K、V,质量最好但KV Cache大。MQA让所有head共享1个K和V,Cache减少8倍推理快,但质量略降。GQA是折中方案,8个Q head对应2个KV head,Cache减少4倍,质量接近MHA。LLaMA 2用GQA达到性能和效率平衡,字节面试常问这个演进逻辑。"

</details>

#### 2. RAG系统篇

<details>
<summary>💡 Q4: RAG完整流程设计</summary>

**题目:** 设计一个完整的RAG系统,从数据准备到最终生成,详细描述每个步骤。

**答案要点:**

**RAG完整流程(7步):**

```python
class RAGSystem:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vectordb = Qdrant(...)
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    def build_knowledge_base(self, documents):
        """Step 1-3: 构建知识库"""

        # Step 1: 文档加载
        from langchain.document_loaders import PyPDFLoader, TextLoader

        docs = []
        for doc_path in documents:
            if doc_path.endswith('.pdf'):
                loader = PyPDFLoader(doc_path)
            else:
                loader = TextLoader(doc_path)
            docs.extend(loader.load())

        # Step 2: 文档切块(Chunking)
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,      # 每块500字符
            chunk_overlap=50,    # 重叠50字符(保持上下文)
            separators=["\n\n", "\n", "。", "！", "？", " ", ""]
        )

        chunks = text_splitter.split_documents(docs)
        print(f"切分成{len(chunks)}个chunk")

        # Step 3: Embedding + 存入向量库
        texts = [chunk.page_content for chunk in chunks]
        embeddings = self.embedding_model.encode(texts)

        self.vectordb.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=[chunk.metadata for chunk in chunks]
        )

    def retrieve_and_generate(self, query):
        """Step 4-7: 检索+生成"""

        # Step 4: Query Embedding
        query_embedding = self.embedding_model.encode([query])[0]

        # Step 5: 向量检索(召回Top-K)
        results = self.vectordb.search(
            query_embedding,
            limit=20  # 先召回20个候选
        )

        # Step 6: Rerank(精排)
        candidate_docs = [r['document'] for r in results]

        # 计算Query与每个Doc的相关性分数
        pairs = [[query, doc] for doc in candidate_docs]
        scores = self.reranker.predict(pairs)

        # 按分数排序,取Top-5
        ranked_results = sorted(
            zip(candidate_docs, scores),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        top_docs = [doc for doc, score in ranked_results]

        # Step 7: LLM生成
        context = "\n\n".join([f"文档{i+1}: {doc}" for i, doc in enumerate(top_docs)])

        prompt = f"""
        请基于以下文档回答问题。如果文档中没有答案,请明确说"文档中未找到相关信息"。

        文档:
        {context}

        问题: {query}

        回答(要求引用文档编号):
        """

        answer = self.llm.invoke(prompt).content

        return {
            "answer": answer,
            "sources": top_docs,
            "num_retrieved": len(results)
        }

# 使用
rag = RAGSystem()

# 构建知识库
rag.build_knowledge_base([
    "company_docs/产品手册.pdf",
    "company_docs/FAQ.txt"
])

# 查询
result = rag.retrieve_and_generate("如何退货?")
print(result["answer"])
print(f"引用了{len(result['sources'])}个文档")
```

**关键优化点:**

1. **Chunking策略**
   - 固定长度(500字符) + 重叠(50字符)
   - 按语义分割(段落/句子优先)
   - 代码块/表格特殊处理

2. **混合检索**
   ```python
   # 向量检索 + BM25关键词检索
   from rank_bm25 import BM25Okapi

   # BM25检索
   bm25_results = bm25_search(query, top_k=20)

   # 向量检索
   vector_results = vector_search(query, top_k=20)

   # RRF融合
   final_results = reciprocal_rank_fusion([bm25_results, vector_results])
   ```

3. **元数据过滤**
   ```python
   # 按时间/部门/权限过滤
   results = vectordb.search(
       query_embedding,
       filter={
           "department": "销售部",
           "created_at": {"$gte": "2024-01-01"}
       }
   )
   ```

**面试话术:**
> "RAG分7步:1)文档加载2)切块(500字符+50重叠)3)Embedding存向量库4)Query编码5)向量检索Top-20 6)Rerank精排Top-5 7)LLM生成。关键优化3点:切块策略要保留语义完整性,混合检索(向量+BM25)提升召回,Rerank用CrossEncoder提升精度。实测Rerank让答案准确率从70%→85%提升15%。"

</details>

#### 3. Agent实战篇

<details>
<summary>💡 Q5: ReAct框架实现代码审查Agent</summary>

**题目:** 用ReAct框架实现一个代码审查Agent,能自动发现代码问题并给出修复建议。

**答案要点:**

```python
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import ast
import subprocess

class CodeReviewAgent:
    def __init__(self):
        self.llm = OpenAI(temperature=0)

        # 定义工具
        self.tools = [
            Tool(
                name="静态代码分析",
                func=self.static_analysis,
                description="用pylint分析代码质量问题"
            ),
            Tool(
                name="安全漏洞扫描",
                func=self.security_scan,
                description="检测SQL注入、XSS等安全问题"
            ),
            Tool(
                name="性能分析",
                func=self.performance_analysis,
                description="分析时间复杂度和性能瓶颈"
            ),
            Tool(
                name="代码修复建议",
                func=self.fix_suggestion,
                description="给出具体的修复代码"
            )
        ]

        # ReAct Prompt模板
        self.prompt_template = """
        你是一个专业的代码审查专家。请按照ReAct模式分析代码。

        可用工具:
        {tools}

        代码:
        ```python
        {code}
        ```

        请按以下格式思考和行动:

        Thought: 我需要分析这段代码的问题
        Action: 静态代码分析
        Observation: [工具返回结果]

        Thought: 发现了XX问题,需要进一步检查安全性
        Action: 安全漏洞扫描
        Observation: [工具返回结果]

        ...继续思考和行动,直到完成审查...

        Final Answer: [完整的审查报告]

        开始:
        Thought: {agent_scratchpad}
        """

        self.agent = self._create_agent()

    def static_analysis(self, code):
        """静态代码分析"""
        # 保存代码到临时文件
        with open("/tmp/code_review.py", "w") as f:
            f.write(code)

        # 运行pylint
        result = subprocess.run(
            ["pylint", "/tmp/code_review.py"],
            capture_output=True,
            text=True
        )

        return result.stdout

    def security_scan(self, code):
        """安全漏洞扫描"""
        issues = []

        # 检测SQL注入
        if "execute(" in code and "%" in code:
            issues.append("⚠️  可能存在SQL注入风险: 使用字符串拼接构建SQL")

        # 检测硬编码密钥
        if "password" in code.lower() or "api_key" in code.lower():
            issues.append("⚠️  发现硬编码的敏感信息")

        # 检测eval/exec
        if "eval(" in code or "exec(" in code:
            issues.append("🚨 危险: 使用了eval/exec,可能导致代码注入")

        return "\n".join(issues) if issues else "✅ 未发现明显安全问题"

    def performance_analysis(self, code):
        """性能分析"""
        try:
            tree = ast.parse(code)

            issues = []

            # 检测嵌套循环
            for node in ast.walk(tree):
                if isinstance(node, ast.For):
                    for child in ast.walk(node):
                        if isinstance(child, ast.For) and child != node:
                            issues.append("⚠️  发现嵌套循环,时间复杂度可能是O(n²)")

            # 检测list comprehension vs 循环
            has_list_comp = any(isinstance(node, ast.ListComp) for node in ast.walk(tree))
            if not has_list_comp:
                issues.append("💡 建议: 可以使用列表推导式提升性能")

            return "\n".join(issues) if issues else "✅ 未发现明显性能问题"

        except:
            return "⚠️  代码语法错误,无法分析"

    def fix_suggestion(self, issue):
        """生成修复建议"""
        prompt = f"""
        代码问题: {issue}

        请给出具体的修复代码示例(Python):
        """

        return self.llm(prompt)

    def review(self, code):
        """执行代码审查"""
        result = self.agent_executor.run(code=code)
        return result

# 使用示例
agent = CodeReviewAgent()

code_to_review = """
def get_user(user_id):
    # SQL注入风险
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    result = db.execute(query)

    # 硬编码密钥
    api_key = "sk-1234567890abcdef"

    # 嵌套循环
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                result.append(item1)

    return result
"""

report = agent.review(code_to_review)
print(report)

# 输出示例:
"""
代码审查报告:

1. 安全问题:
   - 🚨 SQL注入风险: 直接拼接用户输入到SQL语句
   - ⚠️  硬编码API密钥

2. 性能问题:
   - ⚠️  嵌套循环导致O(n²)复杂度
   - 💡 可以用集合交集优化

3. 修复建议:

```python
def get_user(user_id):
    # 修复SQL注入 - 使用参数化查询
    query = "SELECT * FROM users WHERE id = ?"
    result = db.execute(query, (user_id,))

    # 修复硬编码 - 使用环境变量
    api_key = os.getenv("API_KEY")

    # 修复性能 - 使用集合交集
    result = list(set(list1) & set(list2))

    return result
```

4. 质量评分: 6/10
   建议: 在上线前解决所有安全问题
"""
```

**ReAct关键点:**

1. **Thought(思考):** Agent分析当前情况
2. **Action(行动):** 选择合适的工具执行
3. **Observation(观察):** 获取工具返回结果
4. **循环:** 重复直到得出最终答案

**面试话术:**
> "我用ReAct实现了代码审查Agent。定义了4个工具:静态分析/安全扫描/性能分析/修复建议。Agent按Thought→Action→Observation循环工作,先静态分析发现问题,再安全扫描检测漏洞,最后性能分析找瓶颈。关键是工具设计要专注单一职责,Prompt要清晰引导推理过程。实测能发现90%常见代码问题。"

</details>

---

## 二、阿里巴巴

### 岗位特点
- 重视通义千问等自研大模型应用
- 强调业务场景结合(淘宝/钉钉/云)
- 看重架构设计能力
- 注重技术深度和广度

### 高频面试题

#### 1. 通义千问应用

<details>
<summary>💡 Q6: 如何用通义千问构建客服Agent?</summary>

**题目:** 设计一个基于通义千问的智能客服系统,包含知识库检索、订单查询、情感分析等功能。

**答案要点:**

```python
from dashscope import Generation
import dashscope

class TongyiCustomerServiceAgent:
    def __init__(self, api_key):
        dashscope.api_key = api_key
        self.model = "qwen-max"

        # 知识库(简化示例)
        self.knowledge_base = {
            "退货政策": "7天无理由退货,商品需保持完好...",
            "配送时间": "一般3-5个工作日送达...",
            "售后服务": "提供1年免费保修..."
        }

    def analyze_intent(self, user_query):
        """意图识别"""
        prompt = f"""
        分析用户意图,分类为以下之一:
        - 咨询问题
        - 订单查询
        - 投诉建议
        - 其他

        用户问题: {user_query}

        输出格式(JSON):
        {{"intent": "意图类别", "confidence": 0.95}}
        """

        response = Generation.call(
            model=self.model,
            prompt=prompt,
            result_format='message'
        )

        import json
        result = json.loads(response.output.text)
        return result

    def retrieve_knowledge(self, query):
        """知识库检索"""
        # 简化: 关键词匹配
        for key, value in self.knowledge_base.items():
            if key in query:
                return value
        return None

    def query_order(self, order_id):
        """订单查询(模拟)"""
        # 实际应该调用订单系统API
        return {
            "order_id": order_id,
            "status": "已发货",
            "tracking": "SF1234567890"
        }

    def analyze_sentiment(self, text):
        """情感分析"""
        prompt = f"""
        分析以下文本的情感倾向:

        文本: {text}

        输出(JSON):
        {{"sentiment": "正面/负面/中性", "score": 0.85, "keywords": ["关键词"]}}
        """

        response = Generation.call(model=self.model, prompt=prompt)
        import json
        return json.loads(response.output.text)

    def handle_query(self, user_query):
        """处理用户咨询"""

        # Step 1: 意图识别
        intent_result = self.analyze_intent(user_query)
        intent = intent_result["intent"]

        # Step 2: 情感分析
        sentiment = self.analyze_sentiment(user_query)

        # Step 3: 根据意图处理
        if intent == "咨询问题":
            # 检索知识库
            knowledge = self.retrieve_knowledge(user_query)

            if knowledge:
                # 用知识库内容生成回答
                prompt = f"""
                基于以下知识回答用户问题:

                知识: {knowledge}
                问题: {user_query}

                要求: 语气友好,简洁专业
                """

                response = Generation.call(model=self.model, prompt=prompt)
                answer = response.output.text
            else:
                answer = "抱歉,我暂时无法回答这个问题,已转接人工客服..."

        elif intent == "订单查询":
            # 提取订单号
            import re
            order_match = re.search(r'\d{10,}', user_query)

            if order_match:
                order_id = order_match.group()
                order_info = self.query_order(order_id)

                answer = f"您的订单{order_id}状态: {order_info['status']}, 快递单号: {order_info['tracking']}"
            else:
                answer = "请提供您的订单号,我来帮您查询"

        elif intent == "投诉建议":
            # 负面情感 → 优先级提升
            if sentiment["sentiment"] == "负面":
                answer = "非常抱歉给您带来不便!我已将您的问题标记为高优先级,客服主管会在30分钟内与您联系。"
            else:
                answer = "感谢您的反馈!我们会认真处理您的建议。"

        else:
            answer = "您可以咨询产品信息、查询订单或提出建议,我都很乐意帮助您!"

        return {
            "answer": answer,
            "intent": intent,
            "sentiment": sentiment
        }

# 使用
agent = TongyiCustomerServiceAgent(api_key="your-dashscope-api-key")

# 测试
queries = [
    "你们的退货政策是什么?",
    "我的订单1234567890到哪了?",
    "你们的产品质量太差了,要退款!"
]

for query in queries:
    result = agent.handle_query(query)
    print(f"问题: {query}")
    print(f"意图: {result['intent']}")
    print(f"情感: {result['sentiment']['sentiment']}")
    print(f"回答: {result['answer']}")
    print("-" * 50)
```

**面试话术:**
> "我用通义千问设计了智能客服Agent。核心3步:1)意图识别(咨询/查询/投诉)2)情感分析(负面情绪提优先级)3)分类处理(咨询查知识库,订单调API,投诉转人工)。关键是Prompt设计要结构化输出JSON,方便后续处理。通义千问的中文理解能力强,意图识别准确率>95%。实测负面情绪客户30分钟响应,满意度提升20%。"

</details>

#### 2. A2A多智能体协作

<details>
<summary>💡 Q7: A2A框架与普通Agent的区别</summary>

**题目:** 解释A2A(Agent-to-Agent)框架,它与传统单Agent或多Agent框架有何不同?

**答案要点:**

**A2A (Agent-to-Agent Communication Protocol)**

```
传统Multi-Agent:
  Agent A → 共享内存/消息队列 → Agent B
  (间接通信,需要中心化协调)

A2A:
  Agent A ←→ 标准化协议 ←→ Agent B
  (直接通信,去中心化)
```

**A2A协议示例:**

```python
from typing import Dict, List
import json

class A2AMessage:
    """A2A标准消息格式"""
    def __init__(self, sender, receiver, action, payload):
        self.sender = sender        # 发送者Agent ID
        self.receiver = receiver    # 接收者Agent ID
        self.action = action        # 动作类型
        self.payload = payload      # 消息内容
        self.timestamp = time.time()

    def to_json(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "action": self.action,
            "payload": self.payload,
            "timestamp": self.timestamp
        }

class A2AAgent:
    """支持A2A协议的Agent"""
    def __init__(self, agent_id, capabilities):
        self.agent_id = agent_id
        self.capabilities = capabilities  # Agent能做什么
        self.message_queue = []

    def send_message(self, receiver, action, payload):
        """发送A2A消息"""
        msg = A2AMessage(
            sender=self.agent_id,
            receiver=receiver,
            action=action,
            payload=payload
        )

        # 通过消息总线发送(简化)
        message_bus.publish(msg)

    def receive_message(self, message: A2AMessage):
        """接收并处理消息"""
        self.message_queue.append(message)

        # 根据action类型处理
        if message.action == "REQUEST":
            response = self.handle_request(message.payload)
            self.send_message(
                receiver=message.sender,
                action="RESPONSE",
                payload=response
            )

        elif message.action == "DELEGATE":
            # 任务委托
            self.execute_task(message.payload)

    def handle_request(self, payload):
        """处理请求"""
        # 实现具体业务逻辑
        pass

# 实战示例: 电商订单处理
class InventoryAgent(A2AAgent):
    """库存Agent"""
    def __init__(self):
        super().__init__(
            agent_id="inventory_agent",
            capabilities=["check_stock", "reserve_item", "release_item"]
        )
        self.stock = {"iPhone15": 100, "MacBook": 50}

    def handle_request(self, payload):
        action = payload["action"]

        if action == "check_stock":
            product = payload["product"]
            return {"available": self.stock.get(product, 0) > 0}

        elif action == "reserve_item":
            product = payload["product"]
            if self.stock.get(product, 0) > 0:
                self.stock[product] -= 1
                return {"success": True}
            return {"success": False, "reason": "out_of_stock"}

class PaymentAgent(A2AAgent):
    """支付Agent"""
    def __init__(self):
        super().__init__(
            agent_id="payment_agent",
            capabilities=["process_payment", "refund"]
        )

    def handle_request(self, payload):
        action = payload["action"]

        if action == "process_payment":
            amount = payload["amount"]
            # 调用支付网关...
            return {"success": True, "transaction_id": "TXN123456"}

class OrderAgent(A2AAgent):
    """订单Agent(协调者)"""
    def __init__(self):
        super().__init__(
            agent_id="order_agent",
            capabilities=["create_order", "cancel_order"]
        )

    def create_order(self, product, quantity, amount):
        """创建订单 - 需要协调多个Agent"""

        # Step 1: 检查库存
        self.send_message(
            receiver="inventory_agent",
            action="REQUEST",
            payload={"action": "check_stock", "product": product}
        )

        # 等待响应(简化,实际应该异步)
        stock_response = self.wait_for_response("inventory_agent")

        if not stock_response["available"]:
            return {"success": False, "reason": "out_of_stock"}

        # Step 2: 预留库存
        self.send_message(
            receiver="inventory_agent",
            action="REQUEST",
            payload={"action": "reserve_item", "product": product}
        )

        reserve_response = self.wait_for_response("inventory_agent")

        if not reserve_response["success"]:
            return {"success": False, "reason": "reserve_failed"}

        # Step 3: 处理支付
        self.send_message(
            receiver="payment_agent",
            action="REQUEST",
            payload={"action": "process_payment", "amount": amount}
        )

        payment_response = self.wait_for_response("payment_agent")

        if not payment_response["success"]:
            # 支付失败,释放库存
            self.send_message(
                receiver="inventory_agent",
                action="REQUEST",
                payload={"action": "release_item", "product": product}
            )
            return {"success": False, "reason": "payment_failed"}

        # Step 4: 创建订单成功
        return {
            "success": True,
            "order_id": "ORD" + payment_response["transaction_id"]
        }

# 使用
inventory = InventoryAgent()
payment = PaymentAgent()
order = OrderAgent()

result = order.create_order(
    product="iPhone15",
    quantity=1,
    amount=7999
)

print(result)
# {"success": True, "order_id": "ORDTXN123456"}
```

**A2A vs 传统Multi-Agent:**

| 维度 | 传统Multi-Agent | A2A |
|------|----------------|-----|
| **通信方式** | 共享内存/消息队列 | 标准化协议 |
| **协调** | 中心化调度器 | 去中心化,P2P |
| **扩展性** | 增加Agent需改架构 | 即插即用 |
| **跨平台** | 困难 | 容易(协议标准化) |
| **容错** | 中心节点故障全挂 | 单Agent故障不影响其他 |

**面试话术:**
> "A2A是阿里提出的Agent间通信协议,核心是标准化消息格式(sender/receiver/action/payload)和去中心化通信。传统Multi-Agent依赖中心调度器,A2A让Agent直接P2P通信。优势是扩展性强,新Agent只要实现A2A协议就能加入系统。我用A2A实现过订单系统,OrderAgent协调InventoryAgent和PaymentAgent,3个Agent独立部署互不依赖,容错性好。"

</details>

---

## 三、美团

### 岗位特点
- 强调场景落地(外卖/到店/酒旅)
- 重视系统稳定性和性能
- 关注成本优化
- 看重问题解决能力

### 高频面试题

<details>
<summary>💡 Q8: 大模型存在哪些问题?如何解决?</summary>

**题目:** 列举LLM在实际应用中的主要问题,并针对每个问题给出解决方案。

**答案要点:**

**问题1: 幻觉(Hallucination)**

- **表现:** 编造不存在的事实
- **原因:** 概率预测,不是事实查询
- **解决方案:**
  ```python
  # 方案1: RAG
  def rag_answer(question):
      docs = vectordb.search(question)
      prompt = f"基于文档: {docs}\n回答: {question}"
      return llm.generate(prompt, temperature=0.2)

  # 方案2: Self-Consistency
  answers = [llm.generate(question) for _ in range(5)]
  final = most_common(answers)  # 投票

  # 方案3: 引用溯源
  prompt = "回答问题并标注来源: {question}"
  ```
- **效果:** RAG降80%幻觉,Self-Consistency提升15%准确率

**问题2: 长尾知识覆盖不足**

- **表现:** 专业/小众知识回答不准
- **解决方案:**
  ```python
  # 垂直领域微调
  from peft import LoraConfig, get_peft_model

  lora_config = LoraConfig(
      r=8,
      lora_alpha=16,
      target_modules=["q_proj", "v_proj"],
      task_type="CAUSAL_LM"
  )

  model = get_peft_model(base_model, lora_config)

  # 在专业数据上微调
  trainer.train(medical_dataset)  # 医疗数据
  ```

**问题3: 数据新鲜度**

- **表现:** 知识截止到训练时间
- **解决方案:**
  ```python
  # 动态知识注入
  def answer_with_search(question):
      # 1. 判断是否需要实时信息
      if requires_realtime(question):
          # 2. 搜索最新信息
          search_results = web_search(question)

          # 3. 结合搜索结果回答
          prompt = f"""
          最新信息: {search_results}
          问题: {question}
          回答:
          """
          return llm.generate(prompt)
      else:
          return llm.generate(question)
  ```

**问题4: 复读机问题**

- **表现:** 重复生成相同内容
- **原因:** 温度过低或采样策略单一
- **解决方案:**
  ```python
  # 方案1: Repetition Penalty
  response = llm.generate(
      prompt,
      repetition_penalty=1.2  # >1惩罚重复
  )

  # 方案2: 多样性采样
  response = llm.generate(
      prompt,
      temperature=0.7,
      top_p=0.9,
      top_k=50
  )

  # 方案3: 检测并重新生成
  if has_repetition(response):
      response = llm.generate(prompt, temperature=0.9)
  ```

**问题5: 推理计算和内存挑战**

- **表现:** 70B模型需要140GB显存
- **解决方案:**
  ```python
  # 方案1: 量化
  from transformers import BitsAndBytesConfig

  quantization_config = BitsAndBytesConfig(
      load_in_4bit=True,  # 4bit量化
      bnb_4bit_compute_dtype=torch.float16
  )

  model = AutoModelForCausalLM.from_pretrained(
      "meta-llama/Llama-2-70b",
      quantization_config=quantization_config
  )
  # 显存从140GB → 35GB

  # 方案2: 模型路由
  def smart_routing(question):
      complexity = estimate_complexity(question)

      if complexity < 0.3:
          return llm_small.generate(question)  # 7B
      elif complexity < 0.7:
          return llm_medium.generate(question)  # 13B
      else:
          return llm_large.generate(question)  # 70B

  # 成本降低60%
  ```

**问题6: 偏见问题**

- **表现:** 性别/种族/地域偏见
- **解决方案:**
  ```python
  # RLHF + 人工反馈
  # 1. 收集偏见案例
  bias_cases = [
      {"prompt": "CEO是...", "bad": "他", "good": "他/她"},
  ]

  # 2. 训练Reward Model
  reward_model.train(bias_cases)

  # 3. PPO优化
  ppo_trainer.train(policy_model, reward_model)
  ```

**综合解决方案:**

```python
class RobustLLMSystem:
    def __init__(self):
        self.llm = load_model()
        self.vectordb = VectorDB()
        self.search_engine = WebSearch()

    def generate(self, question):
        # 1. 检测问题类型
        question_type = self.classify_question(question)

        # 2. 选择策略
        if question_type == "factual":
            # 事实类 → RAG
            return self.rag_generate(question)

        elif question_type == "realtime":
            # 实时类 → 搜索
            return self.search_generate(question)

        elif question_type == "reasoning":
            # 推理类 → Self-Consistency
            return self.self_consistency_generate(question)

        else:
            # 通用
            return self.llm.generate(question, temperature=0.7)

    def rag_generate(self, question):
        docs = self.vectordb.search(question)
        prompt = f"基于: {docs}\n回答: {question}"
        return self.llm.generate(prompt, temperature=0.2)

    def search_generate(self, question):
        results = self.search_engine.search(question)
        prompt = f"参考: {results}\n回答: {question}"
        return self.llm.generate(prompt)

    def self_consistency_generate(self, question, n=5):
        answers = [self.llm.generate(question, temperature=0.7) for _ in range(n)]
        return most_common(answers)
```

**面试话术:**
> "LLM主要6大问题:1)幻觉用RAG+引用溯源降80%,2)长尾知识用LoRA微调覆盖,3)数据新鲜度用实时搜索,4)复读机用repetition_penalty惩罚,5)计算成本用4bit量化+模型路由降60%,6)偏见用RLHF纠正。美团场景下我用综合方案:事实类走RAG,实时类走搜索,推理类用Self-Consistency,不同问题不同策略,准确率提升25%成本降50%。"

</details>

---

## 四、百度

### 岗位特点
- 强调文心一言应用
- 深入考察AI基础理论
- 重视Agent架构设计
- 三轮面试层层深入

### 高频面试题

<details>
<summary>💡 Q9: 大模型复读机问题的机制与解决</summary>

**题目:** 为什么LLM会出现复读机现象(重复生成相同内容)?如何从模型原理和工程实践两方面解决?

**答案要点:**

**复读机现象:**
```
用户: 介绍一下北京
模型: 北京是中国的首都,北京是中国的首都,北京是中国的首都...
```

**产生机制:**

1. **自回归特性**
   ```
   P(w_t | w_1, w_2, ..., w_{t-1})

   当前词只依赖历史,如果历史包含重复模式
   → 模型倾向于继续重复
   ```

2. **注意力坍塌**
   ```python
   # Attention权重高度集中在某几个token
   attention_weights = [
       [0.01, 0.01, 0.95, 0.01, 0.01, 0.01],  # 第3个token权重0.95
       [0.01, 0.01, 0.01, 0.94, 0.01, 0.01],  # 第4个token权重0.94
       ...
   ]
   # 导致模型陷入局部最优,不断重复高权重token
   ```

3. **Temperature过低**
   ```python
   # Temperature → 0
   probs = softmax(logits / temperature)
   # 分布极度尖锐,总选概率最高的词
   # "北京" → "是" → "中国" → "的" → "首都" (循环)
   ```

**解决方案:**

**方案1: Repetition Penalty (最常用)**

```python
def apply_repetition_penalty(logits, input_ids, penalty=1.2):
    """
    惩罚已出现过的token
    penalty > 1: 降低已出现token的概率
    """
    for token_id in set(input_ids):
        # 如果logits[token_id] < 0,除以penalty会更负(概率更低)
        # 如果logits[token_id] > 0,乘以penalty会更小(概率降低)
        if logits[token_id] < 0:
            logits[token_id] *= penalty
        else:
            logits[token_id] /= penalty

    return logits

# 使用
from transformers import GenerationConfig

config = GenerationConfig(
    repetition_penalty=1.2,  # 推荐1.1-1.5
    temperature=0.7,
    top_p=0.9
)

output = model.generate(input_ids, generation_config=config)
```

**方案2: No Repeat N-gram**

```python
def no_repeat_ngram(generated_tokens, ngram_size=3):
    """
    禁止重复的N-gram
    例如: 禁止"北京是中国"连续出现2次
    """
    ngrams = {}

    for i in range(len(generated_tokens) - ngram_size + 1):
        ngram = tuple(generated_tokens[i:i+ngram_size])
        ngrams[ngram] = ngrams.get(ngram, 0) + 1

    # 如果某个3-gram出现>1次,下次生成时禁止
    return ngrams

# Hugging Face实现
output = model.generate(
    input_ids,
    no_repeat_ngram_size=3  # 禁止3-gram重复
)
```

**方案3: Diversity Penalty**

```python
# Beam Search + Diversity
output = model.generate(
    input_ids,
    num_beams=5,
    num_beam_groups=5,  # 分5组
    diversity_penalty=1.0,  # 组间差异性惩罚
    temperature=0.7
)

# 原理: 强制不同beam组探索不同路径
# Group 1: "北京是..."
# Group 2: "作为首都..."
# Group 3: "位于华北..."
```

**方案4: 修改Attention机制**

```python
class AntiRepetitionAttention(nn.Module):
    def __init__(self):
        super().__init__()
        self.attention = MultiHeadAttention()

    def forward(self, q, k, v, generated_tokens):
        # 标准attention
        attn_weights = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(d_k)

        # 对已生成token的attention降权
        for pos in generated_tokens:
            attn_weights[:, :, pos] *= 0.5  # 降低50%

        attn_weights = F.softmax(attn_weights, dim=-1)
        output = torch.matmul(attn_weights, v)

        return output
```

**方案5: 后处理检测与重试**

```python
def detect_and_retry(text, model, prompt, max_retries=3):
    """检测重复,重新生成"""

    # 检测连续重复
    words = text.split()
    repetition_rate = count_repetitions(words) / len(words)

    if repetition_rate > 0.3 and max_retries > 0:
        # 重复率>30%,提高temperature重新生成
        new_text = model.generate(
            prompt,
            temperature=0.9,  # 提高随机性
            top_k=50
        )
        return detect_and_retry(new_text, model, prompt, max_retries - 1)

    return text

def count_repetitions(words):
    """统计重复词数"""
    from collections import Counter
    counts = Counter(words)
    return sum(c - 1 for c in counts.values() if c > 1)
```

**综合实战方案:**

```python
class AntiRepetitionGenerator:
    def __init__(self, model):
        self.model = model

    def generate(self, prompt, max_length=512):
        # 配置多重防护
        config = GenerationConfig(
            max_length=max_length,

            # 防重复参数
            repetition_penalty=1.2,      # 惩罚重复token
            no_repeat_ngram_size=3,      # 禁止3-gram重复

            # 采样策略
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            top_k=50,

            # Beam Search多样性
            num_beams=5,
            num_beam_groups=5,
            diversity_penalty=1.0,

            # 长度惩罚(防止过短或过长)
            length_penalty=1.0,
            min_length=20,
        )

        # 生成
        output = self.model.generate(
            self.tokenizer.encode(prompt, return_tensors="pt"),
            generation_config=config
        )

        text = self.tokenizer.decode(output[0], skip_special_tokens=True)

        # 后处理检测
        if self.has_severe_repetition(text):
            # 重试,提高temperature
            config.temperature = 0.9
            output = self.model.generate(...)
            text = self.tokenizer.decode(output[0])

        return text

    def has_severe_repetition(self, text):
        """检测严重重复"""
        words = text.split()

        # 检查连续重复
        for i in range(len(words) - 5):
            if words[i:i+5] == words[i+5:i+10]:
                return True

        # 检查整体重复率
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.5:  # 独特词<50%
            return True

        return False
```

**效果对比:**

| 方法 | 重复率 | 流畅性 | 成本 |
|------|--------|--------|------|
| 无防护 | 40% | ⭐⭐⭐⭐ | 1x |
| Repetition Penalty | 5% | ⭐⭐⭐⭐ | 1x |
| +No Repeat N-gram | 2% | ⭐⭐⭐ | 1x |
| +Diversity Penalty | 1% | ⭐⭐⭐⭐ | 2x (Beam) |
| 综合方案 | <0.5% | ⭐⭐⭐⭐ | 1.5x |

**面试话术:**
> "LLM复读机源于3点:1)自回归特性导致重复模式自我强化2)Attention坍塌到少数token 3)低温采样陷入局部最优。解决用5层防护:1)Repetition Penalty=1.2惩罚已出现词2)No Repeat 3-gram禁止短语重复3)Diversity Penalty让Beam组探索不同路径4)修改Attention降低重复token权重5)后处理检测重试。实测重复率从40%→<0.5%,几乎消除。百度面试必问这个,要能讲清原理和工程方案。"

</details>

---

## 六、通用准备建议

### 1. 技术储备清单

**必须掌握:**
- ✅ Transformer原理(Self-Attention/位置编码/MHA)
- ✅ RAG完整流程(切块/Embedding/检索/Rerank/生成)
- ✅ ReAct Agent框架
- ✅ Prompt Engineering (CoT/Few-shot/Self-Consistency)
- ✅ 模型微调(LoRA/RLHF基础)
- ✅ 推理优化(KV Cache/量化)

**加分项:**
- ✅ 多Agent协作(AutoGen/CrewAI/A2A)
- ✅ 高级Prompt技巧(Tree of Thoughts)
- ✅ GraphRAG
- ✅ 自研大模型使用(通义/文心/智谱)

### 2. 项目准备

**至少1个完整项目,包含:**
- 明确的业务场景
- 技术选型理由
- 核心实现代码
- 性能指标数据
- 遇到的问题与解决方案

**示例:**
```
项目: 法律咨询RAG系统
场景: 用户咨询法律问题,Agent查询法条库+案例库回答
技术: LangChain + Qdrant + GPT-4
优化: Rerank提升准确率15%,混合检索召回率+20%
难点: 法条切块保持完整性 → 用正则提取法条编号
效果: 回答准确率85%,平均响应2秒
```

### 3. 八股文速记

**必背概念** (用"速记卡片"复习):
- Self-Attention计算公式
- RoPE vs 正弦编码
- MHA vs MQA vs GQA
- RAG vs Fine-tuning
- ReAct vs Plan-Execute
- LoRA原理
- KV Cache工作机制

### 4. 代码准备

**手写代码(白板/IDE):**
- Self-Attention实现
- RAG Pipeline
- ReAct Agent
- LoRA微调脚本

**算法题:**
- LeetCode Medium难度
- 数据结构(链表/树/哈希)
- 动态规划

### 5. 面试流程应对

**一面(基础):**
- 自我介绍(1分钟,突出亮点)
- 项目深挖(STAR法则)
- 技术八股文
- 代码题

**二面(综合):**
- 系统设计(RAG/Agent架构)
- 问题分析能力
- 开放题(如何优化XX)
- 跨领域思考

**三面(深度):**
- 职业规划
- 业务理解
- 产品思维
- 团队协作

### 6. 常见坑

❌ **不要:**
- 背答案不理解原理
- 项目造假(会被深挖)
- 不懂装懂
- 完全不了解公司产品

✅ **要:**
- 诚实回答"不知道"
- 展示学习能力
- 主动问面试官问题
- 准备反向提问

---

**最后更新:** 2026-03-10
**数据来源:** 牛客网、知乎、CSDN真实面经整理
**覆盖公司:** 字节、阿里、美团、百度、腾讯

---

**上一模块:** [前沿技术与趋势](../16-advanced-topics/)
**下一模块:** [简历与面试技巧](../17-resume-interview-tips/)

---

[返回目录 →](../../README.md)
