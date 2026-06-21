<div align="center">

<img src="assets/banner.svg" width="100%" alt="多智能体协作系统">

<br>

### 👥 多智能体协作系统

[![Stars](https://img.shields.io/github/stars/dirjaker/multi_agent_crew?style=flat-square&label=Stars&color=FFD700)](https://github.com/dirjaker/multi_agent_crew/stargazers)
[![Forks](https://img.shields.io/github/forks/dirjaker/multi_agent_crew?style=flat-square&label=Forks&color=4A90D9)](https://github.com/dirjaker/multi_agent_crew/network/members)
[![Contributors](https://img.shields.io/github/contributors/dirjaker/multi_agent_crew?style=flat-square&label=Contributors&color=8B4513)](https://github.com/dirjaker/multi_agent_crew/graphs/contributors)
[![License](https://img.shields.io/github/license/dirjaker/multi_agent_crew?style=flat-square&label=License&color=20B2AA)](https://github.com/dirjaker/multi_agent_crew/blob/dev/LICENSE)

</div>

---

## ✨ 功能特性

| 功能 | 描述 |
|------|------|
| 👥 **Crew 抽象** | 团队、角色、任务三层抽象模型 |
| 🔄 **3 种协作模式** | 顺序执行、并行执行、层级管理三种模式 |
| 🧰 **5 种内置工具** | 搜索、分析、写作、代码、计算器工具集 |
| 🤖 **LLM 驱动** | 基于大语言模型的 ReAct 模式智能决策 |
| 📋 **任务编排** | DAG 依赖管理与优先级调度 |
| 📊 **执行追踪** | 完整的协作过程记录与执行报告 |
| 🧠 **记忆系统** | 短期/长期双层记忆，支持上下文累积 |
| 🌐 **Web API** | FastAPI REST 接口，支持远程创建和执行 Crew |
| 🖥️ **桌面 GUI** | tkinter macOS 桌面应用 |
| 🔒 **安全沙箱** | 工具执行沙箱保护，防止代码注入 |

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/dirjaker/multi_agent_crew.git
cd multi_agent_crew

# 创建虚拟环境
conda create -n multi_agent_crew python=3.12 -y
conda activate multi_agent_crew

# 安装依赖
pip install -r requirements.txt

# 运行示例
python examples/sequential_crew.py   # 顺序执行
python examples/parallel_crew.py     # 并行执行
python examples/hierarchical_crew.py # 层级模式

# 启动 Web API
python src/web/app.py
# 访问 http://localhost:8082

# 启动桌面 GUI（macOS）
python src/macos/app.py
```

## 📖 使用示例

```python
from src.agent import create_agent
from src.task import create_task, TaskPriority
from src.crew import create_crew, ProcessType
from src.tools import get_research_tools

# 1. 创建 Agent
researcher = create_agent(
    role="研究员",
    goal="收集和整理相关资料",
    backstory="你是一位经验丰富的研究员。",
    tools=get_research_tools()
)

analyst = create_agent(
    role="分析师",
    goal="分析数据，发现关键洞察",
    backstory="你是一位数据分析专家。"
)

# 2. 创建任务（支持依赖关系）
task1 = create_task(
    description="收集 AI 发展趋势资料",
    agent=researcher,
    priority=TaskPriority.HIGH
)
task2 = create_task(
    description="分析资料，找出关键洞察",
    agent=analyst,
    dependencies=[task1.id]  # 依赖 task1
)

# 3. 创建 Crew 并执行
crew = create_crew(
    name="研究团队",
    agents=[researcher, analyst],
    tasks=[task1, task2],
    process=ProcessType.SEQUENTIAL
)

result = crew.kickoff()
print(result.summary())
```

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **语言** | Python 3.8+ |
| **数据建模** | dataclass + Enum |
| **并行调度** | concurrent.futures.ThreadPoolExecutor |
| **Web 框架** | FastAPI, Pydantic |
| **桌面 GUI** | tkinter |
| **设计模式** | 策略模式、工厂模式、组合模式 |
| **Agent 范式** | ReAct（Reasoning + Acting） |

## 📁 项目结构

```
multi_agent_crew/
├── src/
│   ├── __init__.py          # 包定义与版本信息
│   ├── agent.py             # Agent 智能体模块
│   ├── task.py              # Task 任务模块
│   ├── crew.py              # Crew 协作引擎
│   ├── tools.py             # 内置工具集（含安全沙箱）
│   ├── web/
│   │   ├── app.py           # FastAPI Web API
│   │   └── static/
│   │       └── index.html   # Web 前端页面
│   └── macos/
│       └── app.py           # tkinter 桌面 GUI
├── examples/
│   ├── sequential_crew.py   # 顺序执行示例
│   ├── parallel_crew.py     # 并行执行示例
│   └── hierarchical_crew.py # 层级模式示例
├── docs/                    # 技术文档
├── assets/                  # 静态资源
├── requirements.txt         # 依赖列表
└── README.md
```

## 📝 开发日志

- [x] Agent/Task/Crew 三层抽象模型
- [x] 3 种协作模式（顺序/并行/层级）
- [x] 5 种内置工具 + 安全沙箱
- [x] ReAct 模式 Agent 执行
- [x] 短期/长期记忆系统
- [x] DAG 任务依赖管理
- [x] FastAPI Web API + 前端页面
- [x] tkinter macOS 桌面 GUI
- [ ] 集成真实 LLM API（DeepSeek/OpenAI）
- [ ] 向量记忆存储（FAISS/ChromaDB）
- [ ] Web 可视化任务编辑器
- [ ] 流式输出支持
- [ ] 单元测试覆盖

## 📄 许可证

[MIT License](LICENSE)

---

<div align="center">

🔗 **GitHub**: [dirjaker/multi_agent_crew](https://github.com/dirjaker/multi_agent_crew)

⭐ 如果这个项目对你有帮助，请给一个 Star 支持一下！

</div>
