<div align="center">

# 🚀 Multi-Agent Crew

### 多智能体协作系统

[![Agent](https://img.shields.io/badge/Agent-4+-blue?style=flat-square)]()
[![模式](https://img.shields.io/badge/模式-3-green?style=flat-square)]()
[![框架](https://img.shields.io/badge/框架-CrewAI-orange?style=flat-square)]()
[![更新](https://img.shields.io/badge/更新-2025.06-red?style=flat-square)]()

*多 Agent 协作编排 · 任务分解 · 角色分配 · 结果聚合*

</div>

---

> 多智能体协作框架 - 让 AI Agent 组成团队，协作完成复杂任务

## ✨ 特性

- 🎭 **多种协作模式**：顺序、并行、层级管理
- 🤖 **灵活的 Agent 定义**：角色、目标、背景故事
- 📋 **任务依赖管理**：支持 DAG 任务编排
- 🧠 **记忆系统**：短期记忆 + 长期记忆
- 🔧 **可扩展工具系统**：轻松添加自定义工具

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/dirjaker/multi_agent_crew.git
cd multi_agent_crew

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 基础用法

```python
from src.agent import create_agent
from src.task import create_task
from src.crew import create_crew, ProcessType

# 创建 Agent
researcher = create_agent(
    role="研究员",
    goal="收集资料",
    backstory="你是研究专家"
)

# 创建任务
task = create_task(
    description="研究 AI 趋势",
    agent=researcher
)

# 创建 Crew 并执行
crew = create_crew(
    name="研究团队",
    agents=[researcher],
    tasks=[task],
    process=ProcessType.SEQUENTIAL
)

result = crew.kickoff()
```

## 📁 项目结构

```
multi_agent_crew/
├── src/
│   ├── __init__.py      # 包初始化
│   ├── agent.py         # Agent 智能体定义
│   ├── task.py          # Task 任务定义
│   ├── crew.py          # Crew 协作团队
│   └── tools.py         # 内置工具集
├── examples/
│   ├── sequential_crew.py   # 顺序执行示例
│   ├── parallel_crew.py     # 并行执行示例
│   └── hierarchical_crew.py # 层级执行示例
├── TECHNICAL_DOC.md     # 技术文档
├── DIRECTION.md         # 方向指引
├── VERSION.md           # 版本记录
├── requirements.txt     # 依赖列表
└── README.md            # 项目说明
```

## 🎭 协作模式

### 1. Sequential（顺序执行）

```
Agent1 → Output1 → Agent2 → Output2 → Agent3 → Final
```

适合有依赖关系的任务链。

### 2. Parallel（并行执行）

```
Agent1 ─┐
Agent2 ─┼→ Aggregate → Final
Agent3 ─┘
```

适合独立的任务，可同时执行。

### 3. Hierarchical（层级管理）

```
Manager
├── Worker1 → Task1
├── Worker2 → Task2
└── Worker3 → Task3
    ↓
Manager → Final
```

适合需要协调的复杂任务。

## 🔧 内置工具

| 工具 | 描述 |
|------|------|
| `SearchTool` | 搜索信息 |
| `AnalysisTool` | 数据分析 |
| `WritingTool` | 内容生成 |
| `CodeTool` | 代码生成 |
| `CalculatorTool` | 数学计算 |

## 📊 运行示例

```bash
# 顺序执行示例
python examples/sequential_crew.py

# 并行执行示例
python examples/parallel_crew.py

# 层级执行示例
python examples/hierarchical_crew.py
```

## 🎯 应用场景

- 📝 **研究报告**：研究员收集 → 分析师分析 → 作家撰写
- 📖 **内容创作**：多个写手并行创作不同章节
- 💻 **软件开发**：Tech Lead 规划 → 开发实现 → QA 测试
- 📊 **数据分析**：数据收集 → 清洗 → 分析 → 可视化

## 📚 文档

- [技术文档](TECHNICAL_DOC.md) - 架构设计、模块详解
- [方向指引](DIRECTION.md) - 项目规划、学习路径
- [版本记录](VERSION.md) - 更新日志

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License

