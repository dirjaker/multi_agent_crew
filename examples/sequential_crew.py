"""
示例1：顺序执行的研究团队
========================

演示如何创建一个研究团队，按顺序完成研究任务：
1. 研究员收集资料
2. 分析师分析数据
3. 作家撰写报告
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import Agent, create_agent
from src.task import Task, create_task, TaskPriority
from src.crew import Crew, create_crew, ProcessType
from src.tools import get_research_tools, get_writing_tools


def main():
    print("=" * 60)
    print("示例1：顺序执行的研究团队")
    print("=" * 60)

    # 1. 创建 Agent
    researcher = create_agent(
        role="研究员",
        goal="收集和整理相关资料",
        backstory="你是一位经验丰富的研究员，擅长信息收集和整理。",
        tools=get_research_tools()
    )

    analyst = create_agent(
        role="分析师",
        goal="分析数据，发现关键洞察",
        backstory="你是一位数据分析专家，善于从数据中发现规律。"
    )

    writer = create_agent(
        role="作家",
        goal="撰写清晰、专业的报告",
        backstory="你是一位技术作家，擅长将复杂概念通俗化。"
    )

    print(f"\n创建了 {3} 个 Agent:")
    print(f"  - {researcher.role}: {researcher.goal}")
    print(f"  - {analyst.role}: {analyst.goal}")
    print(f"  - {writer.role}: {writer.goal}")

    # 2. 创建任务
    task1 = create_task(
        description="收集关于 AI Agent 发展趋势的资料",
        agent=researcher,
        expected_output="一份包含 5 个关键趋势的清单",
        priority=TaskPriority.HIGH
    )

    task2 = create_task(
        description="分析收集到的资料，找出关键洞察",
        agent=analyst,
        expected_output="分析报告，包含关键发现和建议",
        dependencies=[task1.id]
    )

    task3 = create_task(
        description="撰写最终研究报告",
        agent=writer,
        expected_output="一份完整的中文研究报告",
        dependencies=[task2.id]
    )

    print(f"\n创建了 {3} 个任务:")
    print(f"  - 任务1: {task1.description}")
    print(f"  - 任务2: {task2.description}")
    print(f"  - 任务3: {task3.description}")

    # 3. 创建 Crew 并执行
    crew = create_crew(
        name="AI 研究团队",
        agents=[researcher, analyst, writer],
        tasks=[task1, task2, task3],
        process=ProcessType.SEQUENTIAL
    )

    print(f"\n开始执行...")
    result = crew.kickoff()

    print("\n执行完成！")
    print(f"成功任务: {result.success_count}")
    print(f"失败任务: {result.failed_count}")


if __name__ == "__main__":
    main()
