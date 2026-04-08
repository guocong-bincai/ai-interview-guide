# 🔥 Agent 可观测性与生产监控面试题

> **难度：** ⭐⭐⭐⭐
> **更新：** 2026-04-09
> **考点：** LangSmith、Arize Phoenix、OpenTelemetry、Prometheus、可观测性架构、指标设计、成本监控

---

## 一、为什么 Agent 可观测性是 2026 年必考题？

2026年，Agent 应用从"能跑通"升级到"能运维"。面试中 **15-20% 的问题围绕生产可观测性展开**，考察维度包括：

- **正确性监控**：任务成功率、幻觉率、工具调用准确率
- **性能监控**：TTFT、端到端延迟、Token 消耗
- **成本监控**：每次任务成本、ROI 分析
- **安全监控**：Prompt 注入、越狱攻击、数据泄露

> "光会搭 LangChain Demo 已经完全不够用了。面试官最想听的是：线上遇到过什么问题，怎么权衡解决的。" —— 2026 面经总结

---

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

**面试话术：**

> "Agent 可观测性核心是 trace_id 串联。我设计时用 OpenTelemetry 的 span 嵌套结构：最外层是 agent_run，内层分 planning 和各个 step，每个 step 里记录 tool_call。每个 span 都打上 user_id、model、token_count 属性。出问题后用 trace_id 在 LangSmith 或 Jaeger 里一键拉出完整链路，哪个 step 耗时最长、哪个工具失败了，一目了然。"

---

### Q2: 如何用 LangSmith 做 Agent 调试？有哪些高级用法？

**LangSmith 核心功能：**

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

### Q3: 如何监控 Agent 的 Token 消耗和成本？有哪些优化策略？

**成本监控架构：**

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

**成本优化策略：**

| 策略 | 节省比例 | 实现方式 |
|------|----------|----------|
| **语义缓存** | 30-50% | Embedding 相似度 > 0.95 直接返回缓存 |
| **模型路由** | 30-40% | 简单任务用 GPT-3.5，复杂用 GPT-4 |
| **上下文压缩** | 40-90% | LLMLingua / Recomp 压缩历史 |
| **Token 配额** | 动态 | 按用户 tier 设置每日上限 |

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

**面试话术：**

> "成本控制是 2026 年面试高频追问。我的思路是三层控制：1）语义缓存，同一问题第二次问直接返回缓存，命中率达 40%；2）模型路由，简单查询路由到 GPT-3.5，复杂推理才用 GPT-4，节省 30%；3）上下文压缩，对话超过 20 轮自动触发 LLMLingua 压缩历史。三个叠加，单任务成本从 $0.12 降到 $0.04，效果量化后给面试官看。"

---

### Q4: 如何检测 Agent 的行为异常？循环、幻觉、死循环如何发现？

**异常检测架构：**

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
@track_cost(model="gpt-4", ...)
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

**面试话术：**

> "Agent 异常检测我分三层：1）循环检测，用状态 hash 记录历史，3次相同状态触发熔断；2）上下文膨胀检测，超 80% 窗口自动压缩；3）幻觉风险检测，用 NLI 模型对每步输出做 Entailment 打分，超过 0.5 就告警。生产环境加上 Prometheus 告警规则：连续 5 个任务失败率 > 10% 自动发 PagerDuty。"

---

### Q5: 如何用 Arize Phoenix 做开源可观测性？和 LangSmith 有什么区别？

**Arize Phoenix 核心用法：**

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

### Q6: 如何设计 Agent 的 SLA 和告警规则？有哪些关键阈值？

**SLA 设计：**

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

### Q7: 如何做 Agent 的 A/B 测试？有哪些评估指标？

**Agent A/B 测试架构：**

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

## 五、面试话术模板

### 被问到"如何监控 Agent 质量"的标准回答：

> "我会从三个层面建立 Agent 监控体系：
> **第一层：任务级指标**——用 trace_id 串联每个任务的全链路，记录成功率、P99 延迟、Token 消耗。工具调用用拦截器自动埋点，失败率 > 5% 触发告警。
> **第二层：模型级指标**——监控 TTFT（首 Token 时间 < 1s）、幻觉风险分数（用 NLI Entailment 模型，> 0.5 告警）、循环检测（3次相同状态自动熔断）。
> **第三层：成本指标**——语义缓存命中率、模型路由比例、日/周/月成本趋势。超预算 80% 触发升级告警。
> 工具链：LangSmith 做链路追踪 + Prometheus 做指标聚合 + Grafana 做可视化 + PagerDuty 做告警。这套体系让我负责的 Agent 服务 SLA 稳定在 99.2%。"

---

*版本: v1.0 | 更新: 2026-04-09 | by 二狗子 🐕*
