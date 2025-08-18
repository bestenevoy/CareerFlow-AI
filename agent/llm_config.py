from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import os

load_dotenv()

SUPPORTED_PROVIDERS = ["openai", "deepseek", "gemini", "azure"]
# "anthropic", "perplexity", "huggingface", "local", "azureopenai"

MODEL_MAPPING = {
    ("openai", "gpt-4o"): "openai/gpt-4o",
    ("openai", "gemini-2.5-pro-preview-05-06"): "openai/gemini-2.5-pro-preview-05-06",
    ("openai", "gemini-2.5-flash-preview-05-20"): "openai/gemini-2.5-flash-preview-05-20",
    ("deepseek", "deepseek-chat"): "deepseek/deepseek-chat",
    ("gemini", "gemini-2.0-flash"): "google/gemini-2.0-flash",
}

DEFAULT_MODEL = "deepseek/deepseek-chat"


class LLMConfig:

    def __init__(self):
        self.target_language = 'zh'

        model_provider = "openai"
        gemini_2_5_flash = "gemini-2.5-flash-preview-05-20"
        gemini_2_flash = "gemini-2.0-flash"
        gpt_4o = "gpt-4o"
        gemini_2_5_pro = "gemini-2.5-pro-preview-05-06"
        deepseek_chat = "deepseek-chat"
        self.server_url = os.getenv("SERVER_URL", "localhost")
        # Helper to init any provider model
        def _init_model(provider_key: str, model_name: str):
            return LiteLlm(model=MODEL_MAPPING.get((provider_key, model_name), DEFAULT_MODEL))

        self.gpt_4o = _init_model(model_provider, gpt_4o)
        self.gemini_2_5_flash = _init_model(model_provider, gemini_2_5_flash)
        self.gemini_2_5_pro = _init_model(model_provider, gemini_2_5_pro)
        self.deepseek_chat = _init_model(model_provider, deepseek_chat)
        self.gemini_2_flash = _init_model(model_provider, gemini_2_flash)


def create_default_config() -> LLMConfig:
    return LLMConfig()

if __name__ == "__main__":
    config = create_default_config()
    print(f"Gemini 2.5 Flash: {config.gemini_2_5_flash}")
    print(f"Gemini 2.5 Pro: {config.gemini_2_5_pro}")
    print(f"GPT 4o: {config.gpt_4o}")
