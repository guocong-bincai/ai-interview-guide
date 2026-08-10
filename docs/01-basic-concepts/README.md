# 📌 LLM 基础概念

## 1. Token 是什么？

**Token** 是 LLM 处理文本的基本单位（不是字，也不是词）。

| 语言 | 换算关系 |
|------|----------|
| 英文 | 1 token ≈ 4 个字符 ≈ 0.75 个单词 |
| 中文 | 1 个汉字 ≈ 1-2 个 tokens |

**例子：**
```
"你好世界" → 4-6 个 tokens
"Hello World" → 2-3 个 tokens
```

**影响：**
- 计费按 token 计算
- 上下文限制按 token 计算
- 生成长度按 token 计算

## 2. Temperature、Top-P、Top-K

### Temperature（温度）

控制输出的随机性：

| 值 | 效果 | 适用场景 |
|----|------|----------|
| 0 | 确定性输出 | 问答、代码生成 |
| 0.3-0.7 | 适度随机 | 通用对话 |
| 0.7-1.0 | 高随机性 | 创意写作 |

### Top-P（核采样）

只从累积概率 > P 的词里采样：
- Top-P = 0.9：从前 90% 概率的词里选
- 比 Top-K 更灵活

### Top-K

只从概率最高的 K 个词里采样：
- Top-K = 50：只从前 50 个候选词里选

### 推荐配置

```python
# RAG/问答
Temperature=0, Top-P=0.9

# 创意写作
Temperature=0.7, Top-P=0.9

# 代码生成
Temperature=0.2, Top-P=0.95
```

## 3. Context Window（上下文窗口）

**定义：** LLM 一次能处理的总 token 数（输入 + 输出）。

| 模型 | 上下文限制 |
|------|------------|
| GPT-4o | 128K |
| GPT-3.5 | 16K |
| Claude | 200K |
| 开源模型 | 4K-32K |

### 超出限制的解决方案

1. **截断** - 保留最近的对话
2. **总结** - 用 LLM 总结历史对话
3. **滑动窗口** - 只保留最近 N 轮
4. **向量检索** - 把历史存向量库，按需检索
5. **分层摘要** - 重要信息摘要 + 最近对话原文

## 4. 常见模型对比

| 模型 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| GPT-4o | 效果最好 | 贵 | 复杂任务 |
| GPT-3.5 | 便宜，快 | 效果一般 | 简单问答 |
| Claude | 上下文大 | 国内访问慢 | 长文档处理 |
| DeepSeek | 中文好，便宜 | 生态少 | 中文场景 |
| Llama 3 | 开源，可本地 | 需要 GPU | 私有部署 |

## 5. 幻觉（Hallucination）

**定义：** 模型编造不存在的信息。

### 减少幻觉的方法

1. **RAG** - 基于检索内容回答
2. **Prompt 约束** - "不要编造，不知道就说不知道"
3. **引用溯源** - 要求标注来源
4. **温度调低** - Temperature < 0.3
5. **人工审核** - 关键场景人工复核

## 📝 面试题

**Q: LLM 的 Token 是什么？中文和英文有什么区别？**

<details>
<summary>💡 参考答案</summary>

- Token 是 LLM 处理文本的基本单位
- 英文：1 token ≈ 4 个字符 ≈ 0.75 个单词
- 中文：1 个汉字 ≈ 1-2 个 tokens
- 影响：计费、上下文限制、生成长度都按 token 算

</details>

---

## 11. 什么是涌现能力(Emergent Abilities)?

**涌现能力** = 模型规模达到一定阈值后,突然出现的新能力

###典型的涌现能力

<details>
<summary>💡 答案要点</summary>

| 能力 | 出现阈值 | 示例 |
|------|----------|------|
| **上下文学习** | 100B+ 参数 | Few-shot学习无需微调 |
| **复杂推理** | 100B+ 参数 | Chain of Thought推理 |
| **指令遵循** | 10B+ 参数 | 理解复杂指令 |
| **代码生成** | 10B+ 参数 | 根据描述生成代码 |

**例子:**
```
小模型(7B): "写一个排序算法" → 代码错误多
大模型(70B+): "写一个排序算法" → 完美实现 + 测试用例
```

**核心特征:**
- 非线性出现: 不是渐进式提升,而是突然质变
- 不可预测: 训练前无法预知会出现什么能力
- 规模依赖: 需要足够的参数量和训练数据

**面试话术:**
> "涌现能力是LLM最神奇的特性之一。当模型参数超过100B后,会突然展现出上下文学习、复杂推理等能力。这也是为什么GPT-3(175B)比GPT-2(1.5B)质的飞跃,而不仅仅是量的提升。"

</details>

---

## 12. 什么是灾难性遗忘(Catastrophic Forgetting)?

**灾难性遗忘** = 模型在学习新任务时,遗忘之前学过的知识

### 典型场景

<details>
<summary>💡 答案要点</summary>

**问题表现:**
```
原模型: 擅长中文问答
微调后: 擅长代码生成,但中文问答能力大幅下降 ❌
```

**解决方案:**

| 方法 | 原理 | 效果 |
|------|------|------|
| **混合训练** | 新旧数据混合训练 | 效果好,成本高 |
| **正则化** | 限制参数变化(EWC算法) | 效果一般 |
| **LoRA微调** | 只训练少量参数 | 效果好,推荐 ⭐ |
| **持续学习** | 渐进式学习架构 | 复杂度高 |

**LoRA优势:**
- 只训练0.1%参数,不影响原模型
- 可以同时保留多个LoRA适配器
- 推理时动态切换,无遗忘问题

**面试话术:**
> "灾难性遗忘是微调的核心挑战。我们项目中用LoRA解决这个问题——原模型参数冻结,只训练小的适配器。这样既学会了新任务,又保留了原能力,而且多个LoRA可以共存。"

</details>

---

## 13. LLM的幻觉(Hallucination)与偏见(Bias)

### 幻觉问题

<details>
<summary>💡 答案要点</summary>

**什么是幻觉?**
模型生成看起来流畅,但事实错误或编造的内容

**典型例子:**
```
用户: "介绍一下诺贝尔物理学奖得主张三"
模型: "张三是2015年诺贝尔物理学奖得主,主要研究量子力学..."  ❌
(实际: 张三是编造的人物)
```

**幻觉类型:**

| 类型 | 示例 | 严重程度 |
|------|------|----------|
| **事实错误** | 错误的日期、人名 | 🔥🔥🔥 |
| **逻辑错误** | 前后矛盾 | 🔥🔥 |
| **无中生有** | 编造不存在的信息 | 🔥🔥🔥🔥🔥 |

**缓解方法:**

1. **RAG(检索增强生成)** - 基于真实文档回答 ⭐⭐⭐⭐⭐
2. **指令约束** - "只根据上下文回答,不确定就说不知道"
3. **温度降低** - Temperature=0,减少随机性
4. **人工审核** - 关键场景人工复核

</details>

### 偏见问题

<details>
<summary>💡 答案要点</summary>

**什么是偏见?**
模型在性别、种族、地域等方面的不公平输出

**典型例子:**
```
输入: "The nurse said ... he/she"
偏见模型: 倾向用 "she" (性别刻板印象)

输入: "程序员通常是..."
偏见模型: "男性" (职业性别偏见)
```

**偏见来源:**
- 训练数据中的社会偏见
- 标注人员的主观偏好
- 采样策略导致的分布偏移

**缓解方法:**

| 方法 | 效果 | 成本 |
|------|------|------|
| **数据平衡** | 增加少数群体样本 | 高 |
| **RLHF对齐** | 人类反馈强化学习 | 高 |
| **提示词工程** | 明确要求公平性 | 低⭐ |
| **后处理过滤** | 检测并修正偏见输出 | 中 |

**面试话术:**
> "幻觉和偏见是LLM两大核心问题。我们项目用RAG解决幻觉——所有回答必须基于知识库,未找到时明确告知。偏见方面,我们在Prompt中明确要求'请公平对待所有性别/种族',并在RLHF阶段强化这一点。"

</details>

---

## 14. 如何评估LLM的输出质量?

**核心指标**

<details>
<summary>💡 答案要点</summary>

### 自动评估指标

| 指标 | 适用场景 | 优缺点 |
|------|----------|--------|
| **BLEU** | 机器翻译 | 快速,但对创意文本不准 |
| **ROUGE** | 摘要生成 | 关注召回率 |
| **BERTScore** | 语义相似度 | 考虑语义,更智能 ⭐ |
| **Perplexity** | 语言模型质量 | 低困惑度=高质量 |

### 人工评估维度

| 维度 | 说明 | 示例问题 |
|------|------|----------|
| **相关性** | 是否回答了问题 | 5分制评分 |
| **准确性** | 事实是否正确 | 有无幻觉 |
| **流畅性** | 语言是否通顺 | 是否自然 |
| **完整性** | 信息是否充分 | 有无遗漏 |

### RAG系统专用指标

```python
# 使用 RAGAS 框架
from ragas import evaluate
from ragas.metrics import (
    faithfulness,        # 忠实度: 回答是否基于检索内容
    answer_relevancy,    # 相关性: 是否回答了问题
    context_recall,      # 召回率: 检索到了关键信息吗
    context_precision    # 精确率: 检索内容是否都有用
)

results = evaluate(
    dataset=test_data,
    metrics=[faithfulness, answer_relevancy, context_recall, context_precision]
)
```

**面试话术:**
> "我们项目用双层评估:自动指标RAGAS跑全量数据,人工抽样200条核心case。关键维度是忠实度(不能幻觉)和相关性(要答对问题)。每次模型迭代都要对比这些指标,确保没有退化。"

</details>

---

## 15. Tokenization分词算法:BPE vs SentencePiece

**Tokenization = 将文本切分成模型能理解的最小单位(Token)**

### BPE(Byte Pair Encoding)算法

<details>
<summary>💡 答案要点</summary>

**BPE = 基于频率的子词分词算法**

**工作原理:**
```
1. 初始化:每个字符是一个token
   "low" → ["l", "o", "w"]
   "lower" → ["l", "o", "w", "e", "r"]
   "lowest" → ["l", "o", "w", "e", "s", "t"]

2. 统计相邻字符对频率
   "lo": 3次 (最高)
   "ow": 3次
   "we": 2次
   ...

3. 合并最高频对
   "lo" → "lo"(一个token)
   "low" → ["lo", "w"]
   "lower" → ["lo", "w", "e", "r"]

4. 重复统计合并,直到词汇表达到目标大小
   "low" → ["low"]
   "lower" → ["low", "er"]
   "lowest" → ["low", "est"]
```

**优点:**
- ✅ 处理未知词:罕见词拆成已知子词
- ✅ 词汇表可控:可设定大小(如50k)
- ✅ 平衡粒度:介于字符和单词之间

**缺点:**
- ❌ 依赖预分词(需要先按空格分)
- ❌ 语言相关(中文日文处理困难)

**代码示例:**
```python
from tokenizers import Tokenizer, models, pre_tokenizers, trainers

# 创建BPE tokenizer
tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

# 训练
trainer = trainers.BpeTrainer(vocab_size=50000, special_tokens=["[PAD]", "[UNK]"])
tokenizer.train(files=["train.txt"], trainer=trainer)

# 使用
output = tokenizer.encode("GPT使用BPE分词")
print(output.tokens)  # ['GPT', '使', '用', 'BP', 'E', '分', '词']
```

</details>

### SentencePiece算法

<details>
<summary>💡 答案要点</summary>

**SentencePiece = 语言无关的分词算法**

**核心特性:**

1. **无需预分词**
   ```
   BPE: "你好世界" → 需要先分词 → ["你好", "世界"]
   SentencePiece: "你好世界" → 直接处理原始文本
   ```

2. **空格也是token**
   ```
   "Hello World"
   → ["▁Hello", "▁World"]  # ▁ 代表空格
   → 可逆解码: "Hello World"
   ```

3. **支持两种算法**
   - **BPE模式**:类似标准BPE
   - **Unigram模式**:概率分词,从大到小删减

**Unigram vs BPE:**

| 维度 | BPE | Unigram |
|------|-----|---------|
| 方向 | 从小到大合并 | 从大到小删减 |
| 确定性 | 确定 | 概率(多种分词) |
| 训练速度 | 慢 | 快 |

**代码示例:**
```python
import sentencepiece as spm

# 训练
spm.SentencePieceTrainer.train(
    input='train.txt',
    model_prefix='m',
    vocab_size=50000,
    model_type='unigram',  # 或'bpe'
    character_coverage=0.9995  # 字符覆盖率
)

# 使用
sp = spm.SentencePieceProcessor(model_file='m.model')
tokens = sp.encode('GPT使用SentencePiece分词', out_type=str)
print(tokens)  # ['▁GPT', '使用', 'Sen', 'tence', 'Piece', '分词']

# 解码
text = sp.decode(tokens)
print(text)  # '你好世界' (完美还原)
```

**优势:**
- ✅ 语言无关(中英日韩都OK)
- ✅ 无损可逆(空格也编码)
- ✅ 无需预分词
- ✅ 主流LLM首选(LLaMA、GPT-4都用)

</details>

### BPE vs SentencePiece对比

<details>
<summary>💡 答案要点</summary>

| 维度 | BPE | SentencePiece |
|------|-----|---------------|
| **预分词** | ✅需要 | ❌不需要 |
| **空格处理** | 丢失 | 保留(▁符号) |
| **多语言** | 困难 | 优秀 |
| **可逆性** | ❌ | ✅ |
| **主流应用** | GPT-2 | GPT-4,LLaMA,T5 |

**实际案例:**
```python
# 同一个文本的分词对比
text = "2024年AI发展很快"

# BPE (GPT-2)
['2024', '年', 'AI', '发', '展', '很', '快']  # 中文粒度太细

# SentencePiece (LLaMA)
['▁2024', '年', 'AI', '发展', '很快']  # 更合理的子词
```

**为什么LLM数学差?**
- Token化不一致
  ```
  "1234" → ["12", "34"]
  "1235" → ["123", "5"]  # 不一致!
  ```
- 模型难以学习数字规律

**面试话术:**
> "BPE是早期分词算法,需要预分词且丢失空格。SentencePiece是改进版,语言无关且可逆,现在主流LLM都用它。我们项目用SentencePiece Unigram模式,中英文混合语料分词效果比BPE好15%。"

</details>

---

## 16. 长文本处理:超出Context Window怎么办?

<details>
<summary>💡 答案要点</summary>

**问题背景:**
```
用户上传100页PDF(约50K tokens)
GPT-4 Context Window: 8K tokens
怎么处理? ❌ 无法直接输入
```

### 解决方案对比

| 方案 | 原理 | 优缺点 | 适用场景 |
|------|------|--------|----------|
| **截断** | 丢弃超出部分 | ❌丢失信息 | 不推荐 |
| **滑动窗口** | 保留最近N个token | ❌丢失早期信息 | 实时对话 |
| **摘要压缩** | LLM递归摘要 | ⚠️可能失真 | 文档概览 |
| **RAG分块** | 切分+向量检索 | ✅最优⭐ | 问答/检索 |
| **长上下文模型** | 用128K窗口模型 | 💰成本高 | 必要时 |

### 方案1: 滑动窗口(Sliding Window)

**原理:**
```python
# 维护一个固定大小的窗口
max_tokens = 4000
history = []

while True:
    user_input = get_user_input()
    history.append(user_input)

    # 计算总token数
    total_tokens = count_tokens(history)

    # 超出窗口,删除最早的消息
    while total_tokens > max_tokens:
        history.pop(0)  # 删除第一条
        total_tokens = count_tokens(history)

    # 用窗口内容生成回复
    response = llm.generate(history)
    history.append(response)
```

**优化: 分层管理**
```python
class ConversationManager:
    def __init__(self, max_recent=3, summary_every=10):
        self.recent_messages = []  # 最近3轮完整保留
        self.summary = ""           # 历史摘要
        self.message_count = 0

    def add_message(self, role, content):
        self.recent_messages.append({"role": role, "content": content})
        self.message_count += 1

        # 保留最近3轮
        if len(self.recent_messages) > 6:  # 3轮=6条消息
            # 把旧消息做摘要
            old = self.recent_messages.pop(0)
            old_pair = self.recent_messages.pop(0)

            self.summary += llm.summarize([old, old_pair])

        return self.get_context()

    def get_context(self):
        # 上下文 = 历史摘要 + 最近3轮原文
        context = []
        if self.summary:
            context.append({
                "role": "system",
                "content": f"历史对话摘要: {self.summary}"
            })
        context.extend(self.recent_messages)
        return context

# 使用
manager = ConversationManager()
manager.add_message("user", "你好")
manager.add_message("assistant", "你好,有什么可以帮你?")
...
context = manager.get_context()  # 自动管理上下文
```

**效果:**
- Token消耗: 稳定在4K以内
- 信息保留: 最近3轮完整+历史摘要
- 成本: 每10轮多1次摘要API调用

### 方案2: RAG分块检索(推荐⭐)

**完整流程:**
```python
# 步骤1: 文档预处理
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # 每块1000字符
    chunk_overlap=200,     # 200字符重叠
    separators=["\n\n", "\n", "。", ". "]
)

chunks = splitter.split_text(long_document)
# 100页PDF → 约150个chunks

# 步骤2: 向量化存储
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vector_store = Qdrant.from_texts(
    texts=chunks,
    embedding=embeddings,
    collection_name="my_documents"
)

# 步骤3: 用户提问时检索
def answer_question(question):
    # 检索top-5相关chunks
    relevant_chunks = vector_store.similarity_search(
        question, k=5
    )

    # 拼接成上下文
    context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])

    # LLM生成答案
    prompt = f"""
    基于以下内容回答问题:

    {context}

    问题: {question}
    答案:
    """

    answer = llm.generate(prompt)
    return answer

# 使用
question = "文档中提到的主要结论是什么?"
answer = answer_question(question)
```

**优势:**
- ✅ 支持无限长文档
- ✅ 只检索相关部分,节省token
- ✅ 可追溯来源(返回chunk ID)

### 方案3: 递归摘要

**Map-Reduce摘要:**
```python
def recursive_summarize(long_text, max_chunk_size=4000):
    # 如果短于限制,直接摘要
    if len(long_text) < max_chunk_size:
        return llm.summarize(long_text)

    # 切分
    chunks = split_text(long_text, max_chunk_size)

    # Map: 每个chunk单独摘要
    summaries = [llm.summarize(chunk) for chunk in chunks]

    # Reduce: 合并摘要
    combined = "\n\n".join(summaries)

    # 递归(如果合并后还是太长)
    return recursive_summarize(combined, max_chunk_size)

# 示例
long_doc = load_100_page_pdf()
summary = recursive_summarize(long_doc)
print(summary)  # 最终浓缩版
```

**适用场景:**
- 只需要概览,不需要细节
- 没有特定问题,想了解大意

### 方案4: 长上下文模型

**模型对比:**

| 模型 | Context Window | 价格(1M tokens) | 适用 |
|------|----------------|-----------------|------|
| GPT-3.5 | 16K | $1.5 | 短对话 |
| GPT-4 | 8K | $30 | 通用 |
| GPT-4-32K | 32K | $60 | 长文档 |
| GPT-4-128K | 128K | $120 | 超长 |
| Claude-2 | 100K | $8 | 性价比⭐ |
| Claude-3 | 200K | $15 | 极长文档 |

**选择策略:**
```python
def choose_model(text_length):
    tokens = count_tokens(text)

    if tokens < 4000:
        return "gpt-3.5-turbo"  # 便宜
    elif tokens < 30000:
        return "claude-2"       # 性价比高
    elif tokens < 120000:
        return "gpt-4-128k"     # 贵但强
    else:
        return "RAG"            # 超长必须分块
```

### Lost in the Middle问题

**现象:**
```
给LLM一个20K的文档,关键信息在中间
→ LLM往往只关注开头和结尾
→ "大海捞针"失败
```

**解决:**
```python
# 方法1: 把关键内容放开头/结尾
prompt = f"""
关键信息: {key_info}

背景资料:
{long_context}

问题: {question}
"""

# 方法2: 分段+多次查询
def multi_pass_qa(long_text, question):
    # Pass 1: 快速扫描找相关段落
    relevant_sections = quick_scan(long_text, question)

    # Pass 2: 深入分析相关段落
    answers = []
    for section in relevant_sections:
        answer = llm.generate(f"{section}\n\n{question}")
        answers.append(answer)

    # Pass 3: 综合答案
    final = llm.generate(f"综合以下答案: {answers}")
    return final
```

**面试话术:**
> "长文本处理首选RAG:切分+检索+生成。滑动窗口适合对话,但会丢失早期信息,我们用分层管理解决——最近3轮保留原文,历史做摘要。长上下文模型虽强但贵,128K窗口成本是8K的15倍,只在必要时用。"

</details>

---

## 17. 2026年主流模型格局：GPT-5/Claude 4/Gemini 3/DeepSeek/Qwen如何选型？

<details>
<summary>💡 答案要点</summary>

**2026年5月最新模型格局：**

| 模型 | 定位 | 上下文 | 核心优势 | 价格 | 适用场景 |
|------|------|--------|----------|------|----------|
| **GPT-5.5** | 通用旗舰 | 200K | 复杂推理/Agentic | ¥30/1M | 复杂任务、生产级Agent |
| **Claude Opus 4.7** | 长文档/分析 | 1M | Extended Thinking强 | ¥45/1M | 长文档分析、代码审查 |
| **Gemini 3.5 Pro** | 多模态旗舰 | 2M | 视频/代码/Agentic | ¥20/1M | 多模态、企业级应用 |
| **DeepSeek V4 Pro** | 高性价比 | 128K | 推理能力强、中文优 | ¥4/1M | 成本敏感、中文场景 |
| **Qwen 3.7 Max** | 国产开源旗舰 | 128K | 开源、可本地部署 | ¥8/1M | 企业内网、中文定制 |
| **Kimi K2.6** | Agent专用 | 256K | Agent Swarm、并发强 | ¥15/1M | 多Agent系统、大规模协作 |

**选型决策树（面试重点）：**

```
场景是否涉及复杂推理？
  ├─ 是 → GPT-5.5 或 Claude Opus 4.7
  │       └─ 需要长上下文？ → Claude Opus 4.7 (1M)
  │       └─ 需要极致推理？ → GPT-5.5 (o3模式)
  └─ 否 → 成本优先？
           ├─ 是 → DeepSeek V4 Pro (¥4/1M)
           └─ 否 → 国产开源？
                    ├─ 是 → Qwen 3.7 Max (可本地部署)
                    └─ 否 → Gemini 3.5 Flash (¥1.5/1M)
```

**2026年新格局变化：**
1. **推理模型分层** — o3/Gemini 2.5 Deep Think/DeepSeek R2/QwQ-32B 成为独立赛道
2. **国产崛起** — Qwen 3.7 Max 在开源模型中达到 SOTA，Kimi K2.6 专注 Agent
3. **价格战** — DeepSeek V4 Pro 推出 ¥4/1M，价格比 GPT-5.5 低 87%
4. **Agent 原生** — Gemini 3.5 Flash/Claude Sonnet 4/GPT-5.5 都强调 Agentic 能力

**面试话术：**
> "2026年选模型要看'任务复杂度×成本'二维矩阵。简单问答用 Gemini 3.5 Flash（¥1.5/1M），复杂推理用 GPT-5.5 o3模式，企业内网用 Qwen 3.7 Max 开源版。我项目中用'模型路由'自动分流——简单问题用小模型省 90% 成本，复杂问题自动升级到大模型。"

</details>

---

## 18. 什么是推理模型（Reasoning Model）？o3/R1/QwQ 和普通模型有什么区别？

<details>
<summary>💡 答案要点</summary>

**推理模型 = 让模型在回答前'先思考'的模型**

普通模型：输入 → 直接输出
推理模型：输入 → 内部思考链（不展示）→ 最终答案

**主流推理模型对比（2026年）：**

| 模型 | 思考方式 | 适用场景 | 价格（/1M tokens） |
|------|----------|----------|-------------------|
| **OpenAI o3** | 显示思考过程 | 复杂推理、数学、代码 | ¥60（思考tokens另计） |
| **DeepSeek R1** | 显示思考过程 | 推理、透明化分析 | ¥4 |
| **QwQ-32B** | 显示思考过程 | 本地部署、推理 | 开源 |
| **Gemini 2.5 Pro** | 隐藏式思考 | 高效推理 | ¥20 |

**核心区别：**

| 维度 | 普通模型 | 推理模型 |
|------|----------|----------|
| **思考过程** | 无，直接输出 | 先推理后回答 |
| **Token 消耗** | 输入+输出 | 输入+思考+输出（贵 3-10x） |
| **准确性** | 一般 | 显著提升（尤其数学/代码） |
| **延迟** | 低 | 高（需等待思考） |
| **适用任务** | 简单问答、创意 | 复杂推理、多步规划 |

**面试话术：**
> "推理模型是 2026 年最重要的模型类型变革。o1 之前，模型'边想边说'；o3 之后，模型'先想后说'。这对 AI 应用开发的影响是：1）成本结构变了——简单问题用普通模型省 90% 成本；2）Prompt 写法变了——不要让推理模型'解释思考过程'，直接给任务；3）产品设计变了——需要展示思考过程给用户看（如 Claude 的 Extended Thinking）。"

**什么时候不用推理模型：**
- 简单问答（天气、时间等）— 普通模型 + 低成本
- 高并发、低延迟要求 — 推理模型延迟高 5-10x
- 成本敏感场景 — 推理模型贵 3-10x

</details>

---

## 19. 什么是 Test-Time Compute（测试时算力）？Thinking Budget 如何控制 AI 的思考量？

<details>
<summary>💡 答案要点</summary>

**Test-Time Compute = 模型推理时消耗的算力（不是训练时）**

传统观点：模型越强越好（训练时 scaling）
2026年新观点：推理时的算力分配同样重要（测试时 scaling）

**核心概念：Thinking Token Budget（思考预算）**

```
Thinking Budget = 允许模型消耗的最大"思考 tokens"数量

预算示例：
- 1024 tokens → 简单思考（简单问题）
- 8192 tokens → 深度思考（复杂问题）
- 32768 tokens → 超深度思考（数学证明）

模型行为：
预算内：模型自由思考
预算外：强制输出答案
```

**四大厂商思考预算对比（2026年）：**

| 厂商 | 功能 | 配置方式 | 思考 token 范围 |
|------|------|----------|----------------|
| **Anthropic** | Extended Thinking | `thinking.budget_tokens` | 1024~128K |
| **OpenAI** | o3 模式 | `max_tokens`（含思考） | 自动分配 |
| **Google** | Gemini Deep Think | `thinkingBudget` | 1024~32K |
| **DeepSeek** | R1/QwQ | 内置思考机制 | 开源可控 |

**为什么重要（面试重点）：**

```python
# 生产级思考预算策略
def route_by_complexity(question: str) -> dict:
    # 简单问题：不值得思考
    if is_simple_factual(question):
        return {"model": "claude-haiku", "thinking_budget": 0}
    
    # 中等问题：适度思考
    elif is_analysis_task(question):
        return {"model": "claude-sonnet", "thinking_budget": 4096}
    
    # 复杂问题：深度思考
    elif is_complex_reasoning(question):
        return {"model": "claude-opus", "thinking_budget": 32768}
    
    # 极限问题：超深度思考
    else:
        return {"model": "gpt-5.5-o3", "thinking_budget": 128000}

# 成本控制
# 简单问题（thinking=0）：¥0.001
# 复杂问题（thinking=32K）：¥0.15
# 差距 150 倍！
```

**Inverse Scaling（反向缩放）问题：**

Anthropic 2025 年研究发现：对于**简单问题**，推理模型反而比普通模型**更差**——因为思考过程可能引入干扰。

```
简单问题：普通模型 > 推理模型（思考干扰）
复杂问题：推理模型 >> 普通模型（思考增益）
```

**最佳实践：**
1. **不要默认开最大思考预算** — 简单问题浪费 150x 成本
2. **用分类模型先判断复杂度** — 再分配预算
3. **监控思考 token 消耗** — 发现异常及时告警

**面试话术：**
> "Test-Time Compute 是 2026 年 AI 成本控制的核心技术。我的策略是'按需分配思考'：简单问题直接回答（¥0.001），复杂问题开启深度思考（¥0.15）。关键是用分类模型提前判断问题复杂度，避免'大炮打蚊子'。实测这套策略可以降低 70% 的 LLM 成本，同时不损失回答质量。"

</details>

---

## 20. 什么是 Logits？LLM 是如何一步步生成下一个 Token 的？

**Logits** = 模型输出层（LM Head）对词表中每个 Token 的打分（未归一化的原始分数），数值越大表示越可能被选中。

### 完整生成流程（面试必答）

```
输入文本 → Tokenizer分词 → Embedding → Transformer多层计算
→ 输出层LM Head得到Logits（长度=词表大小）
→ Softmax归一化成概率 → 采样策略选出下一个Token
→ 拼接到输入 → 循环直到遇到停止符
```

### 关键点

| 概念 | 说明 |
|------|------|
| **Logits** | 未归一化分数，可正可负，数值越大越优 |
| **Softmax** | 把 Logits 转成概率分布（和为1） |
| **Temperature** | 除以 Temperature 再 Softmax，控制分布尖锐度 |
| **LM Head** | 通常是 `hidden_size × vocab_size` 的线性层 |

### 面试话术

> "Logits 是模型对词表每个 Token 的原始打分，经过 Softmax 变成概率。生成时先算 Logits，再用采样策略（贪心/Top-K/Top-P）选 Token，选中的 Token 拼回输入继续预测下一个，直到遇到 EOS 停止符。"

---

## 21. 解码策略对比：贪心解码 vs Beam Search vs 采样

### 三种解码策略

| 策略 | 原理 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|----------|
| **贪心解码** | 每次选概率最大的 Token | 快、稳定 | 易重复、缺多样性 | 代码/问答（配合Temperature=0） |
| **Beam Search** | 每步保留 Top-N 条候选路径 | 全局较优、连贯 | 慢、易重复、缺惊喜 | 翻译、摘要、机器翻译 |
| **采样（Sampling）** | 按概率分布随机选 | 多样、自然 | 不稳定、可能跑偏 | 对话、创意写作 |

### 面试高频追问

- **Beam Size 越大越好？** 不是！越大越慢，且容易陷入重复（常见 4-8）
- **采样怎么控随机性？** Temperature（整体）、Top-K（候选数）、Top-P（累积概率）三者组合
- **为什么机器翻译用 Beam Search？** 因为要全局最优、不容许跑偏，可接受重复风险
- **为什么对话用采样？** 多样性更重要，Beam 会显得呆板

### 面试话术

> "解码策略主要分贪心、Beam Search 和采样三类。贪心最快但易重复；Beam 保留多条路径全局较优，适合翻译摘要；采样引入随机性更自然，适合对话创作。实际工程里问答和代码生成我用贪心+T=0，对话用采样+T=0.7。"

---

## 22. 为什么 Temperature=0 时输出依然不完全确定？

**面试坑点：很多人以为 T=0 就是完全确定，其实不然。**

### 原因（三大层面）

1. **浮点计算非确定性**：GPU 并行计算（如 Attention、矩阵乘法）存在浮点累加顺序差异，导致细微数值抖动，可能影响 argmax 结果
2. **采样随机性（部分框架）**：某些框架 T=0 时若遇到多个 Token 概率并列，会用随机打破平局
3. **批处理/缓存影响**：KV Cache、并行推理可能引入微小差异

### 工程建议

- 追求严格确定：固定 seed + T=0 + 关闭采样随机性 + 单卡单进程推理
- 业务对一致性敏感：加输出校验/重试

### 面试话术

> "Temperature=0 能大幅降低随机性，但不保证 100% 确定，因为 GPU 浮点运算的并行累加顺序有微小差异，极端情况下会影响 argmax 结果。要做到严格可复现，需要固定 seed、关闭采样随机并保证推理环境一致。"

---

## 23. 什么是重复惩罚（repetition_penalty）？如何防止复读机？

### 定义

**重复惩罚** = 对已经出现过的 Token 的 Logits 进行惩罚，降低它再次被选中的概率，从而减少重复。

### 实现原理

```python
# 伪代码：出现过的token，logits除以惩罚系数
for token in seen_tokens:
    if logits[token] > 0:
        logits[token] /= repetition_penalty   # 比如 1.15
    else:
        logits[token] *= repetition_penalty
```

### 参数建议

| 值 | 效果 |
|----|------|
| 1.0 | 不惩罚（默认） |
| 1.05-1.2 | 轻度惩罚，抑制复读 |
| >1.3 | 强惩罚，可能影响语义流畅度 |

### 其他防重复手段

- **Frequency Penalty / Presence Penalty**（OpenAI 风格）：按出现频次/是否出现惩罚
- **No Repeat Ngram Size**：禁止 N-gram 完全重复
- **Beam 内加多样性惩罚**：多条候选路径互相抑制

### 面试话术

> "复读机是解码阶段的常见问题，我用 repetition_penalty 对已出现 Token 的 Logits 做惩罚，一般设 1.1-1.2 兼顾流畅和多样；如果再配合 no_repeat_ngram 和频率惩罚，效果更好。"

---

## 24. 什么是停止符（EOS / Stop Token）？生成是如何终止的？

### 定义

**EOS（End of Sequence）** = 词表中一个特殊的终止 Token，模型生成它即代表回答结束。

### 生成终止的四种方式

| 方式 | 说明 |
|------|------|
| **EOS Token** | 模型自己预测出 EOS，自然结束 |
| **max_tokens** | 达到长度上限强制截断（兜底） |
| **Stop Words** | 命中自定义停止词立即终止（如 \n\n、"再见"） |
| **工具调用/结构化输出** | 命中特定格式边界结束（如 JSON 闭合括号） |

### 工程注意

- max_tokens 必须设置，防止死循环/无限生成（成本失控）
- 流式输出时识别 EOS 立即断开，减少 token 消耗
- 结构化输出（JSON）场景下，停止符配置不当会截断半截 JSON

### 面试话术

> "生成终止有三层保险：模型预测出 EOS 自然结束、max_tokens 硬性截断兜底、Stop Words 按业务边界提前终止。工程上我必设 max_tokens 防成本失控，流式场景识别到 EOS 就立即断开连接。"

---

## 25. 为什么主流 LLM 都是 Decoder-only 架构？

### 三类架构对比

| 架构 | 代表模型 | 特点 | 现状 |
|------|----------|------|------|
| **Encoder-only** | BERT | 双向理解，适合分类/检索 | 被 LLM 时代边缘化 |
| **Encoder-Decoder** | T5、BART | 编码+解码，适合翻译摘要 | 部分场景仍用 |
| **Decoder-only** | GPT、LLaMA、Qwen、DeepSeek | 自回归单向生成 | **主流（ChatGPT 系）** |

### Decoder-only 胜出的原因

1. **训练目标统一**：预训练（next-token prediction）与推理（续写）一致，无需任务适配
2. **架构简单**：单一 Transformer 栈，工程优化（KV Cache、量化）更聚焦
3. **扩展性好**：decoder 在超大参数量下的 scaling law 表现更优
4. **生态成熟**：InstructGPT/RLHF 等对齐技术都是围绕 decoder-only 建立
5. **In-context Learning 强**：统一 autoregressive 目标下少样本学习能力更突出

### 面试话术

> "主流 LLM 选择 Decoder-only，核心是预训练和推理目标统一：都是预测下一个 Token。相比 BERT 需要任务头、T5 需要任务模板，Decoder-only 架构简单、扩展性好、对齐技术成熟，在 Scaling Law 下表现最优，所以 ChatGPT 系模型都走这条路。"

---

## 📝 速记卡片

### LLM基础概念

| 概念 | 一句话解释 |
|------|------------|
| **Token** | LLM处理的最小单位,1中文≈1-2 tokens |
| **Temperature** | 控制随机性,0=确定,1=随机 |
| **Context Window** | 模型一次能看的最大长度(如4K,128K) |
| **长文本处理** | RAG分块(首选)、滑动窗口、递归摘要 |
| **Lost in the Middle** | 长文本中间信息丢失,解决:关键信息放开头 |
| **涌现能力** | 模型足够大时突然出现的新能力(如推理、编程) |
| **灾难性遗忘** | 学新任务忘旧知识,用LoRA解决 |
| **幻觉** | 编造不存在的信息,用RAG缓解 |
| **偏见** | 对性别/种族的不公平输出,RLHF对齐 |
| **RAGAS** | RAG系统评估框架(忠实度、召回率、精确率) |
| **Logits** | 模型对词表每个Token的原始打分,经Softmax变概率 |
| **解码策略** | 贪心/Beam Search/采样,决定下一个Token怎么选 |
| **重复惩罚** | 对已出现Token的Logits惩罚,防复读机 |
| **EOS停止符** | 特殊终止Token,生成遇到它即结束 |
| **Decoder-only** | 主流LLM架构,预训练与推理目标统一(next-token) |

### 分词算法

| 算法 | 原理 | 优缺点 |
|------|------|--------|
| **BPE** | 高频字符对合并 | 需预分词,丢空格 |
| **SentencePiece** | 语言无关,空格编码 | 可逆,主流首选 |
| **Unigram** | 概率分词,大到小删减 | 速度快,LLaMA用 |

---

[返回目录 →](../../README.md)

---

**下一模块：** [Prompt 工程](../02-prompt-engineering/)

---

[返回目录 →](../../README.md)
