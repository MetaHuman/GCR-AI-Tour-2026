from __future__ import annotations
import os
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# --- 核心逻辑：读取并打印 ---
def main():
    # 自动定位路径
    base_path = Path(__file__).parent.parent
    config_path = base_path / "input" / "api" / "rss_list.json"
    
    print(f"📖 正在加载配置: {config_path}")
    
    if not config_path.exists():
        print("❌ 错误：找不到 rss_list.json")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        sources = json.load(f)
        print(f"✅ 已加载 {len(sources)} 个数据源。")

    # 将 rss_list.json 转存为 output/source_list.json，供下一步 tech_fetch_all_to_disk.py 读取
    output_path = base_path / "output" / "source_list.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sources, f, indent=2)
    
    print(f"🚀 任务完成！已将源列表写入: {output_path}")

if __name__ == "__main__":
    main()