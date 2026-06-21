# Multi-Agent Crew 更新日志

本项目遵循 [语义化版本控制](https://semver.org/lang/zh-CN/)。

---

## [未发布]

### 计划中
- 集成 DeepSeek / OpenAI API，实现真实 LLM 调用
- 向量记忆存储（FAISS / ChromaDB）
- Web 可视化任务编辑器
- 流式输出支持
- 单元测试覆盖
- 记忆检索与遗忘机制
- 错误恢复机制

---

## [1.0.0] - 2026-05-30

### 🎉 首个正式版本

#### Agent 智能体模块
- Agent 类定义：角色（Role）、目标（Goal）、背景故事（Backstory）
- AgentMemory 记忆系统：短期记忆（滑动窗口）+ 长期记忆（带重要性评分）
- ReAct 模式执行：思考（think）→ 行动（act）→ 工具调用
- AgentState 状态机：IDLE / WORKING / WAITING / COMPLETED / ERROR
- 工具调用支持：按名称查找、执行结果自动存入记忆
- `create_agent()` 工厂函数

#### Task 任务模块
- Task 类定义：描述、期望输出、优先级、依赖关系
- TaskResult 结果封装：状态、输出、错误、耗时
- TaskStatus 状态机：PENDING / IN_PROGRESS / COMPLETED / FAILED / BLOCKED
- TaskPriority 优先级：LOW / MEDIUM / HIGH / URGENT
- DAG 依赖管理：`is_ready()` 检查前置任务完成状态
- `create_task()` 工厂函数

#### Crew 协作引擎
- Sequential 顺序执行：前序输出自动传递为后续上下文
- Parallel 并行执行：ThreadPoolExecutor + as_completed
- Hierarchical 层级执行：Manager-Worker 模式，轮询分配
- ProcessType 执行模式枚举
- CrewResult 执行结果：统计、摘要报告
- `create_crew()` 工厂函数

#### 工具系统
- Tool 基类：可插拔的组合模式设计
- SearchTool：信息检索
- AnalysisTool：数据分析
- WritingTool：内容生成
- CodeTool：代码生成与分析
- CalculatorTool：数学计算
- 预定义工具组合：`get_default_tools()` / `get_research_tools()` / `get_writing_tools()` / `get_coding_tools()`

#### 示例代码
- `examples/sequential_crew.py` — 研究团队顺序执行
- `examples/parallel_crew.py` — 写手团队并行执行
- `examples/hierarchical_crew.py` — 开发团队层级执行

#### 文档
- README.md — 项目说明与快速开始
- docs/技术文档.md — 完整技术设计文档
- docs/TECHNICAL_DOC.md — 技术文档（精简版）
- docs/VERSION.md — 版本记录
- docs/DIRECTION.md — 项目方向指引

---

## 版本说明

- **主版本号**：不兼容的 API 变更
- **次版本号**：向下兼容的功能新增
- **修订号**：向下兼容的问题修正
