# 🔥 AI 应用安全与评估面试题

> **难度：** ⭐⭐⭐⭐⭐  
> **更新：** 2026-03-03  
> **考点：** AI 安全、内容合规、评估体系、测试方法、成本优化实战

---

## 📋 目录

1. [AI 安全与合规](#一 ai 安全与合规)
2. [评估与测试](#二评估与测试)
3. [成本优化实战](#三成本优化实战)
4. [LangGraph 工作流](#四 langgraph 工作流)
5. [速记卡片](#五速记卡片)

---

## 一、AI 安全与合规

### Q1: 如何防止 AI 应用生成有害内容？（内容安全）

<details>
<summary>💡 答案要点</summary>

**有害内容类型：**
- 违法内容（暴力、恐怖、赌博）
- 色情内容
- 歧视性内容（种族、性别、宗教）
- 虚假信息（谣言、伪科学）
- 隐私泄露

**防护体系：**
```
┌─────────────────────────────────────────────────────────┐
│                   AI 内容安全防护体系                     │
└─────────────────────────────────────────────────────────┘

输入层 → 处理层 → 输出层 → 监控层
  ↓         ↓         ↓         ↓
关键词   模型对齐   内容审核   用户举报
过滤     Prompt    API 检测   审计日志
```

**具体措施：**

| 层级 | 措施 | 实现方式 |
|------|------|----------|
| **输入层** | 关键词过滤 | 敏感词库匹配 |
| **输入层** | Prompt 注入检测 | 检测"忽略指令"等攻击模式 |
| **处理层** | 系统 Prompt 加固 | 明确安全边界和价值观 |
| **输出层** | 内容审核 API | 阿里云/腾讯云内容安全 |
| **输出层** | 自检机制 | 让模型自己检查是否合规 |
| **监控层** | 用户举报 | 快速响应机制 |
| **监控层** | 审计日志 | 完整记录便于追溯 |

**实现示例：**
```python
# 输出层自检
def safety_check(response):
    check_prompt = f"""
    请检查以下内容是否包含有害信息：
    - 违法、暴力、色情内容
    - 歧视性言论
    - 虚假或误导性信息
    
    内容：{response}
    
    如果安全，回复"SAFE"；如果有问题，说明原因。
    """
    result = llm.generate(check_prompt)
    return "SAFE" in result
```

**面试话术：**
> "我建立了四层内容安全防护体系。特别是输出层的自检机制，让模型自己检查是否合规，能发现 80% 的潜在问题。同时接入了第三方内容审核 API，双重保障。"

</details>

---

### Q2: 如何处理用户隐私数据？（PII 保护）

<details>
<summary>💡 答案要点</summary>

**隐私数据类型：**
| 类型 | 示例 | 风险等级 |
|------|------|----------|
| **个人身份** | 姓名、身份证、手机号 | 🔴 高 |
| **联系方式** | 邮箱、地址、社交账号 | 🔴 高 |
| **财务信息** | 银行卡、支付宝、收入 | 🔴 高 |
| **健康信息** | 病历、体检报告 | 🔴 高 |
| **行为数据** | 浏览记录、购买记录 | 🟡 中 |

**保护方案：**

| 方案 | 说明 | 适用场景 |
|------|------|----------|
| **输入脱敏** | 用户输入时自动识别并脱敏 | 所有场景 |
| **输出过滤** | 生成内容中删除隐私信息 | 公开场景 |
| **加密存储** | 敏感数据加密后存储 | 数据库 |
| **访问控制** | 基于角色的权限管理 | 内部系统 |
| **数据留存** | 定期清理过期数据 | 合规要求 |

**脱敏实现：**
```python
import re

def sanitize_pii(text):
    # 手机号脱敏：13812345678 → 138****5678
    text = re.sub(r'1[3-9]\d{9}', 
                  lambda m: m.group()[:3] + '****' + m.group()[-4:], 
                  text)
    
    # 身份证脱敏：110101199001011234 → 110***********1234
    text = re.sub(r'\d{18}', 
                  lambda m: m.group()[:3] + '***********' + m.group()[-4:], 
                  text)
    
    # 邮箱脱敏：test@example.com → t***@example.com
    text = re.sub(r'(\w)[\w.]*(@\w+\.\w+)', 
                  lambda m: m.group(1) + '***' + m.group(2), 
                  text)
    
    return text
```

**面试话术：**
> "我在输入和输出层都做了 PII 脱敏，用正则匹配手机号、身份证、邮箱等敏感数据。日志脱敏后留存 30 天，对话历史用户可以随时删除，符合 GDPR 要求。"

</details>

---

### Q3: 如何防止 AI 应用被滥用？（刷量、攻击）

<details>
<summary>💡 答案要点</summary>

**滥用类型：**
1. **刷量攻击**：恶意调用，消耗 Token 预算
2. **Prompt 注入**：绕过安全限制
3. **数据爬取**：批量获取知识库内容
4. **账号共享**：多人共用一个账号

**防护体系：**
```
┌─────────────────────────────────────────────────────────┐
│                   AI 应用防滥用体系                       │
└─────────────────────────────────────────────────────────┘

接入层 → 行为层 → 数据层 → 响应层
  ↓         ↓         ↓         ↓
鉴权     频率限制   内容保护   动态响应
设备指纹  异常检测   水印     人机验证
```

**具体实现：**

| 层级 | 措施 | 说明 |
|------|------|------|
| **接入层** | API Key 鉴权 | 每个用户独立 Key |
| **接入层** | 设备指纹 | 识别异常设备 |
| **行为层** | 频率限制 | 令牌桶算法 |
| **行为层** | 异常检测 | 机器学习识别异常模式 |
| **数据层** | 响应水印 | 隐藏标记便于追踪 |
| **响应层** | 人机验证 | 可疑时触发验证码 |

**限流实现（Go）：**
```go
type RateLimiter struct {
    tokens chan struct{}
}

func NewRateLimiter(rate int) *RateLimiter {
    rl := &RateLimiter{tokens: make(chan struct{}, rate)}
    go func() {
        for {
            time.Sleep(time.Minute / time.Duration(rate))
            rl.tokens <- struct{}{}
        }
    }()
    return rl
}

func (rl *RateLimiter) Wait() {
    <-rl.tokens
}
```

**面试话术：**
> "我设计了四层防滥用体系。特别是行为层的异常检测，用机器学习识别异常调用模式，有一次发现某个 IP 的 Token 消耗突增 10 倍，及时封禁避免了损失。"

</details>

---

## 二、评估与测试

### Q4: 如何评估 AI 应用的质量？（评估体系）

<details>
<summary>💡 答案要点</summary>

**评估维度：**
```
┌─────────────────────────────────────────────────────────┐
│                    AI 应用评估体系                        │
└─────────────────────────────────────────────────────────┘

准确性 ←→ 相关性 ←→ 安全性 ←→ 体验 ←→ 成本
   ↓         ↓         ↓         ↓       ↓
答案对   答得准   无有害   响应快   花钱少
```

**核心指标：**

| 维度 | 指标 | 计算方法 | 合格线 |
|------|------|----------|--------|
| **准确性** | 答案正确率 | 人工标注/标准答案对比 | > 85% |
| **相关性** | RAGAS Relevance | 答案与问题的语义相似度 | > 0.8 |
| **安全性** | 有害内容比例 | 审核 API 检测 | < 1% |
| **体验** | 首字延迟 | 从请求到第一个 token | < 1s |
| **体验** | 完整响应时间 | 从请求到完整答案 | < 5s |
| **成本** | 单次对话成本 | Token 消耗 × 单价 | < ¥0.01 |

**评估方法：**

| 方法 | 说明 | 优缺点 |
|------|------|--------|
| **人工评估** | 专业人员打分 | 准确但成本高 |
| **自动评估** | RAGAS/TruLens | 快速但不够精确 |
| **A/B 测试** | 对比不同版本 | 真实但周期长 |
| **用户反馈** | 点赞/点踩 | 直接但有偏差 |

**面试话术：**
> "我建立了自动化评估 Pipeline，每次上线前跑 500 道测试题。RAGAS 四个指标（忠实度、相关性、上下文精度、召回率）都要达标。同时加入了人工抽检，随机抽样 5% 的答案人工审核。"

</details>

---

### Q5: 如何做 AI 应用的回归测试？

<details>
<summary>💡 答案要点</summary>

**回归测试挑战：**
1. LLM 输出有随机性，不能简单对比
2. 测试用例维护成本高
3. 评估标准主观性强

**测试框架：**
```
┌─────────────────────────────────────────────────────────┐
│                   AI 应用回归测试框架                     │
└─────────────────────────────────────────────────────────┘

测试集 → 执行 → 评估 → 报告
  ↓       ↓       ↓       ↓
黄金用例  批量运行  自动评分  对比分析
```

**测试用例设计：**

| 类型 | 说明 | 示例 |
|------|------|------|
| **黄金用例** | 标准问题 + 标准答案 | "北京天气？" → "北京今天晴..." |
| **边界用例** | 极端或异常情况 | 超长输入、特殊字符 |
| **对抗用例** | 故意攻击测试 | Prompt 注入、越狱尝试 |
| **回归用例** | 历史 Bug 复现 | 之前修复的问题 |

**评估方法：**
```python
# 语义相似度评估
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def semantic_similarity(text1, text2):
    emb1 = model.encode(text1)
    emb2 = model.encode(text2)
    return cosine_similarity([emb1], [emb2])[0][0]

# 测试用例
test_cases = [
    {"input": "北京天气", "expected": "北京今天晴朗...", "threshold": 0.8},
    {"input": "上海气温", "expected": "上海今天 25 度...", "threshold": 0.8},
]

for case in test_cases:
    actual = llm.generate(case["input"])
    score = semantic_similarity(actual, case["expected"])
    assert score >= case["threshold"], f"相似度 {score} 低于阈值"
```

**面试话术：**
> "我维护了 500+ 道黄金测试题，每次上线前自动跑一遍。用语义相似度评估答案质量，阈值设为 0.8。对抗用例专门检测安全漏洞，确保不会被越狱。"

</details>

---

### Q6: RAGAS 的四个指标是什么？如何优化？

<details>
<summary>💡 答案要点</summary>

**RAGAS 四个核心指标：**

| 指标 | 说明 | 计算方式 | 合格线 |
|------|------|----------|--------|
| **Faithfulness（忠实度）** | 答案是否基于检索内容 | 答案中的陈述能否在上下文中找到依据 | > 0.7 |
| **Answer Relevance（答案相关性）** | 答案是否回答问题 | 答案与问题的语义相似度 | > 0.8 |
| **Context Relevance（上下文相关性）** | 检索内容是否有用 | 检索内容中与问题相关的比例 | > 0.8 |
| **Context Recall（上下文召回率）** | 是否检索到了正确答案 | 标准答案中的信息是否在检索内容中 | > 0.8 |

**优化策略：**

| 指标低 | 可能原因 | 优化方案 |
|--------|----------|----------|
| **Faithfulness 低** | 模型瞎编 | 增加检索结果数量、优化 Prompt |
| **Answer Relevance 低** | 答非所问 | 优化检索查询、改进 Prompt |
| **Context Relevance 低** | 检索内容不相关 | 改进 Embedding、加 Rerank |
| **Context Recall 低** | 没检索到正确答案 | 混合检索、扩大检索范围 |

**面试话术：**
> "Faithfulness 低于 0.7 会触发告警，说明模型可能在瞎编。我通过增加检索结果数量和在 Prompt 中强调'只基于检索内容回答'，把 Faithfulness 从 0.65 提升到了 0.82。"

</details>

---

## 三、成本优化实战

### Q7: 如何降低 AI 应用的 Token 成本？（实战经验）

<details>
<summary>💡 答案要点</summary>

**成本组成：**
```
总成本 = 输入 Token + 输出 Token + 检索 Token
       (30%)      (50%)        (20%)
```

**优化策略：**

| 策略 | 说明 | 节省比例 | 实施难度 |
|------|------|----------|----------|
| **语义缓存** | 相似问题直接返回缓存 | 30-50% | ⭐⭐ |
| **Prompt 压缩** | LLMLingua 压缩检索结果 | 40-90% | ⭐⭐⭐ |
| **模型路由** | 简单问题用小模型 | 30-40% | ⭐⭐ |
| **优化检索** | 减少 k 值，只返回最相关 | 20-30% | ⭐ |
| **流式输出** | 用户满意可提前终止 | 10-15% | ⭐⭐ |
| **批量处理** | 多个请求合并调用 | 10-20% | ⭐⭐⭐ |

**实战案例：**
> "我在项目中综合运用了多种优化策略：
> 1. **语义缓存**：命中率 45%，节省 30% 成本
> 2. **Prompt 压缩**：用 LLMLingua 压缩检索结果，节省 40%
> 3. **模型路由**：简单问题用 GPT-4o-mini，复杂问题用 GPT-4，节省 35%
> 
> 综合下来，整体成本降低了 60%，用户体验没有明显下降。"

**缓存实现：**
```python
from sentence_transformers import SentenceTransformer
import redis

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
redis_client = redis.Redis()

def semantic_cache(query, threshold=0.95):
    query_emb = model.encode(query)
    
    # 检索缓存
    cached = redis_client.hgetall("cache:queries")
    for key, value in cached.items():
        cached_emb = np.frombuffer(key, dtype=np.float32)
        similarity = cosine_similarity([query_emb], [cached_emb])[0][0]
        
        if similarity >= threshold:
            return value  # 返回缓存答案
    
    return None  # 缓存未命中
```

</details>

---

### Q8: 如何设计智能模型路由（Model Router）？

<details>
<summary>💡 答案要点</summary>

**路由策略：**
```
用户问题 → 意图分类 → 选择模型 → 调用 → 返回答案
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
    简单问题    中等问题     复杂问题
   (GPT-4o-mini) (Claude)   (GPT-4)
```

**分类维度：**

| 维度 | 简单 | 中等 | 复杂 |
|------|------|------|------|
| **问题类型** | 打招呼、常识 | 一般问答 | 复杂推理、代码 |
| **Token 预算** | < 500 | 500-2000 | > 2000 |
| **延迟要求** | < 1s | 1-3s | > 3s |
| **推荐模型** | GPT-4o-mini | Claude/Gemini | GPT-4 |

**实现示例：**
```python
class ModelRouter:
    def __init__(self):
        # 用轻量级模型做分类器
        self.classifier = load_classifier()
    
    def route(self, question):
        # 意图分类
        intent = self.classifier.predict(question)
        
        if intent == "simple":
            return "gpt-4o-mini"
        elif intent == "medium":
            return "claude-3-sonnet"
        else:
            return "gpt-4"
    
    def generate(self, question):
        model = self.route(question)
        return call_llm(model, question)
```

**面试话术：**
> "我设计的路由系统把问题分成三档，简单问题用便宜模型（GPT-4o-mini），复杂问题用 GPT-4。分类器本身用轻量级 BERT，成本几乎可以忽略。上线后成本降低了 35%，用户体验没有明显下降。"

</details>

---

## 四、LangGraph 工作流

### Q9: LangGraph 和 LangChain 有什么区别？

<details>
<summary>💡 答案要点</summary>

**核心区别：**

| 维度 | LangChain | LangGraph |
|------|-----------|-----------|
| **定位** | 链式调用 | 图状工作流 |
| **控制流** | 线性 | 支持循环和分支 |
| **状态管理** | 简单 | 持久化状态 |
| **适用场景** | 简单任务 | 复杂 Agent 编排 |
| **调试** | 困难 | 可视化追踪 |

**LangGraph 优势：**
1. **循环支持**：Agent 可以反复思考直到任务完成
2. **状态持久化**：支持长时间运行的任务
3. **可视化**：可以查看工作流执行过程
4. **分支逻辑**：根据条件走不同路径

**面试话术：**
> "LangChain 适合简单的链式调用，LangGraph 适合复杂的 Agent 编排。特别是需要循环和状态管理的场景，比如多轮对话、任务规划，LangGraph 更有优势。"

</details>

---

### Q10: 如何用 LangGraph 实现一个多轮对话 Agent？

<details>
<summary>💡 答案要点</summary>

**核心概念：**
```
┌─────────────────────────────────────────────────────────┐
│                   LangGraph 工作流                        │
└─────────────────────────────────────────────────────────┘

State（状态）→ Node（节点）→ Edge（边）→ Graph（图）
```

**实现示例：**
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    current_step: str

# 定义节点
def chat_node(state):
    response = llm.generate(state["messages"])
    return {"messages": [response]}

def tool_node(state):
    # 调用工具
    tool_result = call_tool(state["messages"][-1])
    return {"messages": [tool_result]}

# 定义边（条件路由）
def should_continue(state):
    if has_tool_call(state["messages"][-1]):
        return "tool"
    else:
        return END

# 构建图
workflow = StateGraph(AgentState)
workflow.add_node("chat", chat_node)
workflow.add_node("tool", tool_node)
workflow.set_entry_point("chat")
workflow.add_conditional_edges("chat", should_continue)
workflow.add_edge("tool", "chat")

# 编译运行
app = workflow.compile()
result = app.invoke({"messages": ["你好"], "current_step": "start"})
```

**面试话术：**
> "我用 LangGraph 实现了一个多轮对话 Agent，状态管理用 TypedDict 定义，节点处理不同任务，边控制流程。特别是条件路由，可以根据 Agent 的决策动态选择下一步，非常灵活。"

</details>

---

## 五、速记卡片

### AI 安全核心概念

| 概念 | 一句话解释 |
|------|------------|
| **内容安全** | 四层防护：输入过滤、Prompt 加固、输出审核、监控举报 |
| **PII 保护** | 输入输出双层脱敏，符合 GDPR |
| **防滥用** | 鉴权 + 限流 + 异常检测 + 人机验证 |

### 评估与测试

| 概念 | 一句话解释 |
|------|------------|
| **RAGAS** | 忠实度、相关性、上下文精度、召回率 |
| **黄金用例** | 标准问题 + 标准答案，用于回归测试 |
| **语义相似度** | 用 Embedding 计算答案相似度，阈值 0.8 |

### 成本优化

| 策略 | 节省比例 |
|------|----------|
| 语义缓存 | 30-50% |
| Prompt 压缩 | 40-90% |
| 模型路由 | 30-40% |
| 优化检索 | 20-30% |

### LangGraph

| 概念 | 一句话解释 |
|------|------------|
| **State** | 工作流状态（TypedDict） |
| **Node** | 处理节点（函数） |
| **Edge** | 流程控制（条件路由） |
| **优势** | 支持循环、状态持久化、可视化 |

---

## 📝 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-03-03 | 新增 AI 安全与评估面试题 10 道 |

---

**上一模块：** [MCP & Skill](../10-mcp-skill/)  
**下一模块：** [框架与运维](../08-framework-ops/)

---

**最后更新：** 2026-03-03  
**维护者：** 二狗子 🐕
