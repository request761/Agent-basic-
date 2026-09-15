# 🎓 UniAgent Space

面向大学生的多智能体空间竞赛项目。

## 1. 项目包含的 10 个独立 Agent

1. 学习规划 Agent
2. 作业辅导 Agent
3. 科研论文 Agent
4. 文献综述 Agent
5. 编程导师 Agent
6. 数据分析 Agent
7. 演示汇报 Agent
8. 校园邮件 Agent
9. 求职简历 Agent
10. 模拟面试 Agent

每个 Agent 都具有独立的角色定义、任务目标、工作流程和工具说明。

## 2. 本地运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

浏览器打开终端显示的本地地址即可。

## 3. 真实大模型模式

没有 API Key 时，项目仍可以运行“演示模式”，用于检查 10 个 Agent 的入口和独立工作流。

部署正式作品时，在环境变量中配置：

```text
OPENAI_API_KEY=你的Key
OPENAI_MODEL=gpt-5.6-luna
```

然后重新启动即可。

## 4. 作品提交建议

空间地址：提交云平台部署后的 HTTPS 地址。

演示视频：建议 2～4 分钟，依次展示：
- 首页 10 个 Agent
- 学习规划 Agent
- 编程导师 Agent
- 数据分析 Agent
- 模拟面试 Agent
- 最后展示 10 个 Agent 的独立配置

## 5. 项目亮点

- 10 个独立专业智能体
- 教育、科研、技术、就业四类真实场景
- 统一智能体空间入口
- 独立 System Prompt
- 工具能力说明
- 可切换演示模式/真实大模型模式
- 适合在线运行与录制演示视频
