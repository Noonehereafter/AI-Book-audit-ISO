from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMConfig(BaseModel):
    provider_type: Literal["openai", "gemini"] = "openai"
    base_url: str = "http://localhost:11434/v1"
    api_key: str = "dummy-key"
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.1
    timeout_seconds: float = 60.0
    max_retries: int = 3
    thinking_budget: int = 12000


class AuditConfig(BaseModel):
    deep_mode: bool = True
    auto_discover_source: bool = True
    allow_grandparent_discovery: bool = True
    output_dir: str = "audit_output"
    cache_dir: str = ".audit_cache"


class CompletionConfig(BaseModel):
    maximum_workflow_rounds: int = 3
    recheck_after_major_or_critical: bool = True


class Settings(BaseSettings):
    llm: LLMConfig = Field(default_factory=LLMConfig)
    audit: AuditConfig = Field(default_factory=AuditConfig)
    completion: CompletionConfig = Field(default_factory=CompletionConfig)

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def load(cls, config_path: str | Path | None = None) -> Settings:
        if config_path is None:
            config_path = Path("configs/config.yaml")
        else:
            config_path = Path(config_path)

        data: dict[str, Any] = {}
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

        return cls(**data)
