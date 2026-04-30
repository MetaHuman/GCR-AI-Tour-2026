import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

def run_lab_with_gemini():
    mcp_dir = Path(__file__).resolve().parent
    base_dir = mcp_dir.parent
    os.chdir(mcp_dir)

    env_path = base_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    auth_type = os.environ.get("GOOGLE_AUTH_TYPE", "apikey").strip().lower()
    if auth_type == "apikey" and not os.environ.get("GOOGLE_API_KEY"):
        print("❌ 错误: GOOGLE_AUTH_TYPE=apikey 但未检测到 GOOGLE_API_KEY。")
        print("请在 .env 中配置 GOOGLE_API_KEY，或将 GOOGLE_AUTH_TYPE 改为 adc。")
        return

    stages = [
        "tech_read_source_list.py",
        "tech_fetch_all_to_disk.py",
        "tech_cluster_or_fallback.py",
        "tech_insight_or_fallback.py",
        "tech_render_report_or_fallback.py",
    ]

    os.environ["AI_ENGINE"] = "gemini"

    for script in stages:
        print(f"\n🚀 正在执行: {script} ...")
        result = subprocess.run(["python", script])
        if result.returncode != 0:
            print(f"\n❌ {script} 执行失败，已停止。")
            break

if __name__ == "__main__":
    run_lab_with_gemini()
