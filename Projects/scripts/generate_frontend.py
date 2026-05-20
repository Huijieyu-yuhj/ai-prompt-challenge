import subprocess
import sys
from pathlib import Path
import os
import shutil
import json
import platform

# ==============================================================================
# Tech-stack scaffolding recipes
# Each recipe defines how to scaffold a project and which dependencies to add.
# ==============================================================================
SCAFFOLD_RECIPES = {
    "vue": {
        "scaffold_cmd": ["npx", "-y", "create-vite@latest", "frontend", "--template", "vue"],
        "base_install_cmd": ["npm", "install"],
        "install_deps_cmd": ["npm", "install"],
        "dependencies": ["element-plus", "vue-router@4", "pinia", "axios"],
        "src_dir": "src",
        "component_ext": ".vue",
    },
    "react": {
        "scaffold_cmd": ["npx", "-y", "create-vite@latest", "frontend", "--template", "react"],
        "base_install_cmd": ["npm", "install"],
        "install_deps_cmd": ["npm", "install"],
        "dependencies": ["react-router-dom", "axios"],
        "src_dir": "src",
        "component_ext": ".jsx",
    },
    "svelte": {
        "scaffold_cmd": ["npx", "-y", "create-vite@latest", "frontend", "--template", "svelte"],
        "base_install_cmd": ["npm", "install"],
        "install_deps_cmd": ["npm", "install"],
        "dependencies": ["axios"],
        "src_dir": "src",
        "component_ext": ".svelte",
    },
    "angular": {
        "scaffold_cmd": ["npx", "-y", "@angular/cli@latest", "new", "frontend", "--defaults", "--skip-git"],
        "base_install_cmd": ["npm", "install"],
        "install_deps_cmd": ["npm", "install"],
        "dependencies": [],
        "src_dir": "src/app",
        "component_ext": ".ts",
    },
    "flutter": {
        "scaffold_cmd": ["flutter", "create", "frontend"],
        "base_install_cmd": ["flutter", "pub", "get"],
        "install_deps_cmd": ["flutter", "pub", "add"],
        "dependencies": ["http", "provider"],
        "src_dir": "lib",
        "component_ext": ".dart",
    },
}


def _detect_recipe(tech_stack: str) -> dict | None:
    """Return the matching scaffold recipe, or None for plain HTML stack."""
    ts_lower = tech_stack.lower()
    for key, recipe in SCAFFOLD_RECIPES.items():
        if key in ts_lower:
            return recipe
    return None


def _run_cmd(cmd: list[str], cwd: str, label: str):
    """Run a subprocess command and print status."""
    print(f"  -> [{label}] Running: {' '.join(cmd)}")
    # On Windows, npm/npx need shell=True to resolve .cmd scripts
    use_shell = platform.system() == "Windows"
    # Let output stream directly to the terminal so users can see progress/errors in real-time
    # Use DEVNULL for stdin so interactive prompts (like Vite 6's new "Install with npm and start now?") are auto-skipped silently
    result = subprocess.run(cmd, cwd=cwd, shell=use_shell, stdin=subprocess.DEVNULL)
    if result.returncode != 0:
        print(f"  -> [{label}] WARNING: command exited with code {result.returncode}")
    else:
        print(f"  -> [{label}] OK")
    return result.returncode


def _phase1_scaffold(project_root: Path, frontend_dir: Path, recipe: dict, tech_stack: str):
    """Phase 1: Deterministic scaffolding via npm/npx commands."""
    print(f"\n{'='*50}")
    print(f"Phase 1: Scaffolding project with {tech_stack}")
    print(f"{'='*50}")

    # 1. Remove existing frontend/ if present
    if frontend_dir.exists():
        print(f"  -> Removing existing frontend/ directory...")
        import time
        try:
            shutil.rmtree(frontend_dir)
        except Exception as e:
            # On Windows, sometimes file locks prevent immediate deletion. Wait and retry.
            time.sleep(1)
            try:
                shutil.rmtree(frontend_dir)
            except Exception as e:
                print(f"  -> ERROR: Failed to remove frontend/ directory: {e}")
                print("     It may be locked by another program (like your IDE or File Explorer).")
                print("     Please close any programs using it and try again.")
                return False
        
        # Verify it is deleted
        for _ in range(5):
            if not frontend_dir.exists():
                break
            time.sleep(0.5)

        if frontend_dir.exists():
            print("  -> ERROR: frontend/ directory still exists after removal.")
            return False

    # 2. Run scaffold command (e.g., npm create vite@latest frontend -- --template vue)
    scaffold_code = _run_cmd(recipe["scaffold_cmd"], cwd=str(project_root), label="Scaffold")
    if scaffold_code != 0:
        print("  -> ERROR: Scaffold command failed.")
        return False

    if not frontend_dir.exists():
        print("  -> ERROR: Scaffold command did not create frontend/ directory.")
        print("     Falling back to manual directory creation.")
        frontend_dir.mkdir(parents=True)
        return False

    # 3. Install base dependencies
    base_install = recipe.get("base_install_cmd", ["npm", "install"])
    if base_install:
        code = _run_cmd(base_install, cwd=str(frontend_dir), label="Base Install")
        if code != 0:
            print("  -> ERROR: Base install failed.")
            return False

    # 4. Install additional dependencies
    if recipe.get("dependencies"):
        install_cmd = recipe.get("install_deps_cmd", ["npm", "install"]) + recipe["dependencies"]
        code = _run_cmd(install_cmd, cwd=str(frontend_dir), label="Dependencies")
        if code != 0:
            print("  -> ERROR: Additional dependencies install failed.")
            return False

    print(f"  -> Phase 1 complete. Project scaffolded at: {frontend_dir}")
    return True


def _phase2_write_components(project_root: Path, frontend_dir: Path, recipe: dict, tech_stack: str):
    """Phase 2: Call Claude to write component code into the scaffolded project."""
    print(f"\n{'='*50}")
    print(f"Phase 2: Claude writing component code...")
    print(f"{'='*50}")

    claude_path = shutil.which("claude") or shutil.which("claude.cmd")
    if not claude_path:
        print("Error: Claude CLI not found in PATH.")
        return

    src_dir = recipe["src_dir"]
    component_ext = recipe["component_ext"]
    deps_str = ", ".join(recipe.get("dependencies", []))
    deps_text = f"Dependencies are already installed (including {deps_str})." if deps_str else "Dependencies are already installed."

    prompt = f"""请立即读取项目根目录的 `Requirements.md` 文件，并利用你的文件编辑工具，在已经搭好脚手架的 `frontend/{src_dir}/` 目录中直接生成完整的前端代码。不要询问我想要构建什么，直接开始写代码。

当前系统状态：
{tech_stack} 项目已经在 `frontend/` 目录中完全初始化好了。{deps_text} 

严格规则：
1. 必须根据 Requirements.md 中所有的功能和UI需求，直接编写 {component_ext} 组件、路由配置和 API 层。
2. 务必包含所有的子页面、弹窗设计。同时，请极其仔细地参考 `paraflow/Screen & Prototype/` 目录中提供的 HTML 原型文件，**必须使最终生成的界面代码在布局结构、CSS 样式和整体视觉效果上与原始 HTML 页面原型保持 95% 以上的极限还原度**。如果发现还原度低，属于重大工作失职！
3. 不要运行任何脚手架初始化命令（如 npm create），不要删除/重建目录。
4. 绝对不要运行开发服务器命令（如 npm run dev），只负责编写代码！
5. 直接执行所有文件写入。任务完成后直接结束，绝对不要回复诸如 "What would you like me to build?" 这样的反问句。"""

    print("-> 实时内部运行状态：您可在项目文件 /claude_frontend_debug.log 中追踪前端编写进度。")
    cmd = [claude_path, "--print", "--dangerously-skip-permissions",
           "--debug-file", "claude_frontend_debug.log", prompt]
    subprocess.run(cmd, cwd=str(project_root))
    print("Phase 2 complete. Components written.")


def _fallback_html(project_root: Path, frontend_dir: Path, tech_stack: str):
    """Fallback: plain HTML/CSS/JS generation (original behavior)."""
    print(f"\n{'='*50}")
    print(f"Generating plain HTML/CSS/JS frontend...")
    print(f"{'='*50}")

    if not frontend_dir.exists():
        frontend_dir.mkdir(parents=True)

    claude_path = shutil.which("claude") or shutil.which("claude.cmd")
    if not claude_path:
        print("Error: Claude CLI not found in PATH.")
        return

    prompt = f"""请立即读取项目根目录或 `paraflow` 目录中的产品原型和需求文件，并利用文件编辑工具，直接在 `frontend/` 文件夹中生成完整的 {tech_stack} 前端代码。不要询问我任何问题，不要等待确认，直接写代码。

务必注意以下几点：
1. 补全任何缺失的 UI 页面，包括弹窗、对话框和子页面。同时，请极其仔细地参考 `paraflow/Screen & Prototype/` 目录中提供的 HTML 原型文件，**必须使最终生成的界面代码在布局结构、CSS 样式和整体视觉效果上与原始 HTML 原型保持 95% 以上的极限还原度**。UI 还原度是最高优先级的指标！
2. 绝对不要启动开发服务器。
3. 确保代码遵循最佳实践，完成后直接结束任务。不要回复任何反问句。"""

    print("-> 实时内部运行状态：您可在项目文件 /claude_frontend_debug.log 中追踪前端编写进度。")
    cmd = [claude_path, "--print", "--dangerously-skip-permissions",
           "--debug-file", "claude_frontend_debug.log", prompt]
    subprocess.run(cmd, cwd=str(project_root))
    print("Frontend generation complete.")


def generate_frontend():
    project_root = Path(__file__).parent.parent
    frontend_dir = project_root / 'frontend'
    config_file = project_root / 'pipeline_config.json'

    # Read tech stack from config
    tech_stack = "HTML/CSS/JS (Standard)"
    try:
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                tech_stack = config.get("frontend_tech_stack", tech_stack)
    except Exception as e:
        print(f"Warning: Could not read pipeline_config.json: {e}")

    print(f"Frontend tech stack: {tech_stack}")

    recipe = _detect_recipe(tech_stack)

    if recipe:
        # Framework-based stack: two-phase approach
        scaffold_ok = _phase1_scaffold(project_root, frontend_dir, recipe, tech_stack)
        if scaffold_ok:
            _phase2_write_components(project_root, frontend_dir, recipe, tech_stack)
        else:
            print("WARNING: Scaffold failed. Falling back to Claude-only generation.")
            _fallback_html(project_root, frontend_dir, tech_stack)
    else:
        # Plain HTML stack: single-phase, Claude does everything
        _fallback_html(project_root, frontend_dir, tech_stack)

    print(f"\n{'='*50}")
    print("Frontend generation finished.")
    print(f"{'='*50}")


if __name__ == '__main__':
    generate_frontend()
