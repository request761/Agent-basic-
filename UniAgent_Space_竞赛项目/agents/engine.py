import os
from typing import List, Dict

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class AgentEngine:
    """统一的智能体运行引擎：每个 Agent 保留独立角色、目标、Prompt 和工具说明。"""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
        self.client = OpenAI(api_key=self.api_key) if (self.api_key and OpenAI) else None

    def run(self, agent: Dict, user_input: str, history: List[Dict] | None = None) -> str:
        if self.client:
            context = ""
            if history:
                # 只带入最近几轮，避免上下文无限增长
                for m in history[-6:]:
                    context += f"\n{m['role']}: {m['content']}"
            prompt = f"""当前用户问题：
{user_input}

最近对话：
{context}

请严格按照你的 Agent 角色完成任务。"""
            response = self.client.responses.create(
                model=self.model,
                instructions=agent["prompt"],
                input=prompt,
            )
            return response.output_text

        return self.demo_response(agent, user_input)

    def demo_response(self, agent: Dict, text: str) -> str:
        """没有 API Key 时也能运行，用于作品在线展示和功能验收。"""
        name = agent["name"]
        if agent["id"] == "study":
            return f"""### {name} · 演示模式

我已接收你的需求：**{text}**

**建议执行流程**
1. 明确课程、考试日期和当前掌握程度
2. 按“考试紧迫度 × 掌握薄弱度”计算优先级
3. 把目标拆成每日 30～90 分钟的小任务
4. 每 3 天进行一次复盘，根据完成情况调整

**示例计划**
- 第 1 阶段：补齐基础知识
- 第 2 阶段：章节练习 + 错题整理
- 第 3 阶段：模拟题 + 查漏补缺

> 这是无 API Key 的演示模式。部署后配置 OPENAI_API_KEY，即可切换为真实大模型运行。"""

        if agent["id"] == "coding":
            return f"""### {name} · 演示模式

收到代码/编程问题：**{text}**

**Debug 标准流程**
1. 复现问题
2. 定位异常行
3. 判断语法、类型、逻辑或边界条件
4. 修改最小必要代码
5. 用测试样例验证
6. 解释为什么修复有效

请把完整代码和报错信息发给我，我会按这个流程逐行分析。"""

        if agent["id"] == "interview":
            return f"""### {name} · 模拟面试模式

你的目标：**{text}**

**第一题：**
请用 60～90 秒介绍一下你自己，并重点说明与你目标岗位最相关的一段经历。

你回答后，我会从：
- 内容完整度
- 逻辑结构
- 岗位匹配度
- 表达清晰度
- 可信度

五个维度评分，并进行追问。"""

        return f"""### {name} · 演示模式

**任务已接收：** {text}

**Agent 工作流**
1. 理解用户目标
2. 提取关键约束
3. 按本 Agent 的专业规则进行分析
4. 输出结构化结果
5. 给出下一步可执行建议

**当前 Agent 的核心能力**
{agent['goal']}

**配置工具**
{', '.join(agent['tools'])}

> 当前页面未配置大模型 API Key，因此使用内置演示结果。部署时加入 API Key 后，这 10 个 Agent 会由真实大模型驱动。"""
