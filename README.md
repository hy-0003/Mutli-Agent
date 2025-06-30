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