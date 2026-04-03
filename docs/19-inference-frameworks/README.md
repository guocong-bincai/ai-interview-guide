# 🔥 大模型推理框架面试题（vLLM / SGLang / TensorRT-LLM）

> **难度：** ⭐⭐⭐⭐⭐
> **更新：** 2026-04-03
> **考点：** vLLM、SGLang、TensorRT-LLM、PagedAttention、RadixAttention、推理优化

## 📋 目录

1. [三大推理框架概述](#一三大推理框架概述)
2. [核心技术对比](#二核心技术对比)
3. [性能基准对比](#三性能基准对比)
4. [选型与落地实践](#四选型与落地实践)
5. [高频面试题](#五高频面试题)

## 一、三大推理框架概述

### Q1: vLLM、SGLang、TensorRT-LLM 三大推理框架各自定位是什么？

<details>
<summary>💡 答案要点</summary>

**三大框架定位对比：**

| 框架 | 开发团队 | 核心定位 | 设计理念 |
|------|----------|----------|----------|
| **vLLM** | UC Berkeley Sky Computing Lab | 高性能通用推理引擎 | PagedAttention + 高吞吐量 + 易用性 |
| **SGLang** | UC Berkeley LMSYS.org | 结构化生成 + 复杂推理 | RadixAttention + 前缀复用 + 编程灵活性 |
| **TensorRT-LLM** | NVIDIA | 极致性能生产部署 | 硬件深度优化 + 极致低延迟 |

**一句话总结：**
- vLLM = 均衡通用，适合大多数场景
- SGLang = 擅长多轮对话 + 结构化输出
- TensorRT-LLM = 极致性能，生产环境首选

**市场使用情况：**
- vLLM：2025年加入PyTorch基金会，V1架构升级，业界最广泛使用
- SGLang：已部署超30万GPU，日处理数万亿tokens，多轮对话场景首选
- TensorRT-LLM：2025年9月发布v1.0，PyTorch-first架构降低使用门槛

**面试话术：**
> "我在项目中用过vLLM做推理服务，PagedAttention把显存利用率从20%提升到90%以上。对于多轮对话场景，SGLang的前缀缓存可以节省30-50%显存。生产环境如果追求极致性能，会选TensorRT-LLM。"

</details>

### Q2: 什么是 PagedAttention？它解决了什么问题？

<details>
<summary>💡 答案要点</summary>

**问题背景：**
- LLM推理需要存储KV Cache（键值缓存）
- 传统方案：连续内存分配，预分配固定大小
- 问题：内存碎片化、显存利用率低（~20%）

**PagedAttention 解决方案：**
```
传统方案：
显存: [请求1的KV  ][请求2的KV  ][    空闲    ]
      4GB        3GB         9GB → 碎片，无法分配

PagedAttention（分页式）：
显存: [块0][块1][块2][块3][块4][块5][块6][块7]
      物理上连续，逻辑上分页，按需分配
      → 显存利用率高达 90%+
```

**核心原理：**
- 受操作系统虚拟内存/分页启发
- KV Cache 按"页"管理，每页 16 个 tokens
- 物理显存连续存储，逻辑上随机访问

**性能提升：**
- 吞吐量提升 2-10 倍（相比 naive 实现）
- 显存利用率从 ~20% → 90%+

**面试话术：**
> "PagedAttention 是 vLLM 的核心创新。传统的 KV Cache 预分配造成严重显存碎片，PagedAttention 用分页管理，按需分配，显存利用率从 20% 提到 90%+。就像内存管理里的虚拟内存，物理上连续，逻辑上分页，按需分配。"

</details>

### Q3: 什么是 RadixAttention？和 PagedAttention 有什么区别？

<details>
<summary>💡 答案要点</summary>

**RadixAttention = SGLang 的核心技术创新**

**核心思想：**
- 多轮对话场景中，前缀（system prompt、few-shot examples）通常是共享的
- RadixAttention 用基数树（Radix Tree）管理 KV Cache
- 实现跨请求的前缀复用和自动缓存

**工作原理：**
```
请求1: [System] + [User1] → 生成 [Response1]
请求2: [System] + [User2] → 生成 [Response2]
请求3: [System] + [User1追问] → 生成 [Response3]

RadixAttention 的 KV Cache 结构：
         [System]
           ↓
    [User1] ← → [User2]
      ↓            ↓
  [Response1]  [Response2]
      ↓
  [User1追问] → [Response3]

→ System prompt 的 KV Cache 被三个请求共享
```

**性能对比：**

| 指标 | PagedAttention (vLLM) | RadixAttention (SGLang) |
|------|----------------------|-------------------------|
| **前缀缓存** | 不支持 | 支持（基数树管理） |
| **多轮对话效率** | 一般 | 优秀（自动复用） |
| **显存节省** | 90% 利用率 | 额外节省 30-50% |

**面试话术：**
> "RadixAttention 是 SGLang 的核心。SGLang 用基数树管理 KV Cache，前缀（System prompt、few-shot）天然共享。比如电商客服场景，同样的 System prompt 被千万次请求复用，SGLang 显存消耗只有 vLLM 的一半。"

</details>

## 二、核心技术对比

### Q4: 三大框架的内存管理机制有什么区别？

<details>
<summary>💡 答案要点</summary>

| 框架 | 技术 | 特点 |
|------|------|------|
| **vLLM** | PagedAttention（分页式） | 物理连续，逻辑分页，按需分配 |
| **SGLang** | RadixAttention（基数树） | 前缀复用，跨请求共享，自动缓存淘汰 |
| **TensorRT-LLM** | Paged KV Cache + In-flight Batching | 显存优化 + 动态批处理 |

**面试话术：**
> "三者的内存管理各有特色。vLLM 的 PagedAttention 是分页管理，显存利用率高；SGLang 的 RadixAttention 多了前缀共享，多轮对话场景省 30-50% 显存；TensorRT-LLM 用编译优化和量化，显存占用最低但仅支持 NVIDIA。"

</details>

### Q5: 什么是连续批处理（Continuous Batching）？

<details>
<summary>💡 答案要点</summary>

**连续批处理 vs 传统批处理：**

```
传统批处理：等所有请求同时开始，同时结束
请求A: [AAAA][BBBB][CCCC][DDDD] → 需要等
请求B: [EEEE][FFFF]               → 必须等
请求C: [GGGG][HHHH][IIII][JJJJ] → 憋住

连续批处理：新请求随时加入，完成即退出
时间t1: [请求A][请求B][请求C] → 一起跑
时间t2: [请求A][请求B][新请求D] → A走了，D加入
时间t3: [请求D][新请求E][新请求F] → B走了
→ GPU利用率大幅提升
```

**性能影响：**
- 吞吐量提升 5-10 倍
- SGLang 前缀缓存 → 多轮场景额外提升 2-3 倍

</details>

### Q6: 三大框架的结构化输出能力有什么差异？

<details>
<summary>💡 答案要点</summary>

| 框架 | 结构化输出 | 实现方式 |
|------|-----------|----------|
| **vLLM** | 基础支持 | 后处理 + 正则约束 |
| **SGLang** | 原生支持 | 正则表达式约束解码 |
| **TensorRT-LLM** | 不支持 | 需后处理 |

**SGLang 的正则约束解码：**
```python
# SGLang 原生支持 JSON 约束
response = sglang.generate(
    prompt="提取用户信息",
    json_schema={
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        }
    }
)
# 模型生成时直接受约束，不会超出 schema
```

**面试话术：**
> "SGLang 的正则约束解码是原生支持的，生成 JSON 时模型直接受约束，不会出现语法错误。vLLM 需要后处理提取 JSON，失败需要重试。生产环境中，SGLang 的结构化输出成功率比 vLLM 高很多。"

</details>

## 三、性能基准对比

### Q7: 三大框架的性能对比数据是什么样的？

<details>
<summary>💡 答案要点</summary>

**吞吐量对比（LLaMA-2-7B，Batch=32）：**

| 硬件 | vLLM | SGLang | TensorRT-LLM |
|------|-------|--------|-------------|
| A100 80GB | 2000-3000 tok/s | 3500-4500 tok/s | 4000-5000 tok/s |
| H100 80GB | 4000-6000 tok/s | 6000-8000 tok/s | 7000-10000 tok/s |

**显存效率（KV Cache 占用，LLaMA-2-7B，Batch=32）：**

| 序列长度 | vLLM | SGLang | TensorRT-LLM |
|----------|-------|--------|-------------|
| 2048 | 10.5 GB | 8.5 GB | 9.8 GB |
| 4096 | 19.8 GB | 15.2 GB | 18.5 GB |

**面试话术：**
> "从数据看，TensorRT-LLM 吞吐量最高，H100上能达到10000 tok/s。SGLang在多轮对话场景有额外优势，前缀缓存能省30-50%显存。vLLM最均衡，易用性好，HuggingFace模型无缝兼容。"

</details>

### Q8: 三大框架的量化支持有什么差异？

<details>
<summary>💡 答案要点</summary>

**量化支持对比：**

| 量化方案 | vLLM | SGLang | TensorRT-LLM |
|----------|------|--------|-------------|
| FP8 | ❌ | ❌ | ✅（H100/L40S专属） |
| INT4 | ✅（AWQ/GPTQ） | ✅（AWQ/GPTQ） | ✅ |
| AWQ | ✅ | ✅ | ✅ |

**量化性能提升（AWQ INT4，LLaMA-2-7B on A100）：**

| 框架 | FP16 | INT4 | 提升 |
|------|------|------|------|
| vLLM | 2500 tok/s | 4200 tok/s | 1.7× |
| SGLang | 3800 tok/s | 5800 tok/s | 1.5× |
| TensorRT-LLM | 4200 tok/s | 6500 tok/s | 1.5× |

**面试话术：**
> "量化是生产环境的标配。INT4 量化后 7B 模型可以从 16GB 降到 8GB，RTX 4090 都能跑。但量化有精度损失，我一般先用 vLLM 的 AWQ 量化，实测精度损失<1%，性能提升 1.5×。"

</details>

## 四、选型与落地实践

### Q9: 如何根据场景选择推理框架？

<details>
<summary>💡 答案要点</summary>

**选型决策树：**

```
追求极致性能？
    ├── 是 → TensorRT-LLM
    ↓ 否
多轮对话场景？
    ├── 是 → SGLang
    ↓ 否
需要结构化输出？
    ├── 是 → SGLang
    ↓ 否
快速验证/通用场景
    → vLLM
```

**场景选型建议：**

| 场景 | 推荐框架 | 原因 |
|------|----------|------|
| 日常推理/RAG API | vLLM | 易用，兼容性好，快速部署 |
| 多轮对话/客服 | SGLang | 前缀缓存，省显存，多轮效率高 |
| 结构化输出（JSON/Tool Call） | SGLang | 原生正则约束，成功率高 |
| 极致吞吐/大并发 | TensorRT-LLM | 性能最强 |
| 非NVIDIA硬件 | vLLM | AMD ROCm支持好 |

**面试话术：**
> "我的选型方法：先vLLM快速验证，再根据瓶颈优化。多轮对话选SGLang，生产环境追求性能选TensorRT-LLM。实际上很多公司是组合使用——vLLM做POC，TensorRT-LLM做生产。"

</details>

### Q10: 推理框架在生产环境有哪些常见问题？如何解决？

<details>
<summary>💡 答案要点</summary>

**常见问题与解决方案：**

### 问题1：显存溢出（OOM）
```python
# 限制最大序列长度
vllm = LLM(max_model_len=8192, gpu_memory_utilization=0.9)
# 量化降低显存
llm = LLM(model="Qwen2.5-7B-AWQ", quantization="AWQ")
```

### 问题2：延迟不稳定
```python
# 启用 chunked prefill
vllm = LLM(enable_chunked_prefill=True, max_num_batched_tokens=8192)
# 启用投机解码
vllm = LLM(speculative_model="Qwen2.5-0.5B")
```

### 问题3：吞吐量低
```python
# 调整 GPU 利用率
vllm = LLM(gpu_memory_utilization=0.95)
# Tensor并行
llm = LLM(tensor_parallel_size=4)
```

**生产环境监控指标：**

| 指标 | 合格线 | 说明 |
|------|--------|------|
| GPU 利用率 | > 80% | 低于说明有瓶颈 |
| TTFT（首字延迟） | < 1s | 用户感知延迟 |
| 错误率 | < 1% | OOM/超时比例 |

**面试话术：**
> "生产环境我遇到过三个经典问题：OOM就限流+量化；尾延迟高就开chunked prefill；吞吐量低就加batch size+前缀缓存。监控指标重点看GPU利用率和TTFT，GPU利用率低于80%一定有优化空间。"

</details>

## 五、高频面试题

### Q11: PagedAttention 为什么能大幅提升吞吐量？

<details>
<summary>💡 答案要点</summary>

**核心原因：解决显存碎片化问题**

- 传统方案：预分配固定大小的 KV Cache，显存碎片化 ~20% 利用率
- PagedAttention：物理连续，逻辑分页，按需分配
- 显存利用率从 ~20% → 90%+
- batch size 可增大 4-5 倍

```
显存利用率 20% → 90%：可用 batch size 增大 4-5 倍
+ 连续批处理：新请求动态加入
= 吞吐量提升 2-10 倍
```

**面试话术：**
> "就像内存管理从固定分区变成分页。固定分区会产生内存碎片，分页管理按需分配，内存利用率大幅提升。PagedAttention 正是这个思想在 GPU 显存管理上的应用。"

</details>

### Q12: SGLang 的 RadixAttention 在什么场景下优势最大？

<details>
<summary>💡 答案要点</summary>

**最佳场景：多轮对话 + 前缀复用**

| 场景 | 前缀特征 | 缓存收益 |
|------|----------|----------|
| 客服机器人 | System prompt 相同 | 高 |
| AI 助教 | Few-shot examples 相同 | 高 |
| 代码助手 | 项目 context 相同 | 高 |
| 单轮问答 | 无前缀复用 | 无收益 |

**性能数据（多轮对话，8轮）：**

| 框架 | 显存占用 | 吞吐量 |
|------|----------|--------|
| vLLM | 100% | 基准 |
| SGLang | 50-60% | 2-3× |

**面试话术：**
> "RadixAttention 在 Agent 场景优势最大，因为 Agent 的 System prompt 通常很长（可能几千 tokens），描述工具、约束、few-shot examples。每一轮对话都能复用这段前缀，显存节省 40-50%，延迟降低 30-50%。"

</details>

### Q13: TensorRT-LLM 为什么能实现极致性能？它的局限是什么？

<details>
<summary>💡 答案要点</summary>

**极致性能的来源：**
1. **内核融合**：减少显存访问次数
2. **FP8 量化**：硬件级支持，显存带宽翻倍（H100/L40S）
3. **TensorRT 编译器优化**：算子融合、图优化，比 PyTorch 快 2-5 倍

**局限：**

| 局限 | 说明 |
|------|------|
| 仅支持 NVIDIA | 苹果AMD都不支持 |
| 模型需编译 | 转换需额外时间（10-60分钟） |
| 调试困难 | 黑盒优化，出错难排查 |

**面试话术：**
> "TensorRT-LLM 的极致性能来自内核融合和硬件级优化，H100上能做到比vLLM快2-3倍。但它的局限也很明显：只支持NVIDIA，模型需要预编译。我的建议是：POC用vLLM快速验证，生产环境用TensorRT-LLM优化。"

</details>

### Q14: 什么是 Speculative Decoding？

<details>
<summary>💡 答案要点</summary>

**投机解码：用小模型"打草稿"，大模型"批改"**

```
Draft Model（小模型0.5B）：一次生成 k=4 个候选
生成: [今天][天气][很][好]

Target Model（大模型70B）：并行验证这4个token
- 今天 ✓  天气 ✓  很 ✓  好 ✗

接受: [今天][天气][很] → 接受3个
继续: [不错]...

原本1次生成1个token → 现在1次接受3个 → 3倍加速
```

**适用条件：**
- Draft 和 Target 模型相近（同系列）
- 输出有一定可预测性

**面试话术：**
> "Speculative Decoding 速度提升2-3倍，回复越长加速越明显。但要注意 Draft 和 Target 模型要相近，不然拒绝率太高反而更慢。"

</details>

### Q15: vLLM 和 SGLang 可以一起用吗？

<details>
<summary>💡 答案要点</summary>

**可以！两者是正交的优化，可以叠加。**

- SGLang 底层可以用 vLLM 作为后端
- vLLM 也在加入前缀缓存功能
- 两者功能越来越接近，最终都是连续批处理 + 前缀缓存 + 量化优化

**面试话术：**
> "vLLM 和 SGLang 不是互斥的。SGLang 可以用 vLLM 作为后端，同时享受两者的优化。选型时看团队熟悉哪个，vLLM 社区更大文档更全，SGLang 在复杂 Agent 场景更顺手。"

</details>

---

*版本: v2.4 | 更新: 2026-04-03 | by 二狗子 🐕*
