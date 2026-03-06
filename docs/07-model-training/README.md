# 🎓 大模型微调与训练面试题

> **难度：** ⭐⭐⭐⭐
> **更新：** 2026-03-05
> **考点：** LoRA、RLHF、DPO、微调策略、训练优化

## 📋 目录

1. [微调基础概念](#一微调基础概念)
2. [LoRA与PEFT](#二lora与peft)
3. [对齐技术](#三对齐技术-rlhf与dpo)
4. [训练优化](#四训练优化)
5. [速记卡片](#五速记卡片)

## 一、微调基础概念

### Q1: 什么是微调（Fine-tuning）？为什么需要微调？

<details>
<summary>💡 答案要点</summary>

**微调 = 在预训练模型基础上，用特定任务数据继续训练**

**为什么需要微调？**

| 场景 | 预训练模型 | 微调后 |
|------|------------|--------|
| **领域适配** | 通用知识 | 专业领域（医疗、法律） |
| **任务优化** | 多任务能力 | 特定任务（分类、摘要） |
| **风格定制** | 标准输出 | 特定风格（客服、助手） |
| **行为对齐** | 可能不安全 | 符合人类价值观 |

**微调 vs 预训练：**

| 维度 | 预训练 | 微调 |
|------|--------|------|
| **数据量** | 海量（TB级） | 较少（GB-MB级） |
| **训练时间** | 数周-数月 | 数小时-数天 |
| **成本** | 极高（数百万美元） | 较低（数千-数万美元） |
| **目标** | 学习通用知识 | 适配特定任务 |

**面试话术：**
> "微调是在预训练模型基础上的二次训练。预训练让模型学会语言，微调让模型学会特定任务。就像通才变专家。"

</details>

### Q2: 全量微调 vs 参数高效微调（PEFT）有什么区别？

<details>
<summary>💡 答案要点</summary>

**核心区别：更新多少参数**

| 类型 | 更新参数量 | 内存占用 | 训练时间 | 效果 |
|------|------------|----------|----------|------|
| **全量微调** | 100% | 高（需存储全部梯度） | 长 | 最好 |
| **PEFT** | 0.1-1% | 低（只存储少量梯度） | 短 | 接近全量 |

**PEFT 的主要方法：**

```
参数高效微调（PEFT）
├── LoRA（Low-Rank Adaptation）
├── Adapter（适配器层）
├── Prompt Tuning（提示词微调）
├── Prefix Tuning（前缀微调）
└── P-Tuning（混合方法）
```

**资源对比（以 7B 模型为例）：**

| 方法 | 可训练参数 | GPU 显存 | 训练时间 |
|------|------------|----------|----------|
| 全量微调 | 7B（100%） | ~80GB | 10h |
| LoRA | 70M（1%） | ~20GB | 3h |
| Prompt Tuning | 1M（0.01%） | ~16GB | 1h |

**面试话术：**
> "PEFT 是用 1% 的参数达到 95% 的效果。特别是 LoRA，在资源受限时是首选。我在项目中用 LoRA 微调 13B 模型，单卡 A100 就够了。"

</details>

### Q3: 什么时候用微调，什么时候用 RAG？

<details>
<summary>💡 答案要点</summary>

**选择矩阵：**

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| **知识库问答** | RAG | 知识更新快，需要引用溯源 |
| **格式输出** | 微调 | 固定格式（JSON、SQL） |
| **风格迁移** | 微调 | 学习特定语言风格 |
| **代码生成** | RAG + 微调 | RAG检索示例，微调学习模式 |
| **客服对话** | RAG + 微调 | RAG检索知识，微调学习话术 |

**决策树：**
```
需要最新知识？
    └── 是 → RAG
    └── 否 → 固定格式输出？
            └── 是 → 微调
            └── 否 → 数据量大（>10K）？
                    └── 是 → 微调
                    └── 否 → RAG + Few-shot
```

**面试话术：**
> "RAG 和微调不是对立的，而是互补的。RAG 解决知识更新问题，微调解决行为和格式问题。我在项目中结合两者：用 RAG 检索知识，用微调优化输出格式。"

</details>

## 二、LoRA与PEFT

### Q4: 什么是 LoRA？它的原理是什么？

<details>
<summary>💡 答案要点</summary>

**LoRA = Low-Rank Adaptation（低秩适配）**

**核心思想：** 不直接修改原始权重，而是添加一个低秩矩阵来捕获变化。

**数学原理：**
```
原始权重：W ∈ R^(d×k)
全量微调：W' = W + ΔW（ΔW 也是 d×k）

LoRA 微调：W' = W + BA
  其中：
  - B ∈ R^(d×r)
  - A ∈ R^(r×k)
  - r << min(d, k)（秩很小，如 r=8）

参数量对比：
  全量：d × k
  LoRA：d × r + r × k ≈ r(d + k)

  例如：d=4096, k=4096, r=8
  全量：16M 参数
  LoRA：65K 参数（减少 250 倍）
```

**工作流程：**
```
输入 → 原始层（冻结）→ 输出1
    ↓
    → LoRA层（可训练）→ 输出2
    ↓
    输出 = 输出1 + 输出2
```

**关键超参数：**

| 参数 | 说明 | 典型值 | 影响 |
|------|------|--------|------|
| **r（秩）** | 低秩矩阵的维度 | 4-64 | 越大效果越好，但参数越多 |
| **α（缩放）** | 缩放因子 | 16-32 | 控制 LoRA 的影响强度 |
| **target_modules** | 应用 LoRA 的层 | q_proj, v_proj | 越多效果越好，但参数越多 |

**面试话术：**
> "LoRA 的本质是用两个小矩阵的乘积来近似大矩阵的更新。就像用压缩格式存储变化。我在项目中用 LoRA r=8 微调 13B 模型，只需要 20GB 显存，而全量微调需要 80GB。"

</details>

### Q5: LoRA 的超参数怎么选？r 和 alpha 如何影响性能？

<details>
<summary>💡 答案要点</summary>

**超参数选择指南：**

**1. 秩（r）：**

| 任务复杂度 | 推荐 r 值 | 说明 |
|------------|-----------|------|
| 简单（情感分类） | 4-8 | 任务简单，低秩足够 |
| 中等（摘要生成） | 8-16 | 平衡效果和效率 |
| 复杂（代码生成） | 16-64 | 需要更强表达能力 |

**2. 缩放因子（α）：**
- 实际学习率 = α / r
- 常见设置：α = 2r（如 r=8, α=16）
- α 越大，LoRA 影响越强

**3. 目标模块（target_modules）：**

| 策略 | 模块 | 参数量 | 效果 |
|------|------|--------|------|
| 最小 | q_proj, v_proj | 最少 | 基础 |
| 推荐 | q_proj, k_proj, v_proj, o_proj | 中等 | 良好 |
| 最大 | 所有线性层（含 MLP） | 最多 | 最好 |

**实验结果（7B 模型，GSM8K 数据集）：**

| r | α | 准确率 | 训练时间 | 显存 |
|---|---|--------|----------|------|
| 4 | 8 | 82.3% | 2h | 18GB |
| 8 | 16 | 85.7% | 2.5h | 20GB |
| 16 | 32 | 87.1% | 3h | 24GB |
| 64 | 128 | 88.5% | 5h | 35GB |

**选择策略：**
```python
# 简单任务
r = 8
alpha = 16
target_modules = ["q_proj", "v_proj"]

# 复杂任务
r = 16
alpha = 32
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]
```

**面试话术：**
> "我通常从 r=8, α=16 开始，如果效果不够好再增加到 r=16。target_modules 优先选择注意力层（q/k/v），因为它们对语义理解影响最大。"

</details>

### Q6: QLoRA 和 LoRA 有什么区别？

<details>
<summary>💡 答案要点</summary>

**QLoRA = Quantized LoRA（量化 LoRA）**

**核心区别：在量化基础模型上应用 LoRA**

| 维度 | LoRA | QLoRA |
|------|------|-------|
| **基础模型精度** | FP16/BF16 | 4-bit（NF4） |
| **显存占用（7B）** | ~20GB | ~6GB |
| **训练速度** | 快 | 稍慢（量化开销） |
| **效果** | 基准 | 接近 LoRA（0.1-0.5% 差距） |

**QLoRA 的三大创新：**

1. **4-bit NormalFloat（NF4）量化**
   - 专为正态分布设计的数据类型
   - 比传统 INT4 更适合神经网络权重

2. **双重量化（Double Quantization）**
   - 对量化常数本身再量化
   - 节省额外 0.37GB 显存（7B 模型）

3. **分页优化器（Paged Optimizers）**
   - 使用 CPU-GPU 统一内存
   - 避免 OOM（内存溢出）

**显存对比（Llama 7B）：**

| 方法 | 模型 | 梯度 | 优化器 | 总计 |
|------|------|------|--------|------|
| 全量微调 | 28GB | 28GB | 56GB | 112GB |
| LoRA | 14GB | 0.3GB | 0.6GB | 15GB |
| QLoRA | 3.5GB | 0.3GB | 0.6GB | 4.4GB |

**面试话术：**
> "QLoRA 让我在消费级 GPU（如 RTX 4090 24GB）上微调 13B 模型成为可能。代价是训练速度慢 15-20%，但效果几乎没有损失。"

</details>

## 三、对齐技术：RLHF与DPO

### Q7: 什么是 RLHF？为什么需要对齐？

<details>
<summary>💡 答案要点</summary>

**RLHF = Reinforcement Learning from Human Feedback（基于人类反馈的强化学习）**

**为什么需要对齐？**

| 问题 | 示例 | 影响 |
|------|------|------|
| **价值观偏差** | 生成有害内容 | 安全风险 |
| **事实错误** | 编造不存在的信息 | 信任危机 |
| **格式混乱** | 答非所问、重复 | 用户体验差 |
| **不够有用** | 过于简短或啰嗦 | 实用性低 |

**RLHF 三阶段：**

```
┌─────────────────────────────────────────────────────────┐
│                    RLHF 完整流程                         │
└─────────────────────────────────────────────────────────┘

阶段1：监督微调（SFT）
  高质量对话数据 → 微调 → 基础对齐模型

阶段2：训练奖励模型（RM）
  人类标注偏好对比数据 → 训练 → 奖励模型
  （输入：问题+答案，输出：分数）

阶段3：强化学习优化（PPO）
  用奖励模型指导 → PPO 算法 → 最终模型
```

**详细流程：**

**阶段1 - SFT（Supervised Fine-Tuning）：**
```
数据：{问题, 高质量答案}
目标：让模型学会基本对话能力
数据量：1万-10万条
```

**阶段2 - RM（Reward Model）：**
```
数据：{问题, 答案A（好）, 答案B（差）}
目标：训练评分模型，评估答案质量
模型：通常用 SFT 模型改造
损失函数：
  L = -log(σ(r_好 - r_差))
  让"好答案"分数高于"差答案"
```

**阶段3 - PPO（Proximal Policy Optimization）：**
```
流程：
1. 模型生成答案
2. 奖励模型打分
3. PPO 更新策略
4. 添加 KL 散度惩罚（防止偏离太远）

目标函数：
  maximize E[r(x,y)] - β·KL(π_θ || π_ref)
  其中：
  - r(x,y)：奖励模型分数
  - KL：与参考模型的散度
  - β：惩罚系数
```

**面试话术：**
> "RLHF 是让 AI 学会'什么是好答案'。SFT 是打基础，RM 是建立评价标准，PPO 是不断优化。GPT-3.5/4、Claude 都用了 RLHF。"

</details>

### Q8: 什么是 DPO？它和 RLHF 有什么区别？

<details>
<summary>💡 答案要点</summary>

**DPO = Direct Preference Optimization（直接偏好优化）**

**核心思想：** 跳过奖励模型，直接从偏好数据优化策略。

**RLHF vs DPO：**

| 维度 | RLHF | DPO |
|------|------|-----|
| **流程复杂度** | 三阶段（SFT→RM→PPO） | 两阶段（SFT→DPO） |
| **训练稳定性** | 不稳定（PPO 难调） | 稳定（监督学习） |
| **计算成本** | 高（需训练 RM + PPO） | 低（只需一次微调） |
| **效果** | 好 | 接近甚至超越 RLHF |
| **显存占用** | 需同时加载多个模型 | 只需一个模型 |

**DPO 工作原理：**

```
输入数据：{问题, 好答案, 差答案}

损失函数：
L = -log(σ(β·log(π_θ(y_好|x)/π_ref(y_好|x))
          - β·log(π_θ(y_差|x)/π_ref(y_差|x))))

核心思想：
- 增加"好答案"的概率
- 降低"差答案"的概率
- 不偏离参考模型太远
```

**简化理解：**
```
RLHF：
  问题 → 生成答案 → 奖励模型打分 → PPO优化 → 更新模型

DPO：
  问题 + 好/差答案对 → 直接优化概率 → 更新模型
```

**对比示例（Llama 2 7B，Helpfulness 数据集）：**

| 方法 | 训练时间 | GPU 显存 | Win Rate |
|------|----------|----------|----------|
| RLHF | 12h | 80GB（4卡） | 68.5% |
| DPO | 4h | 40GB（2卡） | 69.8% |

**面试话术：**
> "DPO 是 RLHF 的简化版，但效果不打折扣。我在项目中用 DPO 替代 RLHF，训练时间减少 60%，效果还略好。特别适合资源受限的场景。"

</details>

### Q9: RLHF/DPO 的数据怎么标注？成本高吗？

<details>
<summary>💡 答案要点</summary>

**数据格式：**
```json
{
  "prompt": "请解释什么是量子计算",
  "chosen": "量子计算是利用量子力学原理...",
  "rejected": "量子计算就是很快的计算机"
}
```

**标注方法：**

| 方法 | 说明 | 成本 | 质量 |
|------|------|------|------|
| **人工标注** | 人工对比两个答案，选择更好的 | 高（$0.5-2/条） | 高 |
| **AI 辅助** | GPT-4 生成对比数据 | 中（$0.01-0.05/条） | 中 |
| **自动生成** | 用规则（长度、格式）筛选 | 低（几乎免费） | 低 |

**人工标注流程：**
```
1. 准备问题列表（1000个问题）
2. 让模型生成多个答案（每个问题4-8个）
3. 标注员两两对比，选择更好的
4. 质量控制（多人标注，投票）
5. 得到偏好数据对
```

**成本估算（训练一个 7B 对齐模型）：**

| 阶段 | 数据量 | 单价 | 总成本 |
|------|--------|------|--------|
| SFT 数据 | 10K | $1/条 | $10K |
| 偏好数据 | 50K对 | $0.5/对 | $25K |
| **总计** | - | - | **$35K** |

**降低成本的方法：**

1. **混合标注**
   - 核心数据：人工标注（5K，高质量）
   - 扩展数据：AI 生成（45K，批量）

2. **主动学习**
   - 优先标注模型不确定的样本
   - 减少 50% 标注量

3. **使用公开数据集**
   - Anthropic HH-RLHF（16万对话）
   - OpenAssistant（1万对话）
   - 免费，但可能不适配特定领域

**面试话术：**
> "我在项目中采用混合标注：5000 条核心数据人工标注，4.5万条扩展数据用 GPT-4 生成。成本从 $25K 降到 $7K，效果下降不到 5%。"

</details>

## 四、训练优化

### Q10: 训练时遇到 OOM（显存不足）怎么办？

<details>
<summary>💡 答案要点</summary>

**显存占用分析：**
```
总显存 = 模型 + 梯度 + 优化器状态 + 激活值 + 缓存

示例（7B 模型，FP16）：
  模型：14GB
  梯度：14GB
  优化器（Adam）：28GB
  激活值：10-20GB（取决于 batch size）
  总计：66-76GB
```

**解决方案：**

| 方法 | 显存节省 | 速度影响 | 实现难度 |
|------|----------|----------|----------|
| **梯度累积** | 50-80% | 无 | ⭐ |
| **混合精度（FP16）** | 50% | +20% | ⭐ |
| **梯度检查点** | 30-40% | -20% | ⭐⭐ |
| **DeepSpeed ZeRO** | 75-90% | -10% | ⭐⭐⭐ |
| **LoRA/QLoRA** | 80-95% | 无 | ⭐⭐ |
| **量化（8bit/4bit）** | 75% | -15% | ⭐⭐ |

**1. 梯度累积（Gradient Accumulation）：**
```python
# 原来：batch_size=32，一次性计算
loss = model(batch_32)
loss.backward()

# 改进：分 4 次，每次 batch_size=8
accumulation_steps = 4
for micro_batch in split_batch(batch_32, 4):
    loss = model(micro_batch) / accumulation_steps
    loss.backward()  # 梯度累积，不更新
optimizer.step()  # 累积 4 次后统一更新
```

**2. 梯度检查点（Gradient Checkpointing）：**
```python
# 不保存中间激活值，需要时重新计算
model.gradient_checkpointing_enable()

# 代价：训练时间增加 20%
# 收益：显存减少 30-40%
```

**3. DeepSpeed ZeRO：**
```
ZeRO-1：分片优化器状态（节省 4x）
ZeRO-2：分片梯度（节省 8x）
ZeRO-3：分片模型参数（节省 N x，N=GPU数）
```

**综合方案（7B 模型，单卡 A100 40GB）：**
```python
# 配置
model = AutoModelForCausalLM.from_pretrained(
    "llama-7b",
    load_in_4bit=True,  # 4bit 量化
    bnb_4bit_compute_dtype=torch.float16,
)

# LoRA
peft_config = LoraConfig(r=8, lora_alpha=16)

# 训练参数
training_args = TrainingArguments(
    per_device_train_batch_size=1,  # 小 batch
    gradient_accumulation_steps=16,  # 累积梯度
    gradient_checkpointing=True,  # 梯度检查点
    fp16=True,  # 混合精度
)

# 结果：显存占用 ~25GB，可以训练
```

**面试话术：**
> "遇到 OOM，我的解决流程是：先开梯度累积和 FP16（几乎无损），还不够就用 LoRA（轻量），实在不行就 QLoRA（最省）。曾经在单卡 24GB 上微调 13B 模型。"

</details>

### Q11: 如何防止微调时的灾难性遗忘（Catastrophic Forgetting）？

<details>
<summary>💡 答案要点</summary>

**灾难性遗忘 = 微调后模型忘记了预训练时学到的通用知识**

**示例：**
```
微调前：
  Q: 首都北京在哪个国家？
  A: 中国

微调后（用客服数据）：
  Q: 首都北京在哪个国家？
  A: 抱歉，我只能回答产品相关问题
  （忘记了通用知识）
```

**原因：**
- 微调数据分布与预训练数据差异大
- 训练时间过长，学习率过高
- 数据量太小，过拟合

**解决方案：**

| 方法 | 说明 | 效果 |
|------|------|------|
| **混合通用数据** | 微调时混入预训练数据 | ⭐⭐⭐⭐⭐ |
| **降低学习率** | 使用更小的学习率 | ⭐⭐⭐⭐ |
| **Early Stopping** | 不要训练太久 | ⭐⭐⭐ |
| **LoRA** | 只更新部分参数 | ⭐⭐⭐⭐⭐ |
| **正则化** | L2/Dropout | ⭐⭐⭐ |

**最佳实践：**

**1. 混合通用数据（推荐）：**
```python
# 微调数据：领域数据 + 通用数据
dataset = {
    "domain_data": 8000,  # 80% 领域数据
    "general_data": 2000,  # 20% 通用数据
}

# 通用数据来源
- Wikipedia 摘要
- 常识问答
- 代码片段
- 数学题
```

**2. 学习率策略：**
```python
# 全量微调
learning_rate = 1e-5  # 比预训练小 10-100 倍

# LoRA 微调
learning_rate = 3e-4  # 可以稍大，因为只更新少量参数
```

**3. 使用 LoRA：**
```python
# LoRA 天然防止灾难性遗忘
# 原因：原始参数冻结，只训练小矩阵
# 即使 LoRA 过拟合，移除后模型恢复原状
```

**评估遗忘程度：**
```python
# 微调前后对比
tasks = [
    "常识问答",  # MMLU
    "数学推理",  # GSM8K
    "代码生成",  # HumanEval
]

for task in tasks:
    score_before = evaluate(base_model, task)
    score_after = evaluate(finetuned_model, task)
    retention = score_after / score_before
    print(f"{task} 保留率: {retention:.1%}")

# 合格线：保留率 > 95%
```

**面试话术：**
> "我在微调时混入 20% 的通用数据，学习率设为 1e-5，用 LoRA 代替全量微调。微调后在 MMLU 上的表现只下降了 2%，成功避免了灾难性遗忘。"

</details>

### Q12: PEFT方法对比:LoRA vs QLoRA vs Adapter vs Prefix-Tuning

<details>
<summary>💡 答案要点</summary>

**PEFT (Parameter-Efficient Fine-Tuning) = 参数高效微调**

### 核心方法对比

| 方法 | 原理 | 可训参数比例 | 性能 | 显存占用 | 推理开销 |
|------|------|--------------|------|----------|----------|
| **全量微调** | 更新所有参数 | 100% | ⭐⭐⭐⭐⭐ | 高 | 无 |
| **LoRA** | 低秩矩阵 | 0.1-1% | ⭐⭐⭐⭐⭐ | 低 | 无(合并后) |
| **QLoRA** | 量化+LoRA | 0.1-1% | ⭐⭐⭐⭐ | 极低 | 稍慢 |
| **Adapter** | 瓶颈层 | 1-3% | ⭐⭐⭐⭐ | 低 | 略有 |
| **Prefix-Tuning** | 可学习前缀 | 0.01-0.1% | ⭐⭐⭐ | 极低 | 略有 |
| **Prompt-Tuning** | Soft Prompts | <0.01% | ⭐⭐ | 极低 | 略有 |

### 1. LoRA (推荐⭐⭐⭐⭐⭐)

**原理:**
```
W_new = W_frozen + B × A
其中 B ∈ R^(d×r), A ∈ R^(r×k), r << d,k
```

**优势:**
- ✅ 可合并到原模型,无推理开销
- ✅ 多个LoRA可共存切换
- ✅ 训练快,显存低
- ✅ 性能接近全量微调

**适用场景:** 所有微调场景,首选方案

**代码示例:**
```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=8,                          # 秩
    lora_alpha=16,                # 缩放因子
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none"
)
model = get_peft_model(model, config)
```

### 2. QLoRA (资源受限⭐⭐⭐⭐⭐)

**原理:** 4bit量化基础模型 + LoRA微调

**关键技术:**
- 4bit NormalFloat (NF4) 量化
- Double Quantization (双重量化)
- Paged Optimizers (分页优化器)

**性能对比 (Llama-70B):**

| 方法 | 显存需求 | 训练速度 | 性能损失 |
|------|----------|----------|----------|
| 全量FP16 | 280GB | 1x | 0% |
| LoRA FP16 | 80GB | 1.2x | ~1% |
| **QLoRA 4bit** | **48GB** | **1.1x** | **~3%** |

**适用场景:** 单卡A100/4090微调65B+大模型

**代码示例:**
```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-70b",
    quantization_config=bnb_config
)

# 再应用 LoRA
peft_config = LoraConfig(r=16, lora_alpha=32)
model = get_peft_model(model, peft_config)
```

### 3. Adapter (经典方案⭐⭐⭐⭐)

**原理:** 在Transformer层之间插入小的瓶颈模块

**结构:**
```
Input (d维)
  ↓
Down-projection (d → r)  # 降维
  ↓
Activation (ReLU/GELU)
  ↓
Up-projection (r → d)    # 升维
  ↓
Skip Connection         # 残差连接
  ↓
Output (d维)
```

**优势:**
- ✅ 多任务学习友好(每任务一个Adapter)
- ✅ 参数隔离,互不干扰
- ✅ 易于管理和切换

**劣势:**
- ❌ 推理时有额外计算开销
- ❌ 参数量比LoRA多2-3倍

**适用场景:** 多任务场景,需要频繁任务切换

### 4. Prefix-Tuning (极低参数⭐⭐⭐)

**原理:** 为每个任务学习一组虚拟Token作为前缀

```
[Prefix Tokens (可学习)] + [User Input] → Model → Output
```

**参数量:** 通常<0.1%

**优势:**
- ✅ 参数极少
- ✅ 适合多任务

**劣势:**
- ❌ 性能不如LoRA
- ❌ 占用上下文位置

**适用场景:** 超多任务场景(100+),资源极度受限

### 选择指南

**推荐流程图:**
```
需要微调?
  ↓
显存充足(>80GB) → 全量微调
  ↓
显存有限(40-80GB) → LoRA
  ↓
显存紧张(24-40GB) → QLoRA
  ↓
多任务切换频繁 → Adapter
  ↓
任务数量极多(100+) → Prefix-Tuning
```

**面试话术:**
> "PEFT的核心是trade-off:用更少的参数换取相似的性能。LoRA是最均衡的方案,性能几乎无损且无推理开销。QLoRA适合单卡微调大模型,我们用4090单卡成功微调了65B模型。Adapter适合多任务场景,但有推理开销。"

</details>

---

## 13. 微调数据如何准备?数据质量如何保证?

<details>
<summary>💡 答案要点</summary>

**数据质量 > 数据数量**

### 数据准备流程(6步)

**Step 1: 需求分析**
```python
# 明确微调目标
task_requirements = {
    "任务类型": "客服问答",  # 分类/生成/对话等
    "领域": "电商",
    "数据量需求": "至少1000条",
    "质量要求": "准确率>95%"
}
```

**Step 2: 数据收集**

| 来源 | 优点 | 缺点 | 适用 |
|------|------|------|------|
| **真实业务数据** | 最贴近实际 | 可能有噪声 | 首选 |
| **公开数据集** | 免费,量大 | 可能不匹配领域 | 补充 |
| **人工标注** | 质量可控 | 成本高 | 高质量小数据 |
| **LLM生成** | 快速,便宜 | 可能有偏差 | 数据增强 |

**Step 3: 数据清洗**

```python
def clean_training_data(raw_data):
    """数据清洗pipeline"""
    cleaned = []

    for item in raw_data:
        # 1. 去重
        if is_duplicate(item, cleaned):
            continue

        # 2. 过滤低质量
        if len(item["instruction"]) < 10:  # 问题太短
            continue
        if len(item["output"]) < 20:  # 回答太短
            continue

        # 3. 过滤有害内容
        if contains_sensitive(item["output"]):
            continue

        # 4. 格式标准化
        item["instruction"] = normalize_text(item["instruction"])
        item["output"] = normalize_text(item["output"])

        # 5. 语言过滤(只保留中文)
        if not is_chinese(item):
            continue

        cleaned.append(item)

    return cleaned

def normalize_text(text):
    """文本标准化"""
    # 统一标点符号
    text = text.replace("，", ",")
    text = text.replace("。", ".")

    # 去除多余空格
    text = re.sub(r'\s+', ' ', text).strip()

    # 统一大小写(英文)
    return text

# 使用
raw_data = load_raw_data("customer_service.jsonl")
cleaned = clean_training_data(raw_data)
print(f"清洗前: {len(raw_data)}, 清洗后: {len(cleaned)}")
# 清洗前: 5000, 清洗后: 3200 (过滤掉36%)
```

**Step 4: 数据标注**

```python
# 方法1: 人工标注(最准确但慢)
def manual_annotation():
    """人工标注流程"""
    for item in unlabeled_data:
        # 展示给标注员
        display(item["input"])

        # 标注员选择/输入答案
        label = annotator.label(item)

        # 质量检查:双人标注,一致性>90%
        label2 = annotator2.label(item)
        if label != label2:
            # 不一致,提交专家仲裁
            label = expert.resolve(item, label, label2)

        item["output"] = label

# 方法2: LLM辅助标注(快但需验证)
def llm_assisted_annotation(data):
    """LLM自动标注"""
    for item in data:
        # 用GPT-4生成标注
        prompt = f"""
        任务: 客服问答
        问题: {item["question"]}

        请生成专业的客服回答(100-200字):
        """

        label = gpt4.generate(prompt, temperature=0.3)
        item["output"] = label

    # 人工抽检20%
    sample = random.sample(data, int(len(data) * 0.2))
    for item in sample:
        human_check(item)

# 方法3: 主动学习(聪明标注)
def active_learning_annotation(data, budget=1000):
    """优先标注最有价值的数据"""

    # 用已有少量数据训练初始模型
    model = train_initial_model(labeled_data[:100])

    while len(labeled_data) < budget:
        # 让模型预测未标注数据
        predictions = model.predict(unlabeled_data)

        # 选择模型最不确定的样本
        uncertain_samples = select_uncertain(predictions, k=50)

        # 人工标注这些样本
        newly_labeled = manual_annotation(uncertain_samples)

        # 加入训练集,重新训练
        labeled_data.extend(newly_labeled)
        model = train_model(labeled_data)

    return labeled_data

# 效果:
# 随机标注1000条: 准确率75%
# 主动学习1000条: 准确率82% (+7%)
```

**Step 5: 数据格式化**

```python
# 标准格式: Alpaca格式
alpaca_format = {
    "instruction": "用户的指令/问题",
    "input": "额外的输入上下文(可选)",
    "output": "期望的输出"
}

# 示例数据
training_data = [
    {
        "instruction": "总结以下文章的主要内容",
        "input": "人工智能正在改变世界...(长文)",
        "output": "本文主要讲述了人工智能的三大影响:..."
    },
    {
        "instruction": "这个产品的退货政策是什么?",
        "input": "",
        "output": "我们提供7天无理由退货服务。退货流程:..."
    }
]

# 保存为JSONL
with open("train.jsonl", "w") as f:
    for item in training_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
```

**Step 6: 数据验证**

```python
def validate_training_data(data):
    """数据质量检查"""

    issues = []

    # 检查1: 分布均衡
    categories = [item.get("category") for item in data]
    counter = Counter(categories)

    for cat, count in counter.items():
        ratio = count / len(data)
        if ratio < 0.05 or ratio > 0.5:
            issues.append(f"类别'{cat}'占比{ratio:.1%},不均衡")

    # 检查2: 长度分布
    lengths = [len(item["output"]) for item in data]
    avg_len = sum(lengths) / len(lengths)

    if avg_len < 50:
        issues.append(f"平均输出长度{avg_len}太短")

    # 检查3: 重复率
    outputs = [item["output"] for item in data]
    duplicates = len(outputs) - len(set(outputs))
    dup_rate = duplicates / len(outputs)

    if dup_rate > 0.1:
        issues.append(f"重复率{dup_rate:.1%}过高")

    # 检查4: 语言一致性
    languages = [detect_language(item["output"]) for item in data]
    lang_counter = Counter(languages)

    if len(lang_counter) > 1:
        issues.append(f"包含多种语言: {dict(lang_counter)}")

    return issues

# 使用
issues = validate_training_data(training_data)
if issues:
    print("数据质量问题:")
    for issue in issues:
        print(f"- {issue}")
```

### 数据增强技术

**技术1: 同义词替换**
```python
def synonym_augmentation(text):
    """同义词替换增强数据"""
    from synonyms import nearby

    words = text.split()
    new_words = []

    for word in words:
        # 10%概率替换
        if random.random() < 0.1:
            syns = nearby(word)
            if syns:
                new_words.append(random.choice(syns[:3]))
            else:
                new_words.append(word)
        else:
            new_words.append(word)

    return " ".join(new_words)

# 原始: "这个产品质量很好"
# 增强: "这个商品品质很棒"
```

**技术2: 回译(Back Translation)**
```python
def back_translation(text, lang="en"):
    """中文→英文→中文,生成变体"""

    # 翻译成英文
    en_text = translator.translate(text, src="zh", dest=lang)

    # 翻译回中文
    zh_text = translator.translate(en_text, src=lang, dest="zh")

    return zh_text

# 原始: "我想退货"
# 回译: "我希望退回商品" (略有变化但意思相同)
```

**技术3: LLM生成变体**
```python
def llm_paraphrase(instruction, output, n=3):
    """用LLM生成n个语义相同的变体"""

    prompt = f"""
    原始指令: {instruction}
    原始输出: {output}

    请生成{n}个语义相同但表达不同的变体。

    要求:
    1. 保持语义完全一致
    2. 改变措辞和句式
    3. 保持专业性

    变体(JSON数组):
    """

    variants = json.loads(llm.generate(prompt))
    return variants

# 使用
original = {
    "instruction": "如何退货?",
    "output": "请在7天内联系客服..."
}

variants = llm_paraphrase(
    original["instruction"],
    original["output"],
    n=3
)

# 生成:
# 1. "退货流程是什么?" → "您可以在收货后7天内..."
# 2. "我要退货怎么办?" → "退货需在7日内..."
# 3. "退款步骤?" → "请于7天内..."
```

### 数据比例建议

| 任务类型 | 最小数据量 | 推荐数据量 | 说明 |
|---------|-----------|-----------|------|
| **简单分类** | 500 | 2000+ | 类别明确 |
| **复杂分类** | 1000 | 5000+ | 类别多,边界模糊 |
| **生成任务** | 1000 | 10000+ | 需要多样性 |
| **对话系统** | 5000 | 50000+ | 需要大量对话数据 |
| **领域适配** | 10000 | 100000+ | 领域知识密集 |

**面试话术:**
> "微调数据准备分6步:需求分析→收集→清洗→标注→格式化→验证。关键是质量>数量,我们清洗掉36%低质数据,用主动学习优先标注不确定样本,准确率+7%。数据增强用回译+LLM变体,从1000条扩充到3000条。最后验证分布均衡、长度合理、重复率<10%。实测1000条高质量数据效果超过5000条低质量数据。"

</details>

---

## 五、速记卡片

### 微调核心概念

| 概念 | 一句话解释 |
|------|------------|
| **微调** | 在预训练模型基础上，用特定任务数据继续训练 |
| **全量微调** | 更新所有参数，效果最好但成本高 |
| **PEFT** | 只更新 1% 参数，效果接近全量 |
| **SFT** | 监督微调，用标注数据训练 |
| **数据准备** | 6步:需求→收集→清洗→标注→格式化→验证,质量>数量 |

### LoRA核心概念

| 概念 | 一句话解释 |
|------|------------|
| **LoRA** | 用低秩矩阵近似权重更新，参数少 |
| **r（秩）** | 低秩维度，越大效果越好但参数越多 |
| **α（缩放）** | 控制 LoRA 影响强度，通常 α=2r |
| **QLoRA** | 在 4bit 量化模型上应用 LoRA |

### 对齐核心概念

| 概念 | 一句话解释 |
|------|------------|
| **RLHF** | 基于人类反馈的强化学习，三阶段 |
| **RM** | 奖励模型，评估答案质量 |
| **PPO** | 强化学习算法，优化策略 |
| **DPO** | 直接偏好优化，简化版 RLHF |

### 训练优化

| 方法 | 显存节省 | 速度影响 |
|------|----------|----------|
| 梯度累积 | 50-80% | 无 |
| FP16 | 50% | +20% |
| 梯度检查点 | 30-40% | -20% |
| LoRA | 80-90% | 无 |
| QLoRA | 90-95% | -15% |

## 📝 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-03-05 | 新增大模型微调与训练面试题 11 道 |


---

**上一模块：** [向量索引优化](../06-vector-index-optimization/)
**下一模块：** [推理优化](../08-inference-optimization/)

---

[返回目录 →](../../README.md)
