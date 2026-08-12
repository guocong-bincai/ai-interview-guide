# 🔥 Agent 可观测性与生产监控面试题

> **难度：** ⭐⭐⭐⭐
> **更新：** 2026-04-09
> **考点：** LangSmith、Arize Phoenix、OpenTelemetry、Prometheus、可观测性架构、指标设计、成本监控

---

## 📋 目录

1. [为什么 Agent 可观测性是必考题](#why-observability)
2. [核心监控指标体系](#metrics)
3. [面试高频追问](#follow-ups)
4. [速记卡片](#quick-reference)
5. [面试话术模板](#answer-template)
6. [Voice Agent 评估](#voice-evaluation)
7. [可观测性平台与生产实践](#platform-comparison)

---

<a id="why-observability"></a>

## 一、为什么 Agent 可观测性是 2026 年必考题？

2026年，Agent 应用从"能跑通"升级到"能运维"。面试中 **15-20% 的问题围绕生产可观测性展开**，考察维度包括：

- **正确性监控**：任务成功率、幻觉率、工具调用准确率
- **性能监控**：TTFT、端到端延迟、Token 消耗
- **成本监控**：每次任务成本、ROI 分析
- **安全监控**：Prompt 注入、越狱攻击、数据泄露

> "光会搭 LangChain Demo 已经完全不够用了。面试官最想听的是：线上遇到过什么问题，怎么权衡解决的。" —— 2026 面经总结

---

<a id="metrics"></a>

## 二、核心监控指标体系

### Q1: 如何建立 Agent 的可观测性体系？有哪些核心指标？

**核心指标分类：**

| 类别 | 指标 | 采集方式 |
|------|------|----------|
| **任务级** | 任务成功率、任务耗时、中断率 | trace_id 串联 |
| **模型级** | Token 消耗、TTFT、首 Token 延迟 | API 埋点 |
| **工具级** | 工具调用成功率、工具响应时间、工具误调用率 | 工具拦截器 |
| **Agent 级** | 循环检测率、规划步数、上下文膨胀率 | Agent 状态机 |
| **成本级** | 单任务成本、日成本、月成本、ROI | 计费日志 |

**可观测性三大支柱：**

```
1. Logging（日志）
   → 结构化日志：trace_id / span_id / event_type
   → 关键事件：工具调用/结果/异常/重试

2. Tracing（链路追踪）
   → OpenTelemetry 串联全链路
   → LangSmith / Phoenix 自动可视化

3. Metrics（指标）
   → Prometheus 聚合 + Grafana 展示
   → 告警规则：SLO / SLA
```

**生产级代码示例：**

<details>
<summary>展开 Python 代码示例（49 行）</summary>

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource

# 创建 tracer
resource = Resource.create({"service.name": "agent-service"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

class ObservableAgent:
    def __init__(self, llm, tools, callbacks=None):
        self.llm = llm
        self.tools = tools
        self.callbacks = callbacks or []
    
    async def run(self, task: str) -> str:
        with tracer.start_as_current_span("agent_run") as span:
            span.set_attribute("task", task)
            span.set_attribute("user_id", get_current_user())
            
            # 1. 规划阶段
            with tracer.start_as_current_span("planning") as plan_span:
                plan = await self.plan(task)
                plan_span.set_attribute("plan_steps", len(plan))
            
            # 2. 执行阶段（每个步骤一个 span）
            results = []
            for i, step in enumerate(plan):
                with tracer.start_as_current_span(f"step_{i}") as step_span:
                    step_span.set_attribute("step_type", step["type"])
                    step_span.set_attribute("step_description", step["desc"])
                    
                    result = await self.execute_step(step)
                    
                    # 检测循环
                    if self.is_looping(results, step):
                        step_span.set_attribute("loop_detected", True)
                        span.set_attribute("had_loop", True)
                        raise LoopDetectedError("Agent appears to be looping")
                    
                    results.append(result)
                    step_span.set_attribute("success", True)
            
            span.set_attribute("total_steps", len(results))
            span.set_attribute("total_tokens", self.get_token_count())
            
            return self.summarize(results)
```

</details>

**面试话术：**

> "Agent 可观测性核心是 trace_id 串联。我设计时用 OpenTelemetry 的 span 嵌套结构：最外层是 agent_run，内层分 planning 和各个 step，每个 step 里记录 tool_call。每个 span 都打上 user_id、model、token_count 属性。出问题后用 trace_id 在 LangSmith 或 Jaeger 里一键拉出完整链路，哪个 step 耗时最长、哪个工具失败了，一目了然。"

---

### Q1: 如何用 LangSmith 做 Agent 调试？有哪些高级用法？
**LangSmith 核心功能：**

<details>
<summary>展开 Python 代码示例（32 行）</summary>

```python
# LangSmith 配置
import langsmith

client = langsmith.Client(
    api_key=os.environ["LANGSMITH_API_KEY"],
    project="agent-production"
)

# 装饰器方式追踪
@client.traceable(project_name="tool-calling-agent")
async def agent_with_tools(query: str):
    # 完整链路自动记录
    result = await agent.run(query)
    return result

# 手动记录额外信息
run = client.create_run(
    project_name="agent-production",
    name="customer-support-agent",
    run_type="agent",
    inputs={"query": query},
    extra={"user_tier": "premium"}  # 自定义字段
)

# 记录每个工具调用
client.create_feedback(
    run.id,
    key="tool_accuracy",
    score=0.95,  # 0-1 评分
    correction={"expected_tool": "get_order_status"},
    comment="工具参数基本正确，1次轻微偏差"
)
```

</details>

**LangSmith 高级用法 - Prompt 版本管理：**

```python
# 对比两个不同 Prompt 版本的效果
from langsmith.schemas import Example, Run

def compare_prompt_versions(prompt_v1: str, prompt_v2: str, test_set: list):
    results = []
    
    for query in test_set:
        # v1 版本
        run_v1 = await agent_with_prompt(query, prompt_v1)
        
        # v2 版本
        run_v2 = await agent_with_prompt(query, prompt_v2)
        
        # 对比
        comparison = client.evaluate_run_pair(
            run_v1, run_v2,
            evaluation_config={
                "evaluators": ["cot_qa", "precision", "recall"]
            }
        )
        results.append({
            "query": query,
            "v1_score": comparison.score_v1,
            "v2_score": comparison.score_v2,
            "winner": "v2" if comparison.score_v2 > comparison.score_v1 else "v1"
        })
    
    return results
```

**面试话术：**

> "LangSmith 调试三板斧：1）用 traceable 装饰器零成本埋点；2）用 create_feedback 给每次运行打分，建立 ground truth；3）用 evaluate_run_pair 对比新旧 Prompt 版本。我线上用这套发现过一个问题：凌晨2-4点错误率异常高，后来定位是那时候客服人员下班、AI 开始胡说八道。加上时段告警后，SLA 从 95% 提到了 99.2%。"

---

### Q2: 如何监控 Agent 的 Token 消耗和成本？有哪些优化策略？
**成本监控架构：**

<details>
<summary>展开 Python 代码示例（53 行）</summary>

```python
import prometheus_client as prom
from prometheus_client import Counter, Histogram, Gauge

# 定义指标
TOKEN_USAGE = Counter(
    'agent_tokens_total',
    'Total tokens consumed',
    ['model', 'agent_type', 'user_tier']
)

TASK_COST = Histogram(
    'agent_task_cost_usd',
    'Cost per task in USD',
    ['agent_type'],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
)

MONTHLY_BUDGET = Gauge(
    'agent_monthly_budget_remaining_usd',
    'Remaining monthly budget'
)

# 成本追踪装饰器
def track_cost(model: str, price_per_1k_input: float, price_per_1k_output: float):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_tokens = get_token_count()
            result = await func(*args, **kwargs)
            
            end_tokens = get_token_count()
            input_tokens = end_tokens['input'] - start_tokens['input']
            output_tokens = end_tokens['output'] - start_tokens['output']
            
            cost = (input_tokens / 1000 * price_per_1k_input + 
                    output_tokens / 1000 * price_per_1k_output)
            
            TOKEN_USAGE.labels(model=model, agent_type=func.__name__).inc(
                input_tokens + output_tokens
            )
            TASK_COST.labels(agent_type=func.__name__).observe(cost)
            
            return result
        return wrapper
    return decorator

# 预算告警
def check_budget_alert():
    monthly_spent = get_monthly_cost()
    monthly_limit = get_monthly_limit()
    MONTHLY_BUDGET.set(monthly_limit - monthly_spent)
    
    if monthly_spent > monthly_limit * 0.8:
        send_alert(f"月度预算已达 80%，剩余 ${monthly_limit - monthly_spent:.2f}")
```

</details>

**成本优化策略：**

| 策略 | 节省比例 | 实现方式 |
|------|----------|----------|
| **语义缓存** | 30-50% | Embedding 相似度 > 0.95 直接返回缓存 |
| **模型路由** | 30-40% | 简单任务用 DeepSeek V4-Flash，复杂用 GPT-4 |
| **上下文压缩** | 40-90% | LLMLingua / Recomp 压缩历史 |
| **Token 配额** | 动态 | 按用户 tier 设置每日上限 |

<details>
<summary>展开 Python 代码示例（30 行）</summary>

```python
# 语义缓存实现
class SemanticCache:
    def __init__(self, similarity_threshold=0.95):
        self.cache = FAISS.from_texts(CACHE_TEXTS, CACHE_EMBEDDINGS)
        self.similarity_threshold = similarity_threshold
        self.cache_hits = 0
        self.cache_misses = 0
    
    async def get(self, query: str) -> Optional[str]:
        query_emb = get_embedding(query)
        scores, indices = self.cache.search(query_emb, k=1)
        
        if scores[0] > self.similarity_threshold:
            self.cache_hits += 1
            return self.cache_results[indices[0]]
        
        self.cache_misses += 1
        return None
    
    async def set(self, query: str, response: str):
        # 异步写入，避免阻塞
        await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: self.cache.add_texts([query], [get_embedding(query)])
        )
        self.cache_results.append(response)
    
    def hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0
```

</details>

**面试话术：**

> "成本控制是 2026 年面试高频追问。我的思路是三层控制：1）语义缓存，同一问题第二次问直接返回缓存，命中率达 40%；2）模型路由，简单查询路由到 DeepSeek V4-Flash，复杂推理才用 GPT-4，节省 30%；3）上下文压缩，对话超过 20 轮自动触发 LLMLingua 压缩历史。三个叠加，单任务成本从 $0.12 降到 $0.04，效果量化后给面试官看。"

---

### Q3: 如何检测 Agent 的行为异常？循环、幻觉、死循环如何发现？
**异常检测架构：**

<details>
<summary>展开 Python 代码示例（71 行）</summary>

```python
class AgentAnomalyDetector:
    def __init__(self):
        self.consecutive_identical = 0
        self.max_identical_steps = 3
        self.max_total_steps = 20
        self.history_hashes = []  # 存储历史状态 hash
    
    def detect_loop(self, step_result: str) -> bool:
        """检测重复步骤"""
        current_hash = hash(step_result)
        
        if current_hash in self.history_hashes:
            self.consecutive_identical += 1
            if self.consecutive_identical >= self.max_identical_steps:
                return True
        else:
            self.consecutive_identical = 0
        
        self.history_hashes.append(current_hash)
        return False
    
    def detect_context_bloat(self, messages: list) -> bool:
        """检测上下文膨胀"""
        total_tokens = sum(count_tokens(m) for m in messages)
        # 超过上下文窗口 80% 则告警
        if total_tokens > CONTEXT_LIMIT * 0.8:
            return True
        return False
    
    def detect_hallucination_risk(self, response: str, context: list) -> float:
        """用 Entailment 模型检测幻觉风险"""
        # 检测 response 中的事实陈述是否被 context 支持
        facts = extract_factual_statements(response)
        supported = 0
        
        for fact in facts:
            # 用 NLI 模型判断 entailment
            if nli_model.verify(fact, context) == "entailment":
                supported += 1
        
        return 1.0 - (supported / len(facts)) if facts else 0.0

# 生产集成示例
@track_cost(model="qwen3.5-plus", ...)
async def agent_run(query: str):
    detector = AgentAnomalyDetector()
    messages = []
    step_count = 0
    
    while step_count < MAX_STEPS:
        step_result = await agent.step(query, messages)
        
        # 循环检测
        if detector.detect_loop(step_result):
            raise LoopDetectedError("Detected repeated steps")
        
        # 上下文膨胀检测
        if detector.detect_context_bloat(messages):
            messages = compress_with_llmlingua(messages)
        
        # 幻觉风险检测
        hallucination_score = detector.detect_hallucination_risk(
            step_result, messages
        )
        if hallucination_score > 0.5:
            logger.warning(f"High hallucination risk: {hallucination_score}")
        
        messages.append(step_result)
        step_count += 1
    
    return final_response(messages)
```

</details>

**面试话术：**

> "Agent 异常检测我分三层：1）循环检测，用状态 hash 记录历史，3次相同状态触发熔断；2）上下文膨胀检测，超 80% 窗口自动压缩；3）幻觉风险检测，用 NLI 模型对每步输出做 Entailment 打分，超过 0.5 就告警。生产环境加上 Prometheus 告警规则：连续 5 个任务失败率 > 10% 自动发 PagerDuty。"

---

### Q4: 如何用 Arize Phoenix 做开源可观测性？和 LangSmith 有什么区别？
**Arize Phoenix 核心用法：**

<details>
<summary>展开 Python 代码示例（40 行）</summary>

```python
from phoenix.trace.tracer import Tracer
from phoenix.trace.openai import OpenAIInstrumentor
from phoenix.trace.llama_index import LlamaIndexInstrumentor
from phoenix.evals import run_evaluation

# 初始化 Phoenix
import phoenix as px
px.launch_app()

# 自动埋点 OpenAI 和 LlamaIndex
OpenAIInstrumentor().instrument()
LlamaIndexInstrumentor().instrument()

# 自定义 span
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("agent_reasoning")
async def agent_reasoning(agent, query):
    with trace.get_current_span() as span:
        span.set_attribute("query_type", classify_query(query))
        
        result = await agent.run(query)
        
        span.set_attribute("reasoning_steps", len(result.steps))
        span.set_attribute("tools_used", [t.name for t in result.tool_calls])
        
        return result

# 离线评估示例
df = px.session.active_session().get_trace_dataset()
eval_df = run_evaluation(
    dataframe=df,
    evaluators=[
        "relevance-to-query",
        "factuality",
        "harmfulness"
    ]
)
```

</details>

**LangSmith vs Arize Phoenix 对比：**

| 维度 | LangSmith | Arize Phoenix |
|------|-----------|---------------|
| **定位** | LangChain 官方 SaaS | 开源自托管 |
| **部署** | 云服务，无需运维 | Docker 一键部署，数据完全私有 |
| **成本** | 按量收费，免费版有限 | 完全免费，开源 |
| **评估** | 内置 LLM-as-Judge | 需手动配置 evals |
| **集成** | LangChain/LangGraph 原生 | 框架无关，支持 OpenTelemetry |
| **适用** | 快速起步 / 原型验证 | 企业数据合规 / 生产环境 |

**面试话术：**

> "选 LangSmith 还是 Phoenix 看场景：快速验证用 LangSmith，5 分钟接入；但我们生产用 Phoenix，数据完全在 VPC 里，审计合规没问题。Phoenix 的优势是 trace 数据全链路可查，Agent 跑了 20 步哪步慢了、幻觉在哪冒出来，图形界面一目了然。而且它是开源的，GitHub 3k+ 星，社区活跃。"

---

### Q5: 如何设计 Agent 的 SLA 和告警规则？有哪些关键阈值？
**SLA 设计：**

<details>
<summary>展开 Yaml 代码示例（67 行）</summary>

```yaml
# prometheus_alerts.yml
groups:
  - name: agent_sla
    rules:
      # SLA 1: 任务成功率 >= 95%
      - alert: AgentTaskSuccessRateLow
        expr: |
          (
            sum(rate(agent_tasks_total{status="success"}[5m]))
            /
            sum(rate(agent_tasks_total[5m]))
          ) < 0.95
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Agent 任务成功率低于 SLA (95%)"
          description: "当前成功率: {{ $value | humanizePercentage }}"
      
      # SLA 2: P99 延迟 <= 30s
      - alert: AgentLatencyHigh
        expr: |
          histogram_quantile(0.99, 
            sum(rate(agent_task_duration_seconds_bucket[5m])) 
            by (le)
          ) > 30
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Agent P99 延迟超过 30s"
      
      # SLA 3: Token 成本日增幅 > 20%
      - alert: AgentCostSpike
        expr: |
          (
            sum(increase(agent_tokens_total[24h]))
            /
            sum(increase(agent_tokens_total[24h] offset 7d))
          ) > 1.2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Agent Token 消耗日环比增长超过 20%"
      
      # 工具调用失败率 > 5%
      - alert: ToolCallFailureRateHigh
        expr: |
          (
            sum(rate(tool_calls_total{status="failure"}[5m]))
            /
            sum(rate(tool_calls_total[5m]))
          ) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "工具调用失败率 {{ $value | humanizePercentage }}，检查工具可用性"
      
      # 循环检测
      - alert: AgentLoopingDetected
        expr: increase(agent_loops_detected_total[5m]) > 0
        labels:
          severity: critical
        annotations:
          summary: "检测到 Agent 循环，任务已自动熔断"
```

</details>

**SLO 设计文档：**

| SLA 指标 | 目标值 | 告警阈值 | 测量方式 |
|----------|--------|----------|----------|
| 任务成功率 | 95% | < 93% PagerDuty | Prometheus counter |
| P50 延迟 | < 5s | > 8s 告警 | histogram |
| P99 延迟 | < 30s | > 45s PagerDuty | histogram |
| TTFT | < 1s | > 3s 告警 | histogram |
| 日 Token 消耗 | 基线 * 1.2 | > 1.5x 升级 | counter delta |
| 工具可用性 | 99.5% | < 99% 告警 | availability check |

**面试话术：**

> "SLA 设计核心是量化承诺。我的 Agent 平台 SLA：成功率 95%、P99 延迟 30s。告警分三级：warning（Slack 通知值班）、critical（PagerDuty 叫醒人）、emergency（连续 5 分钟 SLA 违约）。每个告警规则都有 runbook 链接，点进去能看到：1）当前状态；2）可能原因；3）止血步骤；4）后续复盘模板。告警不是目的，能快速止血才是。"

---

### Q6: 如何做 Agent 的 A/B 测试？有哪些评估指标？
**Agent A/B 测试架构：**

<details>
<summary>展开 Python 代码示例（76 行）</summary>

```python
from scipy.stats import chi2_contingency
import random

class AgentABTest:
    def __init__(self, variant_a: callable, variant_b: callable):
        self.variant_a = variant_a
        self.variant_b = variant_b
        self.results = {"a": [], "b": []}
    
    def assign_variant(self, user_id: str) -> str:
        # 稳定的 hash 分桶，确保同一用户始终分到同一组
        bucket = hash(user_id) % 100
        return "a" if bucket < 50 else "b"
    
    async def run_test(self, test_queries: list, duration_hours: int = 24):
        """运行 A/B 测试"""
        for query in test_queries:
            variant = self.assign_variant(hash_user(query))
            
            start = time.time()
            result = await (self.variant_a if variant == "a" else self.variant_b)(query)
            duration = time.time() - start
            
            self.results[variant].append({
                "query": query,
                "result": result,
                "duration": duration,
                "success": self.evaluate_success(result),
                "token_cost": self.count_tokens(result)
            })
    
    def analyze(self) -> dict:
        """统计分析"""
        results_a = self.results["a"]
        results_b = self.results["b"]
        
        # 成功率检验
        success_a = sum(1 for r in results_a if r["success"])
        success_b = sum(1 for r in results_b if r["success"])
        
        _, p_value = chi2_contingency([
            [success_a, len(results_a) - success_a],
            [success_b, len(results_b) - success_b]
        ])[:2]
        
        return {
            "variant_a": {
                "n": len(results_a),
                "success_rate": success_a / len(results_a),
                "avg_duration": mean([r["duration"] for r in results_a]),
                "avg_cost": mean([r["token_cost"] for r in results_a])
            },
            "variant_b": {
                "n": len(results_b),
                "success_rate": success_b / len(results_b),
                "avg_duration": mean([r["duration"] for r in results_b]),
                "avg_cost": mean([r["token_cost"] for r in results_b])
            },
            "statistical_significance": {
                "p_value": p_value,
                "significant": p_value < 0.05,
                "confidence_level": "95%"
            }
        }

# 使用示例
ab_test = AgentABTest(
    variant_a=lambda q: agent_v1.run(q),  # 旧版本
    variant_b=lambda q: agent_v2.run(q)  # 新版本
)
await ab_test.run_test(test_queries, duration_hours=24)
analysis = ab_test.analyze()

# 如果 B 版本显著更好，则推广
if analysis["statistical_significance"]["significant"]:
    rollout_to_production("variant_b")
```

</details>

**Agent A/B 测试评估指标：**

| 指标 | 测量方式 | 最小样本量 |
|------|----------|------------|
| **任务成功率** | 人工标注或 LLM-as-Judge | ~1000/组 |
| **用户满意度** | CSAT 评分（1-5） | ~200/组 |
| **平均任务时长** | 埋点计时 | ~500/组 |
| **Token 消耗** | API 日志 | ~500/组 |
| **工具调用次数** | Agent 日志 | ~500/组 |

**面试话术：**

> "Agent A/B 测试比普通功能复杂，因为'任务完成'本身就是模糊的。我的解法：定义清晰的完成标准（任务成功率、用户评分、Token 消耗），用 chi2 检验算 p 值，p<0.05 才推广。上线前用 5% 流量先跑 24 小时看数据。实践中发现，新版 Agent 加了 Reflexion 反思机制后，任务成功率从 78% 提到 86%（p=0.003，统计显著），才全量发布。"

---

<a id="follow-ups"></a>

## 三、面试高频追问

### Q8: Agent 可观测性和传统微服务可观测性有什么区别？

**核心区别：**

| 维度 | 传统微服务 | Agent 可观测性 |
|------|-----------|---------------|
| **追踪对象** | HTTP 请求、数据库查询 | LLM 调用、工具调用、规划步骤 |
| **不确定性** | 确定性逻辑，无幻觉 | LLM 输出不可预测，有幻觉风险 |
| **状态管理** | 无状态或短状态 | 多轮对话、长期记忆、上下文累积 |
| **性能指标** | 延迟、QPS、错误率 | TTFT、Token 速率、循环检测 |
| **调试难度** | 日志+链路追踪足够 | 需理解 LLM 推理过程，需 Prompt 可视化 |
| **特殊需求** | 标准 OpenTelemetry | LLM 原生支持（采样/Hallucination 检测） |

**Agent 可观测性特殊挑战：**

```python
# 挑战1：LLM 输出不确定性 → 需要输出质量追踪
outputs = []
for run in runs:
    outputs.append({
        "output": run.output,
        "hallucination_score": detect_hallucination(run.output),
        "toxicity_score": detect_toxicity(run.output),
        "factual_recall": measure_factual_recall(run.output, run.expected)
    })

# 挑战2：上下文累积 → 需追踪上下文膨胀
token_trend = [
    sum(count_tokens(m) for m in run.messages)
    for run in runs
]
# 检测：随任务复杂度增长，上下文是否线性膨胀

# 挑战3：工具调用链路 → 需追踪工具调用树
tool_tree = build_tool_call_tree(run.tool_calls)
# 检测：是否有不必要的工具调用、调用顺序是否最优
```

**面试话术：**

> "Agent 可观测性比微服务复杂在三点：1）LLM 输出不确定，同一个 Prompt 三次调用结果可能不同，必须追踪输出质量分布；2）上下文会累积，需要监控 Token 膨胀曲线；3）工具调用链路是树状结构，不是线性链路。我用 LangSmith 的 trace 串联所有步骤，每个 span 打上 step_type 和 tool_name 属性，出问题后从根节点一路点下去就能定位。"

---

<a id="quick-reference"></a>

## 四、速记卡片

| 话题 | 核心要点 |
|------|----------|
| **可观测性三大支柱** | Logging（结构化日志）+ Tracing（OpenTelemetry）+ Metrics（Prometheus） |
| **LangSmith** | LangChain 官方，5 分钟接入，支持 Prompt 版本对比和 LLM-as-Judge |
| **Arize Phoenix** | 开源自托管，数据完全私有，框架无关，支持离线评估 |
| **成本监控** | 语义缓存 30-50% + 模型路由 30-40% + 上下文压缩 40-90% |
| **异常检测** | 循环检测（hash 去重）+ 上下文膨胀检测（80% 窗口阈值）+ 幻觉风险（NLI Entailment） |
| **SLA 指标** | 成功率 95%、P99 延迟 30s、Token 日增幅 20% 告警 |
| **A/B 测试** | Hash 分桶 + chi2 检验 + p<0.05 推广 |
| **Agent vs 微服务** | 多了 LLM 输出质量追踪、上下文膨胀监控、工具调用树追踪 |

---

<a id="answer-template"></a>

## 五、面试话术模板

### 被问到"如何监控 Agent 质量"的标准回答：

> "我会从三个层面建立 Agent 监控体系：
> **第一层：任务级指标**——用 trace_id 串联每个任务的全链路，记录成功率、P99 延迟、Token 消耗。工具调用用拦截器自动埋点，失败率 > 5% 触发告警。
> **第二层：模型级指标**——监控 TTFT（首 Token 时间 < 1s）、幻觉风险分数（用 NLI Entailment 模型，> 0.5 告警）、循环检测（3次相同状态自动熔断）。
> **第三层：成本指标**——语义缓存命中率、模型路由比例、日/周/月成本趋势。超预算 80% 触发升级告警。
> 工具链：LangSmith 做链路追踪 + Prometheus 做指标聚合 + Grafana 做可视化 + PagerDuty 做告警。这套体系让我负责的 Agent 服务 SLA 稳定在 99.2%。"

---

<a id="voice-evaluation"></a>

## 六、Voice Agent 评估新框架：EVA（Q9）

### Q7: EVA 框架是什么？为什么"Accuracy-Experience Tradeoff"是 Voice Agent 评估的核心发现？
<details>
<summary>💡 答案要点</summary>

**背景问题：Voice Agent 评估的困境**

对话式语音 Agent 有两个核心目标：
1. **Accuracy（准确性）**——正确完成用户任务
2. **Experience（体验）**——自然、简洁、符合口语交互

这两个目标经常冲突：听错确认码 = 即使 LLM 推理完美也白搭；一股脑列出所有选项 = 口语场景用户无法浏览；延迟通过准确性检查但实际体验很差。

**现有框架的问题：**

| 框架 | 评估内容 | 局限性 |
|------|---------|--------|
| AudioBench, VoxEval | 单轮语音转录 | 无多轮交互 |
| FD-Bench, Talking Turns | 对话动态（打断、接话） | 与任务完成脱节 |
| VoiceAgentBench, CAVA | Agent 能力 | 不评估完整对话流程 |

**EVA 框架：首个端到端联合评估**

ServiceNow 2026年3月发布的 EVA，首次同时评估任务完成 + 对话体验：

```
┌─────────────────────────────────────────┐
│           EVA 评估框架                  │
├─────────────────────────────────────────┤
│  EVA-A (Accuracy)                       │
│  ├─ 任务完成率                          │
│  ├─ 工具调用正确性                      │
│  └─ 多步推理链完整性                    │
│                                         │
│  EVA-X (Experience)                     │
│  ├─ 响应自然度（无过度检索）            │
│  ├─ 延迟体验（P99 < 3s）                │
│  └─ 口语化程度（无机械感）              │
└─────────────────────────────────────────┘
```

**核心发现：Accuracy-Experience Tradeoff**

> "任务完成率高的 Agent，用户体验往往更差；用户体验好的 Agent，任务完成率往往较低。"

这是因为：
- 高准确性 → 需要更多确认步骤 → 用户觉得啰嗦
- 好体验 → 快速响应、少打断 → 可能漏掉关键信息

**EVA 航空数据集 benchmark 结果（20 个系统）：**

- 纯语音模型（S2S）和大音频语言模型（LALM）表现差异大
- Cascade 系统（STT→LLM→TTS）调优空间大
- 没有系统能同时在 EVA-A 和 EVA-X 上都领先

**面试话术：**

> "Voice Agent 评估和文本 Agent 完全不同——它必须同时看任务完成度和对话体验。EVA 框架告诉我，不能只优化准确率，否则做出来的 Bot 像个'复读机'；也不能只追求体验，否则任务经常完不成。2026年语音 Agent 会爆发，这个评估框架是面试高频点。"

</details>

---

*版本: v1.0 | 更新: 2026-04-14 | by 二狗子 🐕*

---

<a id="platform-comparison"></a>

## 十、2026年新锐Agent可观测性平台：Opik vs Maxim AI vs Latitude（Q10）

### Q8: Opik、Maxim AI、Latitude 三大2026新锐平台各有什么特点？如何选型？
<details>
<summary>💡 答案要点</summary>

**为什么需要关注新锐平台？**

2026年Agent进入生产阶段，原有LLM监控工具（LangSmith Arize Phoenix）无法满足多步骤轨迹分析需求。三个新平台快速崛起。

**三大平台核心定位：**

| 平台 | 定位 | 核心优势 | 适合场景 |
|------|------|----------|----------|
| **Comet Opik** | MLOps老牌推出的LLM追踪平台 | 与Weights & Biases生态深度集成；自动化评估Pipeline；100%开源 | 已经用W&B的团队；需要实验追踪的AI研发 |
| **Maxim AI** | 端到端Agent生命周期平台 | 仿真+评估+监控三合一；GEPA自动生成评估；跨职能协作界面 | 需要完整Agent生命周期的团队 |
| **Latitude** | AI应用可观测性+问题追踪 | 首创问题追踪生命周期；GEPA自动生成评估；生产故障直连代码 | 需要"可观测性+Issue管理"闭环的团队 |

**Comet Opik 详解：**

```python
# Opik 快速集成示例
from opik import track

@track
def my_agent_step(query: str):
    # 自动追踪每个Agent步骤
    return agent.run(query)

# 自动记录：输入/输出/Token消耗/延迟/工具调用链
```

- 与W&B无缝集成，实验结果自动同步
- 支持LangChain LangGraph的自动检测
- 提供自动化Prompt版本管理和A/B测试
- 开源可自托管

**Maxim AI 三大核心功能：**

1. **Agent仿真测试**：上线前用仿真环境测试多步骤轨迹
2. **GEPA（Generative Evaluation via Process Analysis）：** 自动从标注的生产故障生成评估集
3. **全生命周期监控**：预发布仿真→生产监控一体化

```python
# Maxim AI 评估Pipeline
from maxim import Evaluator

evaluator = Evaluator(
    framework="langgraph",
    metrics=["task_completion", "tool_accuracy", "safety"]
)
evaluator.run_simulation(test_cases)
evaluator.connect_to_production(tracing_enabled=True)
```

**Latitude 独特创新——问题追踪闭环：**

传统可观测性平台：发现异常 → 手动调查 → 跨工具切换

Latitude方案：发现异常 → 直接创建Issue → 自动关联Agent执行轨迹 → 修复后验证

```
生产告警 → Latitude Issue创建 → 自动携带Agent执行trace → 开发者review → 修复 → 自动replay验证
```

**三平台选型决策树：**

```
你的团队用W&B吗？
  ├─ 是 → Opik（与W&B生态集成最佳）
  └─ 否 → 需要"问题追踪闭环"吗？
           ├─ 是 → Latitude（Issue管理一体化）
           └─ 否 → 需要"仿真+评估+监控"全生命周期吗？
                    ├─ 是 → Maxim AI
                    └─ 否 → Langfuse自托管（最省钱）
```

**面试话术：**
> "2026年Agent可观测性选型，关键是回答'你要观测什么'。如果团队已经用W&B做实验追踪，Opik是自然延伸；如果需要预发布仿真加生产监控的闭环，Maxim AI最完整；如果想要'告警→Issue→修复'一体化，Latitude首创了这条路。我个人最关注Latitude，因为它的GEPA功能能从真实故障自动生成评估集，解决了'评估集过时'的痛点——生产出什么问题，评估集就自动长什么。"

**与现有平台的区别：**

| 维度 | LangSmith | Arize Phoenix | Opik | Maxim AI | Latitude |
|------|-----------|---------------|------|----------|----------|
| 部署模式 | 云/SaaS | 云+自托管 | 自托管 | 云 | 云 |
| Agent仿真 | ❌ | ❌ | ❌ | ✅ | ❌ |
| 问题追踪 | ❌ | ❌ | ❌ | ❌ | ✅ |
| W&B集成 | ❌ | ❌ | ✅ | ❌ | ❌ |
| 免费额度 | 限制 | 有限 | 开源免费 | 有限 | 最慷慨 |

</details>

### Q9: 为什么说"Agent可观测性≠传统LLM监控"？Agent轨迹追踪有哪些独特挑战？
<details>
<summary>💡 答案要点</summary>

**核心结论：Agent失败出现在多步骤因果链中，而非单次调用层**

传统LLM监控：单次API调用 → 延迟/Token/响应质量

Agent监控：多步骤轨迹 → 工具选择正确性→步骤间状态传递→整体任务完成率

**Agent可观测性的四大独特挑战：**

**1. 多步骤轨迹关联（Trace Correlation）**

```
用户说"帮我订明天北京的酒店"
  ↓
Step 1: search_hotel(tool) → 10个结果
  ↓  
Step 2: compare_price() → 筛选3个
  ↓
Step 3: book_hotel(tool) → 失败！日期格式错误
  ↓
Step 4: retry with date_format() → 成功

传统监控：每个步骤单独看都是正常的
Agent监控：要在Step 1-4的上下文中才能发现"日期解析模块有bug导致Step 3失败"
```

**2. 工具调用正确性判断（Tool Call Correctness）**

```python
# 传统评估：LLM输出质量
metric = "response_relevance"  # 单点评估

# Agent评估：工具序列质量
# 需要判断：
# - 选择了对的工具吗？（Tool Selection Accuracy）
# - 调用参数正确吗？（Parameter Accuracy）  
# - 调用顺序合理吗？（Sequence Optimality）
# - 整体任务完成了吗？（Task Completion）
metrics = {
    "tool_selection_accuracy": 0.95,
    "parameter_accuracy": 0.88,
    "sequence_optimality": 0.72,  # 这个低说明有冗余步骤
    "task_completion": 0.90
}
```

**3. 状态在步骤间传递（State Propagation）**

```
ReAct Loop中的状态管理问题：
- 中间结果存在哪里？（内存？文件？向量库？）
- 状态序列化失败怎么办？
- 多轮对话中历史状态膨胀怎么处理？
- 状态不一致如何检测？

这是传统LLM监控完全不关心的问题
```

**4. 非确定性执行路径（Non-Deterministic Execution）**

```
同一个任务，Agent可能走不同路径：
路径A：search → compare → book（3步完成）
路径B：search → filter → search → compare → book（5步完成）
路径C：search → error → retry → compare → book（4步完成）

评估必须考虑路径多样性，不能只看"最终是否完成"
```

**三维度对比：**

| 维度 | 传统LLM监控 | Agent可观测性 |
|------|------------|---------------|
| **粒度** | 单次API调用 | 多步骤轨迹链 |
| **失败定位** | 单点定位 | 因果链回溯 |
| **评估指标** | 延迟/Token/质量 | 工具选择/序列/完成率 |
| **根因分析** | 看单次响应 | 看轨迹上下文 |
| **可重现性** | 高（确定性） | 低（非确定性路径） |

**生产级Agent可观测性架构：**

```
┌──────────────────────────────────────────────────────┐
│           Agent可观测性全栈架构                       │
├──────────────────────────────────────────────────────┤
│  数据采集层                                          │
│  ├── LangSmith/Arize Phoenix/Opik（追踪Agent轨迹）   │
│  ├── Helicone/OpenLIT（API层成本追踪）               │
│  └── OpenTelemetry（统一导出）                        │
│                                                      │
│  分析层                                              │
│  ├── 工具调用正确性评估                              │
│  ├── 轨迹相似性聚类（发现异常模式）                   │
│  ├── 状态一致性检测                                  │
│  └── 端到端任务完成率                                 │
│                                                      │
│  告警层                                              │
│  ├── 异常轨迹实时告警（而非单次失败）                 │
│  ├── 非确定性路径模式告警                            │
│  └── 工具选择质量下滑告警                            │
│                                                      │
│  闭环层                                              │
│  ├── 自动生成评估集（GEPA）                          │
│  ├── 回归测试验证                                    │
│  └── Issue创建→修复→Replay验证                       │
└──────────────────────────────────────────────────────┘
```

**面试话术：**
> "Agent可观测性和传统LLM监控的本质区别是'看树还是看森林'。传统监控看你一次API调用正不正常，Agent可观测性看整个任务执行链。2026年我踩过的坑是：Agent在Step 3失败，但根因在Step 1的搜索结果质量差，导致后续步骤都在错误基础上做决策。这种问题只看单次API完全发现不了。生产级Agent可观测性必须做到：采集全轨迹、分析工具选择质量、检测状态一致性、在异常时能重建整个执行链。"

</details>

### Q10: OpenTelemetry 在 Agent 系统中的完整接入实战
<details>
<summary>💡 答案要点</summary>

**为什么 Agent 需要 OpenTelemetry？**

```
传统监控：单次 API 调用（输入 → 输出）
Agent 监控：多步骤轨迹链（Thought → Action → Observation → ... → Final）

OpenTelemetry = 统一采集 + 跨服务追踪 + 上下文传播
```

**架构图：**

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenTelemetry Agent 接入架构              │
├─────────────────────────────────────────────────────────────┤
│  1. Trace 采集（跨 Agent 链路追踪）                          │
│     ├── traceparent header 传递（TraceID/SpanID）           │
│     ├── 每个 Tool 调用 = 一个 Span                           │
│     └── 父Span → 子Span 自动关联                            │
│                                                              │
│  2. Metrics 采集（指标监控）                                 │
│     ├── token_consumption_total（累计 Token 消耗）           │
│     ├── tool_call_duration_seconds（工具调用延迟）           │
│     ├── step_count_per_task（每任务步数分布）                │
│     └── agent_retry_count（重试次数分布）                    │
│                                                              │
│  3. Logs 采集（结构化日志）                                  │
│     ├── trace_id 关联（同一请求的所有日志）                   │
│     ├── span_id（定位到具体步骤）                            │
│     └── attributes（tool_name、model、temperature 等）        │
│                                                              │
│  4. Baggage 传播（跨服务上下文）                              │
│     ├── user_id、session_id、feature_flags                  │
│     └── 在所有 Span 间自动传递                               │
└─────────────────────────────────────────────────────────────┘
```

**最小接入实现：**

<details>
<summary>展开 Python 代码示例（65 行）</summary>

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import Status, StatusCode

# 1. 初始化 Provider
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://collector:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# 2. 用装饰器自动追踪 Agent 步骤
class OpenTelemetryAgent:
    def __init__(self, name: str):
        self.name = name
        self.tracer = tracer
    
    async def run(self, task: str, tools: list):
        with self.tracer.start_as_current_span(
            f"agent.{self.name}.run",
            attributes={"task": task, "tool_count": len(tools)}
        ) as span:
            try:
                context = span.get_span_context()
                
                for step_idx, (thought, action, obs) in enumerate(self.reasoning_loop(task)):
                    with self.tracer.start_as_current_span(
                        f"agent.step.{step_idx}",
                        kind=trace.SpanKind.CLIENT,
                        attributes={
                            "step.thought": thought,
                            "step.action": action,
                            "step.observation": str(obs)[:200]
                        }
                    ) as step_span:
                        step_span.set_attribute("step.index", step_idx)
                        step_span.set_attribute(
                            "llm.token_usage", 
                            obs.get("token_count", 0) if isinstance(obs, dict) else 0
                        )
                        if "error" in obs:
                            step_span.set_status(Status(StatusCode.ERROR, obs["error"]))
                
                span.set_status(Status(StatusCode.OK))
                return final_result
                
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

# 3. 自动注入 trace_id 到工具调用
def call_tool_with_trace(tool_name: str, tool_args: dict, parent_span):
    with tracer.start_as_current_span(
        f"tool.{tool_name}",
        context=parent_span.get_span_context()
    ) as tool_span:
        tool_span.set_attribute("tool.name", tool_name)
        tool_span.set_attribute("tool.args", str(tool_args))
        result = tool_execute(tool_name, tool_args)
        tool_span.set_attribute("tool.result_type", type(result).__name__)
        return result
```

</details>

**关键配置（docker-compose）：**

```yaml
# otel-collector.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s

exporters:
  prometheus:
    endpoint: 0.0.0.0:8889
  jaeger:
    endpoint: http://jaeger:14250

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

**面试话术：**
> "我在生产环境中用 OpenTelemetry 做 Agent 可观测性，核心是三点：① 每个 Tool 调用是一个 Span，父Span自动关联子Span，能看清整个轨迹；② token消耗、步数、重试次数都入库，可以做成本分析和异常检测；③ trace_id 在所有日志里，打通了日志和链路。最实用的经验是用装饰器包装Agent的run方法，零侵入接入，不用改业务代码。"

</details>

### Q11: Grafana Dashboard 设计：Agent 监控面板关键指标
<details>
<summary>💡 答案要点</summary>

**Agent 监控 Dashboard 设计原则：**

```
传统微服务 Dashboard：CPU / 内存 / QPS / 延迟
Agent Dashboard：任务完成率 / 步数分布 / Token 成本 / 工具调用质量
```

**四象限 Dashboard 布局：**

```
┌────────────────────────────────────────────────────────────────┐
│                   Agent 生产监控 Dashboard                       │
├──────────────────────┬──────────────────────────────────────────┤
│   【业务健康度】      │   【成本分析】                           │
│   任务完成率: 94.2%  │   Token消耗: $1,247/日                   │
│   异常率: 5.8%       │   平均单次成本: $0.023                    │
│   用户满意度: 4.6/5  │   成本趋势: 📈 (+12% vs 上周)            │
├──────────────────────┼──────────────────────────────────────────┤
│   【Agent 行为分析】  │   【系统性能】                           │
│   平均步数: 4.3      │   P50延迟: 1.2s                          │
│   步数分布: [2,3,4,5]│   P99延迟: 4.8s                          │
│   最常用工具: search │   吞吐量: 850 QPS                        │
│   工具失败率: 2.1%   │   GPU利用率: 67%                         │
└──────────────────────┴──────────────────────────────────────────┘
```

**核心 Panel 配置（PromQL）：**

<details>
<summary>展开 Yaml 代码示例（37 行）</summary>

```yaml
# 1. 任务完成率 Panel
- title: 任务完成率
  expr: |
    sum(rate(agent_task_completed_total[5m])) 
    / 
    sum(rate(agent_task_started_total[5m])) * 100
  legend: 完成率 %
  thresholds:
    - value: 90
      color: red
    - value: 95
      color: yellow
    - value: 98
      color: green

# 2. Token 成本趋势 Panel
- title: 日Token消耗趋势
  expr: |
    sum(increase(agent_token_usage_total[1d])) by (model)
  legend: "{{model}}"
  type: area

# 3. 步数分布 Panel（发现异常长轨迹）
- title: 任务步数分布
  expr: |
    histogram_quantile(0.95, 
      sum(rate(agent_steps_per_task_bucket[5m])) by (le)
    )
  legend: P95步数

# 4. 工具调用质量 Panel
- title: 工具调用成功率
  expr: |
    sum(rate(agent_tool_call_success_total[5m])) by (tool_name)
    / 
    sum(rate(agent_tool_call_total[5m])) by (tool_name) * 100
  legend: "{{tool_name}}: {{value}}%"
```

</details>

**告警规则（alerting_rules.yaml）：**

<details>
<summary>展开 Yaml 代码示例（36 行）</summary>

```yaml
groups:
  - name: agent_alerts
    rules:
      # 任务完成率低于 85%
      - alert: AgentTaskCompletionRateLow
        expr: |
          sum(rate(agent_task_completed_total[5m])) 
          / sum(rate(agent_task_started_total[5m])) < 0.85
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Agent任务完成率过低"
          description: "当前完成率 {{ $value | humanizePercentage }}，持续5分钟"

      # Token消耗超阈值（日预算$2000，超$1800告警）
      - alert: AgentCostBudgetExceeded
        expr: |
          sum(increase(agent_token_usage_total[1h])) * 24 > 1800
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Agent日成本可能超预算"
          description: "预计日成本 ${{ $value }}，超过$1800阈值"

      # 异常长轨迹（步数>10）
      - alert: AgentTrajectoryTooLong
        expr: |
          sum(rate(agent_steps_over_threshold_total[5m])) > 3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Agent异常长轨迹增多"
          description: "5分钟内发现 {{ $value }} 个超长轨迹(>10步)"
```

</details>

**面试话术：**
> "我的Agent Dashboard按四象限设计：业务健康度（完成率/满意度）、成本分析（Token消耗/趋势）、Agent行为（步数分布/工具质量）、系统性能（延迟/吞吐）。告警规则我设置了三档：warning（完成率<95%）、critical（<85%）、cost alert（预计日成本超预算）。实际运营中发现步数分布最能预警问题——当P95步数突然从5升到8，说明检索质量下降了，需要查向量数据库。"

</details>

### Q12: 多 Agent 系统的分布式追踪：TraceID 传递与关联
<details>
<summary>💡 答案要点</summary>

**核心挑战：**

```
单 Agent：TraceID 在单个进程内传递
多 Agent：TraceID 跨越多个进程/服务，需要手动传播

问题：Agent A 调用 Agent B，trace_id 断了吗？
```

**传播机制对比：**

| 方式 | 原理 | 适用场景 | 局限性 |
|------|------|----------|--------|
| **HTTP Header** | traceparent 自动传播 | HTTP 调用 | 需要所有服务支持 OTEL |
| **消息队列** | 手动注入 baggage | 异步消息 | 需要修改消息格式 |
| **共享内存** | Redis 存储上下文 | 同机器多进程 | 延迟增加 |
| **数据库** | Task 表存储 trace_id | 持久化任务 | 需要事务支持 |

**生产级实现（HTTP + 消息队列双模式）：**

<details>
<summary>展开 Python 代码示例（58 行）</summary>

```python
from opentelemetry import propagate, trace
from opentelemetry.propagate import inject, extract
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

class MultiAgentTracer:
    def __init__(self):
        self.propagator = TraceContextTextMapPropagator()
    
    # 模式1：HTTP 调用（自动传播）
    async def call_agent_http(self, agent_name: str, task: dict, url: str):
        headers = {}
        inject(headers)  # 自动从当前 context 注入 traceparent
        
        response = await httpx.AsyncClient().post(
            url,
            json=task,
            headers={**headers, "X-Agent-Name": agent_name}
        )
        
        span_context = extract(response.headers).get(
            trace_span_context_key, None
        )
        return response.json()
    
    # 模式2：消息队列调用（手动传播）
    async def call_agent_mq(self, agent_name: str, task: dict, mq_client):
        current_span = trace.get_current_span()
        span_context = current_span.get_span_context()
        
        traceparent = f"00-{span_context.trace_id:032x}-{span_context.span_id:016x}-01"
        
        message = {
            **task,
            "_trace_context": {
                "traceparent": traceparent,
                "tracestate": current_span.get_span_context().trace_state,
                "agent_name": agent_name,
                "parent_span_id": span_context.span_id
            }
        }
        
        await mq_client.publish(
            exchange="agent_exchange",
            routing_key=agent_name,
            body=json.dumps(message)
        )

# 跨 Agent 轨迹聚合查询
async def get_full_trace(task_id: str):
    """获取同一任务的所有 Agent 轨迹"""
    trace_id = await redis.hget(f"task:{task_id}", "trace_id")
    
    spans = await jaeger_client.query(
        service=["agent-orchestrator", "agent-search", "agent-executor"],
        trace_id=trace_id
    )
    
    return sorted(spans, key=lambda s: s.start_time)
```

</details>

**数据库 Schema 设计：**

```sql
-- 任务表存储 trace_id 关联
CREATE TABLE agent_tasks (
    id UUID PRIMARY KEY,
    trace_id VARCHAR(64) NOT NULL,
    parent_span_id VARCHAR(32) NOT NULL,
    status VARCHAR(20),
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    INDEX idx_trace_id (trace_id),
    INDEX idx_status (status)
);

-- 子 Agent 任务关联表
CREATE TABLE agent_task_children (
    parent_task_id UUID REFERENCES agent_tasks(id),
    child_agent_name VARCHAR(50),
    child_trace_id VARCHAR(64),
    child_span_id VARCHAR(32),
    status VARCHAR(20),
    PRIMARY KEY (parent_task_id, child_agent_name)
);
```

**面试话术：**
> "多Agent追踪的核心是trace_id的传播方式。HTTP调用自动传播（OTel标准），消息队列需要手动注入traceparent到消息体。生产中我用过两种模式：同步HTTP用自动传播，异步MQ用手工传播（把traceparent放消息头）。每个任务在数据库存trace_id，调试时用Jaeger按trace_id查询，能看到OrchestratorAgent→SearchAgent→ExecutorAgent的完整时序。"

</details>

### Q13: 生产环境 Agent 成本超支告警：预算控制最佳实践
<details>
<summary>💡 答案要点</summary>

**Agent 成本构成：**

```
总成本 = Token成本 + API调用次数成本 + 计算资源成本

Token成本 = Σ(输入Token数 × 单价) + Σ(输出Token数 × 单价)
```

**预算控制四层架构：**

```
┌─────────────────────────────────────────────────────────┐
│              Agent 成本控制四层架构                       │
├─────────────────────────────────────────────────────────┤
│  Layer 1: 每日预算硬限制（最后防线）                      │
│  ├── 日预算 $200，超 $200 自动熔断                        │
│  ├── 按 Agent 拆分预算（Orchestrator: $80, Worker: $120）│
│  └── 余额不足时拒绝新任务，排队等待                       │
├─────────────────────────────────────────────────────────┤
│  Layer 2: 实时告警（提前发现问题）                        │
│  ├── 预计日成本 > 80% 阈值 → warning                     │
│  ├── 预计日成本 > 100% 阈值 → critical                    │
│  └── Token消耗速率异常（突增 > 3x）→ 立即告警             │
├─────────────────────────────────────────────────────────┤
│  Layer 3: 成本优化（主动降本）                            │
│  ├── 模型降级：GPT-4 → DeepSeek V4-Flash（简单任务）               │
│  ├── 缓存命中：相同问题直接返回（省 100%）                │
│  ├── 步数限制：> 10步强制结束（防死循环）                  │
│  └── Prompt压缩：LLMLingua 减少 30% token                │
├─────────────────────────────────────────────────────────┤
│  Layer 4: 成本归因（搞清楚钱花在哪）                      │
│  ├── 按 Agent 类型归因（SearchAgent 消耗最多）            │
│  ├── 按用户归因（Top 10 用户占 60% 成本）                │
│  └── 按任务类型归因（多跳问答比简单问答贵 5x）             │
└─────────────────────────────────────────────────────────┘
```

**实现代码：**

<details>
<summary>展开 Python 代码示例（75 行）</summary>

```python
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

class AgentBudgetController:
    def __init__(
        self,
        daily_budget_usd: float = 200.0,
        warning_threshold: float = 0.8
    ):
        self.daily_budget = daily_budget_usd
        self.warning_threshold = warning_threshold
        self.spent_today = 0.0
        self.agent_budgets = {
            "orchestrator": daily_budget_usd * 0.4,
            "search": daily_budget_usd * 0.3,
            "executor": daily_budget_usd * 0.3
        }
        self.alerted_agents = set()
    
    async def check_budget(self, agent_name: str, task_cost: float):
        """每次 Agent 调用前检查预算"""
        remaining = self.agent_budgets.get(agent_name, 0) - self.spent_today
        
        # Layer 1: 硬限制
        if self.spent_today + task_cost > self.daily_budget:
            raise BudgetExceededError(
                f"日预算已超，当前${self.spent_today:.2f}，剩余${self.daily_budget - self.spent_today:.2f}"
            )
        
        # Layer 2: 实时告警
        cost_rate = self.spent_today / (datetime.now().hour + 1)
        projected_daily = cost_rate * 24
        
        if projected_daily > self.daily_budget * self.warning_threshold:
            if agent_name not in self.alerted_agents:
                await self.send_alert(
                    agent_name=agent_name,
                    severity="warning",
                    message=f"预计日成本${projected_daily:.2f}，超过{self.warning_threshold*100}%阈值"
                )
                self.alerted_agents.add(agent_name)
    
    async def record_cost(
        self,
        agent_name: str,
        input_tokens: int,
        output_tokens: int,
        model: str
    ):
        """记录成本并更新预算"""
        cost = self.calculate_cost(input_tokens, output_tokens, model)
        self.spent_today += cost
        
        cost_gauge.labels(
            agent=agent_name,
            model=model,
            date=datetime.now().strftime("%Y-%m-%d")
        ).inc(cost)
    
    def calculate_cost(self, input_tok: int, output_tok: int, model: str) -> float:
        pricing = {
            "gpt-4o": (0.005, 0.015),
            "deepseek-v4-flash": (0.0005, 0.0015),
            "claude-3-opus": (0.015, 0.075)
        }
        in_price, out_price = pricing.get(model, (0.0, 0.0))
        return (input_tok / 1000 * in_price) + (output_tok / 1000 * out_price)
    
    async def send_alert(self, agent_name: str, severity: str, message: str):
        await pagerduty.create_incident(
            title=f"Agent成本告警: {agent_name}",
            severity=severity,
            body=message
        )
```

</details>

**成本归因 Dashboard：**

```yaml
# Grafana Panel: Agent成本归因
- title: 成本按Agent分布
  expr: |
    sum(increase(agent_cost_total{date="2026-05-15"}[1d])) by (agent_name)
  type: pie

- title: 成本按用户分布（Top 10）
  expr: |
    topk(10, sum(increase(agent_cost_total[1d])) by (user_id))
  type: table

- title: 成本按任务类型分布
  expr: |
    sum(increase(agent_cost_total[1d])) by (task_type)
    / sum(increase(agent_cost_total[1d])) * 100
  legend: "{{task_type}}: {{value}}%"
```

**面试话术：**
> "我的Agent成本控制用四层架构：①日预算硬限制，超$200熔断；②实时告警，预计超80%阈值就发warning；③成本优化，缓存+步数限制+模型降级；④成本归因，搞清楚钱花在哪。我曾在生产中遇到Token消耗突然增加3倍，排查发现是某个用户的查询没有缓存导致每次都走GPT-4，加了缓存后日成本从$180降到$95。成本监控和告警是Agent生产的生命线。"

</details>


### Q14: SLA 违约复盘模板：从告警到根因分析的完整流程
<details>
<summary>💡 答案要点</summary>

**SLA 违约场景分类：**

<details>
<summary>展开 Python 代码示例（31 行）</summary>

```python
# SLA 违约类型与响应级别
SLA_BREACH_TYPES = {
    "availability": {
        "sla": "99.9% 月可用率",
        "breach": "< 99.9%",
        "impact": "用户无法访问",
        "response_time": "15 分钟",
        "severity": "P1"
    },
    "latency_p99": {
        "sla": "P99 < 2s",
        "breach": ">= 2s",
        "impact": "用户体验下降",
        "response_time": "30 分钟",
        "severity": "P2"
    },
    "task_completion": {
        "sla": "任务完成率 > 95%",
        "breach": "< 95%",
        "impact": "业务指标下降",
        "response_time": "1 小时",
        "severity": "P2"
    },
    "cost_overrun": {
        "sla": "日成本 < $200",
        "breach": ">= $200",
        "impact": "财务损失",
        "response_time": "2 小时",
        "severity": "P3"
    }
}
```

</details>

**复盘模板（五步法）：**

<details>
<summary>展开 Markdown 代码示例（30 行）</summary>

```markdown
## SLA 违约复盘报告

### 1. 事件概述
- **时间**: 2026-05-14 14:30 - 15:15
- **持续**: 45 分钟
- **影响**: 3,420 用户受影响，任务完成率从 97% 降至 72%
- **SLA 类型**: P99 延迟超标（P99 = 4.8s > SLA 2s）
- **严重程度**: P1

### 2. 时间线（Timeline）
| 时间 | 事件 |
|------|------|
| 14:30 | 监控系统触发 P99 > 2s 告警 |
| 14:32 | SRE 收到 PagerDuty 告警 |
| 14:35 | 开始排查，发现向量检索延迟异常 |
| 14:42 | 确认 Milvus 服务 CPU 100% |
| 14:50 | 尝试扩容，Pod 无法调度（资源不足） |
| 15:00 | 触发降级预案，切换到本地缓存检索 |
| 15:10 | 服务恢复，P99 恢复到 1.5s |
| 15:15 | 解除告警，通知业务方 |

### 3. 根因分析（Root Cause）
**直接原因**: Milvus 索引碎片化导致查询性能下降

**根本原因**:
1. HNSW 索引没有设置 `maxSegments`，导致段数过多
2. 监控缺失：没有设置 segment count 告警
3. 扩容策略不当：HPA 设置的 maxReplicas 太小

**技术细节**:
```sql

</details>
-- 问题：segment 数量从 5 增长到 156
SELECT segment_name, num_segments, memory_usage 
FROM milvus.segments 
WHERE collection = "user_knowledge"
ORDER BY num_segments DESC;

-- 原因：连续写入 48 小时没有触发合并
```

### 4. 修复措施（Fixes）
| 措施 | 负责 | 状态 | 完成时间 |
|------|------|------|----------|
| 设置 `maxSegments=20` | @SRE-张工 | ✅ 已完成 | 2026-05-14 |
| 添加 segment count 监控 | @SRE-李工 | ✅ 已完成 | 2026-05-15 |
| 扩大 HPA maxReplicas 5→20 | @K8s-王工 | ✅ 已完成 | 2026-05-14 |
| 制定定时 segment 合并 cron | @SRE-张工 | 🔄 进行中 | 2026-05-16 |

### 5. 预防措施（Prevention）
```
┌─────────────────────────────────────────────────────────────┐
│  预防措施清单                                               │
├─────────────────────────────────────────────────────────────┤
│  ✅ 已添加：segment 数量监控（> 30 触发告警）                   │
│  ✅ 已添加：HNSW merge 操作 cron（每日凌晨 3 点）             │
│  ✅ 已添加：HPA maxReplicas 扩容到 20                         │
│  🔄 进行中：降级预案自动化（超时自动切换缓存）                 │
│  ⏳ 待完成：故障演练（每月一次）                              │
└─────────────────────────────────────────────────────────────┘
```

### 6. 影响评估
- **用户影响**: 3,420 用户 × 平均 5 分钟延迟 = 17,100 分钟
- **业务损失**: 约 120 次任务失败，估计影响收入 $2,400
- **已补偿**: 向受影响用户提供 VIP 会员 3 天

### 7. 责任人签收
- SRE Lead: _______________ 日期: _______________
- Engineering Manager: _______________ 日期: _______________

### 8. 下次审查时间
2026-05-21（1周后复查预防措施执行情况）
```

**复盘会议话术：**

```python
复盘话术模板 = """
1. 首先承认问题（不要甩锅）
   "这次 SLA 违约是我们的责任，我代表团队道歉。"
   
2. 明确影响范围（不要轻描淡写）
   "45 分钟内影响了 3,420 用户，有 120 个任务失败。"
   
3. 说明直接原因（技术细节要清晰）
   "Milvus HNSW 索引的 segment 数从 5 增长到 156，
   导致查询性能严重下降。"
   
4. 解释根本原因（不要只说表层原因）
   "根本原因是监控缺失——我们没有监控 segment 数量，
   也没有设置阈值告警，导致问题累积了 48 小时才爆发。"
   
5. 说明已采取的措施（展示行动）
   "我们已经：① 设置了 segment 数量上限；
   ② 添加了定时合并 cron；③ 扩容了 HPA maxReplicas。"
   
6. 承诺预防（展示闭环）
   "我们承诺：1 周内完成故障演练，
   确保同样的问题不会再发生。"
"""
```

**面试话术：**
> "我的复盘方法论是'五步法'：事件概述→时间线→根因→修复→预防。每次 SLA 违约后 24 小时内必须完成初步复盘，1 周内完成完整报告。关键原则：不要甩锅、不要轻描淡写、要找到根本原因（不是表层原因）。我最引以为豪的复盘是发现了一个看似'网络抖动'的问题，实际上是数据库连接池泄漏，修复后类似问题再也没出现过。"

</details>

### Q15: Agent 日志结构化设计：如何让日志可搜索、可分析？
<details>
<summary>💡 答案要点</summary>

**日志设计原则：**

```
传统日志：文本格式，难以搜索
结构化日志：JSON 格式，可查询、可分析、可告警

Agent 日志特殊要求：
① TraceID 关联（同一请求的所有日志）
② 步骤追踪（每个 Tool 调用是独立的 Span）
③ 上下文保存（中间状态的 Thought/Action/Observation）
④ 性能埋点（延迟、Token 消耗、成本）
```

**结构化日志 Schema：**

<details>
<summary>展开 Python 代码示例（77 行）</summary>

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

@dataclass
class AgentLogEntry:
    """Agent 结构化日志条目"""
    
    # 基础字段（必须）
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    level: str = "INFO"  # DEBUG/INFO/WARNING/ERROR
    trace_id: str = ""   # 跨请求唯一
    span_id: str = ""    # 当前步骤唯一
    
    # Agent 上下文
    agent_name: str = ""
    agent_version: str = ""
    task_id: str = ""
    session_id: str = ""
    
    # 步骤信息
    step_index: int = 0
    step_type: str = ""  # "thought"/"action"/"observation"/"result"
    
    # LLM 调用信息
    model: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: int = 0
    cost_usd: float = 0.0
    
    # Tool 调用信息
    tool_name: str = ""
    tool_args: Dict[str, Any] = field(default_factory=dict)
    tool_result: Any = None
    tool_error: Optional[str] = None
    
    # 业务信息
    user_id: str = ""
    intent: str = ""     # 用户意图分类
    success: bool = True
    error_message: Optional[str] = None
    
    # 可扩展字段
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_json(self) -> str:
        """序列化为 JSON"""
        return json.dumps(self.__dict__, ensure_ascii=False, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> "AgentLogEntry":
        """反序列化"""
        return cls(**json.loads(json_str))
    
    def to_otel_span(self) -> dict:
        """转换为 OpenTelemetry Span 格式"""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id if hasattr(self, "parent_span_id") else "",
            "operation_name": f"{self.agent_name}.{self.step_type}",
            "start_time": self.timestamp,
            "duration_ms": self.latency_ms,
            "tags": {
                "agent_name": self.agent_name,
                "step_index": self.step_index,
                "model": self.model,
                "tool_name": self.tool_name,
                "success": str(self.success),
            },
            "logs": [
                {"timestamp": self.timestamp, "fields": self.__dict__}
            ]
        }
```

</details>

**日志采集架构：**

<details>
<summary>展开 Python 代码示例（49 行）</summary>

```python
import logging
from opentelemetry import trace
from logging.handlers import RotatingFileHandler
import json

class AgentJSONFormatter(logging.Formatter):
    """JSON 格式日志 formatter"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": self._get_trace_id(),
            "span_id": self._get_span_id(),
            "agent_name": getattr(record, "agent_name", ""),
            "step_index": getattr(record, "step_index", 0),
            "model": getattr(record, "model", ""),
            "tool_name": getattr(record, "tool_name", ""),
            "success": getattr(record, "success", True),
        }
        
        # 添加额外字段
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        return json.dumps(log_data, ensure_ascii=False)
    
    def _get_trace_id(self) -> str:
        span = trace.get_current_span()
        if span:
            ctx = span.get_span_context()
            return format(ctx.trace_id, "032x") if ctx else ""
        return ""
    
    def _get_span_id(self) -> str:
        span = trace.get_current_span()
        if span:
            ctx = span.get_span_context()
            return format(ctx.span_id, "016x") if ctx else ""
        return ""

# 配置日志
logger = logging.getLogger("agent")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("/var/log/agent/app.log", maxBytes=100_000_000, backupCount=10)
handler.setFormatter(AgentJSONFormatter())
logger.addHandler(handler)
```

</details>

**日志查询示例（Elasticsearch）：**

<details>
<summary>展开 Python 代码示例（74 行）</summary>

```python
# 查询某个 TraceID 的所有日志
QUERY_TRACE = """
{
  "query": {
    "bool": {
      "must": [
        {"match": {"trace_id": "abc123def456"}}
      ]
    }
  },
  "sort": [{"timestamp": "asc"}],
  "size": 1000
}
"""

# 查询所有失败的 Tool 调用
QUERY_FAILED_TOOLS = """
{
  "query": {
    "bool": {
      "must": [
        {"match": {"level": "ERROR"}},
        {"match": {"tool_name": "search_database"}},
        {"range": {"timestamp": {"gte": "now-1h"}}}
      ]
    }
  }
}
"""

# 查询 Token 消耗异常（> 10K）
QUERY_HIGH_TOKEN = """
{
  "query": {
    "bool": {
      "must": [
        {"range": {"total_tokens": {"gt": 10000}}},
        {"range": {"timestamp": {"gte": "now-1d"}}}
      ]
    }
  },
  "aggs": {
    "by_agent": {
      "terms": {"field": "agent_name"},
      "aggs": {
        "avg_tokens": {"avg": {"field": "total_tokens"}},
        "max_tokens": {"max": {"field": "total_tokens"}},
        "p95_tokens": {"percentiles": {"field": "total_tokens", "percents": [95]}}
      }
    }
  }
}
"""

# 统计每小时的错误率
QUERY_ERROR_RATE = """
{
  "query": {
    "bool": {
      "must": [
        {"match": {"level": "ERROR"}},
        {"range": {"timestamp": {"gte": "now-24h"}}}
      ]
    }
  },
  "aggs": {
    "hourly_errors": {
      "date_histogram": {
        "field": "timestamp",
        "interval": "hour"
      }
    }
  }
}
```

</details>

**日志告警规则：**

<details>
<summary>展开 Yaml 代码示例（34 行）</summary>

```yaml
# Prometheus Alert 规则（基于日志 metrics）
groups:
  - name: agent-log-alerts
    rules:
      # 高错误率告警
      - alert: AgentHighErrorRate
        expr: |
          sum(rate(agent_log_errors_total[5m])) by (agent_name)
          / sum(rate(agent_log_total[5m])) by (agent_name) > 0.05
        for: 5m
        annotations:
          summary: "Agent {{ $labels.agent_name }} 错误率超过 5%"
          description: "最近 5 分钟错误率 {{ $value }}"

      # Tool 调用超时告警
      - alert: AgentToolTimeout
        expr: |
          histogram_quantile(0.99, 
            rate(agent_tool_latency_seconds_bucket[5m])
          ) > 10
        for: 3m
        annotations:
          summary: "Tool 调用 P99 延迟超过 10 秒"

      # Token 消耗异常告警
      - alert: AgentHighTokenConsumption
        expr: |
          sum(rate(agent_token_total[1h])) by (agent_name)
          > 1.5 * avg_over_time(
              sum(rate(agent_token_total[1h])) by (agent_name)[7d:1h]
            )
        for: 15m
        annotations:
          summary: "Agent {{ $labels.agent_name }} Token 消耗异常"
```

</details>

**面试话术：**
> "我的 Agent 日志设计核心是'结构化 + 可追溯'。每个日志条目包含 trace_id、span_id、step_index、model、tool_name，每次 LLM 调用都记录 token 消耗和延迟。这样做的好处是：① 查问题快——输入 trace_id 就能看到整个请求链路；② 分析容易——用 Elasticsearch 按 agent_name、tool_name、success 聚合；③ 告警准——错误率/延迟超过阈值自动通知。生产环境我每天查日志 < 10 次，但每次都能 5 分钟内定位问题。"

</details>
