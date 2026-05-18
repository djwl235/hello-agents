import os
from pathlib import Path


def load_env_file(env_path=None):
    env_path = Path(env_path or Path(__file__).with_name(".env"))

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        os.environ.setdefault(key, value)


class Config:
    def __init__(self, env_path=None):
        load_env_file(env_path)

        self.llm_provider = os.getenv("LLM_PROVIDER", "mock")
        self.llm_api_key = os.getenv("LLM_API_KEY", "")
        self.llm_model = os.getenv("LLM_MODEL", "")
        self.llm_base_url = os.getenv("LLM_BASE_URL", "")
