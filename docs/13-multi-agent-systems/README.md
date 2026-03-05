# 🤖 AI Agent 面试题

> **难度：** ⭐⭐⭐  
> **考点：** 智能体设计模式、ReAct、Function Calling、多 Agent 协作

---

## 📋 目录

1. [基础概念题](#一基础概念题)
2. [设计模式题](#二设计模式题)
3. [工程实践题](#三工程实践题)
4. [高分回答模板](#四高分回答模板)

---

## 一、基础概念题

### Q1: 什么是 AI Agent？核心组件是什么？

<details>
<summary>💡 答案要点</summary>

**AI Agent = 能自主决策和行动的 AI**

**核心组件：**
```
┌─────────────────────────────────────────┐
│              AI Agent                   │
├─────────────────────────────────────────┤
│  1. LLM（大脑）   - 负责决策和推理       │
│  2. Tools（工具） - 负责执行（API/DB）   │
│  3. Memory（记忆）- 短期 + 长期记忆      │
│  4. Planning（规划）- 任务分解和反思     │
└─────────────────────────────────────────┘
```

**面试话术：**
> "Agent 和普通 LLM 的区别在于：LLM 只能说话，Agent 能干活。Agent 通过调用工具（搜索、API、数据库）完成实际任务。"

</details>

---

### Q2: ReAct 模式是什么？完整流程是什么？

<details>
<summary>💡 答案要点</summary>

**ReAct = Reasoning + Acting（推理 + 行动）**

**完整流程：**
```
1. Thought（思考）：分析当前情况，决定下一步
2. Action（行动）：调用工具（搜索、API、数据库等）
3. Observation（观察）：获取工具返回结果
4. 循环 1-3，直到任务完成
5. Final Answer（最终答案）
```

**Prompt 示例：**
```
你可以使用以下工具：
- search: 搜索网络信息
- calculator: 计算数学表达式
- database: 查询数据库

格式：
Thought: 你的思考
Action: 工具名称
Action Input: 工具参数
Observation: 工具返回
...（重复）
Final Answer: 最终答案

问题：{question}
```

**适用场景：** 需要多步推理 + 外部工具的任务

</details>

---

### Q3: Function Calling 的原理是什么？

<details>
<summary>💡 答案要点</summary>

**Function Calling = 让 LLM 调用外部函数**

**原理：**
1. **定义工具 Schema**（函数名、参数、描述）
2. **注册工具**（在 LLM 调用时传入 tools 参数）
3. **解析调用**（解析 LLM 返回的 function_call）
4. **执行工具**（调用实际 API 获取数据）
5. **返回结果**（将 API 结果返回给 LLM 生成最终答案）

**面试话术：**
> "Function Calling 的本质是将非结构化的自然语言转化为结构化的 JSON。在实战中，我通过它实现了自然语言直接查询 SQL 数据库，极大地降低了非技术人员的使用门槛。"

</details>

---

## 二、设计模式题

### Q4: 如何防止 Agent 进入死循环？

<details>
<summary>💡 答案要点</summary>

**问题原因：**
1. 工具调用失败，Agent 重复尝试
2. 任务太复杂，Agent 无法完成
3. Prompt 设计不好，Agent 理解错误

**解决方案：**
```python
max_iterations = 10
iteration = 0
visited = set()  # 记录已执行的动作

while iteration < max_iterations:
    action = agent.thought()
    if action in visited:
        break  # 检测到循环
    visited.add(action)
    result = agent.act(action)
    iteration += 1
```

**防护措施：**
1. 最大轮次限制（如最多 10 轮）
2. 超时机制（如 60 秒无进展则停止）
3. 工具调用去重（记录已调用的工具 + 参数）
4. 反思机制（让 Agent 评估当前进展）
5. 人工介入（复杂任务允许用户中断）

</details>

---

### Q5: Plan-and-Execute 和 ReAct 有什么区别？

<details>
<summary>💡 答案要点</summary>

| 维度 | ReAct | Plan-and-Execute |
|------|-------|------------------|
| **流程** | 思考→行动→观察（循环） | 先规划→再执行 |
| **可控性** | 低（动态决策） | 高（预先规划） |
| **可解释性** | 中 | 高（计划可见） |
| **适用场景** | 探索性任务 | 确定性任务 |

**Plan-and-Execute 流程：**
```
1. Planner：把大任务分解成小步骤
   ["步骤 1: 搜索天气", "步骤 2: 查询航班", "步骤 3: 预订酒店"]
   
2. Executor：一步步执行计划
   执行步骤 1 → 执行步骤 2 → 执行步骤 3
   
3. 可选：动态调整计划（如果执行失败）
```

</details>

---

### Q6: 多 Agent 协作怎么设计？

<details>
<summary>💡 答案要点</summary>

**典型架构：**
```
┌─────────────────────────────────────────────────────────┐
│                  多 Agent 协作系统                        │
└─────────────────────────────────────────────────────────┘

用户问题
    │
    ▼
┌─────────────┐
│ Coordinator │ ← 协调者（分配任务）
└──────┬──────┘
       │
       ├──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
│ Researcher│  │  Writer   │  │  Reviewer │  │  Executor │
│ 研究员     │  │  写手      │  │  审核员    │  │  执行者    │
└───────────┘  └───────────┘  └───────────┘  └───────────┘
```

**实战案例：**
> "我在项目中设计了一个内容创作 Agent 系统：
> - Researcher：搜索网络信息
> - Writer：根据检索内容写作
> - Reviewer：检查内容质量和合规性
> - Executor：发布到各个平台
> 
> 通过多 Agent 协作，内容生产效率提升了 3 倍。"

</details>

---

## 三、工程实践题

### Q7: 你设计过哪些类型的 Agent？

<details>
<summary>💡 高分回答</summary>

**案例 1：客服 Agent**
```
功能：自动回答用户咨询
架构：意图识别 → RAG 检索 → 答案生成 → 人工兜底
成果：解决 80% 常见问题，人工成本降低 60%
```

**案例 2：数据分析 Agent**
```
功能：自然语言查询数据库
架构：NL2SQL → SQL 执行 → 结果可视化
成果：非技术人员也能自助分析数据
```

**案例 3：代码生成 Agent**
```
功能：根据需求生成代码
架构：需求理解 → 代码生成 → 单元测试 → 自动修复
成果：简单功能开发效率提升 50%
```

</details>

---

### Q8: Agent 的 Memory 怎么设计？

<details>
<summary>💡 答案要点</summary>

**短期记忆：**
- 存储最近 N 轮对话
- 用列表或环形缓冲区
- 超出限制时总结或截断

**长期记忆：**
- 存储重要信息到向量数据库
- 按需检索相关记忆
- 支持遗忘机制（删除过期记忆）

**实现示例：**
```python
class AgentMemory:
    def __init__(self):
        self.short_term = []  # 最近 10 轮对话
        self.long_term = VectorStore()  # 向量数据库
    
    def add(self, message):
        self.short_term.append(message)
        if len(self.short_term) > 10:
            # 总结后存入长期记忆
            summary = self.summarize(self.short_term[:5])
            self.long_term.add(summary)
            self.short_term = self.short_term[5:]
    
    def get(self, query):
        # 检索相关长期记忆
        memories = self.long_term.search(query, k=3)
        return memories + self.short_term
```

</details>

---

## 四、高分回答模板

### 🌟 谈 Agent 时的"高分点金石"

**不要只说：** "Agent 会调用工具"

**要这样说：**
> "我认为 Agent 的核心在于闭环。模型生成答案后，我会设计一个 Reviewer 节点让它自我检查：'这个答案是否满足用户所有要求？'，如果不满足则重新执行。这种反思机制让 Agent 的可靠性提升了 40%。"

---

### 🌟 谈 Function Calling 时的"高分点金石"

**不要只说：** "调用外部 API"

**要这样说：**
> "Function Calling 的本质是将非结构化的自然语言转化为结构化的 JSON。在实战中，我通过它实现了自然语言直接查询 SQL 数据库，极大地降低了非技术人员的使用门槛。同时我加入了权限校验和参数白名单，防止 Agent 越权访问。"

---

## 📝 速记卡片

| 概念 | 一句话解释 |
|------|------------|
| **Agent** | 能自主决策和行动的 AI |
| **ReAct** | 推理 + 行动的循环模式 |
| **Function Calling** | 让 LLM 调用外部函数 |
| **Planning** | 把大任务分解成小步骤 |
| **Memory** | 短期对话 + 长期向量存储 |
| **Multi-Agent** | 多个 Agent 分工协作 |
| **Reflection** | Agent 自我评估和改进 |

---

**上一模块：** [Prompt 工程](../03-prompt-engineering/)  
**下一模块：** [RAG 系统](../02-rag-system/)

---

[返回目录 →](../../README.md)
