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
| DeepSeek V4-Flash | 16K |
| Claude | 200K |
| 开源模型 | 4K-32K |

### 超出限制的解决方案

1. **截断** - 保留最近的对话
2. **总结** - 用 LLM 总结历史对话
3. **滑动窗口** - 只保留最近 N 轮
4. **向量检索** - 把历史存向量库，按需检索
5. **分层摘要** - 重要信息摘要 + 最近对话原文

## 4. LLM 和传统机器学习模型有什么区别？为什么是"大"语言模型？

**核心：LLM 是"用海量数据训练出来的概率生成模型"，与传统 ML 模型有本质区别。**

### 五大区别（面试必答）

| 维度 | 传统 ML 模型 | LLM（大语言模型） |
|------|-------------|-------------------|
| **任务类型** | 判别式为主（分类/回归） | 生成式（预测下一个 Token） |
| **输入输出** | 结构化特征 → 标签 | 任意文本 → 文本 |
| **训练方式** | 针对单任务标注数据 | 自监督 next-token 预测（无需标注） |
| **能力泛化** | 一个模型只能做一件事 | 一个模型能做所有任务（涌现能力） |
| **部署成本** | 小（MB 级） | 大（GB 级，需 GPU） |

### 判别式 vs 生成式（高频追问）

```
判别式模型：学习 P(标签|输入)，划一条边界
  例：垃圾邮件分类、图像识别（SVM/逻辑回归/CNN）

生成式模型：学习 P(文本)，预测下一个 Token
  例：GPT/LLaMA/Qwen（LLM 都是生成式）
```

### 为什么叫"大"语言模型？

1. **参数大**：从几亿 → 几千亿参数（7B/70B/671B），容量决定知识上限
2. **数据大**：训练用 TB 级、数万亿 Token 的语料
3. **能力大**：涌现出推理、代码、翻译等传统模型不具备的能力
4. **上下文大**：从 2K → 128K → 1M Token 的窗口

### 面试话术

> "LLM 和传统模型最大的区别是生成式 vs 判别式：传统模型学'输入→标签'的映射，LLM 学'下一个 Token 是什么'的概率分布。因为训练数据海量、参数巨大，LLM 涌现出传统模型没有的通用能力——一个模型能对话、写代码、做翻译、解数学题，而传统模型每个任务都要单独训练。"

### 实战补充（应用开发视角）

- **什么时候还在用传统模型？** 小样本、低延迟、可解释性强的场景（如规则匹配、小分类器）
- **什么时候必须用 LLM？** 开放域任务、需要理解语义/上下文、零样本泛化
- **混合架构**：传统模型做前置过滤/分类，LLM 做核心生成，是降本常用手段

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

## 12. LLM 为什么是概率模型？为什么同样的输入输出会不一样？

**核心：LLM 本质是一个"概率分布"——对每个 Token 计算概率，再按策略采样，所以输出天然带随机性。**

### 为什么 LLM 是概率模型？（面试必答）

1. **训练目标就是概率**：预训练学的是 `P(下一个Token | 上文)`，模型输出的是词表上的概率分布（经 Softmax）
2. **生成靠采样**：解码时从概率分布中选 Token（贪心选最大，或按分布随机采）
3. **知识是"统计规律"**：模型学到的不是确定性规则，而是"什么词在什么语境下更可能"——所以同一问题可能给出不同但都合理的答案

### 为什么同样的输入输出会不一样？（高频追问）

| 原因 | 说明 | 可控性 |
|------|------|--------|
| **采样随机性** | Top-P/Top-K/温度>0 时按概率随机选 | ✅ 可调（T=0 降低） |
| **浮点非确定性** | GPU 并行累加顺序差异，极端情况影响 argmax | ⚠️ 固定 seed 缓解 |
| **多轮上下文** | 同样问题在不同对话历史下，模型"想法"不同 | ❌ 天然存在 |
| **模型服务负载** | 部分框架在不同批处理下有小差异 | ⚠️ 少见 |

### 概率模型的工程影响（加分点）

- **需要确定性输出的场景**：T=0 + 固定 seed + 结构化输出校验
- **需要稳定的场景**：加输出格式校验 + 重试策略（解析失败重生成）
- **利用随机性**：多次采样取最佳（Self-Consistency），创意场景故意调高温度

### 面试话术

> "LLM 是概率生成模型，输出层是一个词表上的概率分布，解码时通过采样策略选 Token。所以同样输入可能输出不同——这是采样随机性导致的，不是 bug。工程上我会分场景处理：需要确定性时用 T=0 + 固定 seed + 输出校验；需要多样性时提高温度；需要更可靠时用多次采样投票。"

---

## 13. LLM的幻觉(Hallucination)与偏见(Bias)

### 幻觉问题（补充：如何检测与量化幻觉？）

<details>
<summary>💡 答案要点</summary>

> （什么是幻觉、幻觉类型、基本缓解方法 → 见第 5 节）

**如何检测幻觉（面试高频追问）：**

| 方法 | 原理 | 场景 |
|------|------|------|
| **引用溯源** | 要求模型回答时给出引用/来源 | 生产系统标配 |
| **忠实度评估（Faithfulness）** | RAGAS 等框架检测"回答是否忠于检索内容" | RAG 系统 |
| **交叉验证** | 同一问题问多次/问不同模型，对比一致性 | 高价值场景 |
| **事实核对** | 关键实体（人名/日期/数字）用外部工具验证 | 知识密集型 |
| **不确定性探测** | 问模型"你有多确定"，或检查 logprobs 置信度 | 低成本粗筛 |

**量化指标（RAGAS 忠实度）：**
```python
from ragas import evaluate
from ragas.metrics import faithfulness

result = evaluate(dataset, metrics=[faithfulness])
# faithfulness: 回答中有多少陈述能从检索内容中找到依据（0-1）
```

**工程最佳实践：**
1. 生产环境必须带引用/溯源，这是幻觉的第一道防线
2. 定期抽样评估 faithfulness 指标，监控幻觉率变化
3. 高价值场景（金融/医疗）加交叉验证或人工复核

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

**优化: Token 预算分配组合方案（2026 生产实践）：**

```
核心原则：让模型"忘掉细节，记住要点"——不是单一方案，是组合拳：

1. 实时计算 Token 数：每次发送前计算消息列表总 Token（所有策略的基础）
2. 分层保留优先级：System Prompt 必须保留 → 当前问题必须保留 → 历史按优先级裁剪
3. 摘要触发条件：历史 Token 超预算 60% 时触发——最早 N 轮调 LLM 压成摘要替换原文
4. 兜底：摘要后仍超限 → 摘要存向量库，按当前问题检索最相关片段

分层保真原则（关键）：
  近期对话 → 原文保留（保真）
  远期对话 → 摘要压缩（保要）
  超远期 → 向量检索（按需）

⚠️ 误区：不要把所有历史都做摘要——摘要是有损压缩，每压一次丢一些细节。
  分层管理：近保真、远保要、超远按需。
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
| DeepSeek V4-Flash | 16K | $1.5 | 短对话 |
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
        return "deepseek-v4-flash"  # 便宜
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

## 17. 如何给 LLM 选型？质量/速度/成本怎么权衡？（方法论）

<details>
<summary>💡 答案要点</summary>

**核心：选型不是"选最强"，而是"任务复杂度 × 质量要求 × 成本预算"三维权衡。**

### 三维决策框架（面试重点）

```
任务是什么？
  ├─ 简单问答/分类 → 便宜小模型（Flash/Lite 系列）
  ├─ 代码生成/复杂推理 → 中高端模型（Plus/Pro 系列）
  └─ 超复杂推理/Agent长任务 → 旗舰（Max/Opus 系列）

质量要求多高？
  ├─ 内部工具/草稿 → 可接受小模型
  └─ 对外生产/金融医疗 → 必须高端 + 人工复核

成本预算多少？
  ├─ 按量计费：看单价（输入/输出分别计费）
  └─ 高并发：考虑缓存命中折扣（Prompt Caching）
```

### 2026 年主流模型档位（按性价比分层，价格会变，看方法论）

| 档位 | 代表 | 特点 | 适用 |
|------|------|------|------|
| **超便宜档** | DeepSeek V4-Flash、Qwen Flash、Gemini Flash-Lite | 1-2元/百万输出 | 高频、量大、简单任务 |
| **性价比档** | Qwen Plus、DeepSeek V4-Pro、GLM | 4-8元/百万输出 | 通用生产任务 |
| **旗舰档** | GPT/Claude Opus/Qwen Max/Kimi | 30-100元/百万输出 | 复杂推理、高价值 |
| **推理档** | o3/R1/QwQ/DeepThink | 思考tokens另计 | 数学/代码/多步推理 |

### 选型五步法（面试必答）

1. **先测基准**：用你的真实任务在小样本上测几个候选模型（质量对比）
2. **看成本结构**：输入/输出单价 + 缓存命中价（高输入场景缓存价更关键）
3. **算峰值需求**：并发量 × 单次调用 token 数 × 单价 = 月成本预算
4. **考虑峰谷**：部分厂商高峰时段溢价（如 DeepSeek 白天 2 倍价），夜间批量任务可省一半
5. **留 fallback**：主模型 + 备用模型链（质量下降/限流时自动切换）

### 工程降本三板斧（加分项）

1. **模型路由**：简单问题走小模型，复杂问题升级大模型（省 60-90% 成本）
2. **Prompt Caching**：静态前缀复用缓存，输入成本降 90%
3. **批量/低峰调度**：非实时任务放夜间跑（避开高峰溢价）

**面试话术：**
> "选型我的方法论是'任务复杂度×质量×成本'三维权衡：先拿真实任务测候选模型的质量，再看单价和缓存价算成本，最后按峰值需求定预算。工程上我会配模型路由——简单问答走小模型（几分钱），复杂推理升级旗舰，再加 Prompt Caching 降输入成本。我现在的 Agent 系统就是 DeepSeek 主力 + Qwen 备用，夜间批量任务专门挑低峰时段跑，成本降了 70% 左右。"

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

## 26. Embedding（嵌入向量）是什么？和 Token 有什么关系？

**Embedding = 把文本/Token 映射成稠密向量的技术**，是 LLM 理解语义的基石。

### 核心概念

| 概念 | 说明 |
|------|------|
| **Token** | 文本的最小切分单位（字符串层面） |
| **Token ID** | Token 在词表中的编号（离散整数） |
| **Embedding** | Token ID 对应的稠密向量（连续浮点数，如 768/1024/4096 维） |

**关系链路：**
```
"我爱AI" → Tokenize → ["我", "爱", "AI"] → 查表 → [[0.12, -0.34, ...], ...]
```

### Embedding 的核心特性

1. **语义相似 → 向量距离近**："苹果"和"水果"余弦相似度高，和"汽车"距离远
2. **两种 Embedding**
   - **静态 Embedding**（Word2Vec/GloVe）：一个词一个向量，不随上下文变化（"bank"河岸/银行都一样）
   - **上下文 Embedding**（BERT/LLM 内部）：同一个词在不同句子中向量不同（"苹果"在水果/手机语境下不同）✅ 主流
3. **维度**：决定表示能力与显存/计算成本（常见 768~8192）

### 应用场景

- **向量检索**（RAG）：文档和问题都转成向量，用余弦相似度找最相关片段
- **语义搜索**：替代关键词匹配
- **聚类/分类**：向量空间聚类

### 代码示例

```python
# OpenAI Embedding API
from openai import OpenAI
client = OpenAI()

resp = client.embeddings.create(
    model="text-embedding-3-large",  # 3072 维
    input=["苹果是一种水果", "苹果公司发布了新手机"]
)
vec1, vec2 = resp.data[0].embedding, resp.data[1].embedding

# 余弦相似度
import numpy as np
def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(cos_sim(vec1, vec2))  # 语义相关度打分
```

**面试话术：**
> "Embedding 是把 Token 映射成稠密向量的过程，语义相近的文本向量距离就近。重点要区分静态 Embedding 和上下文 Embedding——现在的 LLM 都是上下文相关的。在 RAG 里它是检索的基石：文档和问题向量化后用余弦相似度匹配，这也是我们系统召回率的基础。"

---

## 27. 什么是 In-Context Learning（上下文学习）？Zero-shot / Few-shot 有什么区别？

**In-Context Learning（ICL）= 不更新模型参数，仅通过在 Prompt 中提供示例，让模型学会完成新任务。**

### 三种形式（面试必答）

| 形式 | 示例数量 | 说明 | 适用场景 |
|------|----------|------|----------|
| **Zero-shot** | 0 个 | 直接给指令 | 简单任务 |
| **One-shot** | 1 个 | 给 1 个示例 | 格式学习 |
| **Few-shot** | 2~10 个 | 给多个示例 | 复杂/不常见任务 |

### 示例对比

```python
# Zero-shot：只给指令
prompt = "把下面的句子翻译成英文：今天天气很好"

# Few-shot：给示例再提问
prompt = """
把中文翻译成英文：
苹果 → apple
香蕉 → banana
橙子 → orange
葡萄 → ?
"""
```

### ICL vs 微调（核心区别）

| 维度 | In-Context Learning | 微调（Fine-tuning） |
|------|---------------------|---------------------|
| **是否更新参数** | ❌ 不更新 | ✅ 更新权重 |
| **成本** | 仅 Token 费 | 训练 GPU + 数据标注 |
| **生效速度** | 立即 | 小时~天 |
| **能力上限** | 受上下文窗口限制 | 可永久固化知识/风格 |
| **适用场景** | 快速验证、动态任务 | 稳定业务场景 |

### 为什么 ICL 有效？（2025-2026 主流解释）

1. **隐式梯度下降假说**：Transformer 的 Attention+MLP 组合在前向计算中隐式产生类似低秩权重更新（δW），效果上接近对模型做了一次微调
2. **Induction Head（归纳头）**：模型内部学会了"看到 A…B，再看到 A 就接 B"的模式复制机制，示例正是触发这种模式
3. **任务格式对齐**：示例让模型进入正确的"任务状态"（格式、语气、输出结构）

**面试话术：**
> "ICL 是不改参数的学习——通过 Few-shot 示例让模型掌握任务。它和微调的本质区别是：ICL 走前向计算，微调走反向传播。2025 年的研究表明 ICL 底层是 Attention+MLP 隐式形成的低秩更新，效果上等价于一次隐式微调。工程上我常用 ICL 快速验证任务可行性，验证通过后再决定要不要微调固化。"

---

## 28. LLM 是怎么训练出来的？预训练 → SFT → 对齐（RLHF/DPO）三阶段流程？

**主流 LLM 训练分三阶段：预训练（学知识）→ SFT（学对话）→ 对齐（学偏好）**

### 三阶段对比（面试重点）

| 阶段 | 数据 | 训练目标 | 产物 | 成本 |
|------|------|----------|------|------|
| **1. 预训练** | TB 级网页/书籍/代码 | 预测下一个 Token | Base 模型（博学但不会对话） | 千万美金级 |
| **2. SFT** | 几万~几十万条（指令, 标准回答） | 监督学习"按指令回答" | 对话模型（会聊天但可能不听话） | 中等 |
| **3. 对齐** | （指令, 好回答, 差回答）偏好对 | 让回答符合人类偏好（有用/诚实/无害） | 最终产品模型 | 高 |

### 各阶段详解

**阶段 1：预训练（Pre-training）**
```
输入: "今天天气真" → 预测下一个词: "好"
数据: 全网文本（数万亿 Token）
目标: 学习语言规律和世界知识
产出: Base Model（GPT-3、LLaMA base）
```

**阶段 2：SFT（Supervised Fine-Tuning）**
- 用人工撰写的"指令-回答"对教模型交互
- 模型学会：角色扮演、格式遵循、任务理解
- 产出：SFT 模型（能对话，但可能产生有害/无用内容）

**阶段 3：对齐（RLHF / DPO）**
- RLHF：先训练 Reward Model 给回答打分，再用 PPO 优化策略
- DPO：跳过奖励模型，直接在偏好对（好/坏回答）上优化（当前主流）

### 面试高频追问

- **为什么预训练后还要 SFT？** Base 模型只会续写，不会"回答问题"，SFT 教会它指令遵循
- **为什么 SFT 后还要对齐？** SFT 学的是"怎么做"，对齐学的是"什么该做、什么不该做"（安全、价值观）
- **三阶段数据量级差异？** 预训练 1T+ tokens vs SFT 10 万级 vs 偏好对 10 万级——数据量递减，质量要求递增

**面试话术：**
> "LLM 训练是'预训练→SFT→对齐'三阶段流水线：预训练在 TB 级数据上学 next-token 预测，得到博学的 Base 模型；SFT 用高质量指令对教会它对话和遵循指令；最后用 RLHF/DPO 做偏好对齐，决定模型的安全边界和价值观。三阶段数据量级递减、质量要求递增——这也是为什么对齐数据最贵。做应用开发时理解这点很重要：RAG 解决'知识不足'，微调解决'能力不足'，对齐解决'行为不合规'。"

---

## 29. 什么是 Scaling Law（规模定律）？Chinchilla 法则修正了什么？

**Scaling Law = 模型性能（Loss）与参数量、数据量、计算量之间存在可预测的幂律关系。**

### 核心公式（OpenAI 2020）

```
Loss ≈ a·N^(-α) + b·D^(-β) + c

N = 参数量    D = 训练数据量    a,b,c,α,β = 常数
```

- 参数翻倍 → Loss 稳定下降（收益递减）
- 数据翻倍 → Loss 稳定下降
- **结论：模型越大、数据越多，效果越好，且可预测**

### Chinchilla 法则（DeepMind 2022）修正了什么？

**核心结论：参数和数据要按约 1:20 的比例配比（训练 Token 数 ≈ 参数 × 20）**

| 项目 | 之前做法 | Chinchilla 修正后 |
|------|----------|-------------------|
| 参数 70B | 只喂 300B tokens（欠喂） | 应喂 1.4T tokens（1.4万亿） |
| 计算预算固定 | 盲目堆参数 | 参数和数据按比例分配 |

> 类比：堆参数量相当于"天才只读小学课本"，参数和数据要匹配才最优。

### Scaling Law 的意义（面试重点）

1. **可预测性**：用小模型实验（1B）可以推算大模型（70B）的表现，避免盲目烧钱
2. **指导训练预算分配**：固定算力下，算最优参数/数据配比
3. **能力涌现的前提**：规模是涌现能力的基础（呼应"涌现能力"题）
4. **2026 新趋势**：从"训练时 Scaling"扩展到"测试时 Scaling"（Test-Time Compute，见 Q19）——推理阶段多花算力也能换效果

**面试话术：**
> "Scaling Law 说模型效果和参数量、数据量、算力呈幂律关系，可以预测。Chinchilla 修正了'只堆参数'的误区，提出参数和数据约 1:20 配比——70B 模型要喂 1.4T tokens 才最优。工程上它的价值是可预测性：先在 1B 小模型上做实验，再推算 70B 的表现，节省大量试错成本。2026 年 Scaling 已经从训练侧延伸到推理侧，就是 Test-Time Compute。"

---

## 30. KV Cache 是什么？为什么能大幅加速 LLM 推理？（基础概念版）

**KV Cache = 把已经算过的历史 Token 的 K（Key）和 V（Value）缓存起来，避免重复计算。**

### 为什么要缓存？（自回归的重复计算问题）

LLM 是自回归生成：每生成一个 Token，都要让所有历史 Token 重新过一遍 Attention。

```
生成 "我爱吃苹果"：
第1步: 输入"我" → 算"我"的 Q/K/V → 预测"爱"
第2步: 输入"我爱" → 重新算"我"+"爱"的 Q/K/V → 预测"吃"  ❌ "我"的K/V白算了一遍
第3步: 输入"我爱吃" → 又重算一遍全部 Q/K/V → 预测"苹" ❌ 重复计算

不缓存: 复杂度 O(n²)，生成长度翻倍，计算量翻 4 倍
```

### KV Cache 怎么做？

```
第1步: 算"我"的 Q/K/V → 把 K、V 存进缓存 → 预测"爱"
第2步: 只算"爱"的 Q/K/V → K、V 追加到缓存 → 用"爱"的Q 和缓存的K/V做Attention → 预测"吃"
第3步: 只算"吃"的 Q/K/V → 追加缓存 → 预测"苹"

带缓存: 每步只算新 Token 的 Q/K/V，复杂度 O(n)（线性）
```

### 关键点

| 问题 | 答案 |
|------|------|
| **为什么 Q 不缓存？** | Q 是"当前查询"，每个新 Token 都要重新生成，没有复用价值 |
| **代价是什么？** | 显存！KV Cache 随序列长度线性增长 |
| **复杂度变化** | O(n²·d) → O(n·d)，长文本下提速明显 |

### KV Cache 显存估算（面试常考）

```
KV Cache 大小 = 2 × batch × seq_len × n_layers × n_heads × d_head × 字节数

例：LLaMA-7B（32层、32头、d_head=128），batch=1，seq=2048，FP16
= 2 × 1 × 2048 × 32 × 32 × 128 × 2 bytes ≈ 1.07 GB
```

（进阶：PagedAttention 分页管理、KV Cache 量化、Prefix Caching 跨请求复用 → 见推理优化/推理框架模块）

**面试话术：**
> "KV Cache 是 LLM 推理加速最基础的优化：自回归生成时历史 Token 的 K/V 不会变，缓存后每步只需计算新 Token 的 Q/K/V，复杂度从 O(n²) 降到 O(n)。它的代价是显存——所以长上下文场景要配合 PagedAttention 和 KV 量化。我的项目里多轮对话场景靠它把单 token 生成延迟降了一个数量级。"

---

## 31. RLHF 和 DPO 有什么区别？（入门对比版）

**两者都是"对齐"阶段的技术，目标相同：让模型输出符合人类偏好。区别在于实现路径。**

### 一句话版本

- **RLHF**：训练一个奖励模型打分，再用强化学习（PPO）优化策略
- **DPO**：跳过奖励模型，直接在偏好数据上优化，数学上等价于 RLHF 的最优解

### 完整对比（面试重点）

| 维度 | RLHF（PPO） | DPO |
|------|-------------|-----|
| **需要奖励模型** | ✅ 是 | ❌ 否 |
| **需要模型数量** | 4 个（策略/参考/奖励/价值） | 2 个（策略/参考） |
| **训练方式** | 在线采样 + PPO 强化学习 | 离线偏好对直接优化 |
| **实现复杂度** | 极高，训练不稳定 | 中，稳定简单 |
| **灵活性** | 高（可在线迭代、多轮采样） | 低（依赖固定偏好数据） |
| **数据要求** | 可在线生成对比 | 需高质量偏好对（垃圾进垃圾出） |
| **成本** | 高 | 低 |
| **当前趋势** | 大厂精细化场景 | ✅ 主流默认选择 |

### 简版原理

```python
# DPO 核心思想（伪代码）：让"好回答"的概率上升、"差回答"的概率下降
# loss = -log σ( β * (log π(y_good|x) - log π_ref(y_good|x))
#                - β * (log π(y_bad|x) - log π_ref(y_bad|x)) )
# 不需要奖励模型，直接拉大好/坏回答的隐式奖励差
```

### 顺带一提：GRPO（DeepSeek 提出）

- 同一 prompt 生成多个回答，组内相对比较打分
- 不需要奖励模型，也不需要严格的偏好对
- 是 RLHF 和 DPO 之间的折中，适合可验证任务（数学/代码）

### 工程选型建议

- 资源有限、数据规整 → **DPO**（大部分项目首选）
- 有标注团队、追求极致效果、需在线迭代 → **RLHF**
- 可验证任务、数据不规整 → **GRPO**

**面试话术：**
> "RLHF 和 DPO 目标一致但路径不同：RLHF 先训奖励模型再用 PPO 优化，需要维护 4 个模型、训练不稳定但灵活；DPO 直接对偏好对构造损失，数学上等价于 RLHF 的最优解，简单稳定，是当前主流。选型上：资源有限用 DPO，追求极致用 RLHF，可验证任务考虑 GRPO。我们微调项目就用 DPO 做对齐，一周就能收敛。"

---

## 32. 7B 模型需要多少显存？参数量如何换算显存？（高频估算题）

**核心公式：显存（GB）≈ 参数量 × 每参数字节数**

### 推理显存估算（面试必答）

| 精度 | 每参数字节 | 7B 模型权重显存 |
|------|------------|-----------------|
| FP32 | 4 bytes | 28 GB |
| **FP16/BF16（主流）** | 2 bytes | **14 GB** |
| INT8 量化 | 1 byte | 7 GB |
| INT4 量化 | 0.5 byte | 3.5 GB |

```python
# 推理权重显存
params_b = 7
for name, bytes_p in [("FP32", 4), ("FP16", 2), ("INT8", 1), ("INT4", 0.5)]:
    gb = params_b * 1e9 * bytes_p / 1024**3
    print(f"{name}: {gb:.1f} GB")
# FP32: 26.1 GB / FP16: 13.0 GB / INT8: 6.5 GB / INT4: 3.3 GB（按 1e9 换算）
# 更常见的近似说法：7B × 2B ≈ 14GB（按 1024³ 精算约 13GB）
```

**注意：推理实际显存 = 权重 + KV Cache + 激活值**（KV Cache 见 Q30，长上下文时可能超过权重本身）

### 训练显存估算（难度升级）

| 组件 | 每参数字节 | 7B 全参训练 |
|------|------------|-------------|
| 权重 | 2 bytes | 14 GB |
| 梯度 | 2 bytes | 14 GB |
| Adam 优化器状态 | 12 bytes（2×动量 + 8×方差，FP32） | 84 GB |
| **合计** | **16 bytes** | **≈ 112 GB**（需 8×A100 80G） |

### 如何用少量显存训练大模型？

- **LoRA**：只训练 ~0.1% 参数（7B 只训约 830 万参数），显存需求从 112GB → ~16GB
- **QLoRA**：4-bit 量化基座 + LoRA，24GB 消费级显卡即可微调 7B
- **ZeRO / 张量并行**：多卡分摊（显存不够，卡数来凑）

**面试话术：**
> "显存估算的核心是'参数×字节数'：7B 模型 FP16 推理要 14GB，INT4 只要 3.5GB；但全参训练要 16 字节/参数，7B 就要 112GB，所以训练必须上 LoRA——只训 0.1% 的参数，24G 显卡就能微调 7B。面试官问'为什么下载的模型 14G 一跑起来显存超了'，答案就是还有 KV Cache 和激活值。"

---

## 33. 什么是 Chat Template（对话模板）？为什么用错模板效果会暴跌？

**Chat Template = 把多轮消息列表转换成模型在训练时见过的格式（角色标记 + 特殊 Token）。**

### 为什么必须用模板？

模型训练时数据长这样（带角色标记）：
```
<|im_start|>system
你是一个AI助手<|im_end|>
<|im_start|>user
你好<|im_end|>
<|im_start|>assistant
你好！有什么可以帮你？<|im_end|>
```

如果直接拼接消息而不套模板：模型没见过"裸奔"的输入格式 → 角色信息丢失 → 答非所问、忘记 System Prompt。

### 不同模型模板不同（面试重点）

| 模型 | 模板特征 |
|------|----------|
| **ChatML（GPT/Qwen）** | `<|im_start|>system/user/assistant<|im_end|>` |
| **LLaMA 3** | `<|begin_of_text|><|start_header_id|>system<|end_header_id|>` |
| **Mistral / 部分模型** | `[INST] ... [/INST]` |

### 代码示例（正确姿势）

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")

messages = [
    {"role": "system", "content": "你是一个严谨的AI助手"},
    {"role": "user", "content": "1+1等于几？"},
]

# ✅ 用官方模板（自动处理角色标记和特殊Token）
prompt = tokenizer.apply_chat_template(messages, tokenize=False)
# '<|im_start|>system\n你是一个严谨的AI助手<|im_end|>\n<|im_start|>user\n1+1等于几？<|im_end|>\n<|im_start|>assistant\n<|im_end|>'

# ❌ 错误做法：手动字符串拼接，没有角色标记和特殊Token
prompt = f"System: 你是一个严谨的AI助手\nUser: 1+1等于几？\nAssistant:"
```

### 高频追问

- **谁负责套模板？** 推理框架（vLLM 等）一般内置，或调用方用 `apply_chat_template`
- **模板会额外消耗 Token 吗？** 会——特殊 Token 也占 token 数；长 System Prompt + 模板前缀可吃 Prompt Caching 红利
- **为什么开源模型聊天效果差？** 常见原因之一就是没套对模板（或 GenerationConfig 不对）

**面试话术：**
> "Chat Template 就是把消息列表转成模型训练时的输入格式，核心是角色标记和特殊 Token。不同模型模板不同——Qwen 用 ChatML 的 `<|im_start|>`，LLaMA 3 用 `<|start_header_id|>`——所以必须用 `apply_chat_template` 而不是手拼字符串。我在部署开源模型踩过坑：不套模板时模型忘记系统指令，套对模板后效果立竿见影。"

---

## 34. 什么是 MoE（混合专家模型）？为什么 DeepSeek V3 / Qwen3 都用它？（高频）

**MoE（Mixture of Experts）= 把 Transformer 中的 FFN 层替换成"多个专家 + 路由器"，每个 Token 只激活少数几个专家。**

### 核心原理（面试必答）

```
传统 Dense 模型：
输入 → FFN（所有参数都计算）→ 输出

MoE 模型：
输入 → 路由器(Gating) → 选 Top-2 专家 → 只有选中专家参与计算 → 加权求和输出
        └─ 专家1(FFN-A) 专家2(FFN-B) ... 专家8(FFN-H)
```

**三步流程：**
1. **路由器打分**：`G(x) = Softmax(W·x)`，为每个 Token 算出各专家的选择概率
2. **选 Top-K 专家**：一般 K=2（Mixtral 8x7B 激活 2/8；DeepSeek-V3 激活 8/256 个专家路由）
3. **加权融合**：选中专家的输出乘上门控概率再相加

### 关键概念

| 概念 | 说明 |
|------|------|
| **总参数量 vs 激活参数量** | DeepSeek-V3：总参数 671B，单 Token 只激活 37B——"总参大、激活少" |
| **路由器（Router/Gating）** | 一个小 FFN，决定每个 Token 走哪个专家 |
| **稀疏性** | 不是所有专家都激活，这是省算力的根源 |
| **负载均衡损失** | 辅助 Loss 惩罚"所有 Token 都挤向同一个专家"，防止个别专家过载 |

### 为什么 2026 年大模型都用 MoE？（优势）

1. **容量大、知识多**：总参数大 → 记住更多知识（效果好）
2. **计算省、推理快**：激活参数少 → 同预算下 FLOPs 低 50%+，推理成本直降
3. **扩展性好**：加专家 ≈ 加容量，不必重训整个模型（如 Qwen3-MoE 从 30B 扩到 235B 总参）

### 挑战与坑（面试加分点）

- **显存占用高**：所有专家权重都要加载进显存（DeepSeek-V3 671B 需多机）
- **通信开销**：专家并行时 Token 要跨卡转发（All-to-All），专家数越多通信越重
- **负载不均衡**：热门专家被反复选中，需要 Auxiliary Loss 平衡
- **微调更脆弱**：MoE 微调容易过拟合路由偏好，LoRA 微调需同时冻结/约束路由

**面试话术：**
> "MoE 的核心是'总参数大、激活参数少'——用路由器给每个 Token 挑 Top-2 专家，其余专家不计算。DeepSeek-V3 总参 671B 但单 Token 只激活 37B，效果接近稠密大模型、成本只有几分之一。但代价是显存和通信：专家全量驻留显存、跨卡通信是瓶颈，所以训练部署都比稠密模型更依赖集群设计。"

---

## 35. 为什么说 LLM API 是无状态的？多轮对话的"记忆"到底存在哪？（应用开发第一性原理）

**LLM API 无状态 = 每次调用都是独立的一次计算，模型本身不保存任何对话历史。**

### 核心认知

```
LLM = 一个纯函数：f(输入文本) → 输出文本

你上次说了什么？ → 模型不知道（它没有"上次"）
"记忆"的本质 → 应用层把历史消息重新拼进本次输入
```

**为什么无状态？** 模型参数是静态的，一次推理只吃一份输入；"对话"只是把多轮消息按 Chat Template 拼成一个长 Prompt 再喂进去。

### 对工程的影响（面试重点）

| 需求 | 谁负责 | 怎么做 |
|------|--------|--------|
| 多轮记忆 | 应用层 | 把 messages 数组（历史）全部传给 API |
| 记忆裁剪 | 应用层 | 超出上下文就截断/摘要/检索（见 Q16） |
| 用户隔离 | 应用层 | 每个会话维护独立的消息列表（无共享状态，天然无串号风险，也需自己防串号） |
| 持久化 | 应用层 | 会话结束存数据库，下次重建 messages |

### 无状态带来的"福利"（回答加分）

- **天然可水平扩展**：无状态服务随意加副本，不需要同步会话状态
- **天然幂等/可重试**：同一请求重发结果一致（T=0 时），失败重试安全
- **状态全在数据里**：换模型/换供应商不丢记忆，因为记忆是应用的数据不是模型的状态

**面试话术：**
> "LLM API 是无状态的纯函数，'记忆'只是应用层把历史拼进 Prompt 的产物。这带来两个工程结论：一是所有状态管理（裁剪、摘要、持久化）必须自己实现；二是服务天然可水平扩展、可安全重试——因为我们没有需要同步的会话状态。我做的客服 Agent 就是把每轮对话持久化到 Redis，重启服务也不丢上下文。"

---

## 36. 什么是 Prompt Caching（提示词缓存）？为什么能把 LLM 成本降 90%？（API 层高频）

**Prompt Caching = API 层复用相同"前缀"的 KV Cache，跳过重复的 Prefill 计算。**

### 原理（一句话）

同一个前缀（System Prompt + 固定文档）第一次计算后，K/V 缓存保留一段时间；后续请求只要前缀逐字节相同，直接复用缓存，只计算新增部分。

```
请求1: [System Prompt] [文档A] [问题1]  → 全量计算, 写入缓存
请求2: [System Prompt] [文档A] [问题2]  → 前缀命中缓存, 只算[问题2] ✅
请求3: [System Prompt] [文档B] [问题3]  → 前缀变了, 缓存失效, 全量重算 ❌
```

### 与 KV Cache 的区别（高频追问）

| 维度 | KV Cache | Prompt Caching |
|------|----------|----------------|
| 范围 | 单次请求内 | 跨请求共享 |
| 解决 | 自回归重复计算（O(n²)→O(n)） | 重复前缀的 Prefill 浪费 |
| 收益 | 加速生成 | 降本 + 降首 token 延迟（TTFT） |

### 收益与成本（厂商数据）

- 输入 Token 缓存读取价约为标准价的 **10%（90% 折扣）**，命中即大赚
- 实测：结构化 Prompt 场景输入 token 消耗降 40-65%，首 token 延迟降 30-50%
- 配合"语义缓存"（相同问题直接返回历史答案，完全不调 API）可再省一层

### 最佳实践（面试必答）

1. **静态内容在前，动态内容在后**：`[System Prompt] → [检索文档] → [对话历史] → [当前问题]`（缓存键是精确字节序列，一个字符变了就全失效）
2. **System Prompt 里别注入易变内容**：时间戳、用户名、请求 ID 会让每次请求缓存全废
3. **显式标记缓存点**：Anthropic 用 `cache_control: {"type": "ephemeral"}`；OpenAI 自动前缀缓存；DeepSeek 上下文硬盘缓存自动生效
4. **RAG 场景把固定文档块放 System 位置**，多轮追问不重算

（引擎层实现：vLLM APCache / SGLang RadixAttention → 见 08-推理优化、19-推理框架）

**面试话术：**
> "Prompt Caching 是 API 层的 KV 复用：前缀逐字节相同就命中缓存，只算新增 Token。工程上三条铁律：静态放前动态放后、System Prompt 不掺时间戳等易变内容、RAG 固定文档放缓存区。我们多轮 RAG 问答开启后输入成本降了约 60%，TTFT 也明显改善——这是 2026 年降本性价比最高的一个开关。"

---

## 37. 大模型量化是什么？INT8 / INT4 / AWQ / GPTQ 怎么选？（基础概念版）

**量化 = 用更低精度的数值（INT8/INT4）表示模型权重/激活，减少显存占用并加速推理。**

### 一句话原理

```
FP16: 每个权重 2 字节 → 7B 模型 ≈ 14GB
INT8: 每个权重 1 字节 → 7B 模型 ≈ 7GB  （显存减半）
INT4: 每个权重 0.5 字节 → 7B 模型 ≈ 3.5GB（再减半）
```

量化不是简单截断：用 Scale + Zero Point 做线性映射，把 FP16 分布压到 INT 范围，尽量保留原分布。

### 为什么量化能加速？

1. **显存占用降** → 能塞进更小的卡 / 更大 batch
2. **显存带宽需求降** → 权重搬运更快（推理常受带宽瓶颈限制）
3. **部分硬件原生 INT8/INT4 算得快** → 计算也加速

### 常见方案对比（面试选型）

| 方案 | 原理 | 特点 | 适用 |
|------|------|------|------|
| **GPTQ** | 训练后量化，按 Hessian 信息逐层校准 | 经典成熟，GPU 友好 | vLLM 等 GPU 推理（首选之一） |
| **AWQ** | 激活感知：保护对输出影响大的"重要通道" | 精度损失更小（实测 <1%） | 生产环境推荐（vLLM 支持好） |
| **GGUF** | llama.cpp 的量化格式（Q4_K_M 等） | CPU/边缘设备友好 | 本地部署、CPU 推理 |
| **SmoothQuant** | 平滑激活离群值，W8A8 全量化 | 权重+激活都量化 | 追求极致吞吐、需要 W8A8 |

### 精度权衡（面试话术要点）

- **只量化权重（W8A16 / W4A16）**：损失小，是主流做法
- **权重+激活都量化（W8A8）**：吞吐更高，损失稍大，需校准数据
- INT4 时 7B 模型 4GB 显存可跑，但长上下文时 KV Cache 仍是显存大头

（框架级量化支持对比 → 见 19-推理框架）

**面试话术：**
> "量化就是给权重'降精度换显存'：INT8 减半、INT4 再减半。选型看部署环境：GPU 生产环境我优先 AWQ（激活感知，精度损失<1%），离线批量用 GPTQ，CPU/本地用 GGUF。核心原则是只量化权重不碰激活（W4A16），需要极致吞吐再上 W8A8 配合 SmoothQuant。7B 模型 INT4 后 4GB 显存就能跑，但别忽略 KV Cache 的占用。"

---

## 38. 为什么 LLM 数学能力差？怎么缓解？（高频追问）

**LLM 数学差是结构性问题，不是"再训大一点"就能完全解决的。**

### 四大原因（面试必答）

| 原因 | 说明 |
|------|------|
| **1. Tokenization 不一致** | 数字被切碎且不稳定：`1234 → ["12","34"]`，`1235 → ["123","5"]`——模型看不到稳定的"数位"结构，难以学算术规律 |
| **2. 自回归误差累积** | 多步计算中间错一步，后面全错（一步错步步错） |
| **3. 训练目标不匹配** | next-token 预测学的是"文本的统计分布"，而数学要的是"精确符号计算"——两者目标不同 |
| **4. 缺外部工具** | 模型没有"计算器"，大数乘法/高精度运算靠"神经记忆"硬扛 |

### 缓解方案（工程视角）

| 方案 | 做法 | 效果 |
|------|------|------|
| **CoT 分步计算** | 让模型一步步推导（配合验证） | 显著提升，但仍可能中间出错 |
| **代码解释器 / 工具调用** | 让模型写 Python 执行计算（Calculator/Tool Use） | 大数计算 100% 正确 ⭐ |
| **约束解码** | 数字场景用结构化输出 + 格式校验 | 防格式错，不防算错 |
| **自洽性（Self-Consistency）** | 多次采样投票取众数 | 提升稳定性 |
| **专用数学模型** | 数学题切给推理模型（o3/DeepSeek-R1） | 效果最好，成本高 |

### 面试加分点

- 工程上"别让 LLM 硬算"：金额、账目、精确计算一律走代码/规则引擎，LLM 只做意图理解和自然语言生成
- 模型路由：检测到数学类任务自动切推理模型或工具模式

**面试话术：**
> "LLM 数学差有三个根源：数字被 tokenizer 切碎导致学不到数位规律、自回归一步错步步错、训练目标本身就不是精确计算。工程解法是'别让它硬算'——精确计算一律用代码解释器或工具，LLM 只负责理解意图和表达结果；简单算术可以让它 CoT 分步算，复杂数学直接路由给推理模型。我在财务问答系统里就是这么做的，金额计算 0 错误。"

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
| **概率生成** | LLM是概率模型,输出经Softmax采样;同样输入可能不同输出 |
| **LLM vs 传统ML** | 生成式vs判别式;LLM自监督学习预测下一个Token,多任务通用 |
| **幻觉** | 编造不存在的信息,用RAG缓解;检测靠引用溯源/忠实度评估 |
| **偏见** | 对性别/种族的不公平输出,RLHF对齐 |
| **RAGAS** | RAG系统评估框架(忠实度、召回率、精确率) |
| **Logits** | 模型对词表每个Token的原始打分,经Softmax变概率 |
| **解码策略** | 贪心/Beam Search/采样,决定下一个Token怎么选 |
| **重复惩罚** | 对已出现Token的Logits惩罚,防复读机 |
| **EOS停止符** | 特殊终止Token,生成遇到它即结束 |
| **Decoder-only** | 主流LLM架构,预训练与推理目标统一(next-token) |
| **Embedding** | 文本→稠密向量,语义相近距离近;上下文相关是主流 |
| **上下文学习(ICL)** | 不更新参数,靠示例学会任务(Zero/Few-shot) |
| **三阶段训练** | 预训练(学知识)→SFT(学对话)→对齐(学偏好) |
| **Scaling Law** | 参数/数据/算力与Loss的幂律关系;Chinchilla≈1:20 |
| **KV Cache** | 缓存历史K/V,推理复杂度O(n²)→O(n);代价是显存 |
| **RLHF vs DPO** | RLHF=奖励模型+PPO;DPO=直接偏好优化,主流 |
| **显存估算** | 权重=参数×字节数;7B FP16≈14GB,INT4≈3.5GB |
| **Chat Template** | 消息转训练格式(角色标记);不同模型模板不同 |
| **MoE混合专家** | FFN换成多专家+路由器,总参大激活少(DeepSeek V3:671B激活37B) |
| **无状态性** | LLM API不保存状态,"记忆"=应用层拼历史进上下文 |
| **Prompt Caching** | 复用相同前缀KV,静态在前动态在后,输入成本降40-65% |
| **量化** | FP16→INT8/INT4减半再减半;生产用AWQ,CPU用GGUF |
| **LLM数学差** | 数字tokenize不一致+误差累积;精确计算走工具/代码 |
| **LLM选型** | 质量×速度×成本三维权衡;模型路由+缓存降本60-90% |

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
