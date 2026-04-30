import os
import sys
import json
from google import genai
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def main():
    # 路径配置
    base_path = Path(__file__).parent.parent
    input_file = base_path / "output" / "raw_signals.json"
    output_dir = base_path / "output" / "clusters"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "hotspots.json"

    # 1. 配置 API Key (尝试从 .env 加载并检查)
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

    model_id = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    with open(input_file, 'r', encoding='utf-8') as f:
        signals = json.load(f)

    # 3. 构造深度分析 Prompt
    prompt = f"""
    作为一名资深技术架构师，请分析以下技术信号，将它们聚类为最多 12 个最具代表性的技术热点。

    【重要规则】
    - samples 中每篇文章的 "url" 字段，必须原样复制该文章在输入数据中的 "link" 字段值，不得填写 RSS 订阅地址或任何其他 URL。
    - "title" 字段同样原样复制输入数据中的 "title" 字段，不得改写。

    输出要求：
    - 必须返回纯 JSON 对象，格式如下：
    {{
      "mode": "ai_clustered",
      "top_k": 12,
      "hotspots": [
        {{
          "hotspot_id": "H01",
          "title": "热点的概括标题（可自拟）",
          "summary": "简要摘要",
          "category": "trend",
          "overall_heat_score": 80,
          "coverage": {{ "source_count": 2, "companies": [], "platforms": [] }},
          "should_chase": "yes",
          "chase_rationale": ["理由1"],
          "samples": [
            {{
              "platform": "输入数据中的 source_name 字段",
              "title": "输入数据中的 title 字段（原样复制）",
              "url": "输入数据中的 link 字段（原样复制，禁止使用 RSS 地址）"
            }}
          ]
        }}
      ]
    }}

    输入数据（每条含 title、link、source_name 字段）：
    {json.dumps(signals[:30], ensure_ascii=False)}
    """

    print(f"🚀 [付费模式] 正在调用 {model_id} 进行深度聚类...")
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        # 稳健的 JSON 清洗逻辑
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        # 验证 JSON 有效性并保存
        json_data = json.loads(text)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ 聚类成功！热点已存至 {output_file}")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    main()