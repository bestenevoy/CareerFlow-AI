
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
    if tool_context.state.get('analysis_agent_tool_call', None) is None:
        tool_context.state['analysis_agent_tool_call'] = [tool_info]
    else:
        toolcall = tool_context.state['analysis_agent_tool_call']
        toolcall.append(tool_info)
        tool_context.state['analysis_agent_tool_call'] = toolcall
    return


def init_analysis_agent(config):
    """Initialize the analysis agent with the given configuration."""
    selected_model = config.deepseek_chat

    jc = JobCrawler()

    def analyze_salary_by_industry(job_name: str, city_name: str, tool_context: ToolContext) -> dict:

        """
        根据行业维度统计并可视化对应城市、职位的薪资分布。
        Args:
            job_name : str
                职位关键词，如 "Python"。
            city_name : str
                城市名称，必须在 `get_cities_list()` 返回的可选列表内。
        Returns:
            dict
                - img_tag (str): 生成的薪资分布图片的 markdown 标签。
                - data (dict): 以行业为键、对应薪资列表为值的统计结果。
        """
        try:
            res = jc.box_analysis(job_name, city_name)
            print('analyze_salary_by_industry', res)
            return res
        except Exception as e:
            return e
    
    def analyze_job_distribution_by_industry(job_name: str, city_name: str) -> dict:
        """
        按行业统计指定城市、职位的招聘数量及占比，并生成可视化图表。

        Args:
            job_name : str
                职位关键词，例如 "Python"。
            city_name : str
                城市名称，必须是 `get_cities_list()` 返回列表中的有效值。

        Returns:
            dict
                img_tag: str,  # 生成的分布图文件名
                data: dict     # 以行业为键，招聘数量及占比为值的统计结果
        """
        try:
            res = jc.pie_analysis(job_name, city_name)
            return res
        except Exception as e:
            return e

    def gen_job_keywords_wordcloud(job_name: str, city_name: str) -> dict:
        """
        统计岗位关键字数量，并生成词云图。

        Args:
            job_name : str
                职位关键词，例如 "Python"。
            city_name : str
                城市名称，必须是 `get_cities_list()` 返回列表中的有效值。

        Returns:
            dict
                "file_name": str,  # 生成的分布图markdown <img>标签
                "data": dict       # 在搜索条件下所有工作岗位的关键字统计结果
        """
        try:
            res = jc.wordcloud(job_name, city_name)
            print('analysis_job_brandIndustry_dist', res)
            return res
        except Exception as e:
            return e


    # image_viewer_agent = get_image_viewer_agent(config)
    analysis_agent = LlmAgent(
        name="analysis_agent",
        model=selected_model,
        instruction=instructions_v1_zh,
        description="根据用户的问题，查询岗位信息",
        tools=[analyze_salary_by_industry, analyze_job_distribution_by_industry, gen_job_keywords_wordcloud],
        # sub_agents=[image_viewer_agent],
        output_key="analysis_result",
        after_tool_callback=save_query_results,
    )
    return analysis_agent

if __name__ == "__main__":
    config = create_default_config()
    root_agent = init_analysis_agent(config)

