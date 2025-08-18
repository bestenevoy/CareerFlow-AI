
from typing import Dict, Any

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool

from .prompt import instructions_v1, instructions_v1_zh
from ..llm_config import create_default_config

from ..tools.job_crawler import JobCrawler

def save_query_results(
        tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Any
    ) -> None:
    """Callback to modify state parameters for search tools"""
    tool_info = {}
    tool_info['tool_name'] = tool.name
    tool_info['tool_args'] = args
    tool_info['tool_response'] = tool_response
    if tool_context.state.get('database_agent_tool_call', None) is None:
        tool_context.state['database_agent_tool_call'] = [tool_info]
    else:
        toolcall = tool_context.state['database_agent_tool_call']
        toolcall.append(tool_info)
        tool_context.state['database_agent_tool_call'] = toolcall
    return

from typing import Dict, Any
async def read_artifact_by_name(
    artifact_name: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    1. 根据 artifact_name 对文件进行读取
    2. 返回文件内容
    """
                        # "resume_uploaded": True,
                    # "resume_path": file_path
    is_uploaded = tool_context.state.get("resume_exists", False)
    resume_file_path = tool_context.state.get("resume_path", "")
    print("is_uploaded:", is_uploaded)
    print("resume_file_path:", resume_file_path)
    print("call save_and_read", artifact_name)
    # 1️⃣ 读取 Artifact
    artifact_part = await tool_context.load_artifact(artifact_name)
    if not artifact_part:
        return {"error": f"找不到 artifact: {artifact_name}"}
    print("artifact_part:", artifact_part)
    artifact_part = artifact_part.inline_data
    # 2️⃣ 根据 MIME 类型做不同解析
    mime = artifact_part.mime_type or ""
    if mime.startswith("text/"):
        content = artifact_part.data.decode("utf-8") or ""
    elif mime == "application/pdf":
        # 简单示例：假设你已经 pip install pypdf
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(artifact_part.data))
        content = "\n".join(p.extract_text() or "" for p in reader.pages)
    else:
        return {"error": f"不支持的文件类型: {mime}"}
    return content

def init_database_agent(config):
    """Initialize the database agent with the given configuration."""
    selected_model = config.deepseek_chat

    jc = JobCrawler()

    def get_cities_list() -> dict:
        """
        Get cities list.

        Returns:
            A dictionary containing the list of cities
        """
        res = [str(i) for i in jc.cities_dic.keys()]
        print(res)
        return {"cities": res}

    def get_jobs(jobName: str, cityName: str) -> list:
        """
        Get jobs list.

        Args:
            jobName: job name search keyword
            cityName: cityName which must in func get_citis_list() return

        Returns:
            A list of jobs
        """
        if not jc.cities_dic.get(cityName, False):
            return "这个城市名不在城市列表中，请输入正确的应城市名"
        return [job.to_dict() for job in jc.get_jobs(jobName, cityName)]

    database_agent = LlmAgent(
        name="datasearch_agent",
        model=selected_model,
        instruction=instructions_v1_zh,
        description="数据获取Agent。根据用户的问题，查询岗位信息。读取用户上传的文件",
        tools=[get_jobs, read_artifact_by_name],
        output_key="datasearch_agent_result",
        after_tool_callback=save_query_results,
    )
    return database_agent

if __name__ == "__main__":
    config = create_default_config()
    root_agent = init_database_agent(config)
