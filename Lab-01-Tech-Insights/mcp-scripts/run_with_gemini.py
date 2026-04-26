import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

def run_lab_with_gemini():
    # 自动定位到 mcp-scripts 目录
    current_file_path = Path(__file__).resolve()
    mcp_dir = current_file_path.parent
    os.chdir(mcp_dir)
    
    # 尝试加载上层目录的 .env 文件
    env_path = mcp_dir.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    
    # 确保 API Key 存在（双重检查）
    if not os.environ.get("GOOGLE_API_KEY"):
        print("❌ 错误: 未检测到 GOOGLE_API_KEY 环境变量。")
        print("请运行: $env:GOOGLE_API_KEY = '你的KEY'")
        return

    stages = [
        "tech_read_source_list.py",
        "tech_fetch_all_to_disk.py",
        "tech_cluster_or_fallback.py",
        "tech_insight_or_fallback.py",
        "tech_render_report_or_fallback.py"
    ]

    os.environ["AI_ENGINE"] = "gemini"

    for script in stages:
        print(f"\n🚀 正在执行: {script} ...")
        # 修改点：将 stdout/stderr 直接对接到控制台，这样报错会立刻显示
        result = subprocess.run(["python", script]) 
        
        if result.returncode != 0:
            print(f"\n❌ {script} 执行失败，已停止。")
            break

if __name__ == "__main__":
    run_lab_with_gemini()