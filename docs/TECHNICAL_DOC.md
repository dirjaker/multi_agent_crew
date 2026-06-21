# Multi-Agent Crew 协作系统 - 技术文档

## 1. 项目概述

Multi-Agent Crew 是一个多智能体协作框架，支持多个 AI Agent 组成团队，按不同模式协作完成复杂任务。

### 1.1 核心特性

- **多种协作模式**：顺序执行、并行执行、层级管理
- **灵活的 Agent 定义**：角色、目标、背景故事、工具
- **任务依赖管理**：DAG 结构的任务间依赖关系
- **记忆系统**：短期记忆 + 长期记忆
- **工具系统**：可扩展的工具注册机制，含安全沙箱
- **Web API**：FastAPI REST 接口
- **桌面 GUI**：tkinter macOS 应用

### 1.2 应用场景

- 研究报告生成团队
- 内容创作协作
- 软件开发团队模拟
- 复杂问题分解与求解

## 2. 架构设计

### 2.1 核心组件

```
┌─────────────────────────────────────────┐
│                 Crew                     │
│  ┌───────────────────────────────────┐  │
│  │           Agent Manager           │  │
│  │  ┌─────────┐  ┌─────────┐        │  │
│  │  │ Agent 1 │  │ Agent 2 │  ...   │  │
│  │  └─────────┘  └─────────┘        │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │          Task Scheduler           │  │
│  │  ┌─────────┐  ┌─────────┐        │  │
│  │  │ Task 1  │  │ Task 2  │  ...   │  │
│  │  └─────────┘  └─────────┘        │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │         Tool Registry             │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 2.2 执行流程

#### Sequential 模式
```
Agent1(Task1) → Output1 → Agent2(Task2) → Output2 → Agent3(Task3) → Final
```

#### Parallel 模式
```
Agent1(Task1) ─┐
Agent2(Task2) ─┼→ Aggregate → Final
Agent3(Task3) ─┘
```

#### Hierarchical 模式
```
Manager
├── Assign Task1 → Worker1 → Result1
├── Assign Task2 → Worker2 → Result2
└── Assign Task3 → Worker3 → Result3
    ↓
Manager: Aggregate → Final
```

## 3. 模块详解

### 3.1 Agent 模块 (`agent.py`)

#### 核心类

**Agent 类**
```python
@dataclass
class Agent:
    id: str                    # 唯一标识符
    role: str                  # 角色名称
    goal: str                  # 目标
    backstory: str             # 背景故事
    tools: List[Tool]          # 工具列表
    memory: AgentMemory        # 记忆系统
    state: AgentState          # 当前状态
    max_iter: int = 5          # 最大迭代次数
```

**AgentMemory 类**
```python
@dataclass
class AgentMemory:
    short_term: List[Dict]     # 短期记忆（当前任务）
    long_term: List[Dict]      # 长期记忆（历史经验）
    max_short_term: int = 10   # 短期记忆容量
```

#### 关键方法

- `get_system_prompt()`: 生成系统提示词
- `think(context)`: 思考过程
- `act(task)`: 执行任务（ReAct 模式）
- `use_tool(tool_name, **kwargs)`: 使用工具

### 3.2 Task 模块 (`task.py`)

#### 核心类

**Task 类**
```python
@dataclass
class Task:
    id: str                     # 任务 ID
    description: str            # 任务描述
    expected_output: str        # 期望输出
    agent: Agent                # 执行 Agent
    priority: TaskPriority      # 优先级
    dependencies: List[str]     # 依赖任务 ID
    status: TaskStatus          # 当前状态
    result: TaskResult          # 执行结果
```

**TaskResult 类**
```python
@dataclass
class TaskResult:
    task_id: str
    status: TaskStatus
    output: Any
    error: Optional[str]
    duration: float
```

### 3.3 Crew 模块 (`crew.py`)

#### 核心类

**Crew 类**
```python
@dataclass
class Crew:
    name: str                   # 团队名称
    agents: List[Agent]         # Agent 列表
    tasks: List[Task]           # 任务列表
    process: ProcessType        # 执行模式
    max_workers: int = 4        # 并行数
```

#### 关键方法

- `kickoff()`: 开始执行任务
- `_execute_sequential()`: 顺序执行
- `_execute_parallel()`: 并行执行
- `_execute_hierarchical()`: 层级执行

### 3.4 Tools 模块 (`tools.py`)

内置工具：
- `SearchTool`: 搜索工具
- `AnalysisTool`: 分析工具
- `WritingTool`: 写作工具
- `CodeTool`: 代码工具
- `CalculatorTool`: 计算工具（含安全沙箱）

安全沙箱函数：
- `safe_eval()`: 安全的表达式求值
- `safe_exec()`: 安全的代码执行

### 3.5 Web API (`src/web/app.py`)

基于 FastAPI 的 REST API：

| 端点 | 方法 | 功能 |
|------|------|------|
| `/` | GET | Web 前端页面 |
| `/api/health` | GET | 健康检查 |
| `/api/agents` | POST/GET | 创建/列出 Agent |
| `/api/tasks` | POST/GET | 创建/列出任务 |
| `/api/crews` | POST/GET | 创建/列出 Crew |
| `/api/crews/run` | POST | 执行 Crew |
| `/api/stats` | GET | 系统统计 |
| `/api/reset` | DELETE | 重置数据 |

### 3.6 桌面 GUI (`src/macos/app.py`)

tkinter 桌面应用，三个 Tab 页：创建 Agent、创建任务、创建并执行 Crew。

## 4. 使用指南

### 4.1 快速开始

```python
from src.agent import create_agent
from src.task import create_task
from src.crew import create_crew, ProcessType

# 1. 创建 Agent
researcher = create_agent(
    role="研究员",
    goal="收集资料",
    backstory="你是研究专家"
)

# 2. 创建任务
task = create_task(
    description="研究 AI 趋势",
    agent=researcher
)

# 3. 创建 Crew 并执行
crew = create_crew(
    name="研究团队",
    agents=[researcher],
    tasks=[task],
    process=ProcessType.SEQUENTIAL
)

result = crew.kickoff()
print(result.summary())
```

### 4.2 自定义工具

```python
from src.agent import Tool

class MyTool(Tool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="自定义工具",
            function=self._execute
        )

    def _execute(self, **kwargs):
        return "工具执行结果"
```

## 5. 设计决策

### 5.1 为什么选择 ReAct 模式？

ReAct (Reasoning + Acting) 是目前最成熟的 Agent 范式：
- 思考链让决策过程可解释
- 工具调用让 Agent 能够获取外部信息
- 迭代机制让 Agent 能够自我修正

### 5.2 记忆系统设计

- **短期记忆**：用于当前任务的上下文，容量有限
- **长期记忆**：用于存储重要经验，可持久化

### 5.3 任务依赖机制

使用 DAG（有向无环图）管理任务依赖：
- 支持串行依赖
- 支持并行分支
- 通过 `is_ready()` 检查依赖完成状态

## 6. 扩展点

### 6.1 添加新的 Agent 类型

继承 `Agent` 类，实现特定的行为逻辑。

### 6.2 添加新的执行模式

在 `Crew` 类中添加新的 `_execute_*` 方法。

### 6.3 集成真实的 LLM

替换 `Agent.think()` 方法，调用真实的 LLM API。

### 6.4 添加自定义工具

继承 `Tool` 类，实现 `_execute` 方法。

## 7. 已知限制

- 当前使用模拟 LLM，未实际调用 API
- 工具执行是模拟的，未实现真实功能
- 内存中的全局状态无持久化
- 并行执行存在线程安全风险（Agent 共享状态）

## 8. 后续计划

- [ ] 集成 DeepSeek/OpenAI API
- [ ] 添加向量记忆存储
- [ ] 实现工具的沙箱执行增强
- [ ] 添加 Web 可视化编辑器
- [ ] 支持流式输出
- [ ] 单元测试覆盖
