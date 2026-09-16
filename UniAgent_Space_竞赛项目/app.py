import streamlit as st
import base64
from pathlib import Path

from agents.config import AGENTS
from agents.engine import AgentEngine


# ============================================================
# 页面设置
# ============================================================

st.set_page_config(
    page_title="UniAgent Space",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 读取背景图片
# background.jpg 必须和 app.py 在同一个文件夹
# ============================================================

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


BASE_DIR = Path(__file__).resolve().parent

bg_image_path = BASE_DIR / "background.jpg"

bg_image = get_base64_image(bg_image_path)


# ============================================================
# CSS 样式
# ============================================================

st.markdown(
    f"""
<style>

.stApp {{
    background-image:
        linear-gradient(
            rgba(5, 10, 20, 0.76),
            rgba(5, 10, 20, 0.76)
        ),
        url("data:image/jpeg;base64,{bg_image}");

    background-size: cover;
    background-position: center center;
    background-attachment: fixed;
}}


/* 主标题 */

.main-title {{
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}}


/* 副标题 */

.subtitle {{
    font-size: 18px;
    opacity: .75;
    margin-bottom: 22px;
}}


/* Agent 卡片 */

.agent-card {{
    padding: 18px;
    border: 1px solid rgba(255,255,255,.16);
    border-radius: 16px;
    min-height: 185px;
    background: rgba(18, 21, 30, 0.90);
    box-sizing: border-box;
    margin-bottom: 8px;
}}


/* Agent 图标 */

.agent-icon {{
    font-size: 30px;
    line-height: 1.2;
    margin-bottom: 12px;
}}


/* Agent 名称 */

.agent-name {{
    font-size: 17px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 7px;
}}


/* Agent 分类 */

.agent-category {{
    font-size: 13px;
    color: rgba(255,255,255,.68);
    line-height: 1.5;
    margin-bottom: 12px;
}}


/* Agent 功能介绍 */

.agent-goal {{
    font-size: 13px;
    color: rgba(255,255,255,.70);
    line-height: 1.7;
}}


/* 左侧栏 */

[data-testid="stSidebar"] {{
    background: rgba(20, 21, 30, 0.96);
}}


/* 聊天输入框 */

[data-testid="stChatInput"] {{
    background: rgba(20, 21, 30, 0.92);
}}


/* 分割线 */

hr {{
    border-color: rgba(255,255,255,.12);
}}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = {}

if "selected" not in st.session_state:
    st.session_state.selected = "study"


# ============================================================
# Agent Engine
# ============================================================

engine = AgentEngine()

agent_map = {
    a["id"]: a
    for a in AGENTS
}

selected_agent = agent_map[
    st.session_state.selected
]


# ============================================================
# 左侧导航栏
# ============================================================

with st.sidebar:

    st.title("🎓 UniAgent Space")

    st.caption("大学生多智能体空间")

    st.divider()

    st.subheader("10 个独立智能体")

    # ========================================================
    # 左侧 Agent 顺序完全按照 AGENTS
    # ========================================================

    for a in AGENTS:

        if st.button(
            f"{a['icon']} {a['name']}",
            key=f"nav_{a['id']}",
            use_container_width=True
        ):

            st.session_state.selected = a["id"]

            st.rerun()

    st.divider()

    st.info(
        "提示：配置 OPENAI_API_KEY 后，"
        "10 个 Agent 可切换到真实大模型模式。"
    )


# ============================================================
# 主页面标题
# ============================================================

st.markdown(
    '<div class="main-title">🎓 UniAgent Space</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">面向大学生学习、科研、技术与就业场景的多智能体空间</div>',
    unsafe_allow_html=True
)


# ============================================================
# 10 个 Agent 卡片
#
# 这里和左侧使用完全相同的 AGENTS。
#
# AGENTS[0] = 左侧第1个 = 中间第1个
# AGENTS[1] = 左侧第2个 = 中间第2个
# AGENTS[2] = 左侧第3个 = 中间第3个
# ...
# AGENTS[9] = 左侧第10个 = 中间第10个
# ============================================================

cols = st.columns(5)

for i, a in enumerate(AGENTS):

    with cols[i % 5]:

        # ====================================================
        # 注意：
        # 这里故意使用连续 HTML，
        # 不在 HTML 中加入空白行，
        # 避免 Streamlit 把 HTML 标签显示成文字。
        # ====================================================

        card_html = (
            '<div class="agent-card">'
            f'<div class="agent-icon">{a["icon"]}</div>'
            f'<div class="agent-name">{a["name"]}</div>'
            f'<div class="agent-category">{a["category"]} · 独立 Prompt · 独立任务</div>'
            f'<div class="agent-goal">{a["goal"]}</div>'
            '</div>'
        )

        st.markdown(
            card_html,
            unsafe_allow_html=True
        )


# ============================================================
# 分割线
# ============================================================

st.divider()


# ============================================================
# 当前选中的 Agent
# ============================================================

a = selected_agent

st.markdown(
    f"## {a['icon']} {a['name']}"
)

st.caption(
    f"{a['category']} · {a['goal']}"
)

st.write(
    "**能力工具：** "
    + " · ".join(a["tools"])
)


# ============================================================
# 数据分析 Agent 文件上传
# ============================================================

if a["id"] == "data":

    uploaded = st.file_uploader(
        "可选：上传 CSV / Excel 数据文件",
        type=["csv", "xlsx"]
    )

    if uploaded:

        st.success(
            f"已接收文件：{uploaded.name}"
            "（演示界面已完成文件入口）"
        )


# ============================================================
# 聊天历史
# ============================================================

history = st.session_state.messages.setdefault(
    a["id"],
    []
)


for m in history:

    with st.chat_message(
        m["role"]
    ):

        st.markdown(
            m["content"]
        )


# ============================================================
# 示例任务
# ============================================================

example_map = {

    "study":
        "我有高数、Python、经济学三门课，"
        "考试分别在下个月，我每天能学习3小时，"
        "帮我安排计划。",

    "homework":
        "请帮我理解这道题的解题思路，"
        "不要只给最终答案。",

    "research":
        "我的论文主题是大学生 AI 素养，"
        "请帮我设计研究问题和论文结构。",

    "literature":
        "我有5篇关于生成式AI教育应用的论文摘要，"
        "应该如何做文献综述？",

    "coding":
        "Python 报错：IndexError: list index out of range，"
        "我应该怎么排查？",

    "data":
        "我有一份学生成绩 CSV，"
        "想分析平均分、分布和异常值，"
        "应该怎么做？",

    "presentation":
        "我要答辩一个校园二手交易平台项目，"
        "请帮我设计10页PPT。",

    "email":
        "我想给老师写邮件，"
        "请老师帮我看一下课程项目，"
        "怎么写比较礼貌？",

    "career":
        "我想申请数据分析实习，"
        "简历应该重点突出哪些能力？",

    "interview":
        "我要参加 Python 数据分析实习面试，"
        "请开始模拟面试。",
}


example = example_map[
    a["id"]
]

st.caption(
    f"示例任务：{example}"
)


# ============================================================
# Chat Input
# ============================================================

user_input = st.chat_input(
    f"向 {a['name']} 提问……"
)


if user_input:

    history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(
            user_input
        )


    with st.chat_message("assistant"):

        with st.spinner(
            "Agent 正在执行任务……"
        ):

            answer = engine.run(
                a,
                user_input,
                history
            )

        st.markdown(
            answer
        )


    history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ============================================================
# 页面底部
# ============================================================

st.divider()

st.caption(
    "UniAgent Space · 10 个独立、完整、"
    "可运行的有效智能体 · 课程竞赛演示版"
)
