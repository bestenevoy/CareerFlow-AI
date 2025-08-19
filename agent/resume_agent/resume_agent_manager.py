
from typing import Dict, Any

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool

from .prompt import instructions_v1, instructions_v1_zh
from ..llm_config import create_default_config


def save_query_results(
        tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Any
    ) -> None:
    """Callback to modify state parameters for search tools"""
    tool_info = {}
    tool_info['tool_name'] = tool.name
    tool_info['tool_args'] = args
    tool_info['tool_response'] = tool_response
    if tool_context.state.get('resume_agent_tool_call', None) is None:
        tool_context.state['resume_agent_tool_call'] = [tool_info]
    else:
        toolcall = tool_context.state['resume_agent_tool_call']
        toolcall.append(tool_info)
        tool_context.state['resume_agent_tool_call'] = toolcall
    return


def read_resume_file(file_path: str, tool_context: ToolContext) -> str:
    """读取用户上传的简历文件"""
    # print('>>>>> read_resume_file, tool_context.state:', tool_context.state)
    # if not tool_context.state.get('resume_exists', False):
        # return "用户没有上传简历, 请求用户先上传简历"
    # tool_context.load_artifact('resume_file', file_path)
    resume_file = tool_context.state.get('resume_path')
    print('>>>>> read_resume_file, resume_file:', resume_file)
    try:
        with open("./uploads/resume.md", 'r', encoding='utf-8') as file:
            resume_content = file.read()
        print('>>>>> read_resume_file, resume_content:', resume_content)
        return resume_content
    except Exception as e:
        print('>>>>> read_resume_file, error:', e)
        return "读取用户简历失败" + str(e)



def init_resume_agent(config):
    """Initialize the resume agent with the given configuration."""
    selected_model = config.deepseek_chat

    resume_agent = LlmAgent(
        name="resume_agent",
        model=selected_model,
        instruction=instructions_v1_zh,
        description="根据用户的需求，对用户简历进行分析，并根据推荐给用户的岗位信息，或者根据用户的偏好，对用户的简历进行优化，使其更适合推荐的岗位。",
        output_key="resume_result",
        after_tool_callback=save_query_results,
        tools=[read_resume_file],

    )
    return resume_agent

if __name__ == "__main__":
    config = create_default_config()
    root_agent = init_resume_agent(config)
