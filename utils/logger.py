# 📁 文件：utils/logger.py
# 日志追踪工具：记录多智能体协作内容

import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def log_message(role, message, round_id):
    """按轮次记录Agent的输出信息"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = os.path.join(LOG_DIR, f"round_{round_id}.log")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{role}]:\n{message}\n{'-'*60}\n")


def log_summary_report(content, filename="summary_report.md"):
    """将最终撰写者的报告保存到output/"""
    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", filename), "w", encoding="utf-8") as f:
        f.write(content)


# 示例用法：
if __name__ == '__main__':
    log_message("Researcher", "以下是模型的背景分析......", round_id=1)
    log_summary_report("# 项目总结报告\n这是最终输出。")
