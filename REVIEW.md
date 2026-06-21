# 代码审查报告 - multi_agent_crew

**审查日期**: 2026-06-22
**审查范围**: 全部 Python 源文件（11 个）、配置文件、依赖文件

---

## 🔴 致命问题

### 1. eval() 代码注入漏洞
- **文件**: `src/tools.py` **行号**: 92
- **描述**: `CalculatorTool._calculate()` 直接使用 `eval(expression)` 执行用户输入的表达式。这是**远程代码执行 (RCE)** 漏洞，攻击者可执行任意 Python 代码，如 `__import__('os').system('rm -rf /')`。
- **修复建议**:
  ```python
  import ast
  import operator

  SAFE_OPERATORS = {
      ast.Add: operator.add, ast.Sub: operator.sub,
      ast.Mult: operator.mul, ast.Div: operator.truediv,
      ast.Pow: operator.pow, ast.Mod: operator.mod,
  }

  def _safe_eval(self, expression: str) -> float:
      """安全的数学表达式求值"""
      tree = ast.parse(expression, mode='eval')
      return self._eval_node(tree.body)

  def _eval_node(self, node):
      if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
          return node.value
      if isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPERATORS:
          return SAFE_OPERATORS[type(node.op)](
              self._eval_node(node.left), self._eval_node(node.right)
          )
      raise ValueError("不支持的表达式")
  ```

### 2. CORS 配置过于宽松
- **文件**: `src/web/app.py` **行号**: 25
- **描述**: `allow_origins=["*"]` 允许任何来源跨域访问。Web API 暴露了 Crew 创建、执行、数据重置等敏感操作。
- **修复建议**: 限制为可信来源域名。

### 3. 无认证的危险端点
- **文件**: `src/web/app.py` **行号**: 149-158, 177-183
- **描述**:
  - `POST /api/crews/run` - 可执行任意 Crew，消耗服务器资源
  - `DELETE /api/reset` - 无需认证即可**删除所有数据**
- **修复建议**: 至少添加 API Key 认证中间件，reset 端点应要求二次确认或限制为开发环境。

### 4. 监听 0.0.0.0 无访问控制
- **文件**: `src/web/app.py` **行号**: 188
- **描述**: 服务默认绑定 `0.0.0.0:8082`，暴露在所有网络接口。
- **修复建议**: 生产环境使用 `127.0.0.1` 或通过防火墙/反向代理限制访问。

---

## 🟡 警告问题

### 5. 同步阻塞调用在异步端点中
- **文件**: `src/web/app.py` **行号**: 155
- **描述**: `crew.kickoff()` 是同步阻塞调用，直接在 `async def run_crew()` 中执行，会阻塞 FastAPI 的事件循环，导致所有并发请求被阻塞。
- **修复建议**:
  ```python
  import asyncio
  loop = asyncio.get_event_loop()
  result = await loop.run_in_executor(None, crew.kickoff)
  ```

### 6. 线程安全问题
- **文件**: `src/crew.py` **行号**: 187-207（_execute_parallel）
- **描述**: `ThreadPoolExecutor` 并行执行任务时，`Agent` 和 `Task` 对象的状态（如 `agent.state`, `task.status`, `agent.memory`）没有线程保护，并发修改可能导致数据竞争。
- **修复建议**: 对共享状态的修改加锁（`threading.Lock`），或使用线程本地存储。

### 7. 内存中的全局状态无持久化
- **文件**: `src/web/app.py` **行号**: 31-33
- **描述**: `crews`, `agents`, `tasks` 都是内存字典，服务重启后全部丢失。无并发控制，多请求同时操作可能导致数据不一致。
- **修复建议**: 引入 Redis 或 SQLite 持久化，至少添加 `asyncio.Lock` 保护。

### 8. 异常信息泄露
- **文件**: `src/web/app.py` **行号**: 多处 HTTPException
- **描述**: 错误信息包含用户输入内容（如 `f"Agent '{req.agent_role}' 不存在"`），虽然风险较低，但仍建议统一错误格式。
- **修复建议**: 使用结构化错误响应，区分用户可见信息和内部日志。

### 9. Agent 的 LLM 调用为模拟实现
- **文件**: `src/agent.py` **行号**: 153-163
- **描述**: `think()` 方法仅做字符串拼接，未实际调用 LLM。`llm_config` 默认使用 `gpt-3.5-turbo` 但无 API Key 配置。
- **修复建议**: 将 LLM 调用抽象为接口，支持配置 API Key 和 endpoint。

---

## 🔵 建议

### 10. 缺少输入长度限制
- **文件**: `src/web/app.py` **行号**: 36-51（请求模型）
- **描述**: `AgentCreateRequest.role`, `goal`, `backstory` 等字段无长度限制，恶意用户可提交超大文本。
- **修复建议**: 使用 Pydantic 的 `max_length` 约束。

### 11. 依赖版本范围过宽
- **文件**: `requirements.txt`
- **描述**: 所有依赖使用 `>=` 范围约束，可能导致不同环境安装不兼容版本。
- **修复建议**: 使用 `pip freeze` 或 `poetry` 锁定精确版本。

### 12. 缺少日志系统
- **文件**: 多处
- **描述**: 项目使用 `print()` 输出调试信息，未使用标准 `logging` 模块。生产环境无法控制日志级别和输出格式。
- **修复建议**: 替换 `print` 为 `logging` 模块。

### 13. 缺少单元测试
- **描述**: 项目无 `tests/` 目录和测试文件，核心逻辑（Crew 执行、任务调度）缺少测试覆盖。
- **修复建议**: 至少为核心逻辑添加 pytest 测试用例。

### 14. Tool.execute 未做异常处理
- **文件**: `src/agent.py` **行号**: 80-82
- **描述**: `Tool.execute()` 直接调用 `self.function(**kwargs)`，未捕获异常。如果工具执行失败，异常会直接传播到上层。
- **修复建议**: 添加 try-except 并记录工具执行错误。

---

## 总结评分

| 维度 | 分数 | 说明 |
|------|------|------|
| **安全** | 2/10 | 存在 RCE 漏洞（eval）、无认证、CORS 全开，安全形势严峻 |
| **质量** | 5/10 | 抽象设计合理，但线程安全、异常处理、日志系统有明显不足 |
| **架构** | 6/10 | Agent/Task/Crew 抽象清晰，工厂模式良好，但缺少持久化和扩展点 |

**总体评价**: 架构设计有一定水准，但 `eval()` 漏洞是必须立即修复的致命问题。Web API 完全裸奔，需在部署前补齐认证和访问控制。
