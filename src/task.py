"""
Task 任务模块
============

定义任务的核心结构和执行逻辑。

任务类型：
- Simple: 单个任务
- Collaborative: 需要多个 Agent 协作的任务
- Conditional: 有条件分支的任务
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"       # 待处理
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"   # 已完成
    FAILED = "failed"         # 失败
    BLOCKED = "blocked"       # 被阻塞


class TaskPriority(Enum):
    """任务优先级"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class TaskResult:
    """任务执行结果"""
    task_id: str
    status: TaskStatus
    output: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0  # 执行时长（秒）

    def is_success(self) -> bool:
        return self.status == TaskStatus.COMPLETED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "duration": self.duration
        }


@dataclass
class Task:
    """
    任务类

    属性：
        id: 任务唯一标识
        description: 任务描述
        expected_output: 期望的输出格式
        agent: 负责执行的 Agent
        priority: 优先级
        dependencies: 依赖的任务 ID 列表
        context: 任务上下文（来自其他任务的输出）
        status: 当前状态
        result: 执行结果
        max_retries: 最大重试次数
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str = ""
    expected_output: str = "完成任务的详细报告"
    agent: Any = None  # Agent 实例
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: List[str] = field(default_factory=list)
    context: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[TaskResult] = None
    max_retries: int = 3
    retry_count: int = 0

    def is_ready(self, completed_tasks: List[str]) -> bool:
        """
        检查任务是否可以执行（所有依赖都已完成）

        Args:
            completed_tasks: 已完成的任务 ID 列表

        Returns:
            是否可执行
        """
        if self.status != TaskStatus.PENDING:
            return False
        return all(dep in completed_tasks for dep in self.dependencies)

    def execute(self, context: str = "") -> TaskResult:
        """
        执行任务

        Args:
            context: 任务上下文

        Returns:
            任务执行结果
        """
        import time

        if not self.agent:
            return TaskResult(
                task_id=self.id,
                status=TaskStatus.FAILED,
                error="未分配执行 Agent"
            )

        self.status = TaskStatus.IN_PROGRESS
        start_time = time.time()

        try:
            # 构建完整的任务描述
            full_description = self.description
            if context:
                full_description = f"{context}\n\n任务：{self.description}"
            if self.context:
                full_description += f"\n\n参考信息：\n" + "\n".join(self.context)

            # 执行任务
            output = self.agent.act(full_description)

            duration = time.time() - start_time
            self.result = TaskResult(
                task_id=self.id,
                status=TaskStatus.COMPLETED,
                output=output,
                duration=duration
            )
            self.status = TaskStatus.COMPLETED

        except Exception as e:
            duration = time.time() - start_time
            self.result = TaskResult(
                task_id=self.id,
                status=TaskStatus.FAILED,
                error=str(e),
                duration=duration
            )
            self.status = TaskStatus.FAILED

        return self.result

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "agent": self.agent.role if self.agent else None,
            "dependencies": self.dependencies
        }


def create_task(
    description: str,
    agent: Any,
    expected_output: str = "完成任务的详细报告",
    priority: TaskPriority = TaskPriority.MEDIUM,
    dependencies: List[str] = None,
    **kwargs
) -> Task:
    """
    创建任务的工厂函数

    Args:
        description: 任务描述
        agent: 执行 Agent
        expected_output: 期望输出
        priority: 优先级
        dependencies: 依赖任务列表
        **kwargs: 其他参数

    Returns:
        Task 实例
    """
    return Task(
        description=description,
        agent=agent,
        expected_output=expected_output,
        priority=priority,
        dependencies=dependencies or [],
        **kwargs
    )
