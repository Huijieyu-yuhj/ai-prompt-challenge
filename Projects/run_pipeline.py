import os
import sys
import subprocess
from pathlib import Path

def run_step(script_name):
    print(f"\n{'='*50}\nRunning {script_name}...\n{'='*50}")
    result = subprocess.run([sys.executable, f"scripts/{script_name}"])
    if result.returncode != 0:
        print(f"Error executing {script_name}. Aborting pipeline.")
        sys.exit(result.returncode)

def main():
    project_root = Path(__file__).parent
    
    # Run the 4 generation steps
    run_step("generate_requirements.py")
    run_step("generate_frontend.py")
    run_step("generate_prd.py")
    run_step("generate_prd_json.py")
    
    # Create backend directory
    backend_dir = project_root / 'backend'
    backend_dir.mkdir(exist_ok=True)
    print("Ensure backend/ directory exists.")
    
    # Launch ralph.py in a new terminal
    print("Launching ralph.py in a new terminal window...")
    if os.name == 'nt':
        # Windows
        os.system('start cmd /k "python scripts/ralph/ralph.py"')
    else:
        print("Please run python scripts/ralph/ralph.py manually.")

if __name__ == '__main__':
    main()
