"""
Agent 智能体模块
===============

定义智能体的核心属性和行为。

每个 Agent 具有：
- 角色（Role）: Agent 的身份和职责
- 目标（Goal）: Agent 需要达成的目标
- 背景故事（Backstory）: Agent 的背景信息，帮助 LLM 理解上下文
- 工具（Tools）: Agent 可以使用的工具
- 记忆（Memory）: Agent 的短期/长期记忆
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import json
import uuid


class AgentState(Enum):
    """Agent 状态枚举"""
    IDLE = "idle"           # 空闲
    WORKING = "working"     # 工作中
    WAITING = "waiting"     # 等待输入
    COMPLETED = "completed" # 已完成
    ERROR = "error"         # 出错


@dataclass
class AgentMemory:
    """Agent 记忆系统"""
    short_term: List[Dict[str, Any]] = field(default_factory=list)  # 短期记忆（当前任务）
    long_term: List[Dict[str, Any]] = field(default_factory=list)   # 长期记忆（历史经验）
    max_short_term: int = 10  # 短期记忆容量

    def add_short_term(self, content: str, metadata: Dict = None):
        """添加短期记忆"""
        memory = {
            "id": str(uuid.uuid4())[:8],
            "content": content,
            "metadata": metadata or {},
            "timestamp": self._get_timestamp()
        }
        self.short_term.append(memory)
        # 超出容量时移除最旧的记忆
        if len(self.short_term) > self.max_short_term:
            self.short_term.pop(0)

    def add_long_term(self, content: str, importance: float = 0.5):
        """添加长期记忆"""
        memory = {
            "id": str(uuid.uuid4())[:8],
            "content": content,
            "importance": importance,
            "timestamp": self._get_timestamp()
        }
        self.long_term.append(memory)

    def get_context(self, limit: int = 5) -> str:
        """获取记忆上下文"""
        recent = self.short_term[-limit:]
        return "\n".join([m["content"] for m in recent])

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)

    def execute(self, **kwargs) -> Any:
        """执行工具"""
        return self.function(**kwargs)


@dataclass
class Agent:
    """
    智能体类

    属性：
        id: 唯一标识符
        role: 角色名称
        goal: 目标描述
        backstory: 背景故事
        tools: 可用工具列表
        memory: 记忆系统
        state: 当前状态
        verbose: 是否输出详细信息
        max_iter: 最大迭代次数
        llm_config: LLM 配置
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    role: str = "Assistant"
    goal: str = "Help users complete tasks"
    backstory: str = "You are a helpful AI assistant."
    tools: List[Tool] = field(default_factory=list)
    memory: AgentMemory = field(default_factory=AgentMemory)
    state: AgentState = AgentState.IDLE
    verbose: bool = True
    max_iter: int = 5
    llm_config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """初始化后处理"""
        if not self.llm_config:
            self.llm_config = {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 1000
            }

    def get_system_prompt(self) -> str:
        """生成系统提示词"""
        tools_desc = ""
        if self.tools:
            tools_desc = "\n可用工具：\n"
            for tool in self.tools:
                tools_desc += f"- {tool.name}: {tool.description}\n"

        return f"""你是一个名为 {self.role} 的 AI 智能体。

目标：{self.goal}

背景：{self.backstory}

{tools_desc}

请根据你的角色和目标，完成分配给你的任务。
"""

    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """使用工具"""
        for tool in self.tools:
            if tool.name == tool_name:
                result = tool.execute(**kwargs)
                self.memory.add_short_term(
                    f"使用工具 {tool_name}，结果：{result}",
                    {"tool": tool_name, "result": result}
                )
                return result
        raise ValueError(f"工具 {tool_name} 不存在")

    def think(self, context: str) -> str:
        """
        思考过程（模拟 LLM 调用）

        实际项目中这里会调用 LLM API
        """
        self.state = AgentState.WORKING
        # 这里是模拟，实际应该调用 LLM
        thought = f"[{self.role}] 基于上下文思考：{context[:100]}..."
        self.memory.add_short_term(thought)
        return thought

    def act(self, task: str) -> str:
        """
        执行任务

        实现 ReAct 模式：Reasoning + Acting
        """
        self.state = AgentState.WORKING

        # 1. 思考
        thought = self.think(task)

        # 2. 决定是否使用工具
        if self.tools:
            # 简化逻辑：使用第一个可用工具
            tool = self.tools[0]
            action_result = self.use_tool(tool.name, task=task)
            result = f"思考：{thought}\n行动：使用 {tool.name}\n结果：{action_result}"
        else:
            result = f"思考：{thought}\n行动：直接回答\n结果：基于我的知识，{task}"

        self.state = AgentState.COMPLETED
        return result

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "role": self.role,
            "goal": self.goal,
            "state": self.state.value,
            "tools_count": len(self.tools)
        }


def create_agent(
    role: str,
    goal: str,
    backstory: str,
    tools: List[Tool] = None,
    **kwargs
) -> Agent:
    """
    创建 Agent 的工厂函数

    Args:
        role: 角色名称
        goal: 目标
        backstory: 背景故事
        tools: 工具列表
        **kwargs: 其他配置

    Returns:
        Agent 实例
    """
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools or [],
        **kwargs
    )
