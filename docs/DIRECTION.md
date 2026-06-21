# Multi-Agent Crew 项目方向指引

## 🎯 项目定位

Multi-Agent Crew 是一个**多智能体协作框架**，目的是：
1. 实现完整的 Multi-Agent 协作系统
2. 掌握任务分解与分配策略
3. 学习 Agent 间通信与协作机制
4. 提供可扩展的工具系统和交互层
5. 为面试提供可讲解的项目经验

---

## 📚 开发阶段

### 阶段一：核心框架 ✅
- [x] Agent/Task/Crew 三层抽象模型
- [x] 顺序执行（上下文传递）
- [x] 并行执行（ThreadPoolExecutor）
- [x] 层级模式（Manager-Worker）
- [x] 5 种内置工具
- [x] 工具安全沙箱

### 阶段二：记忆与依赖 ✅
- [x] 短期记忆（滑动窗口）
- [x] 长期记忆（重要性评分）
- [x] DAG 任务依赖管理
- [x] 任务优先级系统
- [x] ReAct 模式执行

### 阶段三：交互层 ✅
- [x] FastAPI Web API（9 个端点）
- [x] Web 前端页面
- [x] tkinter macOS 桌面 GUI
- [x] 3 个完整示例

### 阶段四：LLM 集成（进行中）
- [ ] 集成 DeepSeek API
- [ ] 实现流式输出
- [ ] Function Calling 协议

### 阶段五：高级特性（计划中）
- [ ] 向量记忆存储（FAISS/ChromaDB）
- [ ] Web 可视化任务编辑器
- [ ] 错误恢复机制
- [ ] 持久化存储

---

## 🎓 面试要点

### 核心概念
1. **Multi-Agent 架构**：如何设计多智能体系统？
2. **任务分配策略**：如何决定哪个 Agent 执行哪个任务？
3. **协作模式**：顺序、并行、层级各适用于什么场景？
4. **状态管理**：如何管理 Agent 和 Task 的状态？

### 常见问题

**Q: 为什么需要多 Agent？单 Agent 不够吗？**
> 复杂任务需要不同专业能力的 Agent 协作。就像一个团队，每个人专注自己擅长的领域。

**Q: 如何处理 Agent 间的冲突？**
> 1. 使用 Manager Agent 协调
> 2. 定义清晰的任务边界
> 3. 使用投票或优先级机制

**Q: 顺序执行和并行执行如何选择？**
> - 有依赖关系 → 顺序执行
> - 任务独立 → 并行执行
> - 需要协调 → 层级模式

**Q: 如何扩展这个系统？**
> 1. 继承 Tool 类添加新工具
> 2. 添加新的 `_execute_*` 方法实现新执行模式
> 3. 替换 `think()` 方法集成真实 LLM
> 4. 添加新的 Web API 端点

**Q: 工具安全沙箱是怎么实现的？**
> 通过 AST 解析 + 危险模式黑名单 + 内置函数白名单三重保护。`safe_exec()` 和 `safe_eval()` 检查代码中是否包含 `import`、`os.`、`subprocess` 等危险模式，再用 AST 拒绝 Import 节点，最后在受限的命名空间中执行。

---

## 🔗 技术关联

### 项目组件关系

```
multi_agent_crew
├── src/agent.py    ← Agent 核心（ReAct + 记忆）
├── src/task.py     ← Task 调度（DAG + 状态机）
├── src/crew.py     ← Crew 引擎（策略模式）
├── src/tools.py    ← 工具系统（安全沙箱）
├── src/web/        ← Web API（FastAPI）
├── src/macos/      ← 桌面 GUI（tkinter）
└── examples/       ← 使用示例
```

### 技术栈

- **核心**：Python 3.8+, dataclasses, Enum
- **并发**：concurrent.futures.ThreadPoolExecutor
- **Web**：FastAPI, Pydantic, uvicorn
- **GUI**：tkinter
- **设计模式**：策略模式、工厂模式、组合模式

---

## 📖 参考资源

### 论文
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [AutoGen: Multi-Agent Conversation](https://arxiv.org/abs/2308.08155)

### 开源项目
- [CrewAI](https://github.com/joaomdmoura/crewai)
- [AutoGen](https://github.com/microsoft/autogen)
- [LangGraph](https://github.com/langchain-ai/langgraph)

---

## ⚡ 快速命令

```bash
# 运行示例
python examples/sequential_crew.py
python examples/parallel_crew.py
python examples/hierarchical_crew.py

# 启动 Web API
python src/web/app.py

# 启动桌面 GUI
python src/macos/app.py

# 测试代码
python -c "from src.agent import Agent; print('Agent OK')"
python -c "from src.crew import Crew; print('Crew OK')"
python -c "from src.tools import get_default_tools; print('Tools OK', len(get_default_tools()))"
```
