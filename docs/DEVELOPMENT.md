# Multi-Agent Crew 开发指南

## 1. 开发环境搭建

### 1.1 环境要求

- Python 3.8+
- conda（推荐）或 venv

### 1.2 安装步骤

```bash
# 克隆项目
git clone https://github.com/dirjaker/multi_agent_crew.git
cd multi_agent_crew

# 创建虚拟环境
conda create -n multi_agent_crew python=3.12 -y
conda activate multi_agent_crew

# 安装依赖
pip install -r requirements.txt
```

### 1.3 依赖说明

| 依赖 | 版本 | 用途 |
|------|------|------|
| httpx | 0.28.1 | HTTP 客户端（预留 LLM 调用） |
| pydantic | 2.13.4 | 数据验证（Web API 请求模型） |
| pydantic_core | 2.46.4 | Pydantic 核心 |
| typing_extensions | 4.15.0 | 类型注解扩展 |

> 注：FastAPI 和 uvicorn 需要额外安装（用于 Web API）

```bash
pip install fastapi uvicorn
```

## 2. 项目结构

```
multi_agent_crew/
├── src/
│   ├── __init__.py          # 包定义，版本信息 (__version__ = "1.0.0")
│   ├── agent.py             # Agent 智能体模块
│   ├── task.py              # Task 任务模块
│   ├── crew.py              # Crew 协作引擎
│   ├── tools.py             # 内置工具集 + 安全沙箱
│   ├── web/
│   │   ├── app.py           # FastAPI Web API
│   │   └── static/
│   │       └── index.html   # Web 前端
│   └── macos/
│       └── app.py           # tkinter 桌面 GUI
├── examples/
│   ├── sequential_crew.py   # 顺序执行示例
│   ├── parallel_crew.py     # 并行执行示例
│   └── hierarchical_crew.py # 层级模式示例
├── docs/                    # 文档目录
├── assets/                  # 静态资源
├── packaging/
│   └── py2app_setup.py      # macOS 打包配置
├── requirements.txt
├── README.md
└── REVIEW.md                # 代码审查报告
```

## 3. 核心开发流程

### 3.1 创建 Agent

```python
from src.agent import create_agent, Tool

# 基础 Agent
agent = create_agent(
    role="研究员",
    goal="收集资料",
    backstory="你是研究专家"
)

# 带工具的 Agent
from src.tools import get_research_tools
agent = create_agent(
    role="研究员",
    goal="收集资料",
    backstory="你是研究专家",
    tools=get_research_tools()
)
```

### 3.2 创建自定义工具

```python
from src.agent import Tool

class MyTool(Tool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="自定义工具描述",
            function=self._execute,
            parameters={"param1": "参数说明"}
        )

    def _execute(self, param1: str = "", **kwargs) -> str:
        # 工具逻辑
        return f"执行结果: {param1}"
```

### 3.3 创建任务

```python
from src.task import create_task, TaskPriority

task = create_task(
    description="任务描述",
    agent=agent,
    expected_output="期望输出格式",
    priority=TaskPriority.HIGH,
    dependencies=["other_task_id"]  # 可选：依赖其他任务
)
```

### 3.4 组建 Crew 并执行

```python
from src.crew import create_crew, ProcessType

crew = create_crew(
    name="团队名称",
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=ProcessType.SEQUENTIAL,  # 或 PARALLEL / HIERARCHICAL
    max_workers=4  # 仅并行模式生效
)

result = crew.kickoff()
print(result.summary())
```

## 4. 运行示例

```bash
# 顺序执行 - 研究团队
python examples/sequential_crew.py

# 并行执行 - 内容创作团队
python examples/parallel_crew.py

# 层级模式 - 开发团队
python examples/hierarchical_crew.py
```

## 5. 运行 Web API

```bash
# 启动 FastAPI 服务
python src/web/app.py

# 服务默认运行在 http://localhost:8082
# API 文档：http://localhost:8082/docs
```

### API 使用示例

```bash
# 创建 Agent
curl -X POST http://localhost:8082/api/agents \
  -H "Content-Type: application/json" \
  -d '{"role": "研究员", "goal": "收集资料", "backstory": "研究专家"}'

# 创建任务
curl -X POST http://localhost:8082/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"description": "研究 AI 趋势", "agent_role": "研究员"}'

# 创建 Crew
curl -X POST http://localhost:8082/api/crews \
  -H "Content-Type: application/json" \
  -d '{"name": "研究团队", "agent_roles": ["研究员"], "task_descriptions": ["研究 AI 趋势"], "process": "sequential"}'

# 执行 Crew
curl -X POST http://localhost:8082/api/crews/run \
  -H "Content-Type: application/json" \
  -d '{"crew_name": "研究团队"}'
```

## 6. 运行桌面 GUI

```bash
# macOS / Linux（需要 tkinter）
python src/macos/app.py
```

## 7. 验证代码

```bash
# 基础导入测试
python -c "from src.agent import Agent; print('Agent OK')"
python -c "from src.task import Task; print('Task OK')"
python -c "from src.crew import Crew; print('Crew OK')"
python -c "from src.tools import get_default_tools; print('Tools OK', len(get_default_tools()))"
```

## 8. 代码规范

- 使用 `dataclass` 定义数据结构
- 使用 `Enum` 定义状态枚举
- 工厂函数命名：`create_*`
- 工具类命名：`*Tool`
- 文档字符串使用中文
- 安全沙箱函数用于所有外部输入的执行

## 9. 扩展开发

### 9.1 添加新的执行模式

在 `src/crew.py` 的 `Crew` 类中添加新方法：

```python
def _execute_new_mode(self) -> CrewResult:
    """新模式执行逻辑"""
    # 实现逻辑
    return CrewResult(...)
```

然后在 `kickoff()` 中添加分发逻辑。

### 9.2 集成真实 LLM

修改 `src/agent.py` 中的 `think()` 方法：

```python
def think(self, context: str) -> str:
    """调用 LLM API"""
    import httpx
    response = httpx.post(
        "https://api.deepseek.com/v1/chat/completions",
        json={
            "model": self.llm_config["model"],
            "messages": [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": context}
            ]
        },
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    return response.json()["choices"][0]["message"]["content"]
```

### 9.3 添加新的 Web API 端点

在 `src/web/app.py` 中添加新的路由：

```python
@app.post("/api/new-endpoint")
async def new_endpoint(req: NewRequestModel):
    # 实现逻辑
    return {"result": "..."}
```
