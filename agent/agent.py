from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.tools import google_search
from google.adk.tools import FunctionTool
from .llm_config import create_default_config
from google.adk.tools.tool_context import ToolContext
from .prompt import instructions_v1_zh
from .tools import get_image_viewer_agent
from .database_agent.database_manager import init_database_agent
from .analysis_agent.database_manager import init_analysis_agent
from .job_recommend_agent.job_recommend_manager import init_job_recommend_agent
from google.adk.agents import Agent, LoopAgent, SequentialAgent


def save_response(callback_context: CallbackContext, llm_response: LlmResponse) -> None:
    """save llm response to file"""
    if llm_response.content.parts[0].text:
        original_text = llm_response.content.parts[0].text
        print(f"response:{original_text}")
        with open("response.md", "w", encoding="utf-8") as f:
            f.write(f"response: {original_text}")

config = create_default_config()
selected_model = config.deepseek_chat
# selected_model = config.gpt_4o

image_viewer_agent = get_image_viewer_agent(config)
datasearch_agent = init_database_agent(config)
analysis_agent = init_analysis_agent(config)
job_recommend_agent = init_job_recommend_agent(config)

from .tools.a import mark_file_uploaded  # TODO

pipeline_agent = SequentialAgent(
    name="pipeline",
    description="1. 获取数据(datasearch_agent) 2. 生成报告(analysis_agent)",
    sub_agents=[datasearch_agent, analysis_agent]
)

root_agent = LlmAgent(
    name="basic_agent",
    model=selected_model,
    instruction=instructions_v1_zh,
    description="你是一个专业的岗位调研助手，根据用户需求，生成城市岗位调研报告，或者根据用户需求和调研报告改写用户简历。",
    output_key="labor_market_research",
    sub_agents=[image_viewer_agent, pipeline_agent, job_recommend_agent],
    # after_model_callback=save_response
    before_model_callback=mark_file_uploaded,
)
