import os
from sys import version
from google.adk.agents.callback_context  import CallbackContext
from google.genai.types import Content, Part
from google.adk.models import LlmRequest


# 假设我们在项目的根目录下创建一个 'uploads' 文件夹来存放文件
UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

async def mark_file_uploaded(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> None:
    """
    在 LLM 真正调用前，把上传的简历文件保存到本地，
    并在 state 中记录：用户已上传简历，以及文件路径。
    同时，从请求中移除文件部分，以避免 LiteLlm 报错。
    """
    print("--- Running before_model_callback: mark_resume_uploaded ---")
    
    # 用于存放处理后的、只包含文本的 Part
    new_contents = []

    for content in llm_request.contents:
        # 如果 content 本身不是 Content 类型，则跳过
        if not isinstance(content, Content):
            continue

        clean_parts = []
        for part in getattr(content, "parts", []):
            # 检查 Part 是否包含文件数据
            if hasattr(part, "inline_data") and part.inline_data:
                # 这是一个文件 Part，我们需要处理它
                blob = part.inline_data
                file_name = blob.display_name or "untitled"
                file_data = blob.data

                # 1. 保存文件到本地
                file_path = os.path.join(UPLOADS_DIR, file_name)
                version = await callback_context.save_artifact(file_name, part)
                print("version", version)


                with open(file_path, "wb") as f:
                    f.write(file_data)
                
                print(f"File saved to: {file_path}")

                # 2. 更新 state
                state_update = {
                    "resume_exists": True,
                    "resume_path": file_path,
                    "artifact_name": file_name,
                }
                callback_context.state.update(state_update)
                print(f"State updated: {state_update}")

                # 关键：不要将这个文件 part 添加到 clean_parts 列表中
                clean_parts.append(Part(text=f"文件已上传，路径：{file_path}，artifact_name文件名：{file_name}，文件版本：{version}"))
            else:
                # 这是一个文本 Part，保留它
                clean_parts.append(part)
        
        # 如果处理后的 parts 列表不为空，则用它创建一个新的 Content 对象
        if clean_parts:
            new_contents.append(Content(role=content.role, parts=clean_parts))

    # 3. 修改 llm_request，用只包含文本的 new_contents 替换原始的 contents
    # 这是防止 ValueError 的核心步骤
    llm_request.contents = new_contents
    print(f"Cleaned llm_request.contents for LLM: {llm_request.contents}")
    print("----------------------------------------------------------")