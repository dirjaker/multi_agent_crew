"""
Crew 协作团队模块
================

Crew 是多 Agent 协作的核心，负责：
1. 管理 Agent 团队
2. 协调任务分配
3. 控制执行流程
4. 聚合执行结果

支持的执行模式：
- Sequential: 顺序执行
- Parallel: 并行执行
- Hierarchical: 层级模式（Manager 分配任务）
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json

from .agent import Agent
from .task import Task, TaskStatus, TaskResult


class ProcessType(Enum):
    """执行流程类型"""
    SEQUENTIAL = "sequential"  # 顺序执行
    PARALLEL = "parallel"      # 并行执行
    HIERARCHICAL = "hierarchical"  # 层级模式


@dataclass
class CrewResult:
    """Crew 执行结果"""
    crew_name: str
    process_type: ProcessType
    task_results: List[TaskResult] = field(default_factory=list)
    final_output: str = ""
    total_duration: float = 0.0
    success_count: int = 0
    failed_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "crew_name": self.crew_name,
            "process_type": self.process_type.value,
            "total_tasks": len(self.task_results),
            "success": self.success_count,
            "failed": self.failed_count,
            "duration": f"{self.total_duration:.2f}s",
            "final_output": self.final_output[:500]  # 截断
        }

    def summary(self) -> str:
        """生成执行摘要"""
        return f"""
=== Crew 执行报告 ===
团队名称: {self.crew_name}
执行模式: {self.process_type.value}
总任务数: {len(self.task_results)}
成功: {self.success_count}
失败: {self.failed_count}
总耗时: {self.total_duration:.2f}s

最终输出:
{self.final_output[:500]}
========================
"""


@dataclass
class Crew:
    """
    协作团队类

    属性：
        name: 团队名称
        agents: Agent 列表
        tasks: 任务列表
        process: 执行流程类型
        verbose: 是否输出详细信息
        max_workers: 并行执行时的最大线程数
    """
    name: str = "Default Crew"
    agents: List[Agent] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    process: ProcessType = ProcessType.SEQUENTIAL
    verbose: bool = True
    max_workers: int = 4

    def add_agent(self, agent: Agent) -> 'Crew':
        """添加 Agent 到团队"""
        self.agents.append(agent)
        return self

    def add_task(self, task: Task) -> 'Crew':
        """添加任务"""
        self.tasks.append(task)
        return self

    def kickoff(self) -> CrewResult:
        """
        开始执行任务

        根据 process 类型选择执行模式

        Returns:
            CrewResult 执行结果
        """
        start_time = time.time()

        if self.process == ProcessType.SEQUENTIAL:
            result = self._execute_sequential()
        elif self.process == ProcessType.PARALLEL:
            result = self._execute_parallel()
        elif self.process == ProcessType.HIERARCHICAL:
            result = self._execute_hierarchical()
        else:
            raise ValueError(f"未知的执行模式: {self.process}")

        result.total_duration = time.time() - start_time

        if self.verbose:
            print(result.summary())

        return result

    def _execute_sequential(self) -> CrewResult:
        """
        顺序执行任务

        特点：
        - 前一个任务的输出作为下一个任务的上下文
        - 适合有依赖关系的任务链
        """
        results = []
        context = ""

        for task in self.tasks:
            if self.verbose:
                print(f"\n▶ 执行任务: {task.description[:50]}...")

            # 检查依赖
            completed_ids = [r.task_id for r in results if r.is_success()]
            if not task.is_ready(completed_ids):
                result = TaskResult(
                    task_id=task.id,
                    status=TaskStatus.BLOCKED,
                    error=f"依赖未完成: {task.dependencies}"
                )
            else:
                result = task.execute(context)

            results.append(result)

            # 更新上下文
            if result.is_success():
                context = str(result.output)

        # 计算统计
        success = sum(1 for r in results if r.is_success())
        failed = sum(1 for r in results if not r.is_success())
        final_output = results[-1].output if results else ""

        return CrewResult(
            crew_name=self.name,
            process_type=self.process,
            task_results=results,
            final_output=str(final_output),
            success_count=success,
            failed_count=failed
        )

    def _execute_parallel(self) -> CrewResult:
        """
        并行执行任务

        特点：
        - 多个任务同时执行
        - 适合独立的任务
        """
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_task = {}
            for task in self.tasks:
                if self.verbose:
                    print(f"▶ 提交任务: {task.description[:50]}...")
                future = executor.submit(task.execute, "")
                future_to_task[future] = task

            # 收集结果
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(TaskResult(
                        task_id=task.id,
                        status=TaskStatus.FAILED,
                        error=str(e)
                    ))

        success = sum(1 for r in results if r.is_success())
        failed = sum(1 for r in results if not r.is_success())
        final_output = "\n---\n".join([str(r.output) for r in results if r.is_success()])

        return CrewResult(
            crew_name=self.name,
            process_type=self.process,
            task_results=results,
            final_output=final_output,
            success_count=success,
            failed_count=failed
        )

    def _execute_hierarchical(self) -> CrewResult:
        """
        层级模式执行

        特点：
        - Manager Agent 分析任务并分配
        - Worker Agents 执行具体任务
        - Manager 汇总结果
        """
        if len(self.agents) < 2:
            return self._execute_sequential()

        # 第一个 Agent 作为 Manager
        manager = self.agents[0]
        workers = self.agents[1:]

        results = []

        # Manager 分析任务
        if self.verbose:
            print(f"👔 Manager ({manager.role}) 分析任务...")

        # 简化的任务分配逻辑
        for i, task in enumerate(self.tasks):
            # 轮询分配给 Worker
            worker = workers[i % len(workers)]
            task.agent = worker

            if self.verbose:
                print(f"📋 分配任务给 {worker.role}: {task.description[:50]}...")

            result = task.execute()
            results.append(result)

        # Manager 汇总
        if self.verbose:
            print(f"👔 Manager 汇总结果...")

        success = sum(1 for r in results if r.is_success())
        failed = sum(1 for r in results if not r.is_success())
        summary = "\n".join([f"- {r.output}" for r in results if r.is_success()])
        final_output = f"任务汇总 ({success}/{len(results)} 成功):\n{summary}"

        return CrewResult(
            crew_name=self.name,
            process_type=self.process,
            task_results=results,
            final_output=final_output,
            success_count=success,
            failed_count=failed
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "agents": [a.to_dict() for a in self.agents],
            "tasks": [t.to_dict() for t in self.tasks],
            "process": self.process.value
        }


def create_crew(
    name: str,
    agents: List[Agent],
    tasks: List[Task],
    process: ProcessType = ProcessType.SEQUENTIAL,
    **kwargs
) -> Crew:
    """
    创建 Crew 的工厂函数

    Args:
        name: 团队名称
        agents: Agent 列表
        tasks: 任务列表
        process: 执行模式
        **kwargs: 其他配置

    Returns:
        Crew 实例
    """
    return Crew(
        name=name,
        agents=agents,
        tasks=tasks,
        process=process,
        **kwargs
    )
