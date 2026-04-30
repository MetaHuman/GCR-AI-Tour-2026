import os
import sys
import json
from google import genai
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def main():
    base_path = Path(__file__).parent.parent
    hotspots_file = base_path / "output" / "clusters" / "hotspots.json"
    signals_file = base_path / "output" / "raw_signals.json"
    output_dir = base_path / "output" / "insights"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "insights.json"

    from dotenv import load_dotenv
    env_path = base_path / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    auth_type = os.environ.get("GOOGLE_AUTH_TYPE", "apikey").strip().lower()
    if auth_type == "adc":
        import google.auth
        credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        client = genai.Client(credentials=credentials)
        print("🔑 使用 ADC 认证（Application Default Credentials）")
    else:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("❌ 错误: 未检测到 GOOGLE_API_KEY。请在 .env 中配置，或将 GOOGLE_AUTH_TYPE 设为 adc。")
            return
        client = genai.Client(api_key=api_key)

    with open(hotspots_file, 'r', encoding='utf-8') as f:
        hotspots_data = json.load(f)
    with open(signals_file, 'r', encoding='utf-8') as f:
        signals = json.load(f)

    hotspots = hotspots_data.get("hotspots", hotspots_data) if isinstance(hotspots_data, dict) else hotspots_data

    prompt = f"""
    作为一名资深技术分析师，请为以下每个技术热点撰写深度洞察分析。
    输出要求：
    - 必须返回纯 JSON 对象，格式如下：
    {{
      "mode": "ai_insights",
      "insights": [
        {{
          "hotspot_id": "H01",
          "title": "热点标题",
          "what_changed": "发生了什么变化",
          "why_it_matters": "为什么重要",
          "who_is_impacted": ["受影响群体1", "受影响群体2"],
          "next_actions": ["建议行动1", "建议行动2"],
          "risk_notes": ["风险提示"],
          "references": ["参考链接"]
        }}
      ]
    }}

    热点数据：
    {json.dumps(hotspots, ensure_ascii=False)}
    """

    print("🚀 正在使用 google-genai SDK 生成洞察...")

    try:
        model_id = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        json_data = json.loads(text)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print(f"✅ 洞察生成成功！已存至 {output_file}")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    main()
