import base64
from pathlib import Path
from google.adk.tools import ToolContext
from google.adk.agents import Agent
import base64
import io
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams


def show_local_image(file_name: str=None, tool_context: ToolContext=None) -> str:
    """
    返回 HTML 格式的图片链接，可设置显示大小
    
    Args:
        file_name: 相对于当前脚本的图片文件名
    
    Returns:
        HTML 格式的图片链接（带尺寸控制）
    """
    temp_file_name = tool_context.state.get("tmp:analyze_salary_by_industry")
    
    print("temp_file_name:", temp_file_name, file_name)
    # return f![{file_name}](http://localhost:8000/{file_name}) height="200px"'
    return f'<img src="http://localhost:12800/img/{file_name}" height="720px">'


def get_image_viewer_agent(config):
    selected_model = config.deepseek_chat
    agent = Agent(
        name="image_viewer",
        model=selected_model,
        description="当用户想查看图片时，调用 show_local_image 并把文件名传进去。不对输出进行更改。",
        tools=[show_local_image],
    )
    return agent

"""帮我把 baidu.com 转换成二维码
如何显示图片
"""
def get_qr_code(text: str) -> str:
    """ 生成二维码并转 Base64"""
    from qrcode import make
    img = make(text)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"![QR Code](data:image/png;base64,{b64})"

# fetch_tools = MCPToolset(
#     connection_params=SseServerParams(
#         url="https://mcp.api-inference.modelscope.net/8f0ec8c1233e4e/sse",
#         # headers={"Authorization": "Bearer <token>"}
#     )
# )
# search_tools = MCPToolset(
#     connection_params=SseServerParams(  
#         url="https://mcp.api-inference.modelscope.net/19366d9f6bf642/sse",
#     )
# )