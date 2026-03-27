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

## 11. 工具调用失败怎么处理?重试策略?

<details>
<summary>💡 答案要点</summary>

**工具调用会失败的原因:**
```
1. 参数错误 - LLM提取的参数不合法
2. API超时 - 外部服务响应慢
3. 权限不足 - 没权限访问资源
4. 服务异常 - 第三方API挂了
5. 数据不存在 - 查询的数据库记录不存在
```

### 错误分类与策略

| 错误类型 | 是否重试 | 处理策略 | 示例 |
|---------|---------|----------|------|
| **瞬态错误** | ✅重试 | 指数退避+抖动 | 网络超时、429限流 |
| **永久性错误** | ❌不重试 | 提示用户/修正参数 | 参数格式错误、404 |
| **部分失败** | ✅重试失败部分 | 拆分+独立重试 | 批量操作中部分失败 |
| **依赖失败** | ❌不重试 | 降级到备用方案 | 外部服务完全不可用 |

### 方案1: 三层错误处理

```python
from tenacity import retry, stop_after_attempt, wait_exponential
import time
import random

class ToolExecutor:
    def __init__(self):
        self.max_retries = 3
        self.circuit_breaker = CircuitBreaker()

    def execute_tool(self, tool_name, params):
        """
        三层防护:
        1. 参数验证层
        2. 重试层
        3. 降级层
        """

        # 第1层: 参数验证
        try:
            validated_params = self.validate_params(tool_name, params)
        except ValidationError as e:
            # 参数错误不重试,直接返回错误给LLM修正
            return {
                "success": False,
                "error": f"参数错误: {str(e)}",
                "suggestion": "请检查参数格式",
                "retryable": False
            }

        # 第2层: 熔断器检查
        if not self.circuit_breaker.is_available(tool_name):
            # 服务已熔断,直接降级
            return self.fallback(tool_name, params)

        # 第3层: 带重试的执行
        result = self.execute_with_retry(tool_name, validated_params)

        # 记录成功/失败供熔断器统计
        if result["success"]:
            self.circuit_breaker.record_success(tool_name)
        else:
            self.circuit_breaker.record_failure(tool_name)

        return result

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True
    )
    def execute_with_retry(self, tool_name, params):
        """带指数退避的重试"""
        try:
            tool = self.get_tool(tool_name)
            result = tool.execute(**params)
            return {"success": True, "data": result}

        except TimeoutError:
            # 可重试
            raise  # 让tenacity重试

        except PermissionError as e:
            # 不可重试
            return {
                "success": False,
                "error": f"权限不足: {str(e)}",
                "retryable": False
            }

        except Exception as e:
            # 未知错误,保守重试一次
            raise

    def fallback(self, tool_name, params):
        """降级策略"""
        fallback_map = {
            "search_web": self.search_cache,  # 网络搜索降级到缓存
            "query_db": self.query_backup_db,  # 主库降级到备库
        }

        if tool_name in fallback_map:
            return fallback_map[tool_name](params)
        else:
            return {
                "success": False,
                "error": f"服务 {tool_name} 暂时不可用",
                "retryable": False
            }

# 使用
executor = ToolExecutor()
result = executor.execute_tool("query_order", {"order_id": "123"})

if not result["success"]:
    if result["retryable"]:
        # 可重试错误,让Agent重新尝试
        feedback = f"执行失败: {result['error']},请重试"
    else:
        # 不可重试,让Agent换个方案
        feedback = f"无法执行: {result['error']},请尝试其他方法"
```

### 方案2: 指数退避 + 抖动

**为什么需要抖动(Jitter)?**
```
场景: 某个API突然恢复,100个Agent同时重试
→ 惊群效应,API瞬间被打死
→ 又全失败,1秒后再次同时重试
→ 恶性循环

解决: 加入随机抖动,错开重试时间
```

**实现:**
```python
def exponential_backoff_with_jitter(attempt, base=2, max_delay=60):
    """
    指数退避 + 全抖动

    attempt 0: [0, 2] 秒随机
    attempt 1: [0, 4] 秒随机
    attempt 2: [0, 8] 秒随机
    ...
    """
    delay = min(base ** attempt, max_delay)
    jitter = random.uniform(0, delay)
    return jitter

# 使用
for attempt in range(5):
    try:
        result = call_api()
        break  # 成功
    except Exception as e:
        if attempt == 4:
            raise  # 最后一次也失败,抛出

        wait_time = exponential_backoff_with_jitter(attempt)
        print(f"失败,等待 {wait_time:.2f}s 后重试...")
        time.sleep(wait_time)
```

**效果对比:**
```python
# 无抖动: 100个请求同时重试
重试时间: [1s, 1s, 1s, ...] (全同时)
→ 惊群效应

# 有抖动: 重试时间分散
重试时间: [0.3s, 1.8s, 0.7s, 1.2s, ...]
→ 请求分散,服务器压力平稳
```

### 方案3: 熔断器(Circuit Breaker)

**原理:**
```
状态机:
Closed(正常) → Open(熔断) → Half-Open(试探) → Closed

Closed: 正常调用
  ↓ 失败率>50%
Open: 直接拒绝,快速失败
  ↓ 等待30秒
Half-Open: 允许1个请求试探
  ↓ 成功 → Closed
  ↓ 失败 → Open
```

**实现:**
```python
from enum import Enum
from datetime import datetime, timedelta

class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self,
                 failure_threshold=5,      # 5次失败触发熔断
                 timeout=30,               # 熔断30秒后试探
                 success_threshold=2):     # 2次成功恢复
        self.state = State.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None

        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold

    def call(self, func, *args, **kwargs):
        # 检查是否可以调用
        if self.state == State.OPEN:
            # 检查是否超过timeout,可以试探
            if self._should_attempt_reset():
                self.state = State.HALF_OPEN
                print("熔断器进入半开状态,试探性调用")
            else:
                # 快速失败
                raise Exception("熔断器打开,服务不可用")

        # 执行调用
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        """成功回调"""
        if self.state == State.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                # 连续成功,恢复正常
                self.state = State.CLOSED
                self.failure_count = 0
                self.success_count = 0
                print("熔断器关闭,服务恢复")
        else:
            # CLOSED状态,重置失败计数
            self.failure_count = 0

    def _on_failure(self):
        """失败回调"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.state == State.HALF_OPEN:
            # 试探失败,重新打开
            self.state = State.OPEN
            self.success_count = 0
            print("试探失败,熔断器重新打开")

        elif self.failure_count >= self.failure_threshold:
            # 失败次数达到阈值,打开熔断器
            self.state = State.OPEN
            print(f"失败{self.failure_count}次,熔断器打开")

    def _should_attempt_reset(self):
        """是否应该试探恢复"""
        if self.last_failure_time is None:
            return True

        return datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout)

# 使用
breaker = CircuitBreaker()

for i in range(10):
    try:
        result = breaker.call(unreliable_api_call)
        print(f"调用成功: {result}")
    except Exception as e:
        print(f"调用失败: {e}")

    time.sleep(1)

# 输出:
# 调用失败: API错误
# 调用失败: API错误
# ...
# 失败5次,熔断器打开
# 调用失败: 熔断器打开,服务不可用  (快速失败,不再调用API)
# ... (30秒后)
# 熔断器进入半开状态,试探性调用
# 调用成功
# 熔断器关闭,服务恢复
```

### 方案4: 参数修正反馈

```python
def execute_tool_with_feedback(llm, tool, params, max_attempts=3):
    """
    参数错误时,让LLM自己修正
    """
    for attempt in range(max_attempts):
        try:
            # 验证参数
            validated = tool.validate_params(params)
            # 执行
            result = tool.execute(validated)
            return result

        except ValidationError as e:
            if attempt == max_attempts - 1:
                return {"error": "参数多次修正失败"}

            # 让LLM修正参数
            feedback = f"""
            工具调用失败:
            错误: {str(e)}

            你提供的参数:
            {json.dumps(params, indent=2, ensure_ascii=False)}

            工具期望的格式:
            {tool.get_schema()}

            请重新生成正确的参数。
            """

            # LLM生成新参数
            new_params = llm.generate(feedback)
            params = parse_json(new_params)
            print(f"尝试修正参数 (第{attempt+1}次)")

    return {"error": "超过最大重试次数"}
```

### 最佳实践总结

```python
class RobustToolExecutor:
    """
    生产级工具执行器
    """
    def __init__(self):
        self.circuit_breakers = {}  # 每个工具独立熔断
        self.retry_config = {
            "max_attempts": 3,
            "base_delay": 1,
            "max_delay": 30,
        }

    def execute(self, tool_name, params, context=None):
        # 1. 参数验证
        if not self.validate_params(tool_name, params):
            return self.invalid_params_response(tool_name, params)

        # 2. 熔断器检查
        breaker = self.get_or_create_breaker(tool_name)
        if breaker.is_open():
            return self.fallback_response(tool_name, params)

        # 3. 带重试执行
        for attempt in range(self.retry_config["max_attempts"]):
            try:
                result = self.do_execute(tool_name, params)
                breaker.record_success()
                return {"success": True, "data": result}

            except RetryableError as e:
                # 可重试错误
                if attempt < self.retry_config["max_attempts"] - 1:
                    delay = self.calculate_delay(attempt)
                    time.sleep(delay)
                    continue
                else:
                    breaker.record_failure()
                    return {"success": False, "error": str(e), "retryable": True}

            except NonRetryableError as e:
                # 不可重试错误
                breaker.record_failure()
                return {"success": False, "error": str(e), "retryable": False}

        return {"success": False, "error": "Max retries exceeded"}

    def calculate_delay(self, attempt):
        """指数退避+抖动"""
        base = self.retry_config["base_delay"]
        max_delay = self.retry_config["max_delay"]
        delay = min(base * (2 ** attempt), max_delay)
        return delay * (0.5 + random.random() * 0.5)  # 50-100%抖动
```

**面试话术:**
> "工具调用失败分三类处理:参数错误(让LLM修正不重试)、瞬态错误(指数退避+抖动重试)、服务异常(熔断器快速失败+降级)。关键是避免惊群效应,我们用全抖动策略,把100个同时重试分散到0-2秒内随机,服务压力平稳。熔断器在5次失败后打开,30秒后半开试探,2次成功恢复,保护后端服务。"

</details>

---

## 12. Agent记忆系统如何设计?短期vs长期记忆?

<details>
<summary>💡 答案要点</summary>

**记忆系统 = Agent的"大脑存储",决定能否长期陪伴用户**

### 记忆分类

| 类型 | 存储周期 | 容量 | 实现 | 用途 |
|------|---------|------|------|------|
| **短期记忆** | 单次会话 | 小(受Context Window限制) | 对话历史 | 保持对话连贯 |
| **长期记忆** | 跨会话永久 | 大(无限) | 向量数据库 | 用户偏好/历史事实 |
| **工作记忆** | 任务期间 | 中 | 临时变量 | 中间计算结果 |

### 短期记忆实现

**方案1: 滑动窗口**
```python
class ShortTermMemory:
    def __init__(self, max_turns=5):
        self.messages = []
        self.max_turns = max_turns

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

        # 保留最近N轮对话
        if len(self.messages) > self.max_turns * 2:  # *2因为每轮有user+assistant
            self.messages = self.messages[-(self.max_turns * 2):]

    def get_context(self):
        return self.messages

# 问题: 丢失早期信息
```

**方案2: 分层管理(推荐⭐)**
```python
class HierarchicalMemory:
    def __init__(self):
        self.recent = []      # 最近3轮完整保留
        self.summary = ""     # 历史摘要

    def add_turn(self, user_msg, ai_msg):
        self.recent.append({"user": user_msg, "ai": ai_msg})

        # 超过3轮,摘要最早的
        if len(self.recent) > 3:
            old = self.recent.pop(0)

            # 用LLM摘要
            summary_chunk = llm.summarize(
                f"用户: {old['user']}\n助手: {old['ai']}"
            )
            self.summary += summary_chunk + "\n"

    def get_context(self):
        context = []

        # 历史摘要
        if self.summary:
            context.append({"role": "system", "content": f"历史: {self.summary}"})

        # 最近3轮完整对话
        for turn in self.recent:
            context.append({"role": "user", "content": turn["user"]})
            context.append({"role": "assistant", "content": turn["ai"]})

        return context

# 效果:
# 10轮对话,token消耗: 摘要(200) + 最近3轮(1500) = 1700 tokens
# vs 全保留: 5000 tokens
# 节省: 66%
```

### 长期记忆实现

**核心: 向量数据库**

```python
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings

class LongTermMemory:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectordb = Qdrant(
            collection_name="user_memory",
            embedding_function=self.embeddings
        )

    def remember(self, key, value, metadata=None):
        """存储长期记忆"""
        self.vectordb.add_texts(
            texts=[value],
            metadatas=[{
                "key": key,
                "timestamp": time.time(),
                **(metadata or {})
            }]
        )

    def recall(self, query, k=5):
        """检索相关记忆"""
        results = self.vectordb.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    def forget(self, key):
        """删除记忆"""
        self.vectordb.delete(filter={"key": key})

# 使用
memory = LongTermMemory()

# 存储用户偏好
memory.remember(
    key="food_preference",
    value="用户喜欢吃川菜,不吃香菜",
    metadata={"category": "preference"}
)

# 存储历史事实
memory.remember(
    key="birthday",
    value="用户生日是1990年5月20日",
    metadata={"category": "fact"}
)

# 3个月后,检索记忆
query = "用户吃什么?"
memories = memory.recall(query, k=3)
# 返回: ["用户喜欢吃川菜,不吃香菜", ...]
```

### 混合记忆策略

**问题: 如何决定什么存长期,什么存短期?**

```python
class HybridMemoryManager:
    def __init__(self):
        self.short_term = HierarchicalMemory()
        self.long_term = LongTermMemory()

    def add_interaction(self, user_msg, ai_msg):
        # 1. 短期记忆:直接存
        self.short_term.add_turn(user_msg, ai_msg)

        # 2. 判断是否值得长期存储
        if self.is_important(user_msg, ai_msg):
            # 提取关键信息
            key_info = self.extract_key_info(user_msg, ai_msg)

            # 存入长期记忆
            self.long_term.remember(
                key=f"conv_{time.time()}",
                value=key_info
            )

    def is_important(self, user_msg, ai_msg):
        """判断是否重要"""
        # 规则1: 包含用户偏好
        if any(kw in user_msg.lower() for kw in ["我喜欢", "我不喜欢", "我的"]):
            return True

        # 规则2: 包含事实信息
        if any(kw in user_msg for kw in ["是", "叫", "生日", "地址"]):
            return True

        # 规则3: 用LLM判断
        prompt = f"""
        判断以下对话是否包含值得长期记忆的信息(用户偏好/事实/重要决策):

        用户: {user_msg}
        助手: {ai_msg}

        回答: 是/否
        """
        decision = llm.generate(prompt).strip()
        return decision == "是"

    def extract_key_info(self, user_msg, ai_msg):
        """提取关键信息"""
        prompt = f"""
        从对话中提取值得长期记忆的关键信息:

        用户: {user_msg}
        助手: {ai_msg}

        关键信息(一句话):
        """
        return llm.generate(prompt).strip()

    def get_full_context(self, current_query):
        """获取完整上下文"""
        # 1. 短期记忆
        short = self.short_term.get_context()

        # 2. 检索相关长期记忆
        long = self.long_term.recall(current_query, k=3)

        # 3. 合并
        context = []

        # 长期记忆作为背景
        if long:
            context.append({
                "role": "system",
                "content": f"用户背景信息:\n" + "\n".join(long)
            })

        # 短期记忆作为对话历史
        context.extend(short)

        return context

# 实战示例
manager = HybridMemoryManager()

# 第1次对话
manager.add_interaction(
    user_msg="我叫张三,是个程序员",
    ai_msg="你好张三!很高兴认识你。"
)
# → 长期记忆存储: "用户叫张三,职业是程序员"

# 第2次对话
manager.add_interaction(
    user_msg="今天天气真好",
    ai_msg="是啊,适合出去走走。"
)
# → 仅短期记忆,不重要

# 1个月后,第100次对话
context = manager.get_full_context("给我推荐适合程序员的书")
# context包含:
# - 长期记忆: "用户叫张三,职业是程序员"
# - 短期记忆: 最近3轮对话

response = llm.generate(context + [{"role": "user", "content": "给我推荐适合程序员的书"}])
# LLM能结合长期记忆(职业)给出个性化推荐
```

### 记忆索引优化

**问题: 向量检索不准,检索到无关记忆**

**优化: 混合索引**
```python
class EnhancedMemory:
    def __init__(self):
        self.vectordb = Qdrant(...)
        self.metadata_index = {}  # 元数据索引

    def remember(self, key, value, category, tags):
        # 1. 向量存储
        self.vectordb.add_texts(
            texts=[value],
            metadatas=[{
                "key": key,
                "category": category,
                "tags": tags,
                "timestamp": time.time()
            }]
        )

        # 2. 元数据索引
        self.metadata_index[key] = {
            "category": category,
            "tags": tags
        }

    def recall(self, query, category=None, tags=None, k=5):
        # 构建过滤条件
        filter_dict = {}
        if category:
            filter_dict["category"] = category
        if tags:
            filter_dict["tags"] = {"$in": tags}

        # 向量检索+元数据过滤
        results = self.vectordb.similarity_search(
            query,
            k=k,
            filter=filter_dict
        )

        return results

# 使用
memory = EnhancedMemory()

memory.remember(
    key="food1",
    value="用户喜欢吃川菜",
    category="preference",
    tags=["food", "cuisine"]
)

memory.remember(
    key="work1",
    value="用户在字节跳动工作",
    category="fact",
    tags=["job", "company"]
)

# 只检索食物偏好
food_memories = memory.recall(
    query="吃什么",
    category="preference",
    tags=["food"]
)
# 不会检索到工作信息
```

**面试话术:**
> "Agent记忆分短期和长期。短期用分层管理,最近3轮保留原文+历史摘要,节省66% token。长期用向量数据库,存用户偏好和事实,用LLM判断重要性决定是否存储。检索时混合向量+元数据过滤,避免无关记忆。实测3个月后,Agent还记得用户职业,推荐更个性化。"

</details>

---

## 13. Agent如何做规划(Planning)?任务分解策略?

<details>
<summary>💡 答案要点</summary>

**规划 = 把大任务分解成可执行的小步骤**

### 规划方法对比

| 方法 | 原理 | 优点 | 缺点 | 适用 |
|------|------|------|------|------|
| **Chain of Thought** | 逐步推理 | 简单直观 | 不可回退 | 简单任务 |
| **Tree of Thoughts** | 树状搜索 | 可探索多路径 | 计算量大 | 需要试错 |
| **Plan-and-Execute** | 先整体规划再执行 | 结构清晰 | 计划可能过时 | 明确任务 |
| **ReWOO** | 预规划+批量执行 | 高效并行 | 灵活性差 | 工具调用多 |

### 方案1: Plan-and-Execute (推荐⭐)

**流程:**
```
Step 1: Planning - 制定完整计划
Step 2: Execution - 逐步执行
Step 3: Replanning - 根据结果调整计划
```

**实现:**
```python
class PlanAndExecuteAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def run(self, goal):
        # Step 1: 制定计划
        plan = self.make_plan(goal)
        print(f"计划: {plan}")

        # Step 2: 执行每个步骤
        results = []
        for step in plan:
            result = self.execute_step(step, results)
            results.append(result)

            # Step 3: 检查是否需要重新规划
            if self.should_replan(step, result):
                plan = self.replan(goal, results)
                print(f"重新规划: {plan}")

        # Step 4: 综合结果
        final_answer = self.synthesize(goal, results)
        return final_answer

    def make_plan(self, goal):
        """制定计划"""
        prompt = f"""
        任务: {goal}

        请制定详细的执行计划,每个步骤要具体可执行。

        输出格式(JSON):
        [
          {{"step": 1, "action": "搜索最新的AI新闻", "tool": "search"}},
          {{"step": 2, "action": "总结新闻要点", "tool": "llm"}},
          {{"step": 3, "action": "生成周报", "tool": "llm"}}
        ]
        """

        plan_json = self.llm.generate(prompt)
        return json.loads(plan_json)

    def execute_step(self, step, previous_results):
        """执行单个步骤"""
        tool_name = step["tool"]
        action = step["action"]

        # 构造上下文(之前步骤的结果)
        context = "\n".join([
            f"步骤{i+1}结果: {r}"
            for i, r in enumerate(previous_results)
        ])

        # 执行工具
        if tool_name == "search":
            result = self.tools["search"].run(action)
        elif tool_name == "llm":
            result = self.llm.generate(f"{context}\n\n{action}")
        else:
            result = self.tools[tool_name].run(action)

        print(f"步骤{step['step']}: {action} → {result[:100]}...")
        return result

    def should_replan(self, step, result):
        """判断是否需要重新规划"""
        # 检查执行失败
        if "错误" in result or "失败" in result:
            return True

        # 让LLM判断
        prompt = f"""
        步骤: {step['action']}
        结果: {result}

        这个结果是否符合预期? 是否需要调整后续计划?
        回答: 是/否
        """
        decision = self.llm.generate(prompt).strip()
        return decision == "是"

    def replan(self, goal, results):
        """重新规划"""
        context = "\n".join([f"已完成{i+1}: {r[:50]}..." for i, r in enumerate(results)])

        prompt = f"""
        原始任务: {goal}
        已完成步骤:
        {context}

        请根据当前进展,重新规划剩余步骤。
        """
        new_plan = self.llm.generate(prompt)
        return json.loads(new_plan)

# 使用示例
agent = PlanAndExecuteAgent(llm, tools)

result = agent.run("写一份本周AI行业的周报")

# 输出:
# 计划: [
#   {"step": 1, "action": "搜索本周AI新闻", "tool": "search"},
#   {"step": 2, "action": "总结新闻", "tool": "llm"},
#   {"step": 3, "action": "撰写周报", "tool": "llm"}
# ]
# 步骤1: 搜索本周AI新闻 → 找到10篇新闻...
# 步骤2: 总结新闻 → OpenAI发布GPT-5, Google推出Gemini Ultra...
# 步骤3: 撰写周报 → 本周AI行业动态:...
```

### 方案2: Tree of Thoughts (思维树)

**适用:** 需要探索多种可能性的任务(如写作、创意)

```python
class TreeOfThoughts:
    def __init__(self, llm, depth=3, breadth=3):
        self.llm = llm
        self.depth = depth  # 思考深度
        self.breadth = breadth  # 每层生成几个候选

    def solve(self, problem):
        # 根节点
        root = TreeNode(problem, score=0)

        # 逐层扩展
        for level in range(self.depth):
            # 对当前层每个节点
            for node in self.get_layer_nodes(root, level):
                # 生成多个候选下一步
                candidates = self.generate_candidates(node, self.breadth)

                # 评估每个候选
                for candidate in candidates:
                    score = self.evaluate(candidate)
                    child = TreeNode(candidate, score=score)
                    node.add_child(child)

        # 找到最优路径
        best_path = self.find_best_path(root)
        return best_path

    def generate_candidates(self, node, k):
        """生成k个候选思路"""
        prompt = f"""
        当前思路: {node.content}

        请生成{k}个不同的后续思路。
        """
        responses = []
        for _ in range(k):
            response = self.llm.generate(prompt, temperature=0.9)
            responses.append(response)

        return responses

    def evaluate(self, thought):
        """评估思路质量"""
        prompt = f"""
        评估以下思路的质量(0-10分):
        {thought}

        评分:
        """
        score = float(self.llm.generate(prompt).strip())
        return score

    def find_best_path(self, root):
        """找到最高分路径"""
        def dfs(node, path, score):
            if not node.children:
                return path, score

            best = (path, score)
            for child in node.children:
                candidate_path, candidate_score = dfs(
                    child,
                    path + [child.content],
                    score + child.score
                )
                if candidate_score > best[1]:
                    best = (candidate_path, candidate_score)

            return best

        path, score = dfs(root, [root.content], root.score)
        return path

# 使用
tot = TreeOfThoughts(llm, depth=3, breadth=3)
best_solution = tot.solve("写一篇关于AI伦理的文章")

# 会探索 3^3=27 种可能路径,选最优
```

### 方案3: ReWOO (预规划+批量执行)

**优势: 一次性规划所有工具调用,批量并行执行**

```python
class ReWOO:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def run(self, task):
        # Step 1: 一次性规划所有步骤
        plan = self.plan_all_steps(task)

        # Step 2: 识别可并行的步骤
        parallel_groups = self.identify_parallel_groups(plan)

        # Step 3: 批量执行
        results = {}
        for group in parallel_groups:
            # 并行执行同组步骤
            group_results = self.execute_parallel(group)
            results.update(group_results)

        # Step 4: 综合结果
        return self.synthesize(task, results)

    def plan_all_steps(self, task):
        prompt = f"""
        任务: {task}

        请规划完整步骤,标注依赖关系:

        格式:
        #E1 = Search[最新AI新闻]
        #E2 = LLM[总结 #E1]
        #E3 = Search[AI政策]
        #E4 = LLM[综合 #E2 和 #E3]
        """
        plan = self.llm.generate(prompt)
        return self.parse_plan(plan)

    def identify_parallel_groups(self, plan):
        """识别可并行步骤"""
        # #E1 和 #E3 无依赖,可并行
        # #E2 依赖 #E1
        # #E4 依赖 #E2 和 #E3

        groups = [
            [plan["E1"], plan["E3"]],  # 第1组:并行
            [plan["E2"]],               # 第2组:等E1完成
            [plan["E4"]]                # 第3组:等E2,E3完成
        ]
        return groups

    def execute_parallel(self, steps):
        """并行执行步骤"""
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.execute_step, step): step
                for step in steps
            }

            results = {}
            for future in concurrent.futures.as_completed(futures):
                step = futures[future]
                results[step["id"]] = future.result()

        return results

# 效果:
# 传统ReAct: 4个步骤串行,耗时20秒
# ReWOO: 步骤1,3并行,耗时12秒 (节省40%)
```

**面试话术:**
> "Agent规划我用Plan-and-Execute,先用LLM制定完整计划,再逐步执行并根据结果调整。复杂任务用Tree of Thoughts探索多路径,每层生成3个候选思路,评分选最优。工具调用多时用ReWOO预规划+批量并行,比ReAct快40%。关键是要能动态调整计划,而不是死板执行。"

</details>

---

## 14. 什么是Human-in-the-Loop？Agent何时应该暂停等待人工确认？

<details>
<summary>💡 答案要点</summary>

**Human-in-the-Loop (HITL) = 在Agent关键决策节点插入人工确认，保证安全可控**

### 为什么需要HITL

```
纯自动Agent的风险：
Agent决定删除数据库 → 直接执行 → 数据丢失 ❌
Agent误解用户意图 → 发错邮件 → 造成事故 ❌
Agent循环调用API → 账单暴涨  → 损失惨重 ❌

HITL的保障：
Agent决定删除数据库 → 暂停 → 人工确认 → 执行/拒绝 ✅
```

### HITL触发条件设计

```python
from enum import Enum
from typing import Callable

class RiskLevel(Enum):
    LOW = "low"       # 自动执行
    MEDIUM = "medium" # 警告但执行
    HIGH = "high"     # 必须人工确认
    CRITICAL = "critical" # 强制中断

class HITLAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.pending_approvals = []

    def assess_risk(self, action: str, params: dict) -> RiskLevel:
        """评估操作风险等级"""

        # 规则1：不可逆操作 → HIGH
        irreversible_actions = ["delete", "drop", "truncate", "send_email", "post", "pay"]
        if any(kw in action.lower() for kw in irreversible_actions):
            return RiskLevel.HIGH

        # 规则2：涉及金额 → CRITICAL
        if "amount" in params and params.get("amount", 0) > 1000:
            return RiskLevel.CRITICAL

        # 规则3：批量操作 → HIGH
        if params.get("batch_size", 0) > 100:
            return RiskLevel.HIGH

        # 规则4：用LLM判断
        risk_prompt = f"""
        评估以下操作的风险等级（low/medium/high/critical）：
        操作：{action}
        参数：{params}

        考虑因素：是否可逆？影响范围？是否涉及敏感数据？

        输出JSON：{{"level": "风险等级", "reason": "原因"}}
        """
        result = json.loads(self.llm.generate(risk_prompt, temperature=0))
        return RiskLevel(result["level"])

    def execute_with_hitl(self, action: str, params: dict):
        """执行带HITL的操作"""
        risk = self.assess_risk(action, params)

        if risk == RiskLevel.LOW:
            # 直接执行
            return self.tools[action](**params)

        elif risk == RiskLevel.MEDIUM:
            # 执行但记录警告
            print(f"⚠️  中风险操作：{action}({params})")
            result = self.tools[action](**params)
            self.log_action(action, params, result)
            return result

        elif risk == RiskLevel.HIGH:
            # 暂停，请求人工确认
            return self.request_approval(action, params, risk)

        elif risk == RiskLevel.CRITICAL:
            # 强制中断，通知管理员
            self.notify_admin(action, params)
            raise Exception(f"🚨 危险操作已阻止：{action}")

    def request_approval(self, action: str, params: dict, risk: RiskLevel):
        """请求人工审批"""
        approval_id = f"approval_{int(time.time())}"

        # 保存待审批操作
        self.pending_approvals.append({
            "id": approval_id,
            "action": action,
            "params": params,
            "risk": risk.value,
            "status": "pending",
            "created_at": time.time()
        })

        # 通知审批人（实际场景：发钉钉/企微/邮件）
        self.send_approval_request(approval_id, action, params)

        # 等待审批（异步方式，这里简化为轮询）
        return self.wait_for_approval(approval_id)

    def wait_for_approval(self, approval_id: str, timeout=300):
        """等待人工审批，超时自动拒绝"""
        start = time.time()

        while time.time() - start < timeout:
            approval = self.get_approval(approval_id)

            if approval["status"] == "approved":
                # 获批，执行操作
                a = approval["action"]
                return self.tools[a](**approval["params"])

            elif approval["status"] == "rejected":
                return {"error": "操作被拒绝", "reason": approval.get("reason")}

            time.sleep(5)  # 每5秒轮询一次

        # 超时，自动拒绝
        return {"error": "审批超时，操作已取消"}

    def send_approval_request(self, approval_id, action, params):
        """发送审批通知（钉钉机器人示例）"""
        message = f"""
        🔔 Agent操作需要审批

        操作：{action}
        参数：{json.dumps(params, ensure_ascii=False)}

        审批链接：http://your-system/approve/{approval_id}
        超时时间：5分钟
        """
        # dingtalk_bot.send(message)
        print(message)

# 实战场景：邮件发送Agent
agent = HITLAgent(llm, tools={
    "search_web": search_tool,
    "send_email": email_tool,
    "delete_file": delete_tool,
})

# 低风险：自动执行
agent.execute_with_hitl("search_web", {"query": "最新AI新闻"})

# 高风险：暂停等待审批
agent.execute_with_hitl("send_email", {
    "to": "all@company.com",
    "subject": "重要通知",
    "body": "全员涨薪100%"
})
# → 触发HITL，发送钉钉审批消息 → 等待HR确认
```

### LangGraph中实现HITL

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# LangGraph原生支持HITL（interrupt_before）
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("execute_tool", tool_node)
workflow.add_node("human_review", human_review_node)

# 在执行高风险工具前中断，等待人工确认
workflow.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "execute_safe": "execute_tool",    # 低风险直接执行
        "need_review": "human_review",     # 高风险转人工
        "done": END
    }
)

# 保存检查点，支持暂停恢复
checkpointer = MemorySaver()
app = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["human_review"]  # 到达human_review节点时暂停
)

# 使用
thread = {"configurable": {"thread_id": "session_123"}}
result = app.invoke(initial_state, thread)

# Agent暂停在human_review节点
# 人工审批后恢复
app.invoke(None, thread)  # 从检查点恢复执行
```

**面试话术：**
> "HITL是Agent安全的核心机制，关键是定义清晰的触发条件：不可逆操作（删除/发送）、涉及金额超阈值、批量操作超量。我设计了4级风险：LOW自动执行、MEDIUM记录警告、HIGH等待审批、CRITICAL强制中断。用LangGraph的interrupt_before做断点，配合钉钉审批通知，超时5分钟自动拒绝。生产上线后，高风险操作事故率降低了95%。"

</details>

---

## 15. 如何评测Agent的能力？有哪些主流Benchmark？

<details>
<summary>💡 答案要点</summary>

**Agent评测 = 用标准化任务集量化Agent在规划/工具使用/多轮交互的能力**

### 评测维度

| 维度 | 含义 | 指标 |
|------|------|------|
| **任务成功率** | 从头到尾完成任务 | 成功率% |
| **工具使用准确性** | 选对工具+正确参数 | 工具调用准确率 |
| **规划效率** | 步骤数 vs 最优步骤数 | 效率比 |
| **鲁棒性** | 面对错误/噪声的恢复能力 | 错误恢复率 |
| **成本效率** | 完成任务的Token/时间开销 | Cost per task |

### 主流Benchmark

**1. AgentBench（清华/伯克利）**

```python
# 8种真实环境测试
environments = {
    "OS": "操作系统Shell命令",
    "DB": "数据库SQL查询",
    "KG": "知识图谱推理",
    "WebShop": "网购任务",
    "WebArena": "网页操作",
    "HumanEval": "代码生成",
    "Mind2Web": "网页导航",
    "Card Game": "卡牌游戏策略",
}

# GPT-4在AgentBench的表现
gpt4_scores = {
    "OS": 0.58,
    "DB": 0.33,
    "KG": 0.92,
    "WebShop": 0.40,
    # 开源模型普遍<0.05
}
```

**2. 自建Benchmark（生产环境推荐）**

```python
class AgentBenchmark:
    """针对业务场景的自定义评测"""

    def __init__(self, agent, test_cases):
        self.agent = agent
        self.test_cases = test_cases  # 标注好的测试集

    def evaluate(self):
        results = {
            "task_success": [],      # 任务成功率
            "tool_accuracy": [],     # 工具调用准确率
            "step_efficiency": [],   # 步骤效率
            "cost": [],             # Token消耗
        }

        for case in self.test_cases:
            start_time = time.time()

            # 运行Agent
            try:
                result = self.agent.run(case["input"])
                success = self.evaluate_success(result, case["expected_output"])
            except Exception as e:
                success = False
                result = None

            elapsed = time.time() - start_time

            # 记录指标
            results["task_success"].append(success)

            if hasattr(self.agent, "tool_calls_log"):
                tool_acc = self.evaluate_tool_accuracy(
                    self.agent.tool_calls_log,
                    case["expected_tools"]
                )
                results["tool_accuracy"].append(tool_acc)

            results["cost"].append(self.agent.total_tokens)

        # 汇总
        return {
            "task_success_rate": sum(results["task_success"]) / len(results["task_success"]),
            "avg_tool_accuracy": sum(results["tool_accuracy"]) / len(results["tool_accuracy"]),
            "avg_tokens_per_task": sum(results["cost"]) / len(results["cost"]),
        }

    def evaluate_success(self, result, expected):
        """评估任务是否成功"""
        # 方式1：精确匹配
        if result == expected:
            return True

        # 方式2：语义相似度
        similarity = compute_similarity(result, expected)
        return similarity > 0.85

        # 方式3：LLM-as-Judge
        judge_prompt = f"""
        预期答案：{expected}
        Agent实际输出：{result}

        Agent是否正确完成了任务？（是/否）：
        """
        judgment = llm.generate(judge_prompt, temperature=0)
        return "是" in judgment

    def evaluate_tool_accuracy(self, actual_calls, expected_calls):
        """评估工具调用准确率"""
        if not expected_calls:
            return 1.0

        correct = 0
        for i, (actual, expected) in enumerate(zip(actual_calls, expected_calls)):
            # 工具名正确
            if actual["tool"] == expected["tool"]:
                correct += 0.5

            # 参数正确
            param_match = sum(
                actual["params"].get(k) == v
                for k, v in expected["params"].items()
            ) / len(expected["params"])
            correct += 0.5 * param_match

        return correct / len(expected_calls)

# 使用
test_cases = [
    {
        "input": "查询北京明天天气",
        "expected_output": "明天北京气温X度，晴天",
        "expected_tools": [{"tool": "weather_api", "params": {"city": "北京", "date": "tomorrow"}}]
    },
    {
        "input": "帮我发邮件给张三，告诉他明天开会",
        "expected_output": "邮件已发送",
        "expected_tools": [{"tool": "send_email", "params": {"to": "zhangsan@xx.com", "subject": "开会通知"}}]
    }
]

benchmark = AgentBenchmark(my_agent, test_cases)
scores = benchmark.evaluate()

print(f"任务成功率: {scores['task_success_rate']:.1%}")
print(f"工具准确率: {scores['avg_tool_accuracy']:.1%}")
print(f"平均Token消耗: {scores['avg_tokens_per_task']:.0f}")
```

### 持续评测体系

```python
class AgentMonitor:
    """生产环境持续监控"""

    def log_interaction(self, session_id, query, result, tools_used, tokens):
        """记录每次Agent交互"""
        record = {
            "session_id": session_id,
            "timestamp": time.time(),
            "query": query,
            "result": result,
            "tools_used": tools_used,
            "tokens": tokens,
            "user_feedback": None  # 后续收集
        }
        self.db.insert(record)

    def collect_feedback(self, session_id, rating: int, comment: str = ""):
        """收集用户反馈（1-5星）"""
        self.db.update(session_id, {
            "user_feedback": rating,
            "comment": comment
        })

    def generate_weekly_report(self):
        """每周评测报告"""
        records = self.db.query_last_7_days()

        return {
            "total_sessions": len(records),
            "success_rate": self.calc_success_rate(records),
            "avg_feedback": self.calc_avg_feedback(records),
            "tool_usage_stats": self.calc_tool_stats(records),
            "failure_cases": self.find_failures(records),
            "cost_summary": sum(r["tokens"] for r in records)
        }
```

**面试话术：**
> "Agent评测分离线和在线两套。离线用自建Benchmark：覆盖任务成功率、工具调用准确率、步骤效率、Token成本4个维度，测试集至少100条覆盖各种边界情况。评判方式用LLM-as-Judge，比精确匹配更灵活，准确率和人工评估一致性>85%。在线用生产监控：记录每次交互，收集用户1-5星反馈，每周生成报告。我们的Agent上线后，通过持续评测发现工具参数错误率偏高，针对性优化Prompt后，工具准确率从72%→91%。"

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
| **错误处理** | 参数错误不重试,瞬态错误重试,服务异常降级 |
| **重试策略** | 指数退避+抖动(避免惊群),熔断器(快速失败) |
| **记忆系统** | 短期(滑动窗口)+长期(向量DB)+混合策略 |
| **规划方法** | Plan-Execute(推荐)/Tree of Thoughts/ReWOO |
| **Human-in-the-Loop** | 4级风险(LOW/MEDIUM/HIGH/CRITICAL)，不可逆操作强制审批 |
| **Agent评测** | 任务成功率+工具准确率+效率+成本，LLM-as-Judge评判 |
| **Token估算** | 单轮≈1K-4K，多轮含摘要≈2K-8K，滑动窗口控成本 |
| **上下文重写** | 对话历史压缩→语义重写→减少噪声，让检索更准 |
| **Agent部署** | 容器化(隔离/弹性)为主，宿主机部署适合资源敏感场景 |

---

## 高频面试追问（一面/二面真题补充）

### Q: 单轮对话和多轮对话的 Token 消耗大概多少？如何控制？

<details>
<summary>💡 答案要点</summary>

**Token 消耗估算（GPT-4o 参考）：**

| 场景 | 输入 Token | 输出 Token | 合计 | 费用估算 |
|------|-----------|-----------|------|---------|
| 单轮简单问答 | ~500 | ~300 | ~800 | ¥0.003 |
| 单轮复杂分析 | ~2000 | ~800 | ~2800 | ¥0.01 |
| 10轮对话（无压缩） | ~8000 | ~3000 | ~11000 | ¥0.04 |
| 10轮对话（摘要压缩） | ~2000 | ~800 | ~2800 | ¥0.01 |

**消耗构成拆解：**
```
System Prompt:  200-500 tokens（固定成本）
用户输入:        100-500 tokens/轮
RAG 检索内容:   500-2000 tokens（主要成本）
历史对话:       累计增长，不压缩会爆炸
模型输出:       200-500 tokens/轮
```

**多轮对话 Token 控制策略：**

```python
class TokenBudgetManager:
    MAX_CONTEXT_TOKENS = 4000  # 留给历史的预算

    def build_context(self, history: list, system_prompt: str) -> list:
        """滑动窗口 + 摘要压缩"""
        messages = [{"role": "system", "content": system_prompt}]

        # 策略1: 只保留最近 N 轮原文
        recent = history[-3:]  # 最近3轮保留完整原文

        # 策略2: 历史部分做摘要
        if len(history) > 3:
            older = history[:-3]
            summary = self._summarize(older)
            messages.append({
                "role": "system",
                "content": f"[历史摘要] {summary}"
            })

        messages.extend(recent)
        return messages

    def _summarize(self, history: list) -> str:
        """调 LLM 压缩历史，只花一次钱"""
        # 实际用小模型（gpt-3.5/qwen-turbo）做摘要，成本低
        ...
```

**多轮 vs 单轮 Token 增长对比：**
```
第1轮:  800 tokens
第5轮（无压缩）: 800×5 = 4000 tokens
第5轮（有压缩）: 800 + 摘要200 = 1000 tokens  ← 节省75%
第10轮（无压缩）: 800×10 = 8000 tokens
第10轮（有压缩）: 800 + 摘要400 = 1200 tokens  ← 节省85%
```

**面试话术：**
> "单轮对话 Token 消耗约 1K-4K，多轮不控制会线性增长爆成本。我的策略是三层：最近3轮保原文保障连贯性，历史部分用小模型摘要（节省80%成本），RAG 召回内容做相关性过滤只保留 top-k chunk。实测10轮对话 Token 消耗控制在 2K 以内，单次成本 < ¥0.01。"

</details>

### Q: Agent 的记忆架构怎么做？

<details>
<summary>💡 答案要点</summary>

**记忆分类（四类）：**

```
┌─────────────────────────────────────────────────────┐
│                   Agent 记忆体系                      │
├───────────┬───────────┬───────────┬─────────────────┤
│  工作记忆  │  情节记忆  │  语义记忆  │    程序记忆      │
│  当前对话  │  历史事件  │  知识概念  │   技能/流程      │
│ in-context│  向量DB   │  知识图谱  │  工具调用链      │
│  临时      │  可查询   │  持久化   │   持久化         │
└───────────┴───────────┴───────────┴─────────────────┘
```

**工程实现（分层架构）：**

```python
class AgentMemory:
    def __init__(self):
        # Layer 1: 工作记忆（当前 context window）
        self.working_memory = []          # 当前对话消息列表
        self.max_working_tokens = 4000    # 工作记忆上限

        # Layer 2: 情节记忆（历史对话向量化）
        self.episodic_memory = VectorDB() # Chroma/Pinecone

        # Layer 3: 语义记忆（持久知识库）
        self.semantic_memory = KnowledgeBase()

    def remember(self, message: dict):
        """写入记忆"""
        self.working_memory.append(message)

        # 超出工作记忆上限 → 压缩 → 写入情节记忆
        if self._count_tokens() > self.max_working_tokens:
            self._compress_to_episodic()

    def recall(self, query: str) -> list:
        """检索相关记忆"""
        # 1. 先查工作记忆（最近对话，直接用）
        recent = self.working_memory[-3:]

        # 2. 再查情节记忆（历史对话中相关的）
        episodic = self.episodic_memory.search(query, top_k=3)

        # 3. 再查语义知识库
        semantic = self.semantic_memory.search(query, top_k=2)

        return recent + episodic + semantic

    def _compress_to_episodic(self):
        """工作记忆 → 情节记忆（摘要后向量化存储）"""
        old_turns = self.working_memory[:-3]  # 保留最近3轮
        summary = llm_summarize(old_turns)
        self.episodic_memory.add(summary, metadata={"timestamp": now()})
        self.working_memory = self.working_memory[-3:]  # 裁剪
```

**实际项目中的记忆策略选择：**

| 场景 | 推荐策略 | 原因 |
|------|---------|------|
| 简单客服机器人 | 工作记忆（最近5轮） | 简单够用，成本低 |
| 个人助手 | 工作记忆 + 情节记忆 | 需要记住用户偏好 |
| 知识库问答 | 工作记忆 + 语义记忆 | 需要检索外部知识 |
| 复杂多轮Agent | 四层全用 | 复杂任务需要全局记忆 |

**面试话术：**
> "我把 Agent 记忆分四层：工作记忆（当前 context，4K token 上限）、情节记忆（历史对话压缩后存向量DB）、语义记忆（知识库 RAG）、程序记忆（工具调用链缓存）。超出工作记忆上限时，自动压缩老对话写入情节记忆，下次 recall 时语义搜索取回。实测减少 token 消耗 60%，响应速度提升40%。"

</details>

### Q: 上下文语义重写机制是什么？为什么需要它？

<details>
<summary>💡 答案要点</summary>

**为什么需要上下文重写（Query Rewrite）：**

```
用户第1轮: "给我介绍一下张三"
用户第2轮: "他的工作经历是什么？"  ← "他"指的是谁？
用户第3轮: "和李四比呢？"          ← 上下文依赖更深

问题：直接用第2/3轮query去检索，向量数据库不知道"他"是谁！
```

**解决方案：上下文感知重写**

```python
async def rewrite_with_context(
    query: str,
    history: list[dict]
) -> str:
    """将多轮对话query重写为独立完整的查询"""

    prompt = f"""
你是一个查询重写助手。根据对话历史，将用户的最新问题重写为
一个完整、独立、不依赖上下文的查询。

对话历史：
{format_history(history)}

用户最新问题：{query}

重写规则：
1. 解析代词（他/她/它/这个/那个）→ 替换为具体指代
2. 补全省略成分（"和上面说的比呢" → "XXX和YYY相比有什么区别"）
3. 保留原始意图，不要改变问题本质
4. 输出简洁，不要解释

重写后的查询：
    """

    rewritten = await llm.complete(prompt)
    return rewritten

# 示例
history = [
    {"role": "user", "content": "给我介绍一下LangChain"},
    {"role": "assistant", "content": "LangChain是..."}
]
query = "它和LlamaIndex比有什么优势？"

rewritten = await rewrite_with_context(query, history)
# 输出: "LangChain和LlamaIndex相比有什么优势？"
# 现在向量检索就能精准找到相关内容！
```

**完整 RAG 管道中的位置：**
```
用户输入 → [上下文重写] → 向量检索 → Rerank → LLM生成 → 输出
               ↑
          依赖对话历史
```

**面试话术：**
> "上下文重写是多轮对话 RAG 的关键环节。问题是用户第N轮的query往往有代词和省略，直接向量检索效果很差。我的方案是：先用 LLM 把当前 query + 历史 context 一起输入，让模型重写成完整独立的查询，再去检索。额外成本是一次小模型调用（约100 token，¥0.0001），但检索准确率提升 30% 以上。"

</details>

### Q: 整个 Agent 的部署方式，容器化部署还是宿主机部署？

<details>
<summary>💡 答案要点</summary>

**两种方案对比：**

| 维度 | 容器化部署（Docker/K8s） | 宿主机部署 |
|------|------------------------|-----------|
| **隔离性** | ✅ 每个 Agent 独立容器，互不影响 | ❌ 共享进程空间，有干扰 |
| **弹性伸缩** | ✅ K8s HPA 自动扩容 | ❌ 手动扩容，响应慢 |
| **资源开销** | ❌ 容器启动 100-300ms，内存多10% | ✅ 无额外开销 |
| **安全性** | ✅ 容器沙箱，代码执行隔离 | ❌ Agent 可操作宿主机 |
| **部署复杂度** | ❌ 需要容器知识 | ✅ 简单直接 |
| **适用场景** | 生产环境，多 Agent 并发 | 开发调试，资源紧张 |

**推荐方案：容器化 + 容器池预热**

```yaml
# docker-compose.yml 示例
services:
  agent-service:
    image: my-agent:latest
    deploy:
      replicas: 3          # 3个实例
      resources:
        limits:
          cpus: '0.5'
          memory: 512M     # 限制资源防止一个Agent耗尽
    environment:
      - MAX_CONCURRENT_TASKS=5
      - TOOL_EXECUTION_TIMEOUT=30s

  # 容器池：预热避免冷启动
  agent-pool:
    image: my-agent:latest
    command: ["python", "pool_manager.py", "--size=5"]
```

```python
# 容器池管理（参考 OpenClaw/E2B 方案）
class AgentContainerPool:
    def __init__(self, pool_size=5):
        self.pool = []
        self._pre_warm(pool_size)  # 预启动5个容器

    def _pre_warm(self, n: int):
        for _ in range(n):
            container = docker.run("agent:latest", detach=True)
            self.pool.append(container)

    def get_container(self):
        """从池中取容器，100ms内就绪（vs 冷启动300ms）"""
        if self.pool:
            container = self.pool.pop()
            self._pre_warm(1)  # 异步补充一个
            return container
        return docker.run("agent:latest")  # 池空了才冷启动
```

**实际选择建议：**
- **开发/测试**：宿主机直接运行，快速迭代
- **生产单机**：Docker Compose，简单隔离
- **生产集群**：K8s + HPA 自动扩缩容
- **多租户/代码执行**：容器沙箱强制隔离（安全红线）

**面试话术：**
> "我们生产环境用容器化部署，原因是三个：1) 安全隔离，Agent 执行代码工具时在独立容器，rm -rf 也只删容器不影响宿主机；2) 弹性伸缩，K8s HPA 根据队列长度自动扩容；3) 故障隔离，一个 Agent 挂了不影响其他实例。优化点是容器池预热，保持5个热容器，避免冷启动延迟 300ms。"

</details>


---

**上一模块：** [Transformer 架构](../04-transformer-architecture/)
**下一模块：** [向量索引优化](../06-vector-index-optimization/)

---

[返回目录 →](../../README.md)
