# 📁 main.py
# 多智能体协作入口（AutoGen） - 支持模型切换的DeepSeek版本（完整代码捕获版，已支持Verifier捕获并保存用时与模型报告)

import os
import re
import time
import argparse
from datetime import datetime
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv

load_dotenv()

# ==== 命令行参数解析 ====
parser = argparse.ArgumentParser(description='多智能体科研协作系统')
parser.add_argument('--model', type=str, default='mixed', choices=['chat', 'coder', 'mixed'],
                    help="模型选择: 'chat'-全用deepseek-chat, 'coder'-全用deepseek-coder, 'mixed'-混合模式(默认)")
parser.add_argument('--coder-model', type=str, default='deepseek-coder',
                    help="编码类Agent使用的模型")
parser.add_argument('--chat-model', type=str, default='deepseek-chat',
                    help="非编码类Agent使用的模型")
parser.add_argument('--save-all', action='store_true',
                    help="保存所有中间代码版本")
args = parser.parse_args()

# ==== 计时器装饰器 ====
def time_tracker(func):
    """记录函数执行时间的装饰器"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"\n🕒 [{datetime.now().strftime('%H:%M:%S')}] 开始执行: {func.__name__}")
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        print(f"⏱️ [{datetime.now().strftime('%H:%M:%S')}] 完成: {func.__name__} | 耗时: {elapsed:.2f}秒")
        return result
    return wrapper

# ==== DeepSeek API配置 ====
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

def get_llm_config(model_name):
    return {
        "config_list": [{
            "model": model_name,
            "api_key": DEEPSEEK_API_KEY,
            "base_url": DEEPSEEK_BASE_URL,
            "api_type": "openai"
        }],
        "timeout": 120,
        "temperature": 0.3
    }

# ==== 模型选择逻辑 ====
def select_agent_model(agent_name):
    coding_agents = ["Coder", "BugFinder", "Fixer"]
    if args.model == 'chat':
        return args.chat_model
    elif args.model == 'coder':
        return args.coder_model
    else:
        return args.coder_model if agent_name in coding_agents else args.chat_model

# ==== Agent 创建函数 ====
@time_tracker
def create_agent(name, system_message):
    model_name = select_agent_model(name)
    print(f"🤖 创建智能体: {name} | 使用模型: {model_name}")
    return AssistantAgent(
        name=name,
        system_message=system_message,
        llm_config=get_llm_config(model_name)
    )

# ==== 创建智能体 ====
researcher = create_agent(
    "Researcher",
    "你只负责总结研究主题的背景与研究基础，用清晰条目列出核心知识点。完成后说：'背景分析完成，请Questioner提出科学问题。'"
)
questioner = create_agent(
    "Questioner",
    "你只基于研究背景提出3-5个值得深入研究的科学问题，并聚焦可量化。完成后说：'问题已提出，请Coder编写模型代码。'"
)
coder = create_agent(
    "Coder",
    "你只负责编写Python建模代码，输出完整可执行文件，完成后说：'代码编写完成，请BugFinder检查。'"
)
bug_finder = create_agent(
    "BugFinder",
    "你检查代码错误并指出行号和描述，完成后说：'问题已标记，请Fixer修复。'"
)
fixer = create_agent(
    "Fixer",
    "你修复BugFinder的问题，输出修复后的完整代码，完成后说：'修复完成，请Verifier验证。'"
)
verifier = create_agent(
    "Verifier",
    "你验证代码合理性并简要评价，输出最后可运行的完整代码块，必须一字不差把完整代码输出，完成后说：'验证通过，请Writer撰写论文。'"
)
writer = create_agent(
    "Writer",
    "仅在收到'请Writer撰写论文'后，根据前面内容生成完整Markdown研究论文，结构：引言、方法、结果、讨论、结论。完成后说：'论文撰写完成，TERMINATE'"
)

# ==== 用户代理 ====
@time_tracker
def create_user_proxy():
    try:
        return UserProxyAgent(
            name="Student",
            human_input_mode="TERMINATE",
            max_consecutive_auto_reply=5,
            code_execution_config={"work_dir": "workspace", "use_docker": False, "timeout": 300},
            description="Student user proxy agent for research collaboration",
            system_message="You are a student researcher. Provide clear instructions to the agent team."
        )
    except Exception:
        return UserProxyAgent(
            name="Student", human_input_mode="ALWAYS",
            max_consecutive_auto_reply=5,
            code_execution_config={"work_dir": "workspace", "use_docker": False}
        )

user = create_user_proxy()

# ==== 代码捕获功能 ====
class CodeCapture:
    def __init__(self):
        self.versions = []
        self.current_version = 0
        os.makedirs("output/code_versions", exist_ok=True)

    def extract_code(self, content):
        pattern = r'```(?:python)?\s*(.*?)```'
        blocks = re.findall(pattern, content, re.DOTALL)
        return [b.strip() for b in blocks if b.strip()]

    def save_code_version(self, agent_name, content):
        code_blocks = self.extract_code(content)
        if not code_blocks:
            return None
        files = []
        for block in code_blocks:
            self.current_version += 1
            filename = f"output/code_versions/ver_{self.current_version}_{agent_name}.py"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(block)
            self.versions.append({
                "version": self.current_version,
                "agent": agent_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "code": block
            })
            files.append(filename)
        return files

code_capture = CodeCapture()

# ==== 增强进度回调 ====
def track_progress(recipient, messages, sender, config):
    print(f"📬 [{datetime.now().strftime('%H:%M:%S')}] {sender.name} → {recipient.name}")
    if sender.name in ["Coder", "Fixer", "Verifier"] and messages:
        last = messages[-1]
        if "content" in last:
            files = code_capture.save_code_version(sender.name, last["content"])
            if files:
                print(f"💾 {sender.name} 代码已保存: {', '.join(files)}")
    if sender.name == "Writer" and "请Writer撰写论文" not in manager.groupchat.messages[-2]["content"]:
        return True, None
    return False, None

# ==== 组聊天管理器 ====
@time_tracker
def setup_group_chat():
    groupchat = GroupChat(
        agents=[user, researcher, questioner, coder, bug_finder, fixer, verifier, writer],
        messages=[],
        max_round=15,
        speaker_selection_method="round_robin"
    )
    return GroupChatManager(
        groupchat=groupchat,
        name="Manager",
        llm_config=get_llm_config(args.chat_model),
        is_termination_msg=lambda m: "TERMINATE" in m["content"]
    )

manager = setup_group_chat()
for agent in [researcher, questioner, coder, bug_finder, fixer, verifier, writer]:
    agent.register_reply([AssistantAgent, UserProxyAgent, GroupChatManager], reply_func=track_progress)

# ==== 主流程 ====
if __name__ == '__main__':
    os.makedirs("output", exist_ok=True)
    print("\n🚀 欢迎使用多智能体科研助手")
    theme = input("请输入研究主题：")
    text  = input("请输入更具体的文本描述（可选）：")
    prompt = (
        f"我们要开展一个科研项目，主题：{theme}\n"
        "1.Researcher分析背景\n"
        "2.Questioner提出问题\n"
        "3.Coder编写代码\n"
        "4.BugFinder检查\n"
        "5.Fixer修复\n"
        "6.Verifier验证并输出完整代码，必须一字不差把完整代码输出\n"
        "7.Writer撰写论文\n"
        f"更具体的文本：{text}\n"
    )
    start_time = time.time()
    user.initiate_chat(manager, message=prompt)
    collaboration_time = time.time() - start_time
    print(f"✅ 协作流程完成！总耗时: {collaboration_time:.2f}秒")

    # 保存 Verifier 最终代码
    ver_msgs = [m for m in manager.groupchat.messages if m.get("sender", {}).get("name")=="Verifier"]
    if ver_msgs:
        code = ver_msgs[-1]["content"]
        with open("output/final_model_code.py","w",encoding="utf-8") as f:
            f.write(code)
        print("💾 最终代码已保存: output/final_model_code.py")

    # 保存 Writer 论文
    last = manager.groupchat.messages[-1]["content"]
    with open("output/research_summary.md","w",encoding="utf-8") as f:
        f.write(last)
    print("📄 研究论文已保存: output/research_summary.md")

    # 保存用时和模型报告
    report_path = "output/run_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"协作流程耗时: {collaboration_time:.2f}秒\n")
        f.write("模型使用报告:\n")
        for agent in [researcher, questioner, coder, bug_finder, fixer, verifier, writer]:
            model = agent.llm_config["config_list"][0]["model"]
            f.write(f"  - {agent.name}: {model}\n")
    print(f"📝 用时和模型报告已保存: {report_path}")