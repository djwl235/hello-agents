from config import Config
config = Config()
print("provider:", config.llm_provider)
print("model:", config.llm_model)
print("base_url:", config.llm_base_url)
print("has_api_key:", bool(config.llm_api_key))