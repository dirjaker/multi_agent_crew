"""
工具集模块
=========

内置工具集合，供 Agent 使用。

工具类型：
- 搜索工具：信息检索
- 分析工具：数据分析
- 生成工具：内容生成
- 交互工具：用户交互
"""

from typing import Any, Dict, List
from .agent import Tool


class SearchTool(Tool):
    """搜索工具"""

    def __init__(self):
        super().__init__(
            name="search",
            description="搜索信息，获取相关资料",
            function=self._search
        )

    def _search(self, query: str = "", **kwargs) -> str:
        """模拟搜索"""
        # 实际项目中这里会调用搜索引擎 API
        return f"搜索 '{query}' 的结果：找到 10 条相关信息"


class AnalysisTool(Tool):
    """分析工具"""

    def __init__(self):
        super().__init__(
            name="analysis",
            description="分析数据，提取关键信息",
            function=self._analyze
        )

    def _analyze(self, data: str = "", **kwargs) -> str:
        """模拟分析"""
        return f"数据分析结果：\n- 数据量: {len(data)} 字符\n- 关键词: 示例, 分析"


class WritingTool(Tool):
    """写作工具"""

    def __init__(self):
        super().__init__(
            name="writing",
            description="生成文本内容",
            function=self._write
        )

    def _write(self, topic: str = "", style: str = "professional", **kwargs) -> str:
        """模拟写作"""
        return f"关于 '{topic}' 的{style}文章已生成。"


class CodeTool(Tool):
    """代码工具"""

    def __init__(self):
        super().__init__(
            name="code",
            description="生成或分析代码",
            function=self._code
        )

    def _code(self, task: str = "", language: str = "python", **kwargs) -> str:
        """模拟代码生成"""
        return f"# {language} 代码\n# 任务: {task}\nprint('Hello, World!')"


class CalculatorTool(Tool):
    """计算工具"""

    def __init__(self):
        super().__init__(
            name="calculator",
            description="执行数学计算",
            function=self._calculate
        )

    def _calculate(self, expression: str = "", **kwargs) -> str:
        """执行计算"""
        try:
            result = eval(expression)  # 仅用于演示，实际应使用安全的计算库
            return f"计算结果: {expression} = {result}"
        except Exception as e:
            return f"计算错误: {e}"


# 预定义工具集合
def get_default_tools() -> List[Tool]:
    """获取默认工具集"""
    return [
        SearchTool(),
        AnalysisTool(),
        WritingTool(),
        CodeTool(),
        CalculatorTool()
    ]


def get_research_tools() -> List[Tool]:
    """获取研究工具集"""
    return [SearchTool(), AnalysisTool()]


def get_writing_tools() -> List[Tool]:
    """获取写作工具集"""
    return [SearchTool(), WritingTool()]


def get_coding_tools() -> List[Tool]:
    """获取编程工具集"""
    return [CodeTool(), CalculatorTool()]
