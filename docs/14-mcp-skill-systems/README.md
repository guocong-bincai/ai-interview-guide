# 🔥 MCP & Skill 系统面试题

> **难度：** ⭐⭐⭐⭐⭐
> > **更新：** 2026-04-04
> **考点：** MCP 协议、Skill 系统设计、工具标准化、Agent 互操作性

## 📋 目录

1. [MCP 基础概念](#一-mcp 基础概念)
2. [Skill 系统设计](#二-skill 系统设计)
3. [工程实践题](#三工程实践题)
4. [架构设计题](#四架构设计题)
5. [速记卡片](#五速记卡片)

## 一、MCP 基础概念

### Q1: 什么是 MCP（Model Context Protocol）？解决什么问题？

**MCP = Model Context Protocol（模型上下文协议）**

**定义：** 一个开放协议，标准化 AI 模型与外部数据源、工具、服务的连接方式。

**本质：** AI 时代的 USB-C 协议

**解决的问题：**
| 问题 | 传统方案 | MCP 方案 |
|------|----------|----------|
| 协议不统一 | 每个工具自定义 API | 统一协议，一次接入 |
| 发现困难 | 手动配置工具 | 自动发现可用资源 |
| 权限混乱 | 硬编码认证信息 | 标准化权限管理 |
| 互操作性差 | 工具之间无法协作 | 标准化接口，可组合 |

**核心架构：**
```
AI 应用 (MCP Client) ←→ 协议适配层 (MCP Server) ←→ 数据源/工具
```

**面试话术：**
> "MCP 的本质是 AI 时代的 USB-C 协议。我在项目中用 MCP 接入了 10+ 数据源，开发效率提升了 3 倍。"

### Q2: MCP 的三种核心资源类型？

| 类型 | 英文 | 说明 | 示例 |
|------|------|------|------|
| **提示词** | Prompts | 预定义的 Prompt 模板 | "分析这份财报" |
| **资源** | Resources | 可读取的数据源（只读） | 数据库、文件、API |
| **工具** | Tools | 可执行的操作（读写） | 搜索、计算、CRUD |

**面试话术：**
> "MCP 把 AI 能力抽象成三类：Prompts 是预设指令，Resources 是只读数据，Tools 是可执行操作。"

### Q3: MCP Server 和 MCP Client 的职责？

| 角色 | 职责 | 示例 |
|------|------|------|
| **MCP Server** | 暴露能力（资源/工具/提示词） | 数据库服务、搜索服务 |
| **MCP Client** | 发现并调用能力 | AI 应用、Agent 框架 |

## 二、Skill 系统设计

### Q4: Skill 系统和 Function Calling 有什么区别？

| 维度 | Function Calling | Skill 系统 |
|------|------------------|------------|
| 粒度 | 单个函数 | 能力模块 |
| 发现 | 手动注册 | 自动发现 |
| 组合 | 不支持 | 支持链式调用 |
| 复用 | 代码级 | 跨 Agent |

**面试话术：**
> "Function Calling 是单次调用，Skill 系统是可组合的能力生态。我设计了 Skill 链，一个'数据分析'Skill 内部可以组合三个子 Skill。"

### Q5: 如何设计支持动态加载的 Skill 系统？

**推荐方案：** Wasm 沙箱（安全 + 轻量）

**核心架构：**
```
Skill Registry（注册中心）→ Skill Manager（编排）→ Skill Runner（执行）
```

### Q6: Skill 之间的依赖和冲突怎么处理？

**策略：** 版本隔离、命名空间、依赖解析（拓扑排序）、沙箱隔离

## 三、工程实践题

### Q7: 如何保证 Skill 执行的安全性？

**三层防护体系：**
```
接入层 → 执行层 → 数据层 → 监控层
  ↓         ↓         ↓         ↓
鉴权     沙箱     权限     审计
限流     配额     脱敏     告警
```

**面试话术：**
> "安全是 Skill 系统的底线。我用了三层防护：接入层鉴权限流、执行层 Wasm 沙箱隔离、数据层权限过滤。"

### Q8: 如何设计 Skill 的监控和可观测性？

**核心指标：** 调用量、延迟 (P99)、错误率、资源消耗、成功率

**实现：** OpenTelemetry 全链路追踪

### Q9: Skill 版本升级怎么做？（灰度发布、回滚）

**灰度流程：** 10% → 30% → 50% → 100%

**自动回滚：** error_rate > 10% 或 latency_p99 > 10s 时触发

## 四、架构设计题

### Q10: 设计企业级 Skill 平台（100+ Skill，1000+ 并发）

**三层架构：**
```
API Gateway（鉴权/限流）
       ↓
┌──────┴──────┬────────────┐
│注册中心     │编排调度    │监控
└──────┬──────┴────────────┘
       ↓
Skill 执行集群（K8s + Docker）
```

### Q11: MCP 和 Skill 系统怎么结合？

**融合架构：** AI Agent ← MCP Client ← MCP Server(Skill 封装)

**面试话术：**
> "MCP 是协议层，Skill 是能力层。我用 MCP 封装 Skill，实现跨项目复用。"

---

## 四、OpenClaw框架 (2024热点⭐)

### Q12: 什么是OpenClaw?与LangChain有什么区别?

<details>
<summary>💡 答案要点</summary>

**OpenClaw = AI Agent操作系统(Agent OS)**

### 核心定位对比

| 维度 | LangChain | OpenClaw |
|------|-----------|----------|
| **定位** | LLM应用框架 | Agent操作系统 |
| **核心能力** | 链式调用、RAG | 会话管理、任务编排 |
| **工具理念** | 丰富生态,SaaS集成 | 轻量级本地工具(4个原子) |
| **部署** | 云端/本地均可 | 本地优先,零API依赖 |
| **记忆系统** | 外挂向量库 | 内置记忆+文件系统 |
| **适用场景** | 快速原型,云端服务 | 长期助手,本地自动化 |

### OpenClaw核心特性

**1. 轻量级工具调用(4个原子操作)**
```bash
# OpenClaw只提供4个核心工具,组合完成复杂任务
read <file>    # 读文件
write <file>   # 写文件
edit <file>    # 编辑文件
bash <cmd>     # 执行Shell命令

# 示例:下载网页并提取标题
bash "curl https://example.com > page.html"
title=$(bash "grep -oP '<title>.*?</title>' page.html")
write "output.txt" "$title"

# 优势:零外部依赖,离线可用,适配Unix环境
```

**2. 记忆系统(混合检索)**
```typescript
// 三层记忆
shortTerm: []         // 最近10轮对话
longTerm: VectorDB    // Embedding检索历史
filesystem: "/memory" // 持久化存储

// 智能检索
recall(query) {
  semantic = vectorDB.search(embed(query))  // 语义
  recent = shortTerm.filter(time < 1hour)   // 时间
  files = bash("grep -r '${query}' /memory") // 关键词
  return merge(semantic, recent, files)
}
```

**3. 心跳机制(自主进化)**
```typescript
// 每小时自动触发
setInterval(() => {
  // 1. 回顾行为日志
  logs = read("/logs/today.log")

  // 2. 发现模式
  patterns = LLM.analyze("发现重复任务", logs)

  // 3. 生成自动化脚本
  for (pattern in patterns) {
    script = LLM.generateScript(pattern)
    bash("chmod +x ${script}")
    skills.add(pattern.name, script)
  }

  // Agent越用越聪明
}, 3600_000)
```

### 适用场景

| 场景 | 推荐 | 原因 |
|------|------|------|
| 快速原型 | LangChain | 丰富组件 |
| 云端服务 | LangChain | SaaS集成 |
| 本地助手 | OpenClaw⭐ | 零依赖,隐私 |
| 长期陪伴 | OpenClaw⭐ | 记忆进化 |
| 办公自动化 | OpenClaw⭐ | 直接操作文件 |

**面试话术:**
> "OpenClaw定位Agent OS,提供4个原子工具(read/write/edit/bash),零外部依赖。我用它做知识库助手,通过心跳机制每天自动整理笔记,3个月后检索提速5倍。LangChain适合快速原型,OpenClaw适合长期陪伴。"

</details>

---

### Q13: OpenClaw的沙箱技术如何实现?

<details>
<summary>💡 答案要点</summary>

**需求:** Agent可执行bash,如写出`rm -rf /`会删系统,必须隔离。

### 沙箱方案对比

| 方案 | 隔离 | 性能 | 复杂度 |
|------|------|------|--------|
| Docker | 强 | 中 | 中 ⭐推荐 |
| 虚拟机 | 最强 | 差 | 高 |
| chroot | 弱 | 高 | 低 |
| WASM | 强 | 高 | 低 |

### Docker沙箱实现

```typescript
class SandboxRunner {
  async execute(agentId, command) {
    // 创建专属容器
    const container = await docker.create({
      Image: "alpine",
      HostConfig: {
        ReadonlyRootfs: true,  // 只读根
        Memory: "512m",         // 限内存
        NanoCpus: 500_000_000,  // 0.5核
        NetworkMode: "none"     // 禁网络
      },
      Binds: [`/work/${agentId}:/workspace:rw`]
    })

    // 执行命令
    const result = await container.exec(command, {
      timeout: 30000  // 30秒超时
    })

    return result
  }
}
```

### 三层防护

**Layer 1: 命令白名单**
```typescript
ALLOWED = ["ls", "cat", "grep", "python", "node"]
BANNED = ["rm", "chmod", "sudo", "curl", "wget"]

if (BANNED.includes(cmd)) {
  throw Error("禁止危险命令")
}
```

**Layer 2: 参数过滤**
```typescript
// 移除危险参数
cmd = cmd.replace(/-rf/g, "")
         .replace(/>/g, "")   // 重定向
         .replace(/\|/g, "")  // 管道
         .replace(/;/g, "")   // 多命令
```

**Layer 3: 文件访问控制**
```typescript
function checkPath(path) {
  if (path.startsWith("/etc") ||
      path.startsWith("/usr")) {
    throw Error("禁止访问系统目录")
  }
}
```

### 性能优化:容器池

```typescript
// 预热5个容器
const pool = await Promise.all(
  Array(5).fill(0).map(() => createContainer())
)

// 复用容器
const container = pool.pop()  // 100ms取出
await container.exec(command)
await container.exec("rm -rf /workspace/*")  // 清理
pool.push(container)  // 归还

// Before: 3秒创建 + 2秒销毁 = 5秒
// After: 100ms取出 + 50ms清理 = 150ms
```

**面试话术:**
> "OpenClaw用Docker容器沙箱,每个Agent独立容器,限CPU/内存/网络。三层防护:命令白名单+参数过滤+路径检查。为了性能,容器池预热5个,复用只需100ms。Agent写`rm -rf /`也只删容器,宿主安全。"

</details>

---

## 五、速记卡片

### MCP 核心概念
| 概念 | 一句话解释 |
|------|------------|
| **MCP** | AI 时代的 USB-C 协议 |
| **MCP Server** | 能力提供者 |
| **MCP Client** | 能力消费者 |
| **Prompts** | 预定义 Prompt 模板 |
| **Resources** | 可读取数据源 |
| **Tools** | 可执行操作 |

### Skill 核心概念
| 概念 | 一句话解释 |
|------|------------|
| **Skill** | 可组合的能力模块 |
| **动态加载** | 新增 Skill 不重启 |
| **沙箱隔离** | Wasm/Docker 防恶意代码 |

### OpenClaw核心概念
| 概念 | 一句话解释 |
|------|------------|
| **OpenClaw** | AI Agent操作系统,TypeScript开发 |
| **4原子工具** | read/write/edit/bash,零外部依赖 |
| **记忆系统** | 短期+长期+文件系统,混合检索 |
| **心跳机制** | 每小时自省,发现模式,自动化脚本 |
| **沙箱隔离** | Docker容器+3层防护+容器池复用 |
| **vs LangChain** | 本地优先 vs 云端优先,Agent OS vs LLM框架 |

## 📝 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-03-05 | 新增 OpenClaw 框架面试题 2 道 |
| 2026-03-03 | 新增 MCP & Skill 系统面试题 11 道 |


---

**上一模块：** [多智能体系统](../13-multi-agent-systems/)
**下一模块：** [高级专题](../15-advanced-topics/)

---

## 14. MCP UI Framework（2026年1月重大更新）

<details>
<summary>💡 答案要点</summary>

### 什么是 MCP UI Framework？

**MCP UI Framework = MCP协议在2026年1月26日的重大扩展**

**背景：**
- 此前 MCP 纯粹是功能性的：AI 盲目读取数据或执行代码
- 新扩展后：MCP 服务器可以在聊天窗口内直接提供**交互式图形界面**

**核心创新：**
```
传统MCP：
用户 → "帮我查天气" → AI调用工具 → 纯文本回复

MCP UI Framework：
用户 → "帮我查天气" → AI调用工具 → MCP服务器 →
  → 在聊天窗口渲染【交互式天气卡片组件】
  → 用户可以直接在聊天界面点击/滑动/选择
```

### MCP UI Framework vs 传统 Function Calling

| 维度 | 传统Function Calling | MCP UI Framework |
|------|---------------------|-------------------|
| **交互方式** | 纯文本往返 | 聊天窗口内嵌图形UI |
| **状态管理** | 每次调用独立 | 有状态的交互式组件 |
| **用户体验** | 割裂感强 | 流畅一体化 |
| **适用场景** | API调用、数据查询 | 表单填写、图表交互、多步向导 |

### MCP UI Framework 工作原理

```python
# MCP Server返回带UI组件的响应
class MCPWeatherServer:
    @mcp.tool()
    def get_weather(city: str) -> MCPResponse:
        weather_data = fetch_weather(city)

        # 传统方式：返回纯文本
        # return f"北京今天晴，26度"

        # MCP UI Framework方式：返回交互式UI组件
        return MCPResponse(
            components=[
                WeatherCard(
                    city=city,
                    temperature=weather_data.temp,
                    condition=weather_data.condition,
                    interactive=True,  # 用户可点击
                    actions=[
                        Button("查看详情", action="show_details"),
                        Button("切换城市", action="change_city")
                    ]
                )
            ]
        )
```

### 支持的 UI 组件类型

| 组件类型 | 示例 | 使用场景 |
|----------|------|----------|
| **卡片组件** | 天气卡片、产品卡片 | 信息展示 + 快捷操作 |
| **表单组件** | 输入框、下拉框、日期选择 | 多步数据收集 |
| **图表组件** | 折线图、饼图、柱状图 | 数据可视化 |
| **列表组件** | 可展开列表、网格视图 | 内容浏览 |
| **分步向导** | Stepper、Wizard | 引导式任务 |

### 面试话术

> "MCP UI Framework 是2026年1月MCP协议的重大升级。核心改变是：从纯文本工具调用，进化到可以在聊天窗口内渲染交互式图形组件。这让AI应用的用户体验接近原生App，同时保持MCP的统一协议优势。我预测这会成为2026年面试的热点，因为它涉及'如何设计有状态的工具调用'这个新命题。"

</details>

## 15. Claude Skills vs MCP vs Function Calling（2026年选型对比）

<details>
<summary>💡 答案要点</summary>

### 三角关系的本质

```
┌─────────────────────────────────────────────────────────┐
│           Agent 时代的工具生态三角                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│              Function Calling                            │
│           (LLM内置的原始能力)                              │
│                  ↓                                       │
│      ┌───────────────────────┐                          │
│      │       MCP协议          │ ← 标准化层（USB-C）      │
│      │  (Anthropic 2024.11)  │                          │
│      └───────────────────────┘                          │
│                  ↓                                       │
│      ┌───────────────────────┐                          │
│      │     Agent Skills       │ ← 能力封装层（文件夹）    │
│      │   (Anthropic 2025)    │                          │
│      └───────────────────────┘                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 三者详细对比

| 维度 | Function Calling | MCP | Agent Skills |
|------|-----------------|-----|--------------|
| **本质** | LLM内置的JSON Schema能力 | 标准化工具/数据连接协议 | 能力封装+记忆+工作流 |
| **粒度** | 单个函数 | 服务（多个工具集合） | 完整技能模块 |
| **状态管理** | 无状态 | 无状态 | 有状态（带记忆） |
| **发现机制** | 手动注册 | 自动发现 | 按需加载 |
| **标准化** | 无 | 统一协议 | 无标准，各自实现 |
| **生态** | 依赖模型厂商 | 快速成长的开放生态 | Anthropic专属生态 |

### Claude Skills 的核心优势

**Skills = 工具集 + 指令模板 + 工作记忆**

```python
# Claude Skills的组成
class Skill:
    def __init__(self):
        self.name = "数据分析Skill"
        self.instructions = """  # 专家级指令模板
            你是一名资深数据分析师，擅长...
        """
        self.tools = [query_db, visualize, export]  # 绑定工具集
        self.memory = VectorStore()  # 领域知识记忆
        self.context_window = 128000  # 扩展上下文

# Skills的优势
# 1. 开箱即用（Claude官方维护）
# 2. 自动加载相关Skills
# 3. Skills之间可组合
# 4. 带领域专家级Prompt
```

### 什么时候选哪个？

```python
def select_tool_layer():
    """选型决策树"""

    # 场景1：需要调用外部API/数据库
    if need_external_integration:
        return "MCP"  # 统一协议，一次接入多处复用

    # 场景2：需要构建Claude专用Agent
    elif building_claude_agent:
        return "Claude Skills"  # 官方优化，即插即用

    # 场景3：简单的一次性工具调用
    elif simple_function_call:
        return "Function Calling"  # 原生支持，无需额外配置

    # 场景4：企业级多Agent平台
    else:
        return "MCP + Skills"  # MCP做协议层，Skills做能力封装
```

### 面试话术

> "2026年的工具生态已经形成三角格局：Function Calling是地基（LLM内置），MCP是中间层（协议标准化），Skills是最顶层（能力封装）。我的理解是：Function Calling解决'能不能调用'，MCP解决'怎么统一调用'，Skills解决'如何优雅地调用'。在企业内部，我们用MCP做数据源集成，用Skills做Agent能力构建，分层清晰，扩展性强。"

</details>

---

## 16. MCP 2026 Roadmap：企业就绪与协议演进（2026年4月最新）

<details>
<summary>💡 答案要点</summary>

### MCP 2026四大优先方向

**MCP在2024年11月发布，2025年成为AI工具集成的事实标准，2026年进入企业级深水区。**

**2026年MCP四大优先方向：**

| 优先方向 | 核心内容 | 为什么重要 |
|----------|----------|------------|
| **Transport Evolution** | Streamable HTTP水平扩展、无状态会话 | 企业大规模部署的瓶颈 |
| **Agent Communication** | Tasks primitive生命周期完善、重试语义 | 多Agent协作的基础 |
| **Governance Maturation** | SEP提案流程、贡献者梯队、WG委托审查 | 协议健康发展的保障 |
| **Enterprise Readiness** | 审计日志、SSO鉴权、网关行为、配置迁移 | 大规模落地的最后一公里 |

### Transport Evolution：无状态化与水平扩展

**当前问题：**
- Streamable HTTP让MCP服务器可以远程运行
- 但有状态会话与负载均衡器冲突
- 水平扩展需要临时方案

**解决方案：**
```python
# 无状态会话设计
class MCPGateway:
    def handle_request(self, request, session_id):
        # 会话状态外置到Redis，不再保存在服务端
        session_state = redis.get(f"mcp:session:{session_id}")

        # 每个请求都是独立的，支持水平扩展
        response = mcp_server.process(request, session_state)

        # 状态写回
        redis.setex(f"mcp:session:{session_id}", 3600, response.next_state)

        return response
```

**标准化发现机制：**
```
# .well-known/mcp.json（元数据格式）
{
    "name": "企业数据库MCP",
    "version": "1.0",
    "capabilities": ["sql:query", "schema:read"],
    "auth": "oauth2",
    "docs": "https://..."
}

→ 无需连接即可知道服务器能力
→ 支持注册中心和爬虫发现
```

### Agent Communication：Tasks原语的完善

**Tasks primitive（SEP-1686）** 已经作为实验特性发布，解决了基础的Agent间任务传递问题。

**2026年待完善的生命周期问题：**

| 问题 | 当前状态 | 2026年计划 |
|------|----------|------------|
| **重试语义** | 无标准 | 任务失败时自动重试次数、间隔 |
| **结果保留期** | 无标准 | 任务完成后结果保留多久 |
| **超时策略** | 无标准 | 任务超时如何处理 |
| **优先级** | 无标准 | 任务优先级如何调度 |

```python
# 未来的标准化任务定义
task = {
    "id": "task-123",
    "priority": "high",
    "retry": {"max_attempts": 3, "backoff": "exponential"},
    "ttl": 3600,  # 完成后保留1小时
    "timeout": 300  # 超时5分钟
}
```

### Governance：SEP提案优先级机制

**2026年新规则：与四大优先方向一致的SEP优先审查。**

```
SEP 优先级梯队：

第一梯队（快速通道）：
- Transport Evolution相关
- Agent Communication相关
- Enterprise Readiness相关
- Governance Maturation相关

第二梯队（标准审查）：
- 与上述四个方向无关的SEP
- 需要更长审查时间
- 需要更高论证门槛
```


### Enterprise Readiness：企业就绪的具体挑战

**企业部署MCP的四类实际问题：**

| 问题类型 | 具体挑战 | 解决方案方向 |
|----------|----------|------------|
| **审计日志** | 需要记录每个MCP调用 | 结构化日志+SIEM集成 |
| **SSO鉴权** | MCP服务器需要对接企业IdP | OAuth2/SAML标准 |
| **网关行为** | 企业需要在MCP请求前加鉴权层 | MCP Gateway标准化 |
| **配置迁移** | 不同环境的MCP配置如何同步 | 配置即代码+版本控制 |

**重要说明：**
> 企业级需求大多数会作为"扩展（extensions）"而非"核心协议变更"来实现。这样保证核心协议不因为企业需求而变得臃肿。

### 面试话术

> "MCP 2026 roadmap的核心是'从实验到生产'。Transport Evolution解决水平扩展问题，Agent Communication让多Agent协作更可靠，Enterprise Readiness解决审计/SSO/网关这些企业最后一公里问题。面试时能说出SEP优先级机制和四大优先方向，说明你对MCP不只是会用，而是关注它的演进方向，这对架构师岗位很重要。"

</details>

---

[返回目录 →](../../README.md)
