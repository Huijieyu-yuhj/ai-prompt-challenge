import subprocess
import shutil
from pathlib import Path

def generate_requirements():
    project_root = Path(__file__).parent.parent
    paraflow_dir = project_root / 'paraflow'
    
    if not paraflow_dir.exists():
        print(f"Error: {paraflow_dir} does not exist.")
        return
        
    prompt = "请读取 `paraflow` 目录下的所有原文档案，将它们提取、浓缩为一份精炼的 `Requirements.md` 文件并输出保存到系统项目根目录。注意：这是传递给后续流程（前端和PRD）的关键输入文档，你需要梳理它的业务脉络，必须确保所有的核心功能、接口规范、关键交互和验证逻辑都得以无损保留，绝对不可以丢失任何重要部分。"

    claude_path = shutil.which("claude") or shutil.which("claude.cmd")
    if not claude_path:
        print("Error: Claude CLI not found in PATH.")
        return
        
    print("Running Claude to condense paraflow into Requirements.md...")
    print("-> 实时内部运行状态：您可在项目文件 /claude_requirements_debug.log 中追踪工作进度。")
    cmd = [claude_path, "--print", "--dangerously-skip-permissions", "--debug-file", "claude_requirements_debug.log", prompt]
    subprocess.run(cmd, cwd=str(project_root))
    print("Requirements.md generation complete.")

if __name__ == '__main__':
    generate_requirements()
