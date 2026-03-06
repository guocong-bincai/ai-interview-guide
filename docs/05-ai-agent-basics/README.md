# 🤖 AI Agent 面试题

> **难度：** ⭐⭐⭐
> **考点：** 智能体设计模式、ReAct、Function Calling、多 Agent 协作

## 📋 目录

1. [基础概念题](#一基础概念题)
2. [设计模式题](#二设计模式题)
3. [工程实践题](#三工程实践题)
4. [高分回答模板](#四高分回答模板)

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

## 四、高分回答模板

### 🌟 谈 Agent 时的"高分点金石"

**不要只说：** "Agent 会调用工具"

**要这样说：**
> "我认为 Agent 的核心在于闭环。模型生成答案后，我会设计一个 Reviewer 节点让它自我检查：'这个答案是否满足用户所有要求？'，如果不满足则重新执行。这种反思机制让 Agent 的可靠性提升了 40%。"

### 🌟 谈 Function Calling 时的"高分点金石"

**不要只说：** "调用外部 API"

**要这样说：**
> "Function Calling 的本质是将非结构化的自然语言转化为结构化的 JSON。在实战中，我通过它实现了自然语言直接查询 SQL 数据库，极大地降低了非技术人员的使用门槛。同时我加入了权限校验和参数白名单，防止 Agent 越权访问。"

### Q9: 什么是LangGraph?如何构建复杂Agent工作流?

<details>
<parameter name="summary">💡 答案要点</summary>

**LangGraph = 用图结构构建有状态的Agent应用**

**为什么需要LangGraph?**

| 场景 | LangChain(链式) | LangGraph(图式) |
|------|----------------|-----------------|
| 简单对话 | ✅ 够用 | ❌ 过度设计 |
| 需要循环 | ❌ 不支持 | ✅ 原生支持 |
| 条件分支 | ❌ 难实现 | ✅ 轻松实现 |
| 多Agent协作 | ❌ 复杂 | ✅ 简洁 |

**核心概念:**

### 1. 图结构
```python
from langgraph.graph import StateGraph, END

# 定义状态
class AgentState(TypedDict):
    messages: list
    next_action: str

# 创建图
workflow = StateGraph(AgentState)

# 添加节点(每个节点是一个函数)
workflow.add_node("researcher", research_node)
workflow.add_node("writer", write_node)
workflow.add_node("reviewer", review_node)

# 添加边(定义流程)
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")

# 条件边(根据状态决定下一步)
workflow.add_conditional_edges(
    "reviewer",
    should_continue,  # 判断函数
    {
        "continue": "writer",  # 如果需要修改,回到writer
        "end": END  # 如果通过,结束
    }
)
```

### 2. 状态管理
```python
def research_node(state: AgentState):
    """研究节点"""
    query = state["messages"][-1]
    results = search_tool(query)

    # 更新状态
    return {
        "messages": state["messages"] + [results],
        "next_action": "write"
    }

def write_node(state: AgentState):
    """写作节点"""
    research_data = state["messages"][-1]
    draft = llm.generate(f"根据以下信息写文章: {research_data}")

    return {
        "messages": state["messages"] + [draft],
        "next_action": "review"
    }
```

### 3. 循环与分支
```python
def should_continue(state: AgentState):
    """决定是否继续循环"""
    last_message = state["messages"][-1]

    # 让LLM评估质量
    score = llm.evaluate(last_message)

    if score > 8:
        return "end"  # 质量好,结束
    else:
        return "continue"  # 质量差,重新写
```

**完整示例:写作Agent**
```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

# 定义状态
class WritingState(TypedDict):
    topic: str
    outline: str
    draft: str
    revision_count: int

# 各个节点
def outline_node(state):
    outline = llm.invoke(f"为'{state['topic']}'创建大纲")
    return {"outline": outline.content}

def draft_node(state):
    draft = llm.invoke(f"根据大纲写文章:\n{state['outline']}")
    return {"draft": draft.content}

def review_node(state):
    review = llm.invoke(f"评估文章质量(1-10分):\n{state['draft']}")
    score = int(review.content)
    return {"revision_count": state.get("revision_count", 0) + 1}

def should_revise(state):
    if state.get("revision_count", 0) >= 3:
        return "end"  # 最多修改3次

    # 评估质量
    score = llm.invoke(f"评分(1-10): {state['draft']}")
    if int(score.content) >= 8:
        return "end"
    return "revise"

# 构建图
workflow = StateGraph(WritingState)
workflow.add_node("outline", outline_node)
workflow.add_node("draft", draft_node)
workflow.add_node("review", review_node)

workflow.set_entry_point("outline")
workflow.add_edge("outline", "draft")
workflow.add_edge("draft", "review")
workflow.add_conditional_edges(
    "review",
    should_revise,
    {"revise": "draft", "end": END}
)

app = workflow.compile()

# 使用
result = app.invoke({"topic": "AI Agent的未来"})
```

**LangGraph vs AutoGPT:**

| 特性 | AutoGPT | LangGraph |
|------|---------|-----------|
| **控制力** | 低(完全自主) | 高(可精确控制) |
| **可靠性** | 低(易跑偏) | 高(明确流程) |
| **适用场景** | 探索性任务 | 生产环境 |
| **成本** | 高(多次试错) | 可控 |

**面试话术:**
> "LangGraph解决了LangChain的痛点:不支持循环和复杂分支。我们用LangGraph构建了写作Agent,支持多轮迭代优化,从大纲→初稿→评审→修改,循环直到质量达标。比AutoGPT可控,比纯Prompt灵活。"

</details>

---

### Q10: 工具调用的完整流程是什么?如何处理失败?

<details>
<summary>💡 答案要点</summary>

**工具调用完整流程: 识别 → 参数提取 → 执行 → 结果处理**

### 阶段1: 工具定义
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名,如北京、上海"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "搜索数据库",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "table": {"type": "string"}
                },
                "required": ["query", "table"]
            }
        }
    }
]
```

### 阶段2: LLM决策
```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "北京今天天气怎么样?"}
    ],
    tools=tools,
    tool_choice="auto"  # 自动决定是否调用工具
)

# LLM返回:
{
    "role": "assistant",
    "tool_calls": [{
        "id": "call_123",
        "function": {
            "name": "get_weather",
            "arguments": '{"city": "北京", "unit": "celsius"}'
        }
    }]
}
```

### 阶段3: 参数验证与执行
```python
def execute_tool_call(tool_call):
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    # 1. 权限检查
    if not has_permission(function_name):
        return {"error": "权限不足"}

    # 2. 参数验证
    if function_name == "get_weather":
        if "city" not in arguments:
            return {"error": "缺少必需参数: city"}
        if len(arguments["city"]) > 20:
            return {"error": "城市名过长"}

    # 3. 执行(带超时和重试)
    try:
        result = call_with_timeout(
            function_map[function_name],
            arguments,
            timeout=5
        )
        return {"success": True, "data": result}
    except TimeoutError:
        return {"error": "工具调用超时"}
    except Exception as e:
        return {"error": str(e)}
```

### 阶段4: 结果反馈
```python
# 将工具结果返回给LLM
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": json.dumps(tool_result)
})

# LLM基于工具结果生成最终答案
final_response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages
)
```

**失败处理策略:**

### 1. 参数错误
```python
if tool_result.get("error"):
    # 让LLM修正参数
    retry_prompt = f"""
    工具调用失败: {tool_result['error']}
    请修正参数后重试。
    """
    # 重新调用
```

### 2. 超时重试
```python
def call_with_retry(func, args, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func(**args)
        except TimeoutError:
            if attempt == max_retries - 1:
                return {"error": "多次重试失败"}
            time.sleep(2 ** attempt)  # 指数退避
```

### 3. 降级策略
```python
def execute_with_fallback(tool_call):
    primary_result = try_tool(tool_call)

    if primary_result.get("error"):
        # 降级到备用工具
        fallback_result = try_fallback_tool(tool_call)
        if fallback_result.get("error"):
            # 最终降级:返回缓存或默认值
            return get_cached_or_default()
        return fallback_result
    return primary_result
```

### 4. 监控与告警
```python
import logging

def execute_tool(tool_call):
    start_time = time.time()

    try:
        result = _execute(tool_call)

        # 记录成功
        logging.info({
            "tool": tool_call.function.name,
            "latency": time.time() - start_time,
            "status": "success"
        })
        return result

    except Exception as e:
        # 记录失败
        logging.error({
            "tool": tool_call.function.name,
            "error": str(e),
            "status": "failure"
        })

        # 告警(错误率>5%)
        if get_error_rate() > 0.05:
            send_alert("工具调用错误率过高")

        raise
```

**完整示例:**
```python
class AgentWithTools:
    def __init__(self, tools):
        self.tools = tools
        self.messages = []

    def run(self, user_input):
        self.messages.append({
            "role": "user",
            "content": user_input
        })

        max_iterations = 5
        for i in range(max_iterations):
            # LLM决策
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.messages,
                tools=self.tools
            )

            assistant_message = response.choices[0].message
            self.messages.append(assistant_message)

            # 检查是否需要调用工具
            if not assistant_message.tool_calls:
                return assistant_message.content

            # 执行所有工具调用
            for tool_call in assistant_message.tool_calls:
                result = self.execute_tool(tool_call)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

        return "达到最大迭代次数"

    def execute_tool(self, tool_call):
        # 带重试和降级的工具执行
        pass
```

**面试话术:**
> "工具调用的关键是鲁棒性。我们做了4层防护:1)参数白名单防注入 2)超时+指数退避重试 3)主备工具降级 4)监控告警。生产环境工具调用成功率99.2%,P99延迟<2s。"

</details>

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
| **LangGraph** | 用图结构构建有状态Agent,支持循环分支 |
| **工具调用流程** | 定义→决策→验证→执行→反馈,带重试降级 |


---

**上一模块：** [Transformer 架构](../04-transformer-architecture/)
**下一模块：** [向量索引优化](../06-vector-index-optimization/)

---

[返回目录 →](../../README.md)
