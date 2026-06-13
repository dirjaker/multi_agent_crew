"""
Multi-Agent Crew macOS GUI
===========================
tkinter 桌面应用，提供多智能体协作功能的图形界面
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.agent import create_agent
from src.task import create_task, TaskStatus
from src.crew import create_crew, ProcessType


class CrewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Agent Crew - 多智能体协作系统")
        self.root.geometry("900x650")
        self.root.configure(bg="#0d1117")
        self.agents = {}
        self.tasks = {}
        self.crews = {}
        self._build_ui()

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#0d1117")
        style.configure("TNotebook.Tab", background="#161b22", foreground="#c9d1d9", padding=[12, 6])
        style.map("TNotebook.Tab", background=[("selected", "#58a6ff")], foreground=[("selected", "#fff")])
        style.configure("TFrame", background="#0d1117")
        style.configure("TLabel", background="#0d1117", foreground="#c9d1d9")
        style.configure("TButton", background="#238636", foreground="#fff")
        style.map("TButton", background=[("active", "#2ea043")])

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # 创建 Agent Tab
        agent_frame = ttk.Frame(notebook)
        notebook.add(agent_frame, text="创建 Agent")
        ttk.Label(agent_frame, text="角色:").pack(anchor=tk.W, padx=8, pady=(8,2))
        self.agent_role = tk.Entry(agent_frame, bg="#0d1117", fg="#c9d1d9", insertbackground="#c9d1d9", font=("Menlo", 12))
        self.agent_role.pack(fill=tk.X, padx=8)
        ttk.Label(agent_frame, text="目标:").pack(anchor=tk.W, padx=8, pady=(8,2))
        self.agent_goal = tk.Entry(agent_frame, bg="#0d1117", fg="#c9d1d9", insertbackground="#c9d1d9", font=("Menlo", 12))
        self.agent_goal.pack(fill=tk.X, padx=8)
        ttk.Label(agent_frame, text="背景故事:").pack(anchor=tk.W, padx=8, pady=(8,2))
        self.agent_backstory = scrolledtext.ScrolledText(agent_frame, height=4, bg="#0d1117", fg="#c9d1d9",
                                                           insertbackground="#c9d1d9", font=("Menlo", 12))
        self.agent_backstory.pack(fill=tk.X, padx=8)
        ttk.Button(agent_frame, text="创建 Agent", command=self.create_agent).pack(anchor=tk.W, padx=8, pady=6)
        self.agent_result = scrolledtext.ScrolledText(agent_frame, height=4, bg="#161b22", fg="#c9d1d9",
                                                        font=("Menlo", 11), state=tk.DISABLED)
        self.agent_result.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))

        # 创建任务 Tab
        task_frame = ttk.Frame(notebook)
        notebook.add(task_frame, text="创建任务")
        ttk.Label(task_frame, text="任务描述:").pack(anchor=tk.W, padx=8, pady=(8,2))
        self.task_desc = scrolledtext.ScrolledText(task_frame, height=3, bg="#0d1117", fg="#c9d1d9",
                                                     insertbackground="#c9d1d9", font=("Menlo", 12))
        self.task_desc.pack(fill=tk.X, padx=8)
        ttk.Label(task_frame, text="指派 Agent (角色名):").pack(anchor=tk.W, padx=8, pady=(8,2))
        self.task_agent = tk.Entry(task_frame, bg="#0d1117", fg="#c9d1d9", insertbackground="#c9d1d9", font=("Menlo", 12))
        self.task_agent.pack(fill=tk.X, padx=8)
        ttk.Button(task_frame, text="创建任务", command=self.create_task).pack(anchor=tk.W, padx=8, pady=6)
        self.task_result = scrolledtext.ScrolledText(task_frame, height=4, bg="#161b22", fg="#c9d1d9",
                                                       font=("Menlo", 11), state=tk.DISABLED)
        self.task_result.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))

        # 执行 Crew Tab
        crew_frame = ttk.Frame(notebook)
        notebook.add(crew_frame, text="创建并执行 Crew")
        ttk.Label(crew_frame, text="Crew 名称:").pack(anchor=tk.W, padx=8, pady=(8,2))
        self.crew_name = tk.Entry(crew_frame, bg="#0d1117", fg="#c9d1d9", insertbackground="#c9d1d9", font=("Menlo", 12))
        self.crew_name.pack(fill=tk.X, padx=8)
        ttk.Label(crew_frame, text="Agent 角色 (逗号分隔):").pack(anchor=tk.W, padx=8, pady=(8,2))
        self.crew_agents = tk.Entry(crew_frame, bg="#0d1117", fg="#c9d1d9", insertbackground="#c9d1d9", font=("Menlo", 12))
        self.crew_agents.pack(fill=tk.X, padx=8)
        ttk.Label(crew_frame, text="执行模式:").pack(anchor=tk.W, padx=8, pady=(8,2))
        self.process_var = tk.StringVar(value="sequential")
        pf = ttk.Frame(crew_frame)
        pf.pack(fill=tk.X, padx=8)
        for val, text in [("sequential", "顺序"), ("parallel", "并行"), ("hierarchical", "层级")]:
            ttk.Radiobutton(pf, text=text, variable=self.process_var, value=val).pack(side=tk.LEFT, padx=8)
        bf = ttk.Frame(crew_frame)
        bf.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(bf, text="创建并执行", command=self.run_crew).pack(side=tk.LEFT)
        self.crew_result = scrolledtext.ScrolledText(crew_frame, height=12, bg="#161b22", fg="#c9d1d9",
                                                       font=("Menlo", 11), state=tk.DISABLED)
        self.crew_result.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))

    def _set(self, widget, text):
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.config(state=tk.DISABLED)

    def create_agent(self):
        role = self.agent_role.get().strip()
        goal = self.agent_goal.get().strip()
        backstory = self.agent_backstory.get("1.0", tk.END).strip()
        if not role or not goal:
            messagebox.showwarning("提示", "角色和目标不能为空")
            return
        agent = create_agent(role=role, goal=goal, backstory=backstory)
        self.agents[role] = agent
        self._set(self.agent_result, f"已创建 Agent: {role}\n状态: {agent.state.value}")

    def create_task(self):
        desc = self.task_desc.get("1.0", tk.END).strip()
        agent_role = self.task_agent.get().strip()
        if not desc or not agent_role:
            messagebox.showwarning("提示", "任务描述和 Agent 角色不能为空")
            return
        if agent_role not in self.agents:
            messagebox.showerror("错误", f"Agent '{agent_role}' 不存在，请先创建")
            return
        task = create_task(description=desc, agent=self.agents[agent_role])
        self.tasks[desc] = task
        self._set(self.task_result, f"已创建任务: {desc}\n状态: {task.status.value}")

    def run_crew(self):
        name = self.crew_name.get().strip()
        roles = [r.strip() for r in self.crew_agents.get().split(",") if r.strip()]
        if not name or not roles:
            messagebox.showwarning("提示", "Crew 名称和 Agent 角色不能为空")
            return
        crew_agents = []
        for role in roles:
            if role not in self.agents:
                messagebox.showerror("错误", f"Agent '{role}' 不存在")
                return
            crew_agents.append(self.agents[role])

        # 用所有已创建的任务
        crew_tasks = list(self.tasks.values())
        if not crew_tasks:
            messagebox.showwarning("提示", "请先创建至少一个任务")
            return

        process_map = {"sequential": ProcessType.SEQUENTIAL, "parallel": ProcessType.PARALLEL, "hierarchical": ProcessType.HIERARCHICAL}
        crew = create_crew(name=name, agents=crew_agents, tasks=crew_tasks, process=process_map[self.process_var.get()])
        self._set(self.crew_result, f"正在执行 Crew: {name}...\n")
        self.root.update()
        result = crew.kickoff()
        summary = result.summary() if hasattr(result, "summary") else str(result)
        self._set(self.crew_result, summary)


def main():
    root = tk.Tk()
    CrewApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
