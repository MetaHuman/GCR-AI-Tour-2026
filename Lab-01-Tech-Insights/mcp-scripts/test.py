import os

folder_path = "mcp-scripts"
search_text = "gemini-2.0-flash"
replace_text = "gemini-2.5-flash"

for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 如果匹配到旧的模型名称，进行替换并写回
            if search_text in content:
                new_content = content.replace(search_text, replace_text)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"已更新: {file_path}")
                
        except UnicodeDecodeError:
            # 忽略无法按 utf-8 解码的二进制文件
            pass
        except Exception as e:
            print(f"跳过 {file_path}，错误信息: {e}")

print("✅ 批量替换完成！")


# import os
# import sys
# from google import genai
# from dotenv import load_dotenv
# from pathlib import Path

# # 尝试加载上层目录的 .env 文件
# env_path = Path(__file__).resolve().parent.parent / ".env"
# if env_path.exists():
#     load_dotenv(env_path)

# api_key = os.environ.get("GOOGLE_API_KEY")
# if not api_key:
#     print("❌ 错误: 未检测到 GOOGLE_API_KEY 环境变量。")
#     print("请在终端运行: $env:GOOGLE_API_KEY = '你的实际API_KEY'")
#     sys.exit(1)

# client = genai.Client(api_key=api_key)

# print("--- 你当前可用的 Gemini 模型列表 ---")
# for m in client.models.list():
#     print(f"模型名称: {m.name}")

# --- 你当前可用的 Gemini 模型列表 ---
# 模型名称: models/gemini-2.5-flash
# 模型名称: models/gemini-2.5-pro
# 模型名称: models/gemini-2.0-flash
# 模型名称: models/gemini-2.0-flash-001
# 模型名称: models/gemini-2.0-flash-lite-001
# 模型名称: models/gemini-2.0-flash-lite
# 模型名称: models/gemini-2.5-flash-preview-tts
# 模型名称: models/gemini-2.5-pro-preview-tts
# 模型名称: models/gemma-3-1b-it
# 模型名称: models/gemma-3-4b-it
# 模型名称: models/gemma-3-12b-it
# 模型名称: models/gemma-3-27b-it
# 模型名称: models/gemma-3n-e4b-it
# 模型名称: models/gemma-3n-e2b-it
# 模型名称: models/gemma-4-26b-a4b-it
# 模型名称: models/gemma-4-31b-it
# 模型名称: models/gemini-flash-latest
# 模型名称: models/gemini-flash-lite-latest
# 模型名称: models/gemini-pro-latest
# 模型名称: models/gemini-2.5-flash-lite
# 模型名称: models/gemini-2.5-flash-image
# 模型名称: models/gemini-3-pro-preview
# 模型名称: models/gemini-3-flash-preview
# 模型名称: models/gemini-3.1-pro-preview
# 模型名称: models/gemini-3.1-pro-preview-customtools
# 模型名称: models/gemini-3.1-flash-lite-preview
# 模型名称: models/gemini-3-pro-image-preview
# 模型名称: models/nano-banana-pro-preview
# 模型名称: models/gemini-3.1-flash-image-preview
# 模型名称: models/lyria-3-clip-preview
# 模型名称: models/lyria-3-pro-preview
# 模型名称: models/gemini-3.1-flash-tts-preview
# 模型名称: models/gemini-robotics-er-1.5-preview
# 模型名称: models/gemini-robotics-er-1.6-preview
# 模型名称: models/gemini-2.5-computer-use-preview-10-2025
# 模型名称: models/deep-research-max-preview-04-2026
# 模型名称: models/deep-research-preview-04-2026
# 模型名称: models/deep-research-pro-preview-12-2025
# 模型名称: models/gemini-embedding-001
# 模型名称: models/gemini-embedding-2-preview
# 模型名称: models/gemini-embedding-2
# 模型名称: models/aqa
# 模型名称: models/imagen-4.0-generate-001
# 模型名称: models/imagen-4.0-ultra-generate-001
# 模型名称: models/imagen-4.0-fast-generate-001
# 模型名称: models/veo-2.0-generate-001
# 模型名称: models/veo-3.0-generate-001
# 模型名称: models/veo-3.0-fast-generate-001
# 模型名称: models/veo-3.1-generate-preview
# 模型名称: models/veo-3.1-fast-generate-preview
# 模型名称: models/veo-3.1-lite-generate-preview
# 模型名称: models/gemini-2.5-flash-native-audio-latest
# 模型名称: models/gemini-2.5-flash-native-audio-preview-09-2025
# 模型名称: models/gemini-2.5-flash-native-audio-preview-12-2025
# 模型名称: models/gemini-3.1-flash-live-preview