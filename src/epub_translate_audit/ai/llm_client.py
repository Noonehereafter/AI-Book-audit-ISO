from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any, TypeVar
import httpx
from pydantic import BaseModel
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from epub_translate_audit.config import LLMConfig

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    """Universal LLM Client supporting OpenAI-compatible proxies (9router, omniroute, kilo, LM Studio, Ollama)

    and native Gemini API endpoints, with caching and structured output parsing.
    """

    def __init__(self, config: LLMConfig, cache_dir: Path | str | None = None) -> None:
        self.config = config
        self.cache_dir = Path(cache_dir) if cache_dir else Path(".audit_cache/llm_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, prompt: str, schema: type[BaseModel] | None, system_prompt: str | None = None) -> str:
        schema_name = schema.__name__ if schema else "raw"
        raw = f"{self.config.provider_type}|{self.config.base_url}|{self.config.model_name}|{schema_name}|{system_prompt or ''}|{prompt}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def fetch_models(self) -> list[str]:
        """Fetch list of available models from endpoint."""
        if self.config.provider_type == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.config.api_key}"
        else:
            url = self.config.base_url.rstrip("/") + "/models"

        headers = {}
        if self.config.provider_type != "gemini" and self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        try:
            with httpx.Client(timeout=10.0) as client:
                resp = client.get(url, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                models = []
                if self.config.provider_type == "gemini" and "models" in data:
                    for item in data["models"]:
                        name = item.get("name", "").replace("models/", "")
                        if name:
                            models.append(name)
                elif isinstance(data, dict) and "data" in data:
                    for item in data["data"]:
                        if isinstance(item, dict) and "id" in item:
                            models.append(item["id"])
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "id" in item:
                            models.append(item["id"])
                        elif isinstance(item, str):
                            models.append(item)
                return models if models else [self.config.model_name]
        except Exception as e:
            logger.warning("Failed to fetch models from %s: %s", url, e)
            return [self.config.model_name]

    @retry(
        retry=retry_if_exception_type((httpx.HTTPError, TimeoutError)),
        wait=wait_exponential_jitter(initial=1, max=10),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def generate_structured(self, prompt: str, schema: type[T], system_prompt: str | None = None) -> T:
        """Call LLM with structured JSON output enforced by Pydantic schema."""
        cache_key = self._get_cache_key(prompt, schema, system_prompt)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            try:
                content = cache_file.read_text(encoding="utf-8")
                return schema.model_validate_json(content)
            except Exception as e:
                logger.warning("Cache invalid for key %s: %s", cache_key, e)

        schema_json = json.dumps(schema.model_json_schema(), ensure_ascii=False, indent=2)
        base_system = (
            "You are a strict bilingual translation auditor. You MUST reply ONLY with a valid JSON object "
            f"matching this Pydantic schema:\n{schema_json}\nDo NOT wrap in markdown triple backticks."
        )
        final_system = f"{system_prompt}\n\n{base_system}" if system_prompt else base_system

        if self.config.provider_type == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.model_name}:generateContent?key={self.config.api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": f"{final_system}\n\nUSER PROMPT:\n{prompt}"}]}],
                "generationConfig": {
                    "temperature": self.config.temperature,
                    "responseMimeType": "application/json",
                },
            }
        else:
            url = self.config.base_url.rstrip("/") + "/chat/completions"
            headers = {"Content-Type": "application/json"}
            if self.config.api_key:
                headers["Authorization"] = f"Bearer {self.config.api_key}"

            payload = {
                "model": self.config.model_name,
                "messages": [
                    {"role": "system", "content": final_system},
                    {"role": "user", "content": prompt},
                ],
                "temperature": self.config.temperature,
                "response_format": {"type": "json_object"},
            }

        with httpx.Client(timeout=self.config.timeout_seconds) as client:
            resp = client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            res_data = resp.json()

            if self.config.provider_type == "gemini":
                raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                raw_text = res_data["choices"][0]["message"]["content"]

        cleaned_text = raw_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

        result = schema.model_validate_json(cleaned_text)
        cache_file.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        return result
