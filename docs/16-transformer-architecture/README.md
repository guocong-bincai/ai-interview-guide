# 🏗️ Transformer架构与注意力机制面试题

> **难度：** ⭐⭐⭐⭐
> **更新：** 2026-03-05
> **考点：** Transformer、Self-Attention、BERT、GPT、位置编码

---

## 📋 目录

1. [Transformer基础](#一transformer基础)
2. [注意力机制](#二注意力机制)
3. [BERT与GPT](#三bert与gpt)
4. [优化技巧](#四优化技巧)
5. [速记卡片](#五速记卡片)

---

## 一、Transformer基础

### Q1: 什么是Transformer？为什么要引入Transformer？

<details>
<summary>💡 答案要点</summary>

**Transformer = 基于自注意力机制的序列到序列模型**

**为什么需要Transformer？**

**RNN/LSTM 的问题：**

| 问题 | 说明 | 影响 |
|------|------|------|
| **串行计算** | 必须逐个处理token | 训练慢，无法并行 |
| **长程依赖** | 梯度消失/爆炸 | 难以捕捉远距离关系 |
| **信息瓶颈** | 所有信息压缩到隐状态 | 信息丢失 |

**Transformer 的优势：**

```
┌─────────────────────────────────────────────────────────┐
│                  Transformer 架构                        │
└─────────────────────────────────────────────────────────┘

输入序列 → Embedding + 位置编码
     ↓
Encoder (N × 6 层)
├── Multi-Head Self-Attention
├── Add & Norm
├── Feed-Forward Network
└── Add & Norm
     ↓
Decoder (N × 6 层)
├── Masked Multi-Head Self-Attention
├── Add & Norm
├── Encoder-Decoder Cross-Attention
├── Add & Norm
├── Feed-Forward Network
└── Add & Norm
     ↓
Linear + Softmax → 输出概率分布
```

**核心创新：**

1. **Self-Attention（自注意力）**
   - 每个token都能直接"看到"所有其他token
   - 复杂度：O(n²)，但可以并行

2. **Multi-Head Attention（多头注意力）**
   - 多个注意力头，捕捉不同维度的关系
   - 8 或 16 个头

3. **位置编码（Positional Encoding）**
   - 注入序列位置信息
   - sin/cos 函数编码

4. **残差连接 + Layer Norm**
   - 解决梯度消失
   - 稳定训练

**性能对比（机器翻译任务）：**

| 模型 | BLEU | 训练时间 | 参数量 |
|------|------|----------|--------|
| LSTM | 25.3 | 10天 | 200M |
| Transformer Base | 27.3 | 12小时 | 65M |
| Transformer Big | 28.4 | 3.5天 | 213M |

**面试话术：**
> "Transformer 通过自注意力机制替代了RNN的串行计算。每个token可以直接关注所有其他token，实现了并行计算，训练速度提升10-100倍。虽然复杂度是O(n²)，但在实际应用中，并行带来的收益远大于复杂度的损失。"

</details>

---

### Q2: Transformer的Encoder和Decoder有什么区别？

<details>
<summary>💡 答案要点</summary>

**核心区别：Encoder是双向的，Decoder是单向的**

**Encoder（编码器）：**

```python
# Encoder 结构（重复N次，通常N=6）
for layer in range(N):
    # 1. Multi-Head Self-Attention
    # 可以看到整个输入序列（双向）
    attn_output = MultiHeadAttention(
        Q=x, K=x, V=x  # Query、Key、Value 都来自输入
    )
    x = LayerNorm(x + attn_output)  # 残差 + 归一化

    # 2. Feed-Forward Network
    ffn_output = FeedForward(x)
    x = LayerNorm(x + ffn_output)
```

**特点：**
- ✅ 双向注意力（可以看到前后文）
- ✅ 并行处理所有token
- ✅ 输出：编码后的表示（上下文向量）

**Decoder（解码器）：**

```python
# Decoder 结构（重复N次，通常N=6）
for layer in range(N):
    # 1. Masked Multi-Head Self-Attention
    # 只能看到当前及之前的token（单向）
    masked_attn = MaskedMultiHeadAttention(
        Q=y, K=y, V=y,  # 来自目标序列
        mask=causal_mask  # 上三角mask
    )
    y = LayerNorm(y + masked_attn)

    # 2. Encoder-Decoder Cross-Attention
    # Query来自Decoder，Key和Value来自Encoder输出
    cross_attn = MultiHeadAttention(
        Q=y,  # 来自 Decoder
        K=encoder_output,  # 来自 Encoder
        V=encoder_output   # 来自 Encoder
    )
    y = LayerNorm(y + cross_attn)

    # 3. Feed-Forward Network
    ffn_output = FeedForward(y)
    y = LayerNorm(y + ffn_output)
```

**特点：**
- ⚠️ 单向注意力（Masked，只能看之前的）
- ✅ 包含Cross-Attention（连接Encoder和Decoder）
- ⚠️ 自回归生成（逐个token生成）

**关键差异对比：**

| 维度 | Encoder | Decoder |
|------|---------|---------|
| **Self-Attention** | 双向（无mask） | 单向（有mask） |
| **Cross-Attention** | ❌ 无 | ✅ 有（连接Encoder） |
| **输入** | 源序列（如英文） | 目标序列（如中文） |
| **输出** | 编码表示 | 生成序列 |
| **应用** | BERT（仅Encoder） | GPT（仅Decoder） |

**Mask 机制详解：**

```
# Encoder: 无mask，所有token都能互相看到
Input:  [I, love, AI]
Attention Matrix:
      I   love  AI
I    ✓    ✓    ✓
love ✓    ✓    ✓
AI   ✓    ✓    ✓

# Decoder: Causal Mask，只能看当前及之前
Input:  [我, 喜欢, 人工智能]
Attention Matrix:
        我  喜欢  人工智能
我      ✓   ✗    ✗
喜欢    ✓   ✓    ✗
人工智能 ✓   ✓    ✓
```

**面试话术：**
> "Encoder用双向Self-Attention理解输入，Decoder用单向Masked Attention生成输出。Decoder还有Cross-Attention层，让生成的每个token都能关注Encoder的所有输出。BERT只用Encoder（理解任务），GPT只用Decoder（生成任务）。"

</details>

---

## 二、注意力机制

### Q3: Self-Attention（自注意力）是如何计算的？

<details>
<summary>💡 答案要点</summary>

**Self-Attention = 让序列中的每个元素都能关注其他所有元素**

**数学公式：**

```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

**详细步骤：**

**1. 生成 Q、K、V：**
```python
# 输入：X (batch_size, seq_len, d_model)
# 例如：(1, 5, 512)

# 通过线性变换生成 Q、K、V
Q = X @ W_Q  # (batch_size, seq_len, d_k)
K = X @ W_K  # (batch_size, seq_len, d_k)
V = X @ W_V  # (batch_size, seq_len, d_v)

# W_Q, W_K, W_V 是可学习的权重矩阵
# d_k = d_v = d_model / num_heads (通常 64)
```

**2. 计算注意力分数：**
```python
# 点积计算相似度
scores = Q @ K.T  # (batch_size, seq_len, seq_len)
# 例如：(1, 5, 5)

# 缩放（防止梯度消失）
scores = scores / math.sqrt(d_k)

# 应用mask（可选，Decoder用）
if mask is not None:
    scores = scores.masked_fill(mask == 0, -1e9)
```

**3. Softmax归一化：**
```python
# 每一行做softmax，得到注意力权重
attention_weights = softmax(scores, dim=-1)
# (batch_size, seq_len, seq_len)

# 权重和为1
assert attention_weights.sum(dim=-1) == 1.0
```

**4. 加权求和：**
```python
# 用注意力权重加权V
output = attention_weights @ V
# (batch_size, seq_len, d_v)
```

**完整示例（序列长度=3）：**

```python
# 输入
X = [[1.0, 0.5],  # token 1
     [0.8, 1.0],  # token 2
     [0.5, 0.9]]  # token 3

# 假设 W_Q = W_K = W_V = I（单位矩阵）
Q = K = V = X

# 1. 计算相似度矩阵
scores = Q @ K.T
# [[1.25, 1.3, 0.95],
#  [1.3,  1.64, 1.3],
#  [0.95, 1.3, 1.06]]

# 2. 缩放（假设 d_k=2）
scores = scores / sqrt(2)
# [[0.88, 0.92, 0.67],
#  [0.92, 1.16, 0.92],
#  [0.67, 0.92, 0.75]]

# 3. Softmax
attention_weights = softmax(scores, dim=-1)
# [[0.32, 0.35, 0.33],  # token 1 对 3 个token的注意力
#  [0.28, 0.44, 0.28],  # token 2 对 3 个token的注意力
#  [0.29, 0.37, 0.34]]  # token 3 对 3 个token的注意力

# 4. 加权求和
output = attention_weights @ V
# [[0.77, 0.80],  # token 1的输出
#  [0.76, 0.87],  # token 2的输出
#  [0.74, 0.82]]  # token 3的输出
```

**为什么要缩放（除以√d_k）？**

```
问题：
  当 d_k 很大时（如512），QK^T 的值会很大
  → Softmax 梯度接近0（饱和）
  → 梯度消失

解决：
  除以 √d_k，将方差缩放到1
  → 保持Softmax输入在合理范围
  → 梯度稳定
```

**面试话术：**
> "Self-Attention通过 Q、K、V 三个矩阵计算。先用 QK^T 算相似度，除以√d_k 防止梯度消失，然后Softmax归一化得到权重，最后加权求和V得到输出。核心是让每个token都能直接关注其他所有token。"

</details>

---

### Q4: Multi-Head Attention（多头注意力）是什么？为什么要用多头？

<details>
<summary>💡 答案要点</summary>

**Multi-Head Attention = 多个Self-Attention并行，捕捉不同类型的关系**

**为什么需要多头？**

**单头的局限：**
```
单个注意力头只能学习一种模式
例如：
  "我 爱 吃 苹果"

单头可能只关注：
  语法关系："我" ← "爱"（主谓）

但错过了：
  语义关系："吃" ← "苹果"（动宾）
  共指关系："我" → "我"（指代）
```

**多头的优势：**
```
8个头可以学习不同的模式：
  Head 1: 语法关系（主谓宾）
  Head 2: 语义关系（实体-动作）
  Head 3: 位置关系（相邻词）
  Head 4: 长程依赖（句首-句尾）
  ...
  Head 8: 其他模式
```

**架构：**

```python
class MultiHeadAttention:
    def __init__(self, d_model=512, num_heads=8):
        self.num_heads = num_heads
        self.d_k = d_model // num_heads  # 64

        # 每个头有独立的 Q、K、V 权重
        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)

        # 输出投影
        self.W_O = nn.Linear(d_model, d_model)

    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)

        # 1. 线性变换并分头
        # (batch, seq_len, d_model) → (batch, seq_len, num_heads, d_k)
        Q = self.W_Q(Q).view(batch_size, -1, self.num_heads, self.d_k)
        K = self.W_K(K).view(batch_size, -1, self.num_heads, self.d_k)
        V = self.W_V(V).view(batch_size, -1, self.num_heads, self.d_k)

        # 转置以并行计算多头
        # (batch, num_heads, seq_len, d_k)
        Q = Q.transpose(1, 2)
        K = K.transpose(1, 2)
        V = V.transpose(1, 2)

        # 2. 每个头独立计算注意力
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        attention = F.softmax(scores, dim=-1)
        output = torch.matmul(attention, V)

        # 3. 合并多头
        # (batch, num_heads, seq_len, d_k) → (batch, seq_len, d_model)
        output = output.transpose(1, 2).contiguous()
        output = output.view(batch_size, -1, self.num_heads * self.d_k)

        # 4. 输出投影
        output = self.W_O(output)

        return output
```

**可视化示例（8个头）：**

```
输入："The cat sat on the mat"

Head 1（主语-谓语）:
  cat → sat (0.9)

Head 2（谓语-宾语）:
  sat → mat (0.8)

Head 3（修饰关系）:
  the → cat (0.7)
  the → mat (0.6)

Head 4（位置关系）:
  on → the (0.9)

...

最终输出 = Concat(Head1, Head2, ..., Head8) @ W_O
```

**参数对比：**

| 方案 | 参数量 | 表达能力 |
|------|--------|----------|
| 单头（d_model=512） | 512² × 3 = 786K | 低 |
| 8头（d_k=64） | 512² × 3 + 512² = 1.05M | **高** |

**实验证明（BLEU分数，机器翻译）：**

| 头数 | BLEU | 说明 |
|------|------|------|
| 1 | 25.8 | 单头 |
| 2 | 26.4 | +0.6 |
| 4 | 27.1 | +1.3 |
| 8 | **27.3** | **最佳** |
| 16 | 27.2 | 过多反而下降 |

**面试话术：**
> "Multi-Head Attention让模型同时学习多种注意力模式。8个头可以分别关注语法、语义、位置等不同维度的关系。虽然参数量略增，但表达能力大幅提升。实验表明8头是最佳选择。"

</details>

---

### Q5: 位置编码（Positional Encoding）是什么？为什么需要它？

<details>
<summary>💡 答案要点</summary>

**位置编码 = 给每个token注入位置信息**

**为什么需要？**

```
问题：
  Self-Attention 是置换不变的（permutation-invariant）

例子：
  "我 爱 你" 和 "你 爱 我"
  如果没有位置编码，Attention 输出可能相同
  → 无法区分顺序

解决：
  加入位置信息，让模型知道每个token的位置
```

**Transformer 的位置编码（Sinusoidal）：**

**公式：**
```python
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

其中：
  pos: 位置（0, 1, 2, ...）
  i:   维度索引（0 到 d_model/2）
  d_model: 模型维度（如512）
```

**实现：**
```python
def positional_encoding(max_len, d_model):
    # 创建位置矩阵
    position = torch.arange(max_len).unsqueeze(1)  # (max_len, 1)

    # 创建维度矩阵
    div_term = torch.exp(
        torch.arange(0, d_model, 2) *
        -(math.log(10000.0) / d_model)
    )  # (d_model/2,)

    # 初始化位置编码
    pe = torch.zeros(max_len, d_model)

    # 偶数维度用sin
    pe[:, 0::2] = torch.sin(position * div_term)

    # 奇数维度用cos
    pe[:, 1::2] = torch.cos(position * div_term)

    return pe

# 使用
pe = positional_encoding(max_len=100, d_model=512)
# pe.shape: (100, 512)

# 加到输入上
x = embedding(input_ids) + pe[: input_ids.size(1)]
```

**为什么用sin/cos？**

**优势：**

1. **确定性**：位置固定，不需要学习
2. **外推性**：可以处理比训练时更长的序列
3. **周期性**：不同位置间有规律的相对关系

**相对位置关系：**
```python
# PE(pos + k) 可以表示为 PE(pos) 的线性组合
# 这让模型能学习相对位置

例如：
  PE(5) 和 PE(10) 的距离
  = PE(1) 和 PE(6) 的距离
  （相对距离都是5）
```

**可视化（前10个位置，前64维）：**

```
位置  维度0  维度1  维度2  维度3  ...
0     0.00   1.00   0.00   1.00
1     0.84   0.54   0.01   1.00
2     0.91  -0.42   0.02   1.00
3     0.14  -0.99   0.03   1.00
...
```

**其他位置编码方案：**

| 方案 | 优点 | 缺点 | 应用 |
|------|------|------|------|
| **Sinusoidal** | 确定性，外推好 | 固定，不可学习 | Transformer |
| **Learned** | 可学习，灵活 | 不能外推 | BERT |
| **RoPE** | 相对位置，旋转 | 实现复杂 | LLaMA |
| **ALiBi** | 注意力偏置 | 需要重训练 | BLOOM |

**现代改进：RoPE（Rotary Position Embedding）：**

```python
# LLaMA/GPT-NeoX 使用
# 核心思想：在注意力计算时旋转 Q 和 K

def apply_rotary_emb(q, k, cos, sin):
    # 旋转 Q 和 K
    q_rot = rotate_half(q)
    k_rot = rotate_half(k)

    q = q * cos + q_rot * sin
    k = k * cos + k_rot * sin

    return q, k

# 优势：
#   - 相对位置编码
#   - 外推性更好
#   - 长文本性能优
```

**面试话术：**
> "Transformer 用 sin/cos 函数注入位置信息。优点是确定性、可外推、能表示相对位置。现代模型如 LLaMA 用 RoPE 改进，在注意力计算时旋转 Q 和 K，长文本性能更好。"

</details>

---

## 三、BERT与GPT

### Q6: BERT 和 GPT 有什么区别？

<details>
<summary>💡 答案要点</summary>

**核心区别：BERT是双向理解，GPT是单向生成**

**架构对比：**

| 维度 | BERT | GPT |
|------|------|-----|
| **架构** | 仅Encoder | 仅Decoder |
| **注意力** | 双向（无mask） | 单向（causal mask） |
| **训练目标** | MLM + NSP | 自回归语言模型 |
| **任务类型** | 理解（分类、NER） | 生成（文本生成） |
| **参数** | 110M-340M | 117M-175B |

**BERT（Bidirectional Encoder Representations from Transformers）：**

```
┌─────────────────────────────────────────────────────────┐
│                    BERT 架构                             │
└─────────────────────────────────────────────────────────┘

输入："The [MASK] sat on the mat"
  ↓
Embedding + Positional Encoding
  ↓
Transformer Encoder (12/24 层)
├── Multi-Head Self-Attention（双向）
└── Feed-Forward Network
  ↓
输出：每个token的上下文表示
  ↓
任务头（分类/NER/...）
```

**训练目标1：MLM（Masked Language Model）**
```python
# 随机mask 15%的token
原文："The cat sat on the mat"
Mask: "The [MASK] sat on the [MASK]"

# 预测被mask的词
损失 = CrossEntropy(预测, ["cat", "mat"])

# 15%中的策略：
#   80%: 替换为 [MASK]
#   10%: 替换为随机词
#   10%: 保持不变
```

**训练目标2：NSP（Next Sentence Prediction）**
```python
# 判断两句话是否连续
输入：
  A: "The cat sat on the mat."
  B: "It was very comfortable."
  Label: IsNext (1) or NotNext (0)

损失 = BCELoss(预测, Label)
```

**GPT（Generative Pre-trained Transformer）：**

```
┌─────────────────────────────────────────────────────────┐
│                    GPT 架构                              │
└─────────────────────────────────────────────────────────┘

输入："The cat sat on"
  ↓
Embedding + Positional Encoding
  ↓
Transformer Decoder (12/96 层)
├── Masked Multi-Head Self-Attention（单向）
└── Feed-Forward Network
  ↓
输出：下一个token的概率分布
  ↓
预测："the" (概率0.8)
```

**训练目标：自回归语言模型**
```python
# 预测下一个词
输入："The cat sat"
目标："on"

# 训练时并行计算所有位置的损失
损失 = Σ CrossEntropy(预测[i], 目标[i])

# 推理时自回归生成
generated = []
for i in range(max_len):
    next_token = model.predict(generated)
    generated.append(next_token)
```

**能力对比：**

| 任务 | BERT | GPT |
|------|------|-----|
| **文本分类** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **命名实体识别** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **问答** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **文本生成** | ⭐ | ⭐⭐⭐⭐⭐ |
| **摘要** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **对话** | ⭐ | ⭐⭐⭐⭐⭐ |

**实际应用：**

**BERT 擅长：**
```python
# 1. 分类
"This movie is great!" → Positive (0.95)

# 2. NER（命名实体识别）
"Apple was founded by Steve Jobs"
→ [Apple: ORG], [Steve Jobs: PER]

# 3. 问答
Context: "Paris is the capital of France."
Question: "What is the capital of France?"
Answer: "Paris" (span: [0, 5])
```

**GPT 擅长：**
```python
# 1. 文本生成
Prompt: "Once upon a time"
Output: "there was a brave knight..."

# 2. 对话
User: "How are you?"
GPT: "I'm doing well, thank you!"

# 3. 代码生成
Prompt: "Write a Python function to sort a list"
Output: "def sort_list(arr): return sorted(arr)"
```

**为什么BERT用双向，GPT用单向？**

```
BERT：
  目标是理解语言
  双向能看到完整上下文
  例如："bank"（银行 vs 河岸）需要前后文判断

GPT：
  目标是生成语言
  必须单向，否则"作弊"
  生成时只能看已生成的部分
```

**面试话术：**
> "BERT 是理解型模型，用双向Encoder + MLM训练，擅长分类、NER。GPT 是生成型模型，用单向Decoder + 自回归训练，擅长文本生成、对话。BERT看完整上下文理解语义，GPT逐个生成token。"

</details>

---

## 四、优化技巧

### Q7: Transformer 训练时有哪些优化技巧？

<details>
<summary>💡 答案要点</summary>

**核心优化方向：**

1. **学习率调度**
2. **正则化**
3. **训练稳定性**
4. **计算效率**

**1. 学习率调度（Warmup + Decay）：**

```python
# Warmup阶段：线性增加学习率
def get_lr(step, d_model, warmup_steps=4000):
    # Transformer 原论文方案
    lr = d_model ** (-0.5) * min(
        step ** (-0.5),
        step * warmup_steps ** (-1.5)
    )
    return lr

# 为什么需要Warmup？
# - 初始时权重随机，梯度不稳定
# - 小学习率让模型"热身"
# - 然后逐渐增大到峰值
# - 最后逐渐衰减

# 典型曲线：
#   0-4K步：线性增加 0 → peak_lr
#   4K步后：按 1/√step 衰减
```

**2. Label Smoothing（标签平滑）：**

```python
# 问题：Hard Label容易过拟合
hard_label = [0, 0, 0, 1, 0]  # one-hot

# 解决：Label Smoothing
smooth_label = [0.02, 0.02, 0.02, 0.92, 0.02]
# 真实类别：0.92（1 - smoothing）
# 其他类别：0.02（smoothing / (n_classes - 1)）

class LabelSmoothingLoss(nn.Module):
    def __init__(self, n_classes, smoothing=0.1):
        super().__init__()
        self.smoothing = smoothing
        self.n_classes = n_classes

    def forward(self, pred, target):
        # pred: (batch, n_classes)
        # target: (batch,) 类别索引

        confidence = 1.0 - self.smoothing
        smooth_value = self.smoothing / (self.n_classes - 1)

        # 构造smooth label
        smooth_label = torch.full_like(pred, smooth_value)
        smooth_label.scatter_(1, target.unsqueeze(1), confidence)

        # KL散度损失
        loss = -torch.sum(smooth_label * torch.log_softmax(pred, dim=1), dim=1)
        return loss.mean()

# 效果：提升泛化能力，BLEU +0.2
```

**3. Dropout 策略：**

```python
class TransformerLayer(nn.Module):
    def __init__(self, d_model=512, dropout=0.1):
        super().__init__()
        self.dropout = dropout

    def forward(self, x):
        # 1. Attention Dropout
        attn_output = self.attention(x)
        attn_output = F.dropout(attn_output, p=self.dropout, training=self.training)

        # 2. Residual Dropout
        x = x + attn_output

        # 3. FFN Dropout
        ffn_output = self.ffn(x)
        ffn_output = F.dropout(ffn_output, p=self.dropout, training=self.training)

        x = x + ffn_output

        return x

# 典型配置：
#   Attention Dropout: 0.1
#   Residual Dropout: 0.1
#   FFN Dropout: 0.1
#   Embedding Dropout: 0.1
```

**4. 梯度裁剪（Gradient Clipping）：**

```python
# 防止梯度爆炸
max_grad_norm = 1.0

for batch in dataloader:
    loss = model(batch)
    loss.backward()

    # 裁剪梯度
    torch.nn.utils.clip_grad_norm_(
        model.parameters(),
        max_grad_norm
    )

    optimizer.step()
    optimizer.zero_grad()
```

**5. Mixed Precision Training（混合精度）：**

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    optimizer.zero_grad()

    # FP16 前向传播
    with autocast():
        loss = model(batch)

    # 缩放损失，FP16 反向传播
    scaler.scale(loss).backward()

    # 更新权重（FP32）
    scaler.step(optimizer)
    scaler.update()

# 优势：
#   - 速度提升 2-3 倍
#   - 显存节省 50%
#   - 精度损失 < 0.1%
```

**6. 批量大小优化：**

```python
# 问题：GPU显存有限，batch_size受限

# 解决：梯度累积
accumulation_steps = 4
effective_batch_size = batch_size * accumulation_steps

optimizer.zero_grad()
for i, batch in enumerate(dataloader):
    loss = model(batch) / accumulation_steps
    loss.backward()

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()

# 效果：
#   原来：batch_size=32，每步更新
#   现在：batch_size=32×4=128，每4步更新
#   显存不变，效果更好
```

**7. 并行训练：**

```python
# 数据并行（Data Parallel）
model = nn.DataParallel(model)

# 分布式数据并行（Distributed Data Parallel，推荐）
model = nn.parallel.DistributedDataParallel(model)

# 模型并行（Model Parallel，超大模型）
# 不同层放在不同GPU
class ModelParallel(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(*layers[:6]).to('cuda:0')
        self.decoder = nn.Sequential(*layers[6:]).to('cuda:1')

    def forward(self, x):
        x = self.encoder(x.to('cuda:0'))
        x = self.decoder(x.to('cuda:1'))
        return x
```

**典型配置（Transformer Base）：**

| 参数 | 值 |
|------|-----|
| d_model | 512 |
| n_heads | 8 |
| d_ff | 2048 |
| n_layers | 6 |
| dropout | 0.1 |
| warmup_steps | 4000 |
| label_smoothing | 0.1 |
| max_grad_norm | 1.0 |
| batch_size | 25K tokens |
| optimizer | Adam(β1=0.9, β2=0.98, ε=1e-9) |

**面试话术：**
> "Transformer 训练的关键优化包括：Warmup学习率调度（先升后降）、Label Smoothing防过拟合、多层Dropout正则化、梯度裁剪防爆炸。工程上用混合精度训练加速2-3倍，梯度累积模拟大batch。"

</details>

---

## 五、速记卡片

### Transformer 核心概念

| 概念 | 一句话解释 |
|------|------------|
| **Transformer** | 基于自注意力的序列模型，可并行训练 |
| **Self-Attention** | 每个token关注所有其他token |
| **Multi-Head** | 多个注意力头捕捉不同关系 |
| **Positional Encoding** | sin/cos函数注入位置信息 |

### 注意力机制

| 公式/概念 | 说明 |
|----------|------|
| **Attention(Q,K,V)** | softmax(QK^T/√d_k)V |
| **缩放因子** | √d_k，防止梯度消失 |
| **Causal Mask** | 上三角mask，生成时只看之前 |
| **Cross-Attention** | Q来自Decoder，K/V来自Encoder |

### BERT vs GPT

| 维度 | BERT | GPT |
|------|------|-----|
| **架构** | Encoder only | Decoder only |
| **注意力** | 双向 | 单向(masked) |
| **训练** | MLM + NSP | 自回归LM |
| **任务** | 理解(分类/NER) | 生成(对话/摘要) |

### 优化技巧

| 技巧 | 效果 |
|------|------|
| **Warmup** | 稳定训练，先升后降学习率 |
| **Label Smoothing** | 防过拟合，+0.2 BLEU |
| **Gradient Clipping** | 防梯度爆炸，clip=1.0 |
| **Mixed Precision** | 加速2-3倍，节省50%显存 |
| **Gradient Accumulation** | 模拟大batch，不增显存 |

---

## 📝 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-03-05 | 新增 Transformer 架构与注意力机制面试题 7 道 |

---

**上一模块：** [多模态应用](../15-multimodal/)
**下一模块：** [NLP基础](../17-nlp-basics/)

---

**最后更新：** 2026-03-05
**维护者：** 二狗子 🐕
