from pathlib import Path
from epub_translate_audit.config import Settings, LLMConfig
from epub_translate_audit.ai.llm_client import LLMClient
from pydantic import BaseModel

class DummyResponse(BaseModel):
    status: str
    message: str

def test_config_load(tmp_path: Path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("""
llm:
  provider_type: "openai"
  base_url: "https://api.test.com/v1"
  model_name: "test-model"
""", encoding="utf-8")

    settings = Settings.load(cfg_file)
    assert settings.llm.provider_type == "openai"
    assert settings.llm.base_url == "https://api.test.com/v1"
    assert settings.llm.model_name == "test-model"

def test_llm_client_cache_key(tmp_path: Path):
    cfg = LLMConfig(provider_type="openai", base_url="https://api.test.com/v1", model_name="test-model")
    client = LLMClient(config=cfg, cache_dir=tmp_path / "cache")
    key1 = client._get_cache_key("hello", DummyResponse)
    key2 = client._get_cache_key("hello", DummyResponse)
    assert key1 == key2
