"""
Multi-Agent Crew Web API
========================
FastAPI 服务，暴露多智能体协作功能的 REST 接口
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from src.agent import create_agent, AgentState
from src.task import create_task, TaskStatus
from src.crew import create_crew, ProcessType

app = FastAPI(title="Multi-Agent Crew API", version="1.0.0")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost,http://127.0.0.1").split(",")
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 存储已创建的 crew 实例
crews: Dict[str, Any] = {}
agents: Dict[str, Any] = {}
tasks: Dict[str, Any] = {}


class AgentCreateRequest(BaseModel):
    role: str
    goal: str
    backstory: str = ""


class TaskCreateRequest(BaseModel):
    description: str
    agent_role: str  # 对应 agent 的 role


class CrewCreateRequest(BaseModel):
    name: str
    agent_roles: List[str]
    task_descriptions: List[str]
    process: str = "sequential"


class CrewRunRequest(BaseModel):
    crew_name: str


@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = os.path.join(static_dir, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.post("/api/agents")
async def create_agent_api(req: AgentCreateRequest):
    """创建 Agent"""
    agent = create_agent(role=req.role, goal=req.goal, backstory=req.backstory)
    agents[req.role] = agent
    return {"status": "ok", "role": req.role, "state": agent.state.value}


@app.get("/api/agents")
async def list_agents():
    """列出所有 Agent"""
    return {
        "agents": [
            {"role": a.role, "goal": a.goal, "state": a.state.value}
            for a in agents.values()
        ]
    }


@app.post("/api/tasks")
async def create_task_api(req: TaskCreateRequest):
    """创建任务"""
    if req.agent_role not in agents:
        raise HTTPException(404, f"Agent '{req.agent_role}' 不存在")
    task = create_task(description=req.description, agent=agents[req.agent_role])
    tasks[req.description] = task
    return {"status": "ok", "description": req.description, "status_val": task.status.value}


@app.get("/api/tasks")
async def list_tasks():
    """列出所有任务"""
    return {
        "tasks": [
            {"description": t.description, "status": t.status.value, "agent": t.agent.role if t.agent else None}
            for t in tasks.values()
        ]
    }


@app.post("/api/crews")
async def create_crew_api(req: CrewCreateRequest):
    """创建 Crew"""
    crew_agents = []
    for role in req.agent_roles:
        if role not in agents:
            raise HTTPException(404, f"Agent '{role}' 不存在")
        crew_agents.append(agents[role])

    crew_tasks = []
    for desc in req.task_descriptions:
        if desc in tasks:
            crew_tasks.append(tasks[desc])
        else:
            raise HTTPException(404, f"任务 '{desc}' 不存在")

    process_map = {
        "sequential": ProcessType.SEQUENTIAL,
        "parallel": ProcessType.PARALLEL,
        "hierarchical": ProcessType.HIERARCHICAL,
    }
    process = process_map.get(req.process, ProcessType.SEQUENTIAL)

    crew = create_crew(name=req.name, agents=crew_agents, tasks=crew_tasks, process=process)
    crews[req.name] = crew
    return {"status": "ok", "name": req.name, "process": req.process}


@app.get("/api/crews")
async def list_crews():
    """列出所有 Crew"""
    return {
        "crews": [
            {"name": c.name, "process": c.process.value, "agents": len(c.agents), "tasks": len(c.tasks)}
            for c in crews.values()
        ]
    }


@app.post("/api/crews/run")
async def run_crew(req: CrewRunRequest):
    """执行 Crew"""
    if req.crew_name not in crews:
        raise HTTPException(404, f"Crew '{req.crew_name}' 不存在")
    crew = crews[req.crew_name]
    result = crew.kickoff()
    if isinstance(result, dict):
        return result
    return {"result": str(result)}


@app.get("/api/stats")
async def stats():
    """获取统计信息"""
    return {
        "agents": len(agents),
        "tasks": len(tasks),
        "crews": len(crews),
        "agent_states": {
            a.role: a.state.value for a in agents.values()
        },
        "task_statuses": {
            t.description[:50]: t.status.value for t in tasks.values()
        }
    }


@app.delete("/api/reset")
async def reset():
    """重置所有数据"""
    crews.clear()
    agents.clear()
    tasks.clear()
    return {"status": "ok", "message": "已重置所有数据"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
