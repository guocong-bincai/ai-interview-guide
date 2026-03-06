# 🔍 向量数据库索引详解

> **难度：** ⭐⭐⭐⭐⭐
> **更新：** 2026-03-02
> **考点：** 向量索引原理、性能对比、选型指南

## 📋 核心面试题

### Q: 向量数据库有哪些索引？分别有啥区别和原理？

<details>
<summary>💡 完整答案</summary>

**主流索引类型对比：**

| 索引类型 | 全称 | 原理 | 速度 | 精度 | 内存 | 适用场景 |
|----------|------|------|------|------|------|----------|
| **HNSW** | Hierarchical Navigable Small World | 多层图结构，贪心搜索 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 高 | 追求速度，内存充足 |
| **IVF** | Inverted File Index | 先聚类，再在簇内搜索 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 中 | 数据量大，可接受精度损失 |
| **IVF-PQ** | IVF + Product Quantization | IVF + 向量压缩 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 低 | 内存受限，大数据量 |
| **LSH** | Locality Sensitive Hashing | 局部敏感哈希 | ⭐⭐⭐⭐ | ⭐⭐ | 低 | 超大规模，近似即可 |
| **Flat** | 暴力搜索 | 计算所有距离 | ⭐ | ⭐⭐⭐⭐⭐ | 中 | <1 万条数据 |

### 一、HNSW（层次导航小世界）

**原理：**
```
HNSW = 多层图结构 + 贪心搜索

1. 构建多层图：
   - 顶层：节点少，长距离跳跃
   - 底层：节点多，精细搜索
   - 每层都是一个小世界网络

2. 搜索过程：
   - 从顶层入口开始
   - 贪心搜索：找最近的邻居
   - 找到局部最优后，下降到下一层
   - 重复直到最底层
```

**图示：**
```
Layer 2 (顶层):  A ───── B
                       │
Layer 1 (中层):  C ───── D ───── E
                       │
Layer 0 (底层):  F ───── G ───── H ───── I
```

**优点：**
- ✅ 检索速度最快（O(log N)）
- ✅ 精度最高（接近暴力搜索）
- ✅ 支持实时插入

**缺点：**
- ❌ 内存占用高（存储图结构）
- ❌ 构建时间长

**性能数据：**
- 100 万条数据，检索延迟：< 10ms
- 内存占用：约 1-2GB（1536 维）
- 召回率（Recall@10）：> 95%

**适用场景：**
- 数据量 < 1000 万
- 内存充足
- 追求低延迟

**代码示例（Milvus）：**
```python
index_params = {
    "metric_type": "IP",  # 内积相似度
    "index_type": "HNSW",
    "params": {
        "M": 16,           # 每个节点的最大连接数
        "efConstruction": 200  # 构建时的搜索范围
    }
}
collection.create_index(field_name="embedding", index_params=index_params)
```

### 二、IVF（倒排文件索引）

**原理：**
```
IVF = 聚类 + 分桶搜索

1. 训练阶段：
   - 用 K-Means 把向量聚成 N 个簇（如 1024 个）
   - 每个簇有一个质心（centroid）

2. 索引阶段：
   - 每个向量分配到最近的簇
   - 建立 簇 ID → 向量列表 的倒排索引

3. 搜索阶段：
   - 计算查询向量与各簇质心的距离
   - 选最近的 k 个簇（如 k=10）
   - 只在这 k 个簇内暴力搜索
```

**图示：**
```
        查询向量 Q
            ↓
    ┌───────┼───────┐
    ↓       ↓       ↓
  簇 1     簇 2     簇 3  ← 计算与质心距离
    │       │       │
    └───────┼───────┘
            ↓
        选最近的 3 个簇
            ↓
    只在选中簇内暴力搜索
```

**优点：**
- ✅ 内存占用适中
- ✅ 适合大数据量
- ✅ 构建速度快

**缺点：**
- ❌ 精度有损失（近似搜索）
- ❌ 需要调参（簇数量）

**性能数据：**
- 100 万条数据，检索延迟：~50-100ms
- 内存占用：约 500MB-1GB
- 召回率（Recall@10）：85-90%

**适用场景：**
- 数据量 100 万 -1 亿
- 可接受精度损失
- 离线批量构建

**代码示例（FAISS）：**
```python
import faiss

# 创建 IVF 索引
d = 1536  # 向量维度
quantizer = faiss.IndexFlatL2(d)  # 质心索引
index = faiss.IndexIVFFlat(quantizer, d, nlist=1024)  # 1024 个簇

# 训练
index.train(vectors)

# 添加
index.add(vectors)

# 搜索
index.nprobe = 10  # 搜索 10 个簇
D, I = index.search(query_vector, k=10)
```

### 三、IVF-PQ（乘积量化）

**原理：**
```
IVF-PQ = IVF 聚类 + 向量压缩

1. IVF 聚类（同上）

2. 乘积量化（PQ）：
   - 把 1536 维向量切成 M 段（如 16 段）
   - 每段 96 维（1536/16）
   - 每段独立聚类（如 256 个质心）
   - 用质心 ID（1 字节）代替原始向量
   - 1536 维 float（6144 字节）→ 16 字节

3. 搜索：
   - 在压缩空间计算近似距离
   - 速度快，内存小
```

**压缩效果：**
```
原始向量：1536 维 × 4 字节 (float32) = 6144 字节
PQ 压缩后：16 段 × 1 字节 (uint8) = 16 字节
压缩率：6144 / 16 = 384 倍
```

**优点：**
- ✅ 内存占用极低
- ✅ 适合超大数据量
- ✅ 检索速度快

**缺点：**
- ❌ 精度损失较大
- ❌ 需要调参（分段数）

**性能数据：**
- 1000 万条数据，内存占用：约 1-2GB
- 检索延迟：~20-50ms
- 召回率（Recall@10）：80-85%

**适用场景：**
- 数据量 > 1000 万
- 内存受限
- 可接受精度损失

### 四、LSH（局部敏感哈希）

**原理：**
```
LSH = 哈希 + 桶内搜索

1. 核心思想：
   - 相似的向量哈希后落在同一个桶
   - 不相似的向量哈希后落在不同桶

2. 哈希函数：
   - h(v) = sign(w · v)  w 是随机向量
   - 多个哈希函数组成哈希表

3. 搜索：
   - 计算查询向量的哈希值
   - 找到对应桶
   - 只在这个桶内暴力搜索
```

**优点：**
- ✅ 内存占用低
- ✅ 适合超大规模
- ✅ 理论保证

**缺点：**
- ❌ 精度最低
- ❌ 哈希函数设计复杂

**适用场景：**
- 数据量 > 1 亿
- 精度要求不高
- 近似搜索即可

### 五、Flat（暴力搜索）

**原理：**
```
计算查询向量与所有向量的距离，排序取 top-k
```

**优点：**
- ✅ 精度 100%
- ✅ 无需构建索引
- ✅ 实现简单

**缺点：**
- ❌ 速度最慢（O(N)）
- ❌ 不适合大数据量

**性能数据：**
- 1 万条数据，检索延迟：< 10ms
- 100 万条数据，检索延迟：~5000ms

**适用场景：**
- 数据量 < 1 万
- 精度要求极高
- 原型验证

## 📊 性能对比总结

### 速度对比（100 万条数据）

| 索引 | 检索延迟 | 相对速度 |
|------|----------|----------|
| HNSW | ~10ms | 1x（最快） |
| IVF-PQ | ~20ms | 2x |
| IVF-Flat | ~50ms | 5x |
| LSH | ~30ms | 3x |
| Flat | ~5000ms | 500x（最慢） |

### 内存对比（100 万条，1536 维）

| 索引 | 内存占用 | 相对大小 |
|------|----------|----------|
| Flat | ~6GB | 1x |
| HNSW | ~12GB | 2x（图结构开销） |
| IVF-Flat | ~3GB | 0.5x |
| IVF-PQ | ~100MB | 0.017x |
| LSH | ~200MB | 0.033x |

### 精度对比（Recall@10）

| 索引 | 召回率 | 精度等级 |
|------|--------|----------|
| Flat | 100% | 精确 |
| HNSW | 95-98% | 极高 |
| IVF-Flat | 85-90% | 高 |
| IVF-PQ | 80-85% | 中 |
| LSH | 70-80% | 低 |

## 🎯 选型指南

### 按数据量选型

| 数据量 | 推荐索引 | 理由 |
|--------|----------|------|
| **<1 万** | Flat | 简单，精度 100% |
| **1 万 -100 万** | HNSW | 速度快，精度高的 |
| **100 万 -1000 万** | IVF-PQ | 平衡速度和内存 |
| **1000 万 -1 亿** | IVF-PQ / LSH | 内存受限 |
| **>1 亿** | LSH / 分片 | 超大规模 |

### 按场景选型

| 场景 | 推荐索引 | 关键指标 |
|------|----------|----------|
| **实时检索** | HNSW | 延迟 < 10ms |
| **离线分析** | IVF | 构建快 |
| **内存受限** | IVF-PQ | 压缩率高 |
| **超高精度** | Flat / HNSW | Recall > 95% |
| **近似即可** | LSH | 速度快 |

## 💡 面试话术

**标准回答：**
> "向量数据库主流索引有五种：HNSW、IVF、IVF-PQ、LSH、Flat。
>
> HNSW 是多层图结构，速度最快精度最高，但内存占用大，适合千万级以下数据。
> IVF 是先聚类再搜索，适合大数据量，但精度有损失。
> IVF-PQ 在 IVF 基础上加向量压缩，内存占用极低，适合超大数据量。
> LSH 用哈希方法，速度最快但精度最低。
> Flat 是暴力搜索，精度 100% 但只适合小数据量。
>
> 我在项目中用 HNSW，因为数据量 50 万条，内存充足，追求低延迟。"

**进阶回答：**
> "选型时我考虑三个维度：数据量、内存、精度要求。
>
> 数据量<100 万用 HNSW，延迟<10ms，Recall>95%。
> 100 万 -1000 万用 IVF-PQ，内存减少 100 倍，Recall 80-85%。
> >1000 万用 LSH 或分片。
>
> 另外还要考虑实时性：HNSW 支持实时插入，IVF 需要定期重建索引。"

</details>

### Q9: 混合检索的融合策略有哪些?RRF算法详解

<details>
<summary>💡 答案要点</summary>

**混合检索 = BM25(关键词) + Vector Search(语义) 融合**

### 为什么需要融合?

**单一检索的局限:**
```
查询: "Python性能优化"

BM25检索:
✅ 精确匹配"Python"关键词
✅ 找到包含"性能"、"优化"的文档
❌ 漏掉同义词"提速"、"加速"

向量检索:
✅ 找到语义相关的"Python加速技巧"
✅ 理解"优化"≈"提速"
❌ 可能返回"Java性能优化"(语义相似但主题不对)

混合检索:
✅ 精确+语义双重保障
```

### 融合策略对比

#### 1. 加权线性组合

**公式:**
```python
final_score = α * vector_score + (1-α) * bm25_score

其中α∈[0,1]控制权重
```

**问题: 分数范围不一致**
```python
vector_score: 0.3-0.9 (余弦相似度)
bm25_score: 2.5-15.7 (无上限)

直接相加没意义!需要归一化
```

**归一化方法:**
```python
# Min-Max归一化
def normalize(scores):
    min_s, max_s = min(scores), max(scores)
    return [(s - min_s) / (max_s - min_s) for s in scores]

vector_norm = normalize(vector_scores)  # → [0, 1]
bm25_norm = normalize(bm25_scores)      # → [0, 1]

final = α * vector_norm + (1-α) * bm25_norm
```

**缺点:** 归一化复杂,易受异常值影响

#### 2. RRF (Reciprocal Rank Fusion) ⭐推荐

**核心思想: 只看排名,不看分数**

**RRF公式:**
```python
RRF_score(doc) = Σ [1 / (k + rank_i(doc))]

其中:
- rank_i(doc): 文档在第i个检索器中的排名
- k: 平滑常数(通常k=60)
```

**详细计算示例:**
```python
# 查询: "Python优化"

# BM25检索top-5:
bm25_results = [
    (doc_A, score=15.2, rank=1),
    (doc_B, score=12.3, rank=2),
    (doc_C, score=10.1, rank=3),
    (doc_D, score=8.5, rank=4),
    (doc_E, score=7.2, rank=5)
]

# 向量检索top-5:
vector_results = [
    (doc_B, score=0.92, rank=1),  # doc_B也在BM25中
    (doc_F, score=0.88, rank=2),
    (doc_A, score=0.85, rank=3),  # doc_A也在BM25中
    (doc_G, score=0.82, rank=4),
    (doc_C, score=0.79, rank=5)   # doc_C也在BM25中
]

# RRF融合 (k=60):
k = 60

doc_A_rrf = 1/(60+1) + 1/(60+3) = 1/61 + 1/63 = 0.0164 + 0.0159 = 0.0323
doc_B_rrf = 1/(60+2) + 1/(60+1) = 1/62 + 1/61 = 0.0161 + 0.0164 = 0.0325
doc_C_rrf = 1/(60+3) + 1/(60+5) = 1/63 + 1/65 = 0.0159 + 0.0154 = 0.0313
doc_D_rrf = 1/(60+4) + 0 = 0.0156  # 只在BM25中
doc_E_rrf = 1/(60+5) + 0 = 0.0154
doc_F_rrf = 0 + 1/(60+2) = 0.0161  # 只在向量中
doc_G_rrf = 0 + 1/(60+4) = 0.0156

# 最终排序:
# 1. doc_B (0.0325) ← 两边都高
# 2. doc_A (0.0323) ← 两边都高
# 3. doc_C (0.0313)
# 4. doc_F (0.0161)
# 5. doc_D (0.0156)
```

**完整代码实现:**
```python
from collections import defaultdict

def reciprocal_rank_fusion(results_list, k=60):
    """
    results_list: [
        [('doc_A', 15.2), ('doc_B', 12.3), ...],  # BM25结果
        [('doc_B', 0.92), ('doc_F', 0.88), ...]   # 向量结果
    ]
    """
    rrf_scores = defaultdict(float)

    for results in results_list:
        for rank, (doc_id, score) in enumerate(results, start=1):
            rrf_scores[doc_id] += 1 / (k + rank)

    # 按RRF分数排序
    sorted_docs = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return sorted_docs

# 使用
bm25_results = [('doc_A', 15.2), ('doc_B', 12.3), ...]
vector_results = [('doc_B', 0.92), ('doc_F', 0.88), ...]

final_results = reciprocal_rank_fusion([bm25_results, vector_results])
```

**RRF优势:**
- ✅ 无需归一化(只看排名)
- ✅ 鲁棒性强(不受异常分数影响)
- ✅ 参数少(只有k需要调)
- ✅ 工程简单

#### 3. 加权RRF (高级)

**动态调整权重:**
```python
def weighted_rrf(results_list, weights, k=60):
    """
    weights: [0.7, 0.3]  # BM25权重0.7, 向量权重0.3
    """
    rrf_scores = defaultdict(float)

    for results, weight in zip(results_list, weights):
        for rank, (doc_id, score) in enumerate(results, start=1):
            rrf_scores[doc_id] += weight / (k + rank)

    return sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

# 专业查询(如医学术语): BM25权重高
medical_results = weighted_rrf([bm25, vector], weights=[0.8, 0.2])

# 通用查询: 向量权重高
general_results = weighted_rrf([bm25, vector], weights=[0.3, 0.7])
```

### k值选择指南

| k值 | 效果 | 适用场景 |
|-----|------|----------|
| k=10 | 高排名主导 | top结果质量极高 |
| k=60 (默认) | 平衡 | 大多数场景 |
| k=100 | 低排名也有影响 | 结果多样性重要 |

**调优建议:**
```python
# 在验证集上遍历k值
best_k = 60
best_recall = 0

for k in [10, 30, 60, 100, 150]:
    rrf_results = reciprocal_rank_fusion(results, k=k)
    recall = evaluate_recall(rrf_results, ground_truth)

    if recall > best_recall:
        best_recall = recall
        best_k = k

print(f"最优k={best_k}, Recall={best_recall}")
```

**性能对比:**

| 方法 | Recall@10 | 复杂度 | 可解释性 |
|------|-----------|--------|----------|
| BM25 only | 68% | 低 | ⭐⭐⭐⭐⭐ |
| Vector only | 72% | 低 | ⭐⭐⭐ |
| 加权融合 | 78% | 中(需归一化) | ⭐⭐ |
| **RRF (k=60)** | **82%** | **低** | **⭐⭐⭐⭐** |
| 加权RRF | 85% | 中 | ⭐⭐⭐ |

**面试话术:**
> "混合检索的融合策略我推荐RRF——它只看排名不看分数,避免了归一化的麻烦。公式是1/(k+rank)累加,k默认60。我们项目用RRF,召回率从单一检索的70%提升到85%,而且工程实现只要10行代码。"

</details>

---

## 📝 速记卡片

### 向量索引对比

| 索引 | 原理关键词 | 速度 | 精度 | 内存 | 数据量 |
|------|------------|------|------|------|--------|
| **HNSW** | 多层图 + 贪心 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 高 | <1000 万 |
| **IVF** | 聚类 + 分桶 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 中 | 100 万 -1 亿 |
| **IVF-PQ** | IVF+ 压缩 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 低 | 100 万 -1 亿 |
| **LSH** | 哈希 + 桶 | ⭐⭐⭐⭐ | ⭐⭐ | 低 | >1 亿 |
| **Flat** | 暴力搜索 | ⭐ | ⭐⭐⭐⭐⭐ | 中 | <1 万 |

### 混合检索融合

| 方法 | 原理 | 优缺点 | Recall提升 |
|------|------|--------|------------|
| **加权融合** | α×V + (1-α)×B | 需归一化,调参复杂 | +6% |
| **RRF** | Σ1/(k+rank) | 简单鲁棒,首选⭐ | +12% |
| **加权RRF** | Σw/(k+rank) | 动态权重,效果最好 | +15% |

**选型口诀：**
> 小数据用 Flat，大数据用 IVF，
> 要速度用 HNSW，要内存用 PQ，
> 超大规模用 LSH，实时插入 HNSW。
> 混合检索用RRF，简单高效k=60!

## 📊 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-03-02 | 新增向量数据库索引详解专题 |


---

**上一模块：** [AI Agent 基础](../05-ai-agent-basics/)
**下一模块：** [模型训练](../07-model-training/)

---

[返回目录 →](../../README.md)
