# 🔥 MCP & Skill 系统面试题

> **难度：** ⭐⭐⭐⭐⭐
> **更新：** 2026-03-03
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

[返回目录 →](../../README.md)
