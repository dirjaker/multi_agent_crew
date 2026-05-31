"""
Multi-Agent Crew 协作系统
========================

基于 CrewAI 模式的多智能体协作框架。

核心概念：
1. Agent: 具有特定角色和能力的智能体
2. Task: 需要完成的任务
3. Crew: 多个 Agent 组成的团队
4. Process: 任务执行流程（顺序/并行/层级）

支持的协作模式：
- Sequential: 顺序执行，前一个 Agent 的输出作为下一个的输入
- Parallel: 并行执行，独立完成各自任务
- Hierarchical: 层级模式，Manager Agent 分配任务给 Worker Agents

作者：dirjaker
创建日期：2026-05-30
版本：1.0.0
"""

__version__ = "1.0.0"
__author__ = "dirjaker"
