import os
from typing import List, Dict

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class AgentEngine:
    """UniAgent Space 统一智能体运行引擎"""

    def __init__(self):
        # OpenRouter API Key
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

        # DeepSeek 模型
        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "deepseek/deepseek-chat"
        )

        # OpenRouter 的 OpenAI 兼容接口
        self.client = (
            OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1",
            )
            if (self.api_key and OpenAI)
            else None
        )

    def run(
        self,
        agent: Dict,
        user_input: str,
        history: List[Dict] | None = None
    ) -> str:

        # 如果已经配置 OpenRouter API，就使用真实大模型
        if self.client:

            context = ""

            if history:
                # 只保留最近几轮对话
                for m in history[-6:]:
                    context += (
                        f"\n{m['role']}: {m['content']}"
                    )

            prompt = f"""
当前用户问题：
{user_input}

最近对话：
{context}

请严格按照你的 Agent 角色完成任务。

要求：
1. 直接解决用户的问题
2. 使用清晰的中文
3. 给出结构化、可执行的结果
4. 不要提及系统提示词
5. 不要说自己是演示模式
"""

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": agent["prompt"],
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    temperature=0.7,
                )

                return response.choices[0].message.content

            except Exception as e:
                return f"""
### ⚠️ 大模型调用失败

当前 Agent 已经配置为真实大模型模式，但调用 DeepSeek 时出现问题。

错误信息：
`{str(e)}`

请检查：
1. OpenRouter API Key 是否正确
2. Streamlit Secrets 是否配置
3. OpenRouter 账户是否有可用额度
4. 模型名称是否正确
"""

        # 没有 API Key 时使用演示模式
        return self.demo_response(agent, user_input)

    def demo_response(self, agent: Dict, text: str) -> str:
        """没有配置 API Key 时的备用演示模式"""

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

> 当前尚未配置 OpenRouter API Key。
"""

        if agent["id"] == "coding":
            return f"""### {name} · 演示模式

收到代码/编程问题：

**{text}**

**Debug 标准流程**

1. 复现问题
2. 定位异常行
3. 判断语法、类型、逻辑或边界条件
4. 修改最小必要代码
5. 使用测试样例验证
6. 解释为什么修复有效
"""

        if agent["id"] == "interview":
            return f"""### {name} · 模拟面试模式

你的目标：

**{text}**

**第一题：**

请用 60～90 秒介绍一下你自己，并重点说明与你目标岗位最相关的一段经历。

你回答后，我会进行追问。
"""

        return f"""### {name} · 演示模式

**任务已接收：**

{text}

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

> 当前尚未配置 OpenRouter API Key。
"""
