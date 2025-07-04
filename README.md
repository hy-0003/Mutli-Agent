# ✨ 多智能体科研助手 ✨

欢迎来到 **多智能体科研助手**！🎉 这是一个基于 AutoGen 和 Deepseek 的Mutli-Agent协作系统，让你在短时间内完成科研/作业项目！

## 🚀 主要功能

- 🎓 **多智能体分工协作**：
  - 资料分析员：🔍 深入文献，整理核心知识点
  - 问题提出者：❓ 挖掘有趣科研问题
  - 代码编写者：💻 自动生成模型代码 & 可视化
  - Bug识别者：🐞 捕捉潜伏的程序瑕疵
  - 修复建议者：🔧 极速修复并输出完整代码
  - 验证测试者：✅ 一键跑模型、给出评价
  - 论文撰写者：📝 一键产出 Markdown 格式报告
- 🧪 **Code模型模拟**：
  - 自动构建模型，并附代码
  - 可视化传播曲线（`output/seir_output.png`）
- 📄 **自动论文生成**：
  - 结构标准：引言、方法、结果、讨论、结论
  - 一键生成 `output/report.md`，交作业so easy✨
- 📋 **日志记录**：
  - 每轮对话实时落地 `logs/round_<n>.log`
  - 回顾流程、分析思路，好评如潮👍

## 📂 项目结构

```bash
multi_agent_infection_research/
├── main.py               # 启动程序，召唤多智能体
├── utils/
│   └── logger.py         # 日志神器，记录对话 & 报告
├── output/
│   ├── seir_output.png   # 传播曲线萌图
│   └── report.md         # 自动生成的论文报告
├── logs/
│   └── round_<n>.log     # 每轮对话日志
├── .env                  # 环境变量（OpenAI API Key）
├── requirements.txt      # 依赖列表，一键安装
└── README.md             # 你正在看的说明文档
```

## ⚡ 快速开始

1. **克隆项目**
   
2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```
3. **配置 API Key**
   在根目录新建 `.env`，写入：
   ```env
   OPENAI_API_KEY=你的OpenAI_API_KEY
   ```
4. **运行程序**
   ```bash
   python main.py
   ```
   ✍️ 输入你的研究主题（例如 “传染病建模”），剩下的交给 Ta！

## ✨ 大学生速通作业流程 ✨

| 步骤 | 操作 & 输出 | 小贴士 |
|:---:|:-------------|:-------|
| 1️⃣ 环境准备 | 克隆+安装+配置 API Key | 5 分钟搞定 ⏱️ |
| 2️⃣ 运行主程序 | `python main.py` | 资料调研 → 问题设计 → 模型生成 → 报告写作，一气呵成！💨 |
| 3️⃣ 查看结果 | - `output/report.md` 论文<br>- `output/seir_output.png` 图表<br>- `logs/` 对话日志 | 直接复制粘贴，无需二次加工 ✂️ |
| 4️⃣ 可选美化 | 编辑 Markdown<br>转 PDF：<br>```bash pandoc output/report.md -o final_report.pdf ``` | 论文瞬间高大上 🎓 |
| 5️⃣ 提交作业 | ✓ 最终报告 PDF<br>✓ 图表 PPT<br>✓ 简短演示视频 | A+ 向你招手！🏆 |


> 💡 **小提示**：整个流程 **1-2 小时** 内可完成，实践证明超高效率！

---

© 2025 多智能体科研助手  | 精心打造 ✨ Happy Research-ing! 🥳


# ✨ Multi-Agent Research Assistant ✨

Welcome to the **Multi-Agent Research Assistant**! 🎉 This collaborative system powered by AutoGen and DeepSeek helps you complete research/homework projects efficiently!

## 🚀 Core Features

- 🎓 **Multi-Agent Collaboration**:
  - Data Analyst: 🔍 Literature deep-dives & core knowledge organization
  - Problem Proposer: ❓ Identifies compelling research questions
  - Code Engineer: 💻 Auto-generates model code & visualizations
  - Bug Identifier: 🐞 Detects hidden program flaws
  - Fix Advisor: 🔧 Rapid debugging & complete code output
  - Validation Tester: ✅ One-click model execution & evaluation
  - Paper Writer: 📝 Generates Markdown-formatted reports
- 🧪 **Model Simulation**:
  - Automatic model construction with complete code
  - Visualization of propagation curves (`output/seir_output.png`)
- 📄 **Automated Paper Generation**:
  - Standard structure: Introduction, Methods, Results, Discussion, Conclusion
  - One-click generation of `output/report.md`
- 📋 **Logging System**:
  - Real-time conversation logging to `logs/round_<n>.log`
  - Process review & reasoning analysis

## 📂 Project Structure

```bash
multi_agent_infection_research/
├── main.py               # Launches multi-agent system
├── utils/
│   └── logger.py         # Conversation & report logger
├── output/
│   ├── seir_output.png   # Propagation curve visualization
│   └── report.md         # Auto-generated research paper
├── logs/
│   └── round_<n>.log     # Per-round conversation logs
├── .env                  # Environment variables (OpenAI API Key)
├── requirements.txt      # Dependency list
└── README.md             # This documentation
```

## ⚡ Quick Start

1. **Clone Repository**
   
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Key**
   Create `.env` in root directory:
   ```env
   OPENAI_API_KEY=your_OpenAI_API_KEY
   ```
4. **Run Program**
   ```bash
   python main.py
   ```
   ✍️ Enter your research topic (e.g. "Epidemic Modeling") and let the system work!

## ✨ Student Assignment Workflow ✨

| Step | Action & Output | Tips |
|:---:|:----------------|:-----|
| 1️⃣ Setup | Clone + Install + Configure API Key | ~5 minutes ⏱️ |
| 2️⃣ Execute | `python main.py` | Research → Problem design → Model generation → Report writing - seamless workflow! 💨 |
| 3️⃣ Get Results | - `output/report.md`<br>- `output/seir_output.png`<br>- `logs/` | Directly usable outputs ✂️ |
| 4️⃣ Optional Polish | Edit Markdown<br>Convert to PDF:<br>```bash pandoc output/report.md -o final_report.pdf ``` | Professional formatting 🎓 |
| 5️⃣ Submit | ✓ Final PDF report<br>✓ Visualization slides<br>✓ Short demo video | A+ guaranteed! 🏆 |

> 💡 **Pro Tip**: Complete workflow in **1-2 hours** - proven efficiency!

---

© 2025 Multi-Agent Research Assistant | Crafted with care ✨ Happy Researching! 🥳
