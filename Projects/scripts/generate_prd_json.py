import subprocess
from pathlib import Path
import shutil

def generate_prd_json():
    project_root = Path(__file__).parent.parent
    config_file = project_root / 'pipeline_config.json'
    
    backend_tech_stack = "Node.js (Standard)"
    frontend_tech_stack = "HTML/CSS/JS (Standard)"
    try:
        if config_file.exists():
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                backend_tech_stack = config.get("backend_tech_stack", backend_tech_stack)
                frontend_tech_stack = config.get("frontend_tech_stack", frontend_tech_stack)
    except Exception as e:
        print(f"Warning: Could not read pipeline_config.json: {e}")
        
    prompt = f"将prd 转成 prd.json 读取 tasks/prd-fullstack-implementation.md 内容，转换格式后输出到 scripts/ralph/prd.json 中。由于 Ralph Agent 取决于 prd.json 的上下文，请你【必须在 prd.json 的 'description' 字段最前面】加上明确的技术栈要求：'后端必须严格使用 {backend_tech_stack} 进行开发，前端必须严格使用 {frontend_tech_stack} 进行开发。' 否则 Agent 会使用错误的语言和框架。"
    
    claude_path = shutil.which("claude") or shutil.which("claude.cmd")
    if not claude_path:
        print("Error: Claude CLI not found in PATH.")
        return
        
    print("Running Claude to generate prd.json...")
    print("-> 实时内部运行状态：您可在项目文件 /claude_prd_json_debug.log 中追踪转化进度。")
    cmd = [claude_path, "--print", "--dangerously-skip-permissions", "--debug-file", "claude_prd_json_debug.log", prompt]
    subprocess.run(cmd, cwd=str(project_root))
    print("prd.json generation complete.")

if __name__ == '__main__':
    generate_prd_json()
