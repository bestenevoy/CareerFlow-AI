
from typing import Dict, Any

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool

from .prompt import instructions_v1, instructions_v1_zh
from ..llm_config import create_default_config
from ..tools import get_image_viewer_agent

from ..tools.job_crawler import JobCrawler

def save_query_results(
        tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Any
    ) -> None:
    """Callback to modify state parameters for search tools"""
    tool_info = {}
    tool_info['tool_name'] = tool.name
    tool_info['tool_args'] = args
    tool_info['tool_response'] = tool_response
    if tool_context.state.get('job_recommend_agent_tool_call', None) is None:
        tool_context.state['job_recommend_agent_tool_call'] = [tool_info]
    else:
        toolcall = tool_context.state['job_recommend_agent_tool_call']
        toolcall.append(tool_info)
        tool_context.state['job_recommend_agent_tool_call'] = toolcall
    return


def init_job_recommend_agent(config):
    """Initialize the job_recommend agent with the given configuration."""
    selected_model = config.deepseek_chat

    job_recommend_agent = LlmAgent(
        name="job_recommend_agent",
        model=selected_model,
        # instruction=instructions_v1_zh,
        description="根据用户的需求，推荐匹配的岗位信息，推荐数量2-3个。",

        output_key="job_recommend_result",
        after_tool_callback=save_query_results,
    )
    return job_recommend_agent

if __name__ == "__main__":
    config = create_default_config()
    root_agent = init_job_recommend_agent(config)
