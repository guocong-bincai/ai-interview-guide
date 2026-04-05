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

## 9. AutoGen如何实现对话式多Agent协作?

<details>
<summary>💡 答案要点</summary>

**AutoGen = 微软开源的对话式多Agent框架**

### AutoGen核心理念

**通过Agent间对话完成复杂任务,而非预定义工作流**

```
传统工作流:
Agent A → Agent B → Agent C (固定顺序)

AutoGen对话式:
Agent A ←→ Agent B
    ↓          ↓
  Agent C ←→ Agent D
(动态协商,类似人类团队讨论)
```

### AutoGen核心组件

| 组件 | 类型 | 作用 |
|------|------|------|
| **UserProxyAgent** | 代理用户 | 执行代码/收集反馈/与用户交互 |
| **AssistantAgent** | AI助手 | 推理/生成方案/调用工具 |
| **GroupChat** | 多Agent管理 | 管理多Agent对话流程 |
| **GroupChatManager** | 调度器 | 决定下一个发言的Agent |

### AutoGen实战: 数据分析任务

**场景: 分析销售数据并生成报告**

```python
import autogen

# 1. 配置LLM
llm_config = {
    "model": "gpt-4",
    "api_key": "sk-xxx",
    "temperature": 0.7
}

# 2. 创建UserProxyAgent (执行代码)
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",  # 自动执行,不需人工干预
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False  # 本地执行Python代码
    }
)

# 3. 创建AssistantAgent (数据分析师)
data_analyst = autogen.AssistantAgent(
    name="DataAnalyst",
    llm_config=llm_config,
    system_message="""
    你是数据分析专家。
    任务: 分析销售数据,发现趋势,生成Python代码。
    要求: 使用pandas和matplotlib。
    """
)

# 4. 创建AssistantAgent (报告撰写者)
report_writer = autogen.AssistantAgent(
    name="ReportWriter",
    llm_config=llm_config,
    system_message="""
    你是商业报告撰写专家。
    任务: 将数据分析结果写成专业报告。
    要求: 包含关键发现、洞察和建议。
    """
)

# 5. 创建GroupChat
groupchat = autogen.GroupChat(
    agents=[user_proxy, data_analyst, report_writer],
    messages=[],
    max_round=10  # 最多10轮对话
)

# 6. 创建Manager
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# 7. 启动任务
user_proxy.initiate_chat(
    manager,
    message="""
    分析 sales_data.csv,生成月度销售报告。
    要求:
    1. 计算环比增长率
    2. 找出销售额最高的5个产品
    3. 生成趋势图
    4. 撰写200字分析报告
    """
)

# 8. 对话流程(自动进行)
"""
UserProxy: "分析sales_data.csv..." (发起任务)
    ↓
DataAnalyst: "我将用pandas读取数据..." (制定计划)
    ↓
UserProxy: 执行代码: pd.read_csv("sales_data.csv")
    ↓
DataAnalyst: "数据已读取,发现XX趋势,生成可视化代码..."
    ↓
UserProxy: 执行代码: plt.plot(...); plt.savefig("trend.png")
    ↓
ReportWriter: "根据分析结果,我撰写报告如下:..."
    ↓
UserProxy: "任务完成,报告已生成"
"""
```

### AutoGen高级特性

**特性1: 人类在环(Human-in-the-Loop)**

```python
# 关键决策需人工确认
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="ALWAYS",  # 每步都需确认
    # 或: "TERMINATE" - 只在终止前确认
)

# 对话流程:
"""
DataAnalyst: "我将删除销售额<100的数据"
UserProxy: [等待人工确认] → 输入 "y" 确认
DataAnalyst: "已删除,继续分析..."
"""
```

**特性2: 自定义发言顺序**

```python
def custom_speaker_selection(last_speaker, groupchat):
    """自定义下一个发言者"""

    # 规则1: DataAnalyst说完,让UserProxy执行代码
    if last_speaker.name == "DataAnalyst":
        return groupchat.agent_by_name("UserProxy")

    # 规则2: UserProxy执行完,检查是否需要报告
    if last_speaker.name == "UserProxy":
        if "数据分析完成" in groupchat.messages[-1]["content"]:
            return groupchat.agent_by_name("ReportWriter")
        else:
            return groupchat.agent_by_name("DataAnalyst")

    # 规则3: ReportWriter写完,终止
    if last_speaker.name == "ReportWriter":
        return None  # 终止对话

    return None

# 应用自定义策略
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
    speaker_selection_method=custom_speaker_selection
)
```

**特性3: 工具调用集成**

```python
# 定义工具函数
def query_database(sql: str) -> str:
    """查询数据库"""
    conn = sqlite3.connect("sales.db")
    df = pd.read_sql(sql, conn)
    return df.to_string()

def send_email(to: str, subject: str, body: str) -> str:
    """发送邮件"""
    # 实际发送逻辑...
    return f"邮件已发送给{to}"

# 注册工具到AssistantAgent
data_analyst.register_function(
    function_map={
        "query_database": query_database,
        "send_email": send_email
    }
)

# Agent会自动选择工具
"""
DataAnalyst: "我需要查询数据库"
→ 自动调用 query_database("SELECT * FROM sales")
→ 获取结果后继续分析
"""
```

### AutoGen vs CrewAI vs MetaGPT

| 框架 | 核心理念 | 优势 | 适用场景 |
|------|---------|------|----------|
| **AutoGen** | 对话式协作 | 灵活,迭代细化 | 需要讨论的任务(代码debug/数据分析) |
| **CrewAI** | 角色驱动 | 结构清晰 | 类团队协作(研究→撰写→审核) |
| **MetaGPT** | 软件开发 | 专注代码生成 | 自动化软件开发 |

### AutoGen实战案例: 自动化代码Review

```python
# 场景: 自动审查Pull Request

# 1. CodeReviewer Agent
reviewer = autogen.AssistantAgent(
    name="CodeReviewer",
    system_message="""
    你是高级代码审查专家。
    任务: 审查代码质量、安全性、性能问题。
    标准: PEP8规范、无SQL注入风险、时间复杂度合理。
    """
)

# 2. CodeRefactorer Agent
refactorer = autogen.AssistantAgent(
    name="CodeRefactorer",
    system_message="""
    你是代码重构专家。
    任务: 根据CodeReviewer的建议优化代码。
    要求: 保持功能不变,提升可读性和性能。
    """
)

# 3. Tester Agent
tester = autogen.AssistantAgent(
    name="Tester",
    system_message="""
    你是测试工程师。
    任务: 为重构后的代码生成单元测试。
    要求: 覆盖率>80%,包含边界情况。
    """
)

# 4. GroupChat
groupchat = autogen.GroupChat(
    agents=[user_proxy, reviewer, refactorer, tester],
    messages=[],
    max_round=15
)

# 5. 启动Review
user_proxy.initiate_chat(
    manager,
    message="""
    审查以下代码:
    ```python
    def process_user_input(data):
        query = f"SELECT * FROM users WHERE name='{data}'"
        return db.execute(query)
    ```
    """
)

# 6. 对话流程
"""
UserProxy: "审查以下代码..." (提交代码)
    ↓
CodeReviewer:
  "发现问题:
   1. SQL注入风险 - 直接拼接用户输入
   2. 缺少异常处理
   3. 变量名不规范"
    ↓
CodeRefactorer:
  "我将重构代码:
   ```python
   def process_user_input(user_data: str) -> List[Dict]:
       try:
           query = \"SELECT * FROM users WHERE name = ?\"
           return db.execute(query, (user_data,))
       except DatabaseError as e:
           logger.error(f\"Query failed: {e}\")
           raise
   ```"
    ↓
UserProxy: 执行代码(保存重构版本)
    ↓
Tester:
  "我将生成测试:
   ```python
   def test_process_user_input():
       # 正常情况
       assert process_user_input(\"John\") == [...]

       # SQL注入测试
       assert process_user_input(\"'; DROP TABLE users--\") 不会执行危险操作

       # 异常处理
       with pytest.raises(DatabaseError):
           process_user_input(invalid_data)
   ```"
    ↓
UserProxy: "Review完成,代码已优化并附带测试"
"""
```

### AutoGen调试技巧

```python
# 1. 打印对话历史
for msg in groupchat.messages:
    print(f"{msg['name']}: {msg['content'][:100]}...")

# 2. 限制单Agent发言次数
autogen.ConversableAgent(
    max_consecutive_auto_reply=3  # 最多连续说3次
)

# 3. 设置超时
user_proxy.initiate_chat(
    manager,
    message="...",
    clear_history=True,  # 清除历史
    silent=False,        # 打印对话
    timeout=300          # 5分钟超时
)
```

**面试话术:**
> "AutoGen的核心是对话式协作,不同于固定工作流。我用AutoGen做过代码Review:3个Agent(Reviewer审查/Refactorer重构/Tester测试)通过对话迭代优化代码。关键是定义好每个Agent的system_message,让它们有明确分工。AutoGen优势是灵活,Agent可以讨论来回,类似真实团队;缺点是可控性不如固定工作流。实战中我用自定义speaker_selection控制发言顺序,避免无限循环。"

</details>

---

## 10. CrewAI如何实现角色驱动的Agent协作?

<details>
<summary>💡 答案要点</summary>

**CrewAI = 模拟人类团队的多Agent框架**

### CrewAI核心理念

**给每个Agent分配角色(Role)、目标(Goal)、背景(Backstory)**

```
传统:
Agent1(任务: 搜索)
Agent2(任务: 总结)

CrewAI:
Agent1(角色: 研究员, 目标: 找到权威信息, 背景: 10年研究经验)
Agent2(角色: 作家, 目标: 写出引人入胜的文章, 背景: 畅销书作者)
```

### CrewAI核心组件

| 组件 | 作用 | 示例 |
|------|------|------|
| **Agent** | 单个Agent | Researcher / Writer / Reviewer |
| **Task** | 具体任务 | "调研AI趋势" / "撰写文章" |
| **Tool** | 工具函数 | SearchTool / FileReadTool |
| **Crew** | Agent团队 | 组织多个Agent协作 |
| **Process** | 执行流程 | Sequential(顺序) / Hierarchical(层级) |

### CrewAI实战: 内容创作团队

**场景: 自动生成技术博客文章**

```python
from crewai import Agent, Task, Crew, Process
from langchain.tools import DuckDuckGoSearchRun

# 1. 定义工具
search_tool = DuckDuckGoSearchRun()

# 2. 创建Researcher Agent
researcher = Agent(
    role="技术研究员",
    goal="找到关于{topic}的最新、最权威的信息",
    backstory="""
    你是一名资深技术研究员,有10年AI领域经验。
    你擅长快速找到前沿论文、技术博客和行业报告。
    你只信任权威来源,并能区分炒作和真正的突破。
    """,
    verbose=True,
    allow_delegation=False,  # 不能委托给其他Agent
    tools=[search_tool]
)

# 3. 创建Writer Agent
writer = Agent(
    role="技术作家",
    goal="将复杂技术写成通俗易懂的文章",
    backstory="""
    你是畅销技术书作者,擅长用故事和类比解释复杂概念。
    你的文章既有深度又易读,深受开发者喜爱。
    你总是用具体例子和代码示例支撑观点。
    """,
    verbose=True,
    allow_delegation=False
)

# 4. 创建Editor Agent
editor = Agent(
    role="技术编辑",
    goal="确保文章准确性和可读性",
    backstory="""
    你是技术杂志的资深编辑,对技术准确性要求极高。
    你会检查事实、纠正错误、优化表达、统一风格。
    你的标准是"无一处错误,无一句冗余"。
    """,
    verbose=True,
    allow_delegation=False
)

# 5. 定义Task
research_task = Task(
    description="""
    调研{topic}的最新进展:
    1. 找到3-5篇权威来源(论文/博客/文档)
    2. 总结核心技术点
    3. 找出实际应用案例
    4. 识别优势和局限性
    """,
    agent=researcher,
    expected_output="详细的调研报告,包含来源链接"
)

writing_task = Task(
    description="""
    基于调研报告,撰写技术博客:
    1. 标题: 吸引眼球且准确
    2. 引言: 用故事或问题开篇
    3. 正文: 解释技术原理,附代码示例
    4. 结论: 总结要点和展望
    5. 长度: 1500-2000字
    """,
    agent=writer,
    expected_output="完整的博客文章(Markdown格式)"
)

editing_task = Task(
    description="""
    审核并优化文章:
    1. 检查技术准确性
    2. 纠正语法和拼写错误
    3. 优化标题和小标题
    4. 确保代码示例可运行
    5. 统一术语和风格
    """,
    agent=editor,
    expected_output="最终版文章 + 修改说明"
)

# 6. 创建Crew(团队)
content_crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,  # 顺序执行
    verbose=2  # 打印详细日志
)

# 7. 执行任务
result = content_crew.kickoff(inputs={"topic": "LLM Agent的记忆系统"})

print(result)

# 输出: 一篇完整的、经过三人协作的高质量技术博客
```

### CrewAI执行流程

```
1. Researcher开始工作
   → 使用搜索工具找资料
   → 阅读论文和博客
   → 总结关键信息
   → 输出: 调研报告

2. Writer接收Researcher的输出
   → 阅读调研报告
   → 提取核心技术点
   → 撰写文章
   → 输出: 初稿

3. Editor接收Writer的输出
   → 审核技术准确性
   → 优化表达
   → 纠正错误
   → 输出: 最终稿
```

### CrewAI高级特性

**特性1: Agent间委托(Delegation)**

```python
# 允许Manager委托任务给Specialist
manager = Agent(
    role="项目经理",
    goal="协调团队完成项目",
    allow_delegation=True,  # 可以委托
    backstory="你是项目管理专家,善于分配任务和协调资源"
)

specialist = Agent(
    role="数据分析专家",
    goal="分析数据",
    allow_delegation=False,
    backstory="你专注数据分析"
)

# Manager可以说: "我将这个数据分析任务委托给Specialist"
```

**特性2: 层级流程(Hierarchical Process)**

```python
# 有明确的上下级关系
content_crew = Crew(
    agents=[manager, researcher, writer, editor],
    tasks=[...],
    process=Process.hierarchical,  # 层级模式
    manager_llm="gpt-4"  # Manager使用的LLM
)

# 执行流程:
"""
Manager: "我分配任务:
  - Researcher: 调研AI趋势
  - Writer: 撰写文章
  - Editor: 审核文章"

→ Researcher完成调研
→ Manager检查,满意后:

Manager: "Writer,基于调研撰写文章"
→ Writer完成初稿
→ Manager检查,交给Editor

Manager: "Editor,审核文章"
→ Editor完成审核
→ Manager验收最终结果
"""
```

**特性3: 自定义工具**

```python
from crewai_tools import tool

@tool("Code Executor")
def execute_python_code(code: str) -> str:
    """执行Python代码并返回结果"""
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return str(exec_globals.get("result", "执行成功"))
    except Exception as e:
        return f"错误: {str(e)}"

# 分配给Agent
coder = Agent(
    role="Python开发",
    tools=[execute_python_code],
    backstory="你是Python专家"
)
```

### CrewAI实战案例: 招聘流程自动化

```python
# 场景: 自动筛选简历+生成面试题

# 1. Recruiter Agent
recruiter = Agent(
    role="招聘专员",
    goal="筛选符合岗位要求的候选人",
    backstory="你有5年招聘经验,善于从简历中发现潜力"
)

# 2. Technical Interviewer Agent
tech_interviewer = Agent(
    role="技术面试官",
    goal="设计针对性的面试题",
    backstory="你是资深AI工程师,了解如何考察技术深度"
)

# 3. HR Manager Agent
hr_manager = Agent(
    role="HR经理",
    goal="综合评估候选人",
    backstory="你负责最终决策,平衡技术能力和文化契合度"
)

# Tasks
screen_task = Task(
    description="""
    筛选简历,评估候选人:
    - 技术栈匹配度
    - 项目经验相关性
    - 教育背景
    输出: 推荐/不推荐 + 理由
    """,
    agent=recruiter
)

interview_task = Task(
    description="""
    为推荐的候选人设计面试题:
    - 5道技术题(基础+进阶)
    - 2道项目题
    - 1道开放题
    """,
    agent=tech_interviewer
)

decision_task = Task(
    description="""
    综合评估:
    - 简历筛选结果
    - 面试题难度设计
    输出: 是否进入面试 + 面试官建议
    """,
    agent=hr_manager
)

# Crew
hiring_crew = Crew(
    agents=[recruiter, tech_interviewer, hr_manager],
    tasks=[screen_task, interview_task, decision_task],
    process=Process.sequential
)

# 执行
result = hiring_crew.kickoff(inputs={
    "resume": "张三的简历.pdf",
    "job_desc": "AI应用工程师岗位描述"
})
```

**面试话术:**
> "CrewAI的特色是角色驱动,每个Agent有明确的role/goal/backstory,更像真实团队。我用CrewAI做过内容创作:Researcher调研+Writer撰写+Editor审核,顺序执行。CrewAI优势是结构清晰,适合分工明确的任务;缺点是灵活性不如AutoGen。实战中我用Process.hierarchical实现层级管理,Manager分配任务,其他Agent执行。关键是写好backstory,让Agent有'个性',生成的内容更有针对性。"

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
| **AutoGen** | 微软开源,对话式协作,灵活迭代 |
| **CrewAI** | 角色驱动,模拟团队,结构清晰 |

---

## 11. 企业级Agent架构设计（2026年高频考点）

<details>
<summary>💡 答案要点</summary>

### 企业级Agent平台的核心架构

**三层架构设计：**
```
┌─────────────────────────────────────────────────────────────────┐
│                    企业级Agent平台三层架构                        │
├─────────────────────────────────────────────────────────────────┤
│  接入层（Gateway）                                                │
│  ├── 负载均衡（多实例部署）                                        │
│  ├── 鉴权认证（OAuth2/API Key）                                    │
│  ├── 限流熔断（保护后端服务）                                       │
│  └── 请求路由（按业务类型分流）                                      │
│                              ↓                                     │
│  编排层（Orchestration）                                           │
│  ├── 意图识别（确定用哪个Agent）                                    │
│  ├── Agent调度（协调多个Agent协作）                                 │
│  ├── 状态管理（会话上下文、超时控制）                                │
│  └── 结果聚合（合并多个Agent输出）                                   │
│                              ↓                                     │
│  能力层（Capabilities）                                           │
│  ├── 工具注册中心（MCP Server / Function Registry）                │
│  ├── 知识检索（RAG向量库+关键词库）                                  │
│  ├── 模型服务（vLLM/TGI推理集群）                                   │
│  └── 外部集成（ERP/CRM/数据库）                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 大规模Agent编排实战

**场景：客服中心AI平台（日均10万+咨询）**

```python
# 企业级Agent编排器
class EnterpriseAgentOrchestrator:
    def __init__(self):
        self.agent_registry = AgentRegistry()  # Agent注册中心
        self.tool_registry = ToolRegistry()   # 工具注册中心
        self.state_store = RedisStateStore()   # 分布式状态存储
        self.trace_collector = JaegerCollector()  # 链路追踪

    async def handle_request(self, request: AgentRequest) -> AgentResponse:
        trace_id = generate_trace_id()
        self.trace_collector.start_trace(trace_id)

        try:
            # Step 1: 意图识别（路由到合适的Agent）
            intent = await self.classify_intent(request)
            self.trace_collector.add_span(trace_id, "intent_classification", intent)

            # Step 2: 获取Agent实例（支持水平扩展）
            agent = await self.agent_registry.get_agent(
                intent.type,
                pool_size=10  # 每个Agent类型10个实例
            )

            # Step 3: 执行Agent（带超时和重试）
            result = await self.execute_with_fallback(
                agent,
                request,
                timeout=30,
                max_retries=2
            )

            # Step 4: 后处理（结果校验、敏感词过滤）
            result = self.post_process(result)

            return result

        except Exception as e:
            self.trace_collector.record_error(trace_id, e)
            return self.fallback_response()

        finally:
            self.trace_collector.end_trace(trace_id)

    async def classify_intent(self, request):
        # 用小模型做意图分类，节省成本
        classifier = await self.get_classifier("intent-v2")
        return await classifier.predict(request.text)

    async def execute_with_fallback(self, agent, request, timeout, max_retries):
        for attempt in range(max_retries + 1):
            try:
                return await asyncio.wait_for(
                    agent.execute(request),
                    timeout=timeout
                )
            except TimeoutError:
                if attempt == max_retries:
                    raise
                # 重试时换另一个Agent实例
                agent = await self.agent_registry.get_agent(agent.type)
```

### Agent能力分级与智能路由

**分级策略：**
```python
AGENT_TIERS = {
    "tier1": {
        "name": "基础问答",
        "model": "gpt-3.5-turbo",  # 便宜快速
        "examples": ["查天气", "简单FAQ"],
        "cost_per_1k": 0.002,
        "latency_p99": "500ms"
    },
    "tier2": {
        "name": "复杂推理",
        "model": "gpt-4o-mini",   # 中等成本
        "examples": ["数据分析", "代码调试"],
        "cost_per_1k": 0.01,
        "latency_p99": "2s"
    },
    "tier3": {
        "name": "专家级",
        "model": "gpt-4o",        # 高成本高质量
        "examples": ["架构设计", "复杂文案"],
        "cost_per_1k": 0.03,
        "latency_p99": "5s"
    }
}

def route_to_tier(query: str) -> str:
    # 根据问题复杂度自动路由
    complexity = estimate_complexity(query)
    if complexity < 0.3:
        return "tier1"
    elif complexity < 0.7:
        return "tier2"
    else:
        return "tier3"
```

### Agent系统的可观测性设计

**三大核心指标：**

| 指标类型 | 具体指标 | 告警阈值 | 优化方向 |
|----------|----------|----------|----------|
| **延迟** | P50/P95/P99响应时间 | P99>5s | 模型分级、流式输出 |
| **成本** | 每千次请求成本 | 环比>20%上涨 | 缓存、小模型路由 |
| **质量** | 答案正确率、人工满意度 | <85% | Prompt优化、RAG增强 |
| **可用性** | 系统 uptime | <99.9% | 多区域部署、熔断降级 |

**全链路追踪：**
```python
# OpenTelemetry 集成
from opentelemetry import trace

@trace_span("agent.execute")
async def agent_execute(agent, request):
    with tracer.start_as_current_span("tool_call") as span:
        for tool in plan_tools(request):
            with tracer.start_as_current_span(f"tool.{tool.name}"):
                result = await tool.execute(request)
                span.set_attribute("tools_used", tool.name)
                span.set_attribute("cost", result.cost)
    return result
```

### Agent安全与权限控制

```python
class AgentSecurity:
    def __init__(self):
        self.permission_matrix = PermissionMatrix()

    def check_permissions(self, agent: Agent, action: Action) -> bool:
        """
        企业级权限矩阵：
        - Agent只能访问授权的工具
        - 敏感操作需要人工审批
        - 数据访问遵循最小权限原则
        """
        if action.type == "database_write":
            # 写数据库需要审批流程
            return self.approval_workflow.request_approval(agent, action)

        if action.type == "customer_data_access":
            # 客户数据访问需要明确授权
            return self.verify_data_consent(action.customer_id)

        return self.permission_matrix.check(agent.role, action.type)

    def audit_log(self, agent_id, action, result):
        """完整审计日志"""
        logger.info({
            "agent_id": agent_id,
            "action": action,
            "result": "success" if result else "denied",
            "timestamp": datetime.now().isoformat()
        })
```

### 企业级Agent平台的容灾设计

```python
class AgentFailover:
    def __init__(self):
        self.primary_model = "gpt-4o"
        self.fallback_models = ["claude-3-5-sonnet", "gemini-pro"]

    async def execute_with_fallback(self, prompt: str) -> str:
        for model in [self.primary_model] + self.fallback_models:
            try:
                result = await self.call_model(model, prompt)
                metrics.record("model_success", model)
                return result
            except ModelOverloadedError:
                # 触发熔断，等待后重试下一个模型
                await self.circuit_breaker.wait(model)
                metrics.record("model_fallback", model)
                continue
            except ModelRateLimitError:
                # 排队等待重试
                await asyncio.sleep(self.get_backoff(model))
                continue

        # 所有模型都失败，返回兜底答案
        return self.get_graceful_degradation_response()
```

### 面试话术

> "企业级Agent平台的核心是'可观测、可控、可扩展'。我的设计经验：
> 1. **分层路由**：简单问题用小模型省成本，复杂问题才上大模型，每年节省60%成本
> 2. **全链路追踪**：每个请求带trace_id，从入口到模型调用到工具执行全程可查
> 3. **多级容灾**：模型不可用时自动切换，核心功能降级但不中断
> 4. **安全合规**：敏感操作必须有审批流程，所有操作留审计日志"

> "关于Agent编排，我用过两种模式：
> - **固定工作流**：适合流程稳定的场景（如审批流），用LangGraph实现
> - **动态编排**：适合灵活响应场景（如客服），用AutoGen实现
> 实际项目中往往混合使用，固定部分用工作流引擎，灵活部分用Agent协作"

</details>

---

## 12. Agent Policy Engine：企业级Agent安全与权限控制（2026年考点）

<details>
<summary>💡 答案要点</summary>

### 为什么企业级Agent需要Policy Engine？

**核心问题：LLM不受控，不能让它"自由发挥"**
- Agent能调用工具、读写数据、发送消息——这些操作需要边界控制
- LLM只是文本生成器，无法"理解"安全边界
- 必须用结构化Policy Engine在LLM外部强制执行约束

### Policy Engine四层架构

```python
# Policy Engine在LLM和工具之间的位置
class PolicyEngine:
    def __init__(self):
        self.action_classifier = ActionClassifier()      # Layer 1: 动作分类
        self.resource_budget = ResourceBudget()          # Layer 2: 资源预算
        self.scope_guard = ScopeGuard()                 # Layer 3: 范围约束
        self.approval_gate = ApprovalGate()              # Layer 4: 审批门

    def authorize(self, proposed_action: Action) -> Decision:
        # Layer 1: 风险分类
        risk_level = self.action_classifier.classify(proposed_action)

        # Layer 2: 资源检查
        if not self.resource_budget.check(proposed_action):
            return Decision.REJECT("预算耗尽")

        # Layer 3: 范围检查
        if not self.scope_guard.is_allowed(proposed_action):
            return Decision.REJECT("超出范围")

        # Layer 4: 高风险需要审批
        if risk_level == "high" and not self.approval_gate.has_approval(proposed_action):
            return Decision.PENDING_APPROVAL(proposed_action)

        return Decision.APPROVE()
```

### Layer 1：动作风险分类

| 风险等级 | 动作类型 | 无需审批 |
|----------|----------|----------|
| **read-only** | 查询、搜索、读取数据 | ✅ 自动批准 |
| **reversible-write** | 修改个人设置、发送草稿消息 | ✅ 自动批准（有限额） |
| **irreversible-write** | 删除数据、发送外部消息、支付 | ❌ 必须审批 |
| **external-communication** | 发送邮件、API调用、写库 | ❌ 必须审批 |

### Layer 2：资源预算控制

```python
# 硬性限制，LLM无法突破
class ResourceBudget:
    def __init__(self):
        self.limits = {
            "api_calls_per_hour": 1000,
            "tokens_per_day": 1_000_000,
            "cost_per_session": 10.0,  # 美元
            "time_elapsed_max": 3600,   # 秒
        }

    def check(self, action: Action) -> bool:
        current = self.get_current_usage(action.agent_id)

        for resource, limit in self.limits.items():
            if current[resource] >= limit:
                return False  # 超出限制

        return True

    def get_current_usage(self, agent_id: str) -> dict:
        # 从Redis或数据库读取实时使用量
        return redis.hgetall(f"agent:{agent_id}:usage")
```

### Layer 3：Scope约束（范围边界）

**Scope = Agent只能访问特定的工具、数据源、外部系统**

```python
# 范围约束在集成层强制执行，Agent技术上无法越界
class ScopeGuard:
    def __init__(self):
        # 每个Agent只能调用授权的工具
        self.agent_permissions = {
            "customer_service_agent": {
                "allowed_tools": ["search_kb", "reply_template", "view_order"],
                "allowed_data": ["customer_db:read"],
                "blocked_tools": ["delete_user", "refund", "send_external_email"]
            }
        }

    def is_allowed(self, action: Action) -> bool:
        agent_id = action.agent_id
        perms = self.agent_permissions.get(agent_id, {})

        # 检查工具是否在白名单
        if action.tool not in perms.get("allowed_tools", []):
            return False

        # 检查工具是否在黑名单
        if action.tool in perms.get("blocked_tools", []):
            return False

        return True
```

### Layer 4：审批门（Human-in-the-Loop）

```python
# 高风险操作必须人工审批
class ApprovalGate:
    async def request_approval(self, action: Action) -> bool:
        # 构造审批请求
        approval_req = {
            "action": action.to_summary(),
            "risk": action.risk_level,
            "agent": action.agent_id,
            "requester": action.requested_by,
            "timestamp": datetime.now()
        }

        # 发送到审批队列
        await self.approval_queue.send(approval_req)

        # 等待人工响应（超时则拒绝）
        result = await self.approval_queue.wait_for_response(
            timeout=300,  # 5分钟超时
            required_approvers=1
        )

        return result.approved
```

### 为什么不work：仅靠Prompt约束

| 方法 | 为什么不够 | 效果 |
|------|------------|------|
| System Prompt加约束 | LLM只生成文本，不强制执行 | 可被越狱绕过 |
| Prompt说"不要调用删除API" | LLM可能"忘记" | 不安全 |
| **Policy Engine（结构化）** | LLM的输出必须经过Policy检查 | 安全，不可用Prompt绕过 |

**关键认知：**
> "边界必须结构化地执行，不能靠Prompt'建议'。如果Agent技术上能调用危险工具，它迟早会调用。Policy Engine是外部强制约束，不是LLM的内部知识。"

### 生产环境实现

```python
# 完整的Policy Engine Pipeline
class ProductionPolicyEngine:
    def __init__(self):
        self.classifier = RiskClassifier()
        self.budget = ResourceBudget()
        self.scope = ScopeGuard()
        self.approval = ApprovalGate()
        self.audit = AuditLogger()

    async def process(self, llm_output: str, context: AgentContext) -> ProcessedAction:
        # 1. 解析LLM输出的动作
        action = self.parse_action(llm_output)

        # 2. 强制执行Policy检查
        decision = await self.authorize(action, context)

        # 3. 记录审计日志
        await self.audit.log(decision, action, context)

        # 4. 执行或拒绝
        if decision == Decision.APPROVE:
            return await self.executor.execute(action)
        elif decision == Decision.PENDING:
            return await self.approval.request(action)
        else:
            return self.create_rejection_response(decision.reason)
```

### 面试话术

> "Policy Engine是2026年企业级Agent面试的核心考点。核心观点是'边界必须结构化，Prompt不可靠'。我用四层防护：风险分类决定检查强度，资源预算防止过度消耗，Scope约束在技术层面禁止越界，高风险操作必须人工审批。面试时能画出Policy Engine架构图并解释各层职责，说明你有企业级Agent落地经验。"

</details>

---

## 13. Microsoft Agent Governance Toolkit（2026年4月开源发布）

<details>
<summary>💡 答案要点</summary>

### 什么是Agent Governance Toolkit？

**发布方：** Microsoft（2026年4月2日）
**定位：** 开源的Agent运行时安全框架
**官网：** opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit

### 解决的问题

> "Policy Engine定义了规则，但谁来执行？谁来审计？谁来检测异常行为？Agent Governance Toolkit填补了这个空白。"

### 四大核心组件

| 组件 | 功能 | 解决的问题 |
|------|------|------------|
| **Policy Engine** | 定义和执行Agent行为策略 | "Agent能做什么" |
| **Identity Layer** | Agent身份认证和授权 | "Agent是谁" |
| **Audit Trail** | 完整记录所有Agent操作 | "Agent做了什么" |
| **Kill Switch** | 紧急停止Agent操作 | "Agent失控了怎么办" |

### Kill Switch：紧急停止机制

```python
# Kill Switch的典型实现
class AgentKillSwitch:
    def __init__(self):
        self.active_agents = {}  # agent_id -> status
        self.global_kill = False  # 全局终止开关

    def emergency_stop(self, agent_id=None):
        """紧急停止指定Agent或所有Agent"""
        if agent_id:
            self.active_agents[agent_id] = "STOPPED"
            await self.graceful_shutdown(agent_id)
        else:
            self.global_kill = True
            for aid in self.active_agents:
                self.active_agents[aid] = "STOPPED"
                await self.graceful_shutdown(aid)

    async def graceful_shutdown(self, agent_id):
        # 停止接收新任务
        # 等待当前任务完成或超时
        # 关闭所有工具连接
        # 记录最终状态
        pass

    def is_kill_switch_armed(self) -> bool:
        return self.global_kill or any(
            s == "STOPPED" for s in self.active_agents.values()
        )
```

### Audit Trail：操作可追溯

```python
# 每个Agent操作必须记录到审计日志
@dataclass
class AuditRecord:
    timestamp: datetime
    agent_id: str
    action: str
    tool_called: str
    parameters: dict
    result: str
    user_id: str  # 谁触发的
    session_id: str

# 审计日志必须包含：
# 1. 谁（user_id/agent_id）
# 2. 什么时候（timestamp）
# 3. 做了什么（action/tool/parameters）
# 4. 结果是什么（result）
# 5. 上下文是什么（session_id）
```

### 与Policy Engine的关系

```
Policy Engine：定义规则
Agent Governance Toolkit：执行+审计+Kill Switch

两者结合 = 完整的Agent安全体系

Policy Engine负责"规则制定"（静态）
Agent Governance Toolkit负责"规则执行"（动态）
```

### 面试话术

> "Microsoft Agent Governance Toolkit是2026年4月发布的开源框架，解决了'Policy Engine定义了规则但谁来执行'的问题。四大组件：Policy Engine（规则）、Identity（身份）、Audit Trail（审计）、Kill Switch（紧急停止）。面试时能说出Kill Switch的graceful shutdown机制和Audit Trail必须包含的五个要素，说明你有企业级Agent安全落地的实战理解。"

</details>

---

**上一模块：** [框架与工具](../12-frameworks-tools/)
**下一模块：** [MCP Skill 系统](../14-mcp-skill-systems/)

---

[返回目录 →](../../README.md)
