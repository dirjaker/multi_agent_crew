"""
示例2：并行执行的内容创作团队
============================

演示多个 Agent 并行工作的场景：
- 3 个写手同时写不同章节
- 最后汇总结果
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import create_agent
from src.task import create_task, TaskPriority
from src.crew import create_crew, ProcessType
from src.tools import get_writing_tools


def main():
    print("=" * 60)
    print("示例2：并行执行的内容创作团队")
    print("=" * 60)

    # 1. 创建多个写手 Agent
    writers = []
    chapters = ["引言", "技术架构", "实现细节", "性能优化", "总结展望"]

    for i, chapter in enumerate(chapters):
        writer = create_agent(
            role=f"写手{i+1}",
            goal=f"撰写{chapter}章节",
            backstory=f"你是专注于{chapter}写作的专家。"
        )
        writers.append(writer)

    print(f"\n创建了 {len(writers)} 个写手 Agent")

    # 2. 创建并行任务
    tasks = []
    for i, chapter in enumerate(chapters):
        task = create_task(
            description=f"撰写关于 Multi-Agent 系统的{chapter}章节",
            agent=writers[i],
            expected_output=f"约 500 字的{chapter}章节内容",
            priority=TaskPriority.MEDIUM
        )
        tasks.append(task)

    print(f"创建了 {len(tasks)} 个并行任务")

    # 3. 创建 Crew 并执行
    crew = create_crew(
        name="内容创作团队",
        agents=writers,
        tasks=tasks,
        process=ProcessType.PARALLEL
    )

    print(f"\n开始并行执行...")
    result = crew.kickoff()

    print("\n执行完成！")
    print(f"成功: {result.success_count}, 失败: {result.failed_count}")
    print(f"总耗时: {result.total_duration:.2f}s")


if __name__ == "__main__":
    main()
