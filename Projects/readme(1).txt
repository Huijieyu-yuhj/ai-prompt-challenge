用户手册（Windows,Mac用户请自行更改）
-------------------------------------------------------------------------------------------------------------------
前提必须安装claude code（安装教程和模型切换教程自己找）
以下是步骤
1、在https://paraflow.com/网站中生成项目需要的文档+原型，文档中必须要包含test_cases.md（测试用例）-旧项目改造可以自己生成需要的文档和原型放入paraflow文件夹
2、导出项目文档，将paraflow文件夹复制到auto-coding中（根目录即可）
3、打开终端，cd到auto-coding文件夹
4、输入 python C:\Users\Administrator\Desktop\auto-coding\run_pipeline.py  <----run_pipeline.py路径
5、回车开始运行，直到开发完毕

配置文件pipeline_config.json（用来配置前后端使用的技术栈，目前默认vue3和java，如需要改，部分py文件需要再更新）

run_pipeline.py     -总流程控制py
generate_frontend.py      -前端代码生成py
generate_prd.py        -tasks/prd-fullstack-implementation.md生成py
generate_prd_json.py           -prd.json生成py
generate_requirements.py     -Requirements.md生成py
ralph.py        -后端功能&测试py

流程为generate_requirements.py-->generate_frontend.py -->generate_prd.py -->generate_prd_json.py-->ralph.py


================================================================================
Trae 运行方案（新增）
================================================================================

本项目原生基于 Claude Code CLI 设计，但可通过以下方式在 Trae IDE 中运行。

一、Trae 运行前置条件
-----------------------------------------------------------------------
1. 安装 Trae IDE（https://www.trae.ai/）并配置好 AI 模型（如 Kimi、GPT-4o 等）
2. 安装 Python 3.10+（项目脚本均为 Python）
3. 安装 Node.js 18+（前端脚手架需要 npm/npx）
4. 如需后端 Java 开发，安装 JDK 17 + Maven
5. 将项目文件夹 `auto-coding-v2.1` 在 Trae 中打开

二、Trae 中运行步骤（分阶段手动执行）
-----------------------------------------------------------------------
由于 Trae 没有 Claude Code CLI 的 `--print` 和 `--dangerously-skip-permissions` 参数支持，
需要将原 `run_pipeline.py` 的自动流水线拆分为在 Trae 的 AI 聊天中手动分步执行。

步骤1：生成 Requirements.md
- 在 Trae 的 AI 聊天中，上传 `paraflow` 文件夹内的所有文档
- 输入提示词：
  "请读取 paraflow 目录下的所有原文档案，将它们提取、浓缩为一份精炼的 Requirements.md 文件。
   注意：这是传递给后续流程（前端和PRD）的关键输入文档，你需要梳理它的业务脉络，
   必须确保所有的核心功能、接口规范、关键交互和验证逻辑都得以无损保留，绝对不可以丢失任何重要部分。
   请将生成的 Requirements.md 保存到项目根目录。"
- 将 AI 生成的内容保存为项目根目录的 `Requirements.md`

步骤2：生成前端脚手架（generate_frontend.py 等效操作）
- 在 Trae 终端中运行（确保在项目根目录）：
    python scripts/generate_frontend.py
- 或直接让 Trae AI 根据 Requirements.md 和 pipeline_config.json 中的技术栈，
  使用 `npm create vite@latest frontend -- --template vue` 创建前端项目，
  并安装 Element Plus、Vue Router、Pinia、Axios 等依赖

步骤3：生成 PRD（generate_prd.py 等效操作）
- 在 Trae 的 AI 聊天中，上传 `Requirements.md` 和 `pipeline_config.json`
- 输入提示词：
  "请读取 Requirements.md 的内容，并生成完整的 Full-Stack 实现 PRD 到 tasks/prd-fullstack-implementation.md 中。
   技术栈要求：
   - 后端：[从 pipeline_config.json 读取 backend_tech_stack]
   - 前端：[从 pipeline_config.json 读取 frontend_tech_stack]
   绝对禁止自行替换或忽略以上指定的技术栈！
   PRD 文档中只允许出现上述技术栈相关的框架/工具。禁止出现或暗示任何其它技术栈。
   请将生成的 PRD 保存到 tasks/prd-fullstack-implementation.md"

步骤4：生成 prd.json（generate_prd_json.py 等效操作）
- 在 Trae 的 AI 聊天中，上传 `tasks/prd-fullstack-implementation.md`
- 输入提示词：
  "请将 tasks/prd-fullstack-implementation.md 转换为 prd.json 格式，
   输出到 scripts/ralph/prd.json。
   注意：prd.json 的 'description' 字段最前面必须加上明确的技术栈要求：
   '后端必须严格使用 [backend_tech_stack] 进行开发，前端必须严格使用 [frontend_tech_stack] 进行开发。'
   请严格按照 Ralph Agent 所需的 prd.json 格式输出。"

步骤5：运行 Ralph 后端开发（ralph.py 等效操作）
- 在 Trae 终端中运行：
    python scripts/ralph/ralph.py
- 或在 Trae 的 AI 聊天中，让 AI 读取 `scripts/ralph/CLAUDE.md` 和 `scripts/ralph/prd.json`，
  按照 Ralph Agent 的指令循环开发后端功能
- 由于 Trae 不支持 `--dangerously-skip-permissions` 参数，需要手动确认 AI 的每一步操作

三、Trae 运行注意事项
-----------------------------------------------------------------------
1. 权限确认：Trae 的 AI 执行文件操作时需要手动确认，无法像 Claude Code 那样自动跳过权限
2. 终端分离：ralph.py 中需要在新终端运行后端服务，Trae 中可手动新建终端执行
3. 进度追踪：原流程中的 debug 日志文件（如 claude_requirements_debug.log）在 Trae 方案中不再自动生成，
   建议在 Trae AI 聊天中分步保存关键输出
4. 技术栈配置：务必先修改 `pipeline_config.json` 中的技术栈，再开始步骤3和步骤4
5. 目录结构：确保 `paraflow` 文件夹在项目根目录，且包含 `test_cases.md`

四、项目文件结构说明
-----------------------------------------------------------------------
auto-coding-v2.1/
├── paraflow/                  # 从 paraflow.com 导出的项目文档（需自行放入）
├── scripts/
│   ├── generate_requirements.py   # 生成 Requirements.md
│   ├── generate_frontend.py       # 生成前端脚手架
│   ├── generate_prd.py            # 生成 PRD 文档
│   ├── generate_prd_json.py       # 生成 prd.json
│   └── ralph/
│       ├── ralph.py               # Ralph Agent 主程序
│       ├── CLAUDE.md              # Ralph Agent 指令文件
│       ├── VALIDATOR.md           # 验证器指令文件
│       ├── prd.json               # PRD JSON 文件（步骤4生成）
│       ├── progress.txt           # 开发进度日志
│       ├── dashboard.py           # 监控面板
│       └── dashboard.html         # 监控面板页面
├── tasks/                     # 存放生成的 PRD 文档
├── .claude/                   # Claude Code 配置（命令、技能、模板）
├── .cursor/                   # Cursor 配置（命令、技能、模板）
├── .agents/                   # 通用 Agent 配置（命令、技能、模板）
├── pipeline_config.json       # 技术栈配置文件
├── run_pipeline.py            # 自动流水线总入口（Claude Code 专用）
└── readme(1).txt              # 本手册

五、常见问题
-----------------------------------------------------------------------
Q1: Trae 中 AI 无法自动保存文件怎么办？
A: 需要手动将 AI 生成的内容复制到对应文件中保存，或使用 Trae 的 "Apply" 功能应用代码变更。

Q2: 没有 Claude Code CLI 可以用 Trae 完全替代吗？
A: 可以。Trae 的 AI 聊天功能可以替代 Claude Code 的 `--print` 模式，只是需要分步手动执行，
   且每一步的 AI 输出需要手动确认或保存。

Q3: Ralph Agent 的循环执行如何在 Trae 中实现？
A: 由于 Trae 不支持自动循环调用 AI Agent，建议：
   - 方式一：在 Trae 终端中直接运行 `python scripts/ralph/ralph.py`，让脚本调用系统安装的 claude/codex CLI
   - 方式二：手动在 Trae AI 聊天中，每次迭代上传 `prd.json` 和 `progress.txt`，让 AI 完成一个 User Story 后更新文件

Q4: 技术栈不是 Vue3 + Java 怎么办？
A: 修改 `pipeline_config.json` 中的配置，并同步更新 `generate_frontend.py` 中的 SCAFFOLD_RECIPES 以支持对应脚手架命令。
