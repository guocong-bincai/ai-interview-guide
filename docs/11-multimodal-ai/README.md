# 🎨 多模态大模型面试题

> **难度：** ⭐⭐⭐⭐
> **更新：** 2026-03-05
> **考点：** CLIP、BLIP、多模态理解、图文生成

## 📋 目录

1. [多模态基础](#一多模态基础)
2. [CLIP模型](#二clip模型)
3. [BLIP模型](#三blip模型)
4. [应用实战](#四应用实战)
5. [速记卡片](#五速记卡片)

## 一、多模态基础

### Q1: 什么是多模态学习？为什么重要?

<details>
<summary>💡 答案要点</summary>

**多模态学习 = 让模型同时理解多种数据类型（图像、文本、音频、视频）**

**单模态 vs 多模态：**

| 模态 | 单模态 | 多模态 |
|------|--------|--------|
| **文本** | GPT：只看文字 | GPT-4V：看图+文字 |
| **图像** | ResNet：只看图 | CLIP：图+文字对齐 |
| **音频** | Whisper：只听声音 | AudioLM：声音+文字 |

**为什么需要多模态？**

1. **更丰富的理解**
   ```
   单模态：
   看图 → "一个动物"
   看文字 → "猫的特征"

   多模态：
   看图+文字 → "这是一只橘猫，正在睡觉"
   ```

2. **跨模态检索**
   ```
   文本检索图片：
   输入："夕阳下的海滩"
   输出：相关图片

   图片检索文本：
   输入：一张海滩照片
   输出："这是美丽的夕阳海滩..."
   ```

3. **生成任务**
   ```
   看图说话（Image Captioning）
   文生图（Text-to-Image）
   视频理解（Video QA）
   ```

**多模态的挑战：**

| 挑战 | 说明 | 解决方案 |
|------|------|----------|
| **模态对齐** | 图像和文本如何关联？ | 对比学习（CLIP） |
| **模态融合** | 如何结合不同模态？ | 交叉注意力（BLIP） |
| **数据获取** | 图文对数据标注成本高 | 网络爬取（LAION） |
| **计算成本** | 多模态模型参数量大 | 模型压缩、蒸馏 |

**主流多模态任务：**

```
多模态学习
├── 理解任务
│   ├── 图像字幕（Image Captioning）
│   ├── 视觉问答（VQA）
│   ├── 视觉推理（Visual Reasoning）
│   └── 跨模态检索（Cross-Modal Retrieval）
│
└── 生成任务
    ├── 文生图（Text-to-Image）
    ├── 图生文（Image-to-Text）
    ├── 视频生成（Video Generation）
    └── 音频生成（Audio Generation）
```

**面试话术：**
> "多模态学习让 AI 像人一样，能同时看、听、读。单模态是盲人摸象，多模态才能全面理解。CLIP 用对比学习对齐图文，GPT-4V 能看图回答问题。"

</details>

### Q2: 如何评估多模态模型的性能？

<details>
<summary>💡 答案要点</summary>

**评估维度：**

**1. 跨模态检索（Image-Text Retrieval）：**

| 指标 | 说明 | 计算方式 |
|------|------|----------|
| **R@1** | Top-1 召回率 | 正确结果在第1位的比例 |
| **R@5** | Top-5 召回率 | 正确结果在前5位的比例 |
| **R@10** | Top-10 召回率 | 正确结果在前10位的比例 |

**示例（Flickr30K）：**
```
任务：给定图片，从 1000 个候选文本中找出匹配的

CLIP 结果：
  R@1 = 88.0%（第1位就找对）
  R@5 = 98.7%（前5位能找对）
  R@10 = 99.4%（前10位能找对）
```

**2. 视觉问答（VQA）：**

| 指标 | 说明 |
|------|------|
| **准确率** | 答案完全匹配的比例 |
| **CIDEr** | 与人类答案的相似度 |

**3. 图像字幕（Image Captioning）：**

| 指标 | 说明 | 范围 |
|------|------|------|
| **BLEU** | n-gram 重叠度 | 0-1 |
| **METEOR** | 考虑同义词的匹配 | 0-1 |
| **CIDEr** | 共识度量 | 0-10 |
| **SPICE** | 语义匹配 | 0-1 |

**4. 文生图（Text-to-Image）：**

| 指标 | 说明 |
|------|------|
| **FID** | 生成图像与真实图像的分布距离（越小越好） |
| **CLIP Score** | 生成图像与文本的匹配度 |
| **人工评分** | 专家打分（质量、相关性） |

**综合评估（COCO Benchmark）：**

| 模型 | VQA Acc | Caption CIDEr | Retrieval R@1 |
|------|---------|---------------|---------------|
| CLIP | - | - | 58.4% |
| BLIP | 78.3% | 136.7 | 82.3% |
| BLIP-2 | 82.4% | 144.5 | 85.9% |

**面试话术：**
> "多模态评估要看多个维度。检索任务看 R@K，问答看准确率，字幕看 CIDEr。我在项目中用 CLIP Score 评估文生图质量，结合人工抽检确保效果。"

</details>

## 二、CLIP模型

### Q3: CLIP 的核心思想是什么？如何训练？

<details>
<summary>💡 答案要点</summary>

**CLIP = Contrastive Language-Image Pre-training（对比语言-图像预训练）**

**核心思想：** 用对比学习将图像和文本映射到同一个语义空间

**架构：**

```
┌─────────────────────────────────────────────────────────┐
│                     CLIP 架构                            │
└─────────────────────────────────────────────────────────┘

图像编码器（Image Encoder）
  ├── Vision Transformer (ViT)
  └── 或 ResNet
  输出：图像向量 v ∈ R^512

文本编码器（Text Encoder）
  ├── Transformer
  输出：文本向量 t ∈ R^512

对比学习（Contrastive Learning）
  目标：匹配的图文对相似度高，不匹配的低
```

**训练过程：**

**1. 数据准备（4 亿图文对）：**
```
图片1: 一只猫在睡觉.jpg
文本1: "A cat is sleeping"

图片2: 一辆红色汽车.jpg
文本2: "A red car"

...
```

**2. 对比损失（Contrastive Loss）：**
```python
# 批量（N=32768）
images = [img1, img2, ..., imgN]
texts = [text1, text2, ..., textN]

# 编码
I = image_encoder(images)  # N × 512
T = text_encoder(texts)     # N × 512

# 归一化
I = I / ||I||
T = T / ||T||

# 相似度矩阵
S = I @ T.T  # N × N

# 对比损失
正样本：对角线（img1 vs text1, img2 vs text2, ...）
负样本：非对角线（img1 vs text2, img1 vs text3, ...）

目标：
  对角线相似度尽量高（接近1）
  非对角线相似度尽量低（接近0）

损失函数：
  L = -1/N Σ [log(exp(S_ii) / Σ_j exp(S_ij))]
  （让正样本概率最大）
```

**3. 对称损失（双向）：**
```
图像→文本：给定图像，找匹配文本
文本→图像：给定文本，找匹配图像

总损失 = 图像→文本损失 + 文本→图像损失
```

**训练细节：**

| 参数 | 值 | 说明 |
|------|----|----|
| **数据量** | 4亿图文对 | LAION-400M |
| **Batch Size** | 32768 | 超大 batch |
| **负样本数** | 32767 | 同 batch 其他样本 |
| **训练时间** | ~12天 | 256 GPUs |
| **学习率** | 5e-4 | |

**推理（Zero-shot 分类）：**

```python
# 候选类别
classes = ["猫", "狗", "鸟", "车"]

# 构造提示词
prompts = [f"a photo of a {c}" for c in classes]
# ["a photo of a 猫", "a photo of a 狗", ...]

# 编码
image_features = clip.encode_image(image)  # 1 × 512
text_features = clip.encode_text(prompts)  # 4 × 512

# 相似度
similarity = image_features @ text_features.T  # 1 × 4
# [0.8, 0.1, 0.05, 0.05]

# 预测
prediction = classes[similarity.argmax()]  # "猫"
```

**CLIP 的优势：**

| 优势 | 说明 |
|------|------|
| **Zero-shot** | 不需要训练，直接分类任意类别 |
| **通用性** | 适用于各种视觉任务 |
| **鲁棒性** | 对分布偏移（domain shift）不敏感 |

**局限性：**

| 局限 | 说明 | 示例 |
|------|------|------|
| **细粒度分类差** | 难区分相似物体 | 猫的品种识别 |
| **OCR 能力弱** | 不擅长读图中文字 | 识别车牌号 |
| **不能生成** | 只能检索，不能生成字幕 | - |

**面试话术：**
> "CLIP 用对比学习把图像和文本拉到同一空间。一个 batch 有 32K 样本，每个样本都是 32K-1 个负样本。这让 CLIP 学会了强大的图文对齐能力，Zero-shot 分类超越很多有监督模型。"

</details>

### Q4: CLIP 如何做 Zero-shot 分类？为什么效果好？

<details>
<summary>💡 答案要点</summary>

**Zero-shot = 不需要训练，直接分类没见过的类别**

**CLIP 的 Zero-shot 流程：**

**1. 构造提示词模板（Prompt Engineering）：**
```python
# 基础模板
template = "a photo of a {class}"

# 改进模板（效果更好）
templates = [
    "a photo of a {class}",
    "a photo of a large {class}",
    "a photo of a small {class}",
    "a photo of the {class}",
    # ... 共 80 个模板
]

# 示例
class_name = "cat"
prompts = [t.format(class=class_name) for t in templates]
# ["a photo of a cat", "a photo of a large cat", ...]
```

**2. 编码文本和图像：**
```python
# 对所有类别生成提示词
all_prompts = []
for class_name in class_names:
    for template in templates:
        all_prompts.append(template.format(class=class_name))

# 编码提示词（批量）
text_features = clip.encode_text(all_prompts)  # N_class × N_template × 512

# 平均多个模板（ensemble）
text_features = text_features.mean(dim=1)  # N_class × 512

# 编码图像
image_features = clip.encode_image(image)  # 1 × 512

# 归一化
image_features = image_features / ||image_features||
text_features = text_features / ||text_features||
```

**3. 计算相似度并分类：**
```python
# 余弦相似度
similarity = image_features @ text_features.T  # 1 × N_class

# Softmax（转概率）
probabilities = softmax(similarity * temperature)

# 预测
prediction = class_names[probabilities.argmax()]
```

**为什么 Zero-shot 效果好？**

**1. 海量数据学习语义：**
```
训练数据：4 亿图文对
覆盖类别：数百万种物体、场景、动作

结果：
  CLIP 见过大量"猫"的图片和描述
  即使没在特定数据集上训练，也能识别猫
```

**2. 语言作为桥梁：**
```
传统 CV 模型：
  训练：看 1000 个类别的图片
  测试：只能识别这 1000 类

CLIP：
  训练：学习图文对齐
  测试：给任何文本描述，都能找对应图片

示例：
  训练时没见过"金毛犬"
  但见过"狗"、"金色"、"毛茸茸"
  → 能推理出"金毛犬"
```

**3. 提示词工程放大效果：**
```
单模板：
  "a photo of a cat"
  准确率：76.2%

多模板（80个）：
  "a photo of a cat"
  "a photo of a large cat"
  ...
  准确率：82.7%（+6.5%）
```

**实测性能（ImageNet）：**

| 模型 | 训练数据 | Zero-shot | Few-shot（16样本） |
|------|----------|-----------|-------------------|
| ResNet-50 | ImageNet | 0% | 56.4% |
| CLIP ViT-B/32 | 4亿图文对 | 68.3% | 82.7% |
| CLIP ViT-L/14 | 4亿图文对 | 76.2% | 88.9% |

**面试话术：**
> "CLIP 的 Zero-shot 本质是用语言知识迁移到视觉。通过对比学习，CLIP 学会了图文语义对齐。给任何文本描述，都能找到匹配的图像，不需要额外训练。多模板 ensemble 能进一步提升 5-10%。"

</details>

## 三、BLIP模型

### Q5: BLIP 和 CLIP 有什么区别？为什么需要 BLIP？

<details>
<summary>💡 答案要点</summary>

**BLIP = Bootstrapped Language-Image Pre-training（自举语言-图像预训练）**

**核心区别：**

| 维度 | CLIP | BLIP |
|------|------|------|
| **任务类型** | 只能理解（检索） | 理解 + 生成 |
| **训练目标** | 对比学习（ITC） | ITC + ITM + LM（三合一） |
| **架构** | 双编码器 | 编码器 + 解码器 |
| **能力** | 图文匹配 | 图文匹配 + 字幕生成 + VQA |

**为什么需要 BLIP？**

**CLIP 的局限：**
```
任务1：给图片找匹配文本 ✓
任务2：给图片生成字幕 ✗（不支持）
任务3：回答图片相关问题 ✗（不支持）

原因：
  CLIP 只有编码器，不能生成文本
```

**BLIP 的能力：**
```
任务1：图文检索 ✓（继承 CLIP）
任务2：图像字幕 ✓（新增）
任务3：视觉问答 ✓（新增）

实现：
  编码器：理解图像和文本
  解码器：生成文本
```

**BLIP 架构：**

```
┌─────────────────────────────────────────────────────────┐
│                     BLIP 架构                            │
└─────────────────────────────────────────────────────────┘

图像编码器（Image Encoder）
  ViT → 图像特征

文本编码器（Text Encoder）
  BERT → 文本特征（双向）

文本解码器（Text Decoder）
  GPT → 生成文本（单向）

多任务训练：
  1. ITC（Image-Text Contrastive）：对比学习
  2. ITM（Image-Text Matching）：二分类（匹配/不匹配）
  3. LM（Language Modeling）：生成字幕
```

**三个训练目标：**

**1. ITC（对比学习）：**
```python
# 和 CLIP 一样
image_features = image_encoder(image)
text_features = text_encoder(text)
loss_itc = contrastive_loss(image_features, text_features)
```

**2. ITM（匹配分类）：**
```python
# 判断图文是否匹配
combined = cross_attention(image_features, text_features)
logits = classifier(combined)  # [匹配, 不匹配]
loss_itm = bce_loss(logits, label)

# 正样本：真实配对
# 负样本：随机配对
```

**3. LM（生成字幕）：**
```python
# 自回归生成
text_decoder_input = [image_features, caption_prefix]
generated_caption = text_decoder.generate(text_decoder_input)
loss_lm = cross_entropy_loss(generated_caption, target_caption)
```

**BLIP 的创新：CapFilt（字幕过滤）：**

```
问题：
  网络爬取的图文对质量参差不齐
  很多文本描述不准确

BLIP 解决方案：
  1. 用 BLIP 模型生成新字幕（Caption）
  2. 用 BLIP 模型过滤低质量数据（Filter）
  3. 用清洗后的数据重新训练（Bootstrap）

流程：
  原始数据 → BLIP-Base 生成字幕
           → 过滤低质量样本
           → 清洗后数据
           → 训练 BLIP-Large

效果：
  数据质量提升 → 模型性能提升
```

**性能对比（COCO）：**

| 模型 | 图像字幕（CIDEr） | 图文检索（R@1） | VQA准确率 |
|------|-------------------|-----------------|-----------|
| CLIP | - | 58.4% | - |
| ALBEF | 131.4 | 73.1% | 74.5% |
| BLIP | 136.7 | 82.3% | 78.3% |

**面试话术：**
> "CLIP 是理解型模型，BLIP 是理解+生成型。BLIP 用三个训练目标（ITC+ITM+LM）统一了检索和生成任务。特别是 CapFilt 机制，用模型自己清洗数据，形成正反馈循环。"

</details>

### Q6: BLIP-2 有什么改进？Q-Former 是什么？

<details>
<summary>💡 答案要点</summary>

**BLIP-2 = 用更少参数达到更好效果**

**核心创新：Q-Former（Query Transformer）**

**BLIP-2 的动机：**

```
问题：
  BLIP 需要联合训练图像编码器和文本编码器
  → 参数量大（1B+）
  → 训练成本高
  → 难以利用已有的大语言模型（LLM）

目标：
  冻结视觉编码器（如 CLIP ViT）
  冻结语言模型（如 OPT、Flan-T5）
  只训练轻量级的连接层
```

**Q-Former 架构：**

```
┌─────────────────────────────────────────────────────────┐
│                    BLIP-2 架构                           │
└─────────────────────────────────────────────────────────┘

阶段1：视觉-语言表示学习
  冻结图像编码器（CLIP ViT-L）
      ↓
  Q-Former（32个可学习Query）
      ↓
  学习到的视觉表示

阶段2：视觉-语言生成学习
  Q-Former输出
      ↓
  线性层
      ↓
  冻结 LLM（OPT-2.7B / Flan-T5-XL）
      ↓
  生成回答
```

**Q-Former 详解：**

**什么是 Q-Former？**
```python
# 本质：可学习的查询向量 + Transformer

learnable_queries = nn.Parameter(torch.randn(32, 768))
# 32 个查询向量，每个 768 维

# 处理流程
image_features = frozen_image_encoder(image)  # 257 × 1024

# Q-Former 提取信息
queries = learnable_queries.expand(batch_size, -1, -1)
output = q_former(queries, image_features)  # 32 × 768

# 输出：固定长度的视觉表示（32个向量）
```

**为什么需要 Q-Former？**

**1. 降维压缩：**
```
图像编码器输出：257 个 token × 1024 维 = 262K 维
Q-Former 输出：32 个 token × 768 维 = 24K 维

压缩比：10.9x
好处：
  - 减少 LLM 输入长度
  - 提升推理速度
  - 降低计算成本
```

**2. 适配不同模态：**
```
视觉特征（CLIP）：连续、密集
语言特征（LLM）：离散、稀疏

Q-Former 作用：
  把视觉特征转换为 LLM 友好的表示
```

**3. 可学习的信息提取：**
```
固定数量的 Query（32个）
每个 Query 学习提取特定类型的信息：
  Query 1：物体类别
  Query 2：空间位置
  Query 3：颜色
  ...

类似 DETR 的 Object Queries
```

**两阶段训练：**

**阶段1：视觉-语言表示学习**
```python
# 目标：让 Q-Former 学会提取有用的视觉信息
# 损失：ITC + ITM + ITG（Image-Grounded Text Generation）

# 训练数据：图文对（1.29 亿）
# 冻结：图像编码器
# 训练：Q-Former
```

**阶段2：视觉-语言生成学习**
```python
# 目标：让 LLM 理解视觉信息
# 损失：Language Modeling Loss

# 训练数据：指令数据（视觉问答、字幕生成）
# 冻结：图像编码器 + LLM
# 训练：Q-Former + 线性投影层
```

**性能提升：**

| 模型 | 参数量 | 训练数据 | VQA准确率 | COCO字幕（CIDEr） |
|------|--------|----------|-----------|-------------------|
| BLIP | 224M | 1.29亿 | 78.3% | 136.7 |
| Flamingo-80B | 80B | 20亿 | 82.0% | 138.1 |
| BLIP-2 | 188M | 1.29亿 | **82.4%** | **144.5** |

**关键优势：**
```
BLIP-2（188M）> Flamingo（80B）
  - 参数少 400 倍
  - 效果更好
  - 训练更快
```

**面试话术：**
> "BLIP-2 的核心是 Q-Former，用 32 个可学习 Query 提取视觉信息。冻结视觉编码器和 LLM，只训练 Q-Former，参数量从 1B 降到 188M，效果反而更好。这证明了模态适配比联合训练更重要。"

</details>

## 四、应用实战

### Q7: 如何用多模态模型做图文检索系统？

<details>
<summary>💡 答案要点</summary>

**图文检索 = 输入文本找图片，或输入图片找文本**

**系统架构：**

```
┌─────────────────────────────────────────────────────────┐
│                  图文检索系统                             │
└─────────────────────────────────────────────────────────┘

离线索引：
  图片库（100万张）
     ↓
  CLIP 图像编码器
     ↓
  图像向量（100万 × 512维）
     ↓
  向量数据库（Milvus/Qdrant）

在线检索：
  用户输入："夕阳下的海滩"
     ↓
  CLIP 文本编码器
     ↓
  文本向量（1 × 512维）
     ↓
  向量检索（余弦相似度）
     ↓
  Top-K 图片
```

**实现步骤：**

**1. 离线索引（一次性）：**
```python
import clip
import torch
from pymilvus import Collection

# 加载 CLIP 模型
device = "cuda"
model, preprocess = clip.load("ViT-B/32", device=device)

# 编码所有图片
image_paths = load_image_paths()  # 100万张
batch_size = 256

all_features = []
for i in range(0, len(image_paths), batch_size):
    batch_paths = image_paths[i:i+batch_size]

    # 加载并预处理图片
    images = [preprocess(Image.open(p)) for p in batch_paths]
    images = torch.stack(images).to(device)

    # 编码
    with torch.no_grad():
        features = model.encode_image(images)
        features = features / features.norm(dim=-1, keepdim=True)

    all_features.append(features.cpu())

all_features = torch.cat(all_features)  # 100万 × 512

# 存入向量数据库
collection = Collection("image_vectors")
collection.insert([
    image_paths,
    all_features.tolist()
])
collection.create_index("image_vector", {"index_type": "IVF_FLAT", "metric_type": "IP"})
```

**2. 在线检索：**
```python
def search_images(query_text, top_k=10):
    # 编码文本
    text = clip.tokenize([query_text]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    # 向量检索
    results = collection.search(
        data=text_features.cpu().tolist(),
        anns_field="image_vector",
        param={"metric_type": "IP", "nprobe": 10},
        limit=top_k
    )

    # 返回结果
    return [(r.id, r.distance) for r in results[0]]

# 使用
results = search_images("夕阳下的海滩", top_k=10)
# [(img_id_1, 0.89), (img_id_2, 0.85), ...]
```

**3. 反向检索（以图搜文）：**
```python
def search_texts(query_image_path, candidate_texts, top_k=10):
    # 编码图片
    image = preprocess(Image.open(query_image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    # 编码候选文本
    texts = clip.tokenize(candidate_texts).to(device)
    with torch.no_grad():
        text_features = model.encode_text(texts)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    # 计算相似度
    similarity = (image_features @ text_features.T).squeeze(0)

    # 排序
    top_indices = similarity.argsort(descending=True)[:top_k]
    return [(candidate_texts[i], similarity[i].item()) for i in top_indices]
```

**优化策略：**

**1. 多模板 Ensemble：**
```python
templates = [
    "a photo of {}",
    "a picture of {}",
    "{}",
]

query_texts = [t.format(query) for t in templates]
text_features = model.encode_text(clip.tokenize(query_texts))
text_features = text_features.mean(dim=0)  # 平均多个模板
```

**2. 重排序（Rerank）：**
```python
# 第一步：向量检索召回 100 个候选
candidates = collection.search(text_features, limit=100)

# 第二步：用 BLIP 计算精确相似度
rerank_scores = []
for img_id in candidates:
    image = load_image(img_id)
    # 用 BLIP 的 ITM（Image-Text Matching）
    score = blip_itm(image, query_text)
    rerank_scores.append(score)

# 重新排序
final_results = sorted(zip(candidates, rerank_scores),
                      key=lambda x: x[1], reverse=True)[:10]
```

**性能优化：**

| 策略 | 效果 | 成本 |
|------|------|------|
| **ANN 索引** | 10-100x 加速 | 1-2% 精度损失 |
| **量化（INT8）** | 4x 显存节省 | <1% 精度损失 |
| **GPU 推理** | 100x 加速 | 硬件成本 |
| **批处理** | 5-10x 吞吐 | 增加延迟 |

**面试话术：**
> "图文检索的核心是向量相似度搜索。我用 CLIP 编码图文，用 Milvus 做 ANN 检索。100 万张图片，检索延迟 < 50ms。关键优化是 IVF 索引 + GPU 加速 + 多模板 ensemble。"

</details>

### Q8: 如何评估和优化多模态 RAG 系统？

<details>
<summary>💡 答案要点</summary>

**多模态 RAG = 检索图片和文本，生成答案**

**系统架构：**

```
用户问题："这张产品图的价格是多少？"
     ↓
1. 多模态检索
   - 图像检索：CLIP 找相似图片
   - 文本检索：BM25 + Embedding 找相关文档
     ↓
2. 融合排序
   - 图片：产品照片
   - 文档：产品说明、价格信息
     ↓
3. 多模态 LLM 生成
   - GPT-4V / BLIP-2
   - 输入：图片 + 文档 + 问题
   - 输出：答案
```

**评估指标：**

**1. 检索质量：**

| 指标 | 说明 | 计算方式 |
|------|------|----------|
| **Recall@K** | 前K个结果包含答案的比例 | 正确检索数 / 总问题数 |
| **MRR** | 平均倒数排名 | 1/N Σ(1/rank_i) |
| **NDCG** | 归一化折扣累积增益 | 考虑排序质量 |

**2. 生成质量：**

| 指标 | 说明 |
|------|------|
| **准确率** | 答案正确的比例 |
| **忠实度** | 答案基于检索内容的程度 |
| **相关性** | 答案与问题的匹配度 |

**3. 多模态特有指标：**

| 指标 | 说明 |
|------|------|
| **图像相关性** | 检索的图像是否相关 |
| **跨模态一致性** | 图像和文本信息是否一致 |

**优化策略：**

**1. 混合检索（Hybrid Retrieval）：**
```python
def hybrid_retrieve(query, query_image=None):
    results = []

    # 文本检索（BM25 + 向量）
    if query:
        text_results = text_retriever.search(query, k=20)
        results.extend(text_results)

    # 图像检索（CLIP）
    if query_image:
        image_results = clip_retriever.search(query_image, k=10)
        results.extend(image_results)

    # 融合排序（RRF - Reciprocal Rank Fusion）
    final_results = reciprocal_rank_fusion(results)
    return final_results[:10]
```

**2. 多模态 Rerank：**
```python
def multimodal_rerank(query, query_image, candidates):
    scores = []

    for doc in candidates:
        # 文本相似度
        text_score = compute_text_similarity(query, doc.text)

        # 图像相似度（如果文档包含图片）
        if doc.image and query_image:
            image_score = clip_similarity(query_image, doc.image)
        else:
            image_score = 0

        # 融合得分
        final_score = 0.6 * text_score + 0.4 * image_score
        scores.append(final_score)

    # 排序
    ranked = sorted(zip(candidates, scores),
                   key=lambda x: x[1], reverse=True)
    return ranked
```

**3. 提示词优化：**
```python
# 针对多模态的 Prompt
prompt = f"""
基于以下检索到的信息回答问题：

图片信息：
[包含 {len(images)} 张相关图片]

文本信息：
{retrieved_text}

问题：{user_question}

要求：
1. 优先使用图片中的信息
2. 如果图片和文本冲突，说明原因
3. 如果无法确定答案，明确指出
"""
```

**案例：电商客服**

**场景：** 用户上传商品图片，询问价格、尺寸等

**实现：**
```python
def ecommerce_qa(user_image, user_question):
    # 1. 图像检索：找相似商品
    similar_products = clip_search(user_image, k=5)

    # 2. 文本检索：找商品详情
    product_ids = [p.id for p in similar_products]
    product_details = database.query(product_ids)

    # 3. 构造上下文
    context = ""
    for product in product_details:
        context += f"""
        商品名：{product.name}
        价格：{product.price}
        尺寸：{product.size}
        图片相似度：{product.similarity:.2f}
        """

    # 4. 生成答案
    prompt = f"""
    用户上传了一张商品图片，问题是：{user_question}

    检索到的相似商品：
    {context}

    请回答用户问题。如果有多个匹配商品，列出前3个。
    """

    answer = gpt4v.generate(prompt, images=[user_image])
    return answer
```

**效果提升：**

| 优化 | Recall@5 | 准确率 | 用户满意度 |
|------|----------|--------|------------|
| 基线（纯文本 RAG） | 65% | 72% | 3.2/5 |
| + CLIP 图像检索 | 78% | 81% | 3.8/5 |
| + 多模态 Rerank | 85% | 87% | 4.2/5 |
| + GPT-4V 生成 | 85% | 92% | 4.5/5 |

**面试话术：**
> "多模态 RAG 的难点在于跨模态融合。我用 CLIP 做图像检索，BM25+向量做文本检索，RRF 融合排序。关键是 Rerank 阶段同时考虑图像和文本相似度，Recall@5 从 65% 提升到 85%。"

</details>

## 五、速记卡片

### 多模态核心概念

| 概念 | 一句话解释 |
|------|------------|
| **多模态学习** | 让模型同时理解图像、文本、音频等多种数据 |
| **模态对齐** | 将不同模态映射到同一语义空间 |
| **跨模态检索** | 输入一种模态，检索另一种模态 |
| **Zero-shot** | 不需要训练，直接分类任意类别 |

### CLIP

| 概念 | 一句话解释 |
|------|------------|
| **CLIP** | 用对比学习对齐图文，支持 Zero-shot |
| **对比损失** | 让匹配的图文相似，不匹配的不相似 |
| **Prompt 模板** | "a photo of a {class}"提升分类效果 |

### BLIP

| 概念 | 一句话解释 |
|------|------------|
| **BLIP** | 理解+生成，支持检索、字幕、VQA |
| **ITC+ITM+LM** | 三个训练目标：对比+匹配+生成 |
| **CapFilt** | 用模型生成字幕并过滤数据，自举学习 |
| **Q-Former** | 可学习 Query 提取视觉信息，连接视觉和语言 |

### 应用

| 应用 | 技术选型 |
|------|----------|
| **图文检索** | CLIP + 向量数据库 |
| **图像字幕** | BLIP / BLIP-2 |
| **视觉问答** | BLIP-2 + LLM |
| **多模态 RAG** | CLIP检索 + GPT-4V生成 |

## 📝 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-03-05 | 新增多模态大模型面试题 8 道 |


---

**上一模块：** [生产部署](../10-production-deployment/)  
**下一模块：** [框架与工具](../12-frameworks-tools/)

---

[返回目录 →](../../README.md)
