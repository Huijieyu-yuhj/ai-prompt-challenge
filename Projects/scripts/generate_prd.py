import subprocess
from pathlib import Path
import shutil
import json

def generate_prd():
    project_root = Path(__file__).parent.parent
    tasks_dir = project_root / 'tasks'
    tasks_dir.mkdir(exist_ok=True)
    config_file = project_root / 'pipeline_config.json'
    
    backend_tech_stack = "Node.js (Standard)"
    frontend_tech_stack = "HTML/CSS/JS (Standard)"
    try:
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                backend_tech_stack = config.get("backend_tech_stack", backend_tech_stack)
                frontend_tech_stack = config.get("frontend_tech_stack", frontend_tech_stack)
    except Exception as e:
        print(f"Warning: Could not read pipeline_config.json: {e}")
        
    prompt = f"创建一个prd 读取 Requirements.md 的内容，并生成完整的 Full-Stack 实现 PRD 到 tasks/prd-fullstack-implementation.md 中。请务必严格按照以下技术栈来设计架构：\n- **后端技术栈**：{backend_tech_stack}\n- **前端技术栈**：{frontend_tech_stack}\n绝对禁止自行替换或忽略以上指定的技术栈！前端和后端都必须严格使用上述指定的框架和工具链。\n\n额外硬性要求：PRD 文档中只允许出现上述技术栈相关的框架/工具。禁止出现或暗示任何其它技术栈（例如 Next.js、React、Prisma、SQLite、NextAuth、Tailwind、Express、NestJS 等）。如果 Requirements.md 提到了其它技术栈，也必须以“不会采用”的形式明确排除，并给出与指定技术栈兼容的替代方案。"
    
    claude_path = shutil.which("claude") or shutil.which("claude.cmd")
    if not claude_path:
        print("Error: Claude CLI not found in PATH.")
        return
        
    print("Running Claude to generate PRD...")
    print("-> 实时内部运行状态：您可在项目文件 /claude_prd_debug.log 中追踪PRD梳理进度。")
    cmd = [claude_path, "--print", "--dangerously-skip-permissions", "--debug-file", "claude_prd_debug.log", prompt]
    subprocess.run(cmd, cwd=str(project_root))
    print("PRD generation complete.")

if __name__ == '__main__':
    generate_prd()
