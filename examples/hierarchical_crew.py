"""
示例3：层级模式的开发团队
========================

演示 Manager-Worker 模式：
- Tech Lead 分析需求并分配任务
- Developer 完成编码任务
- QA Engineer 进行测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import create_agent
from src.task import create_task, TaskPriority
from src.crew import create_crew, ProcessType
from src.tools import get_coding_tools


def main():
    print("=" * 60)
    print("示例3：层级模式的开发团队")
    print("=" * 60)

    # 1. 创建团队
    tech_lead = create_agent(
        role="Tech Lead",
        goal="规划项目架构，分配开发任务",
        backstory="你是经验丰富的技术负责人，擅长项目管理。"
    )

    developer1 = create_agent(
        role="后端开发",
        goal="完成服务器端开发",
        backstory="你是后端开发专家，擅长 Python 和数据库。",
        tools=get_coding_tools()
    )

    developer2 = create_agent(
        role="前端开发",
        goal="完成用户界面开发",
        backstory="你是前端开发专家，擅长 React 和 CSS。"
    )

    qa_engineer = create_agent(
        role="QA 工程师",
        goal="确保代码质量",
        backstory="你是测试专家，擅长发现和报告问题。"
    )

    print(f"\n团队组成:")
    print(f"  - {tech_lead.role} (Manager)")
    print(f"  - {developer1.role} (Worker)")
    print(f"  - {developer2.role} (Worker)")
    print(f"  - {qa_engineer.role} (Worker)")

    # 2. 创建任务
    tasks = [
        create_task(
            description="设计系统架构",
            agent=tech_lead,
            priority=TaskPriority.HIGH
        ),
        create_task(
            description="开发 API 接口",
            agent=developer1,
            priority=TaskPriority.HIGH
        ),
        create_task(
            description="开发前端页面",
            agent=developer2,
            priority=TaskPriority.MEDIUM
        ),
        create_task(
            description="编写测试用例",
            agent=qa_engineer,
            priority=TaskPriority.MEDIUM
        ),
    ]

    print(f"\n任务数: {len(tasks)}")

    # 3. 创建 Crew 并执行
    crew = create_crew(
        name="开发团队",
        agents=[tech_lead, developer1, developer2, qa_engineer],
        tasks=tasks,
        process=ProcessType.HIERARCHICAL
    )

    print(f"\n开始执行...")
    result = crew.kickoff()

    print("\n执行完成！")


if __name__ == "__main__":
    main()
