import streamlit as st
import base64

from agents.config import AGENTS
from agents.engine import AgentEngine


st.set_page_config(
    page_title="UniAgent Space",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 背景图片
# background.jpg 需要和 app.py 放在同一个文件夹
# ============================================================

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


bg_image = get_base64_image("background.jpg")


# ============================================================
# 原有页面样式 + 背景图片
# ============================================================

st.markdown(f"""
<style>

/* ==============================
   页面背景图片
   ============================== */

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


/* ==============================
   原有标题
   ============================== */

.main-title {{
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}}


/* ==============================
   原有副标题
   ============================== */

.subtitle {{
    font-size: 18px;
    opacity: .75;
    margin-bottom: 22px;
}}


/* ==============================
   原有 Agent 卡片
   ============================== */

.agent-card {{
    padding: 16px;
    border: 1px solid rgba(128,128,128,.25);
    border-radius: 16px;
    min-height: 150px;
}}


/* ==============================
   原有小文字
   ============================== */

.small {{
    font-size: 13px;
    opacity: .72;
}}


/* ==============================
   原有 Badge
   ============================== */

.badge {{
    display: inline-block;
    padding: 4px 8px;
    border-radius: 10px;
    background: rgba(80,130,255,.12);
}}


/* ==============================
   侧边栏保持原来的深色风格
   ============================== */

[data-testid="stSidebar"] {{
    background: rgba(20, 21, 30, 0.95);
}}


/* ==============================
   不改变聊天输入框功能
   ============================== */

[data-testid="stChatInput"] {{
    background: rgba(20, 21, 30, 0.90);
}}


/* ==============================
   分割线
   ============================== */

hr {{
    border-color: rgba(128,128,128,.25);
}}

</style>
""", unsafe_allow_html=True)


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

agent_map = {a["id"]: a for a in AGENTS}

selected_agent = agent_map[st.session_state.selected]


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.title("🎓 UniAgent Space")

    st.caption("大学生多智能体空间")

    st.divider()

    st.subheader("10 个独立智能体")

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
# 页面标题
# ============================================================

st.markdown(
    '<div class="main-title">🎓 UniAgent Space</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '面向大学生学习、科研、技术与就业场景的多智能体空间'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# Agent Cards
# ============================================================

cols = st.columns(5)

for i, a in enumerate(AGENTS):

    with cols[i % 5]:

        st.markdown(
            f"""
            <div class="agent-card">

                <div style="font-size:30px">
                    {a['icon']}
                </div>

                <b>{a['name']}</b>
                <br>

                <span class="small">
                    {a['category']} · 独立 Prompt · 独立任务
                </span>

                <br><br>

                <span class="small">
                    {a['goal']}
                </span>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# Agent 分割线
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
    "**能力工具：** " + " · ".join(a["tools"])
)


# ============================================================
# Data Agent 文件上传
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
# Chat History
# ============================================================

history = st.session_state.messages.setdefault(
    a["id"],
    []
)


for m in history:

    with st.chat_message(m["role"]):

        st.markdown(m["content"])


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


example = example_map[a["id"]]

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

        st.markdown(user_input)


    with st.chat_message("assistant"):

        with st.spinner(
            "Agent 正在执行任务……"
        ):

            answer = engine.run(
                a,
                user_input,
                history
            )

        st.markdown(answer)


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
