from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional
from urllib import error, request

from settings import PROJECT_SETTINGS


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    base_url: str
    api_key: str
    model: str
    timeout: float = 30.0
    headers: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_settings(cls, overrides: Optional[Dict[str, Any]] = None) -> "LLMConfig":
        source = dict(PROJECT_SETTINGS.get("llm", {}))
        if overrides:
            source.update(overrides)
        return cls(
            provider=source.get("provider", "custom"),
            base_url=source.get("base_url", ""),
            api_key=source.get("api_key", ""),
            model=source.get("model", ""),
            timeout=float(source.get("timeout", 30.0)),
            headers=dict(source.get("headers", {})),
        )


class LLMClient:
    def __init__(self, config: LLMConfig):
        self.config = config
        self._completions_url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        logger = logging.getLogger(__name__)
        logger.info(
            "Initialized LLM client with base_url=%s model=%s provider=%s",
            self.config.base_url,
            self.config.model,
            self.config.provider,
        )

    def chat(self, messages: Iterable[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.config.model,
            "messages": list(messages),
        }
        if kwargs:
            payload.update(kwargs)
        try:
            return self._dispatch(payload, purpose=kwargs.get("purpose"))
        except RuntimeError as exc:
            message = str(exc).lower()
            if "data policy" in message and self.config.model.endswith(":free"):
                logger = logging.getLogger(__name__)
                logger.warning(
                    "LLM data policy restriction encountered; retrying without ':free' suffix."
                )
                fallback_payload = dict(payload)
                fallback_payload["model"] = self.config.model.split(":")[0]
                return self._dispatch(fallback_payload, purpose=kwargs.get("purpose"), fallback=True)
            raise

    def _dispatch(self, payload: Dict[str, Any], *, purpose: Optional[str] = None, fallback: bool = False) -> Dict[str, Any]:
        logger = logging.getLogger(__name__)
        logger.info(
            "LLM chat call start model=%s url=%s purpose=%s fallback=%s",
            payload.get("model"),
            self._completions_url,
            purpose or "unspecified",
            fallback,
        )
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
        }
        headers.update(self.config.headers)
        req = request.Request(
            url=self._completions_url,
            data=data,
            headers=headers,
            method="POST",
        )
        try:
            start = time.perf_counter()
            with request.urlopen(req, timeout=self.config.timeout) as response:
                body = response.read().decode("utf-8")
            duration = time.perf_counter() - start
            logger.debug(
                "LLM chat response received (%s bytes) in %.3f seconds",
                len(body),
                duration,
            )
            return json.loads(body)
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            logger.error("LLM request failed with HTTP %s: %s", exc.code, body)
            raise RuntimeError(f"LLM request failed: {exc.code} {body}") from exc
        except error.URLError as exc:
            logger.error("LLM request failed due to network error: %s", exc.reason)
            raise RuntimeError(f"LLM request failed: {exc.reason}") from exc
        finally:
            if "duration" not in locals():
                duration = None
            logger.info(
                "LLM chat call end model=%s purpose=%s duration=%s seconds",
                payload.get("model"),
                purpose or "unspecified",
                f"{duration:.3f}" if duration is not None else "n/a",
            )


def create_llm_client(config_overrides: Optional[Dict[str, Any]] = None) -> LLMClient:
    config = LLMConfig.from_settings(config_overrides)
    return LLMClient(config)


def check_connection(client: LLMClient) -> bool:
    required = [client.config.base_url, client.config.api_key, client.config.model]
    return all(bool(value) for value in required)
