"""
LLM Interface Module: Handles model access via OpenRouter/Groq/OpenAI APIs or local/mock provider with fallback and error handling.
"""

import os
import json
import time
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "meta-llama/llama-3.1-8b-instruct")
        self.use_mock = os.getenv("USE_MOCK_LLM", "false").lower() in ["true", "1", "yes"]

    def complete(self, messages: List[Dict[str, str]], temperature: float = 0.0, max_tokens: int = 800) -> str:
        """
        Sends chat completion request to configured LLM API.
        Falls back to mock mode if API fails or if USE_MOCK_LLM is enabled.
        """
        if self.use_mock or not self.api_key or self.api_key == "your_key_here":
            return self._mock_response(messages)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://cloudserve.internal",
            "X-Title": "CloudServe-Support-AI"
        }

        # Handle OpenRouter vs OpenAI endpoint
        if self.api_key.startswith("sk-or-"):
            url = "https://openrouter.ai/api/v1/chat/completions"
        elif "groq" in self.api_key.lower():
            url = "https://api.groq.com/openai/v1/chat/completions"
        else:
            url = "https://api.openai.com/v1/chat/completions"

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        max_retries = 3
        backoff = 1.0

        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=25)
                if response.status_code == 200:
                    data = response.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0]["message"]["content"].strip()
                elif response.status_code in [429, 502, 503, 504]:
                    time.sleep(backoff)
                    backoff *= 2
                else:
                    break
            except Exception:
                time.sleep(backoff)
                backoff *= 2

        # Graceful degradation fallback if external API is unreachable or fails
        return self._mock_response(messages)

    def _mock_response(self, messages: List[Dict[str, str]]) -> str:
        """Deterministic mock response generator for offline execution and tests."""
        user_msg = ""
        sys_msg = ""
        for m in messages:
            if m["role"] == "system":
                sys_msg += m["content"]
            elif m["role"] == "user":
                user_msg += m["content"]

        combined = (sys_msg + " " + user_msg).lower()

        # Classification prompt mock
        if "classify" in sys_msg.lower() or "intent" in sys_msg.lower():
            intent = "deployment_failure"
            urgency = "high"
            if "bill" in combined or "invoice" in combined or "pricing" in combined:
                intent = "billing_query"
                urgency = "medium"
            elif "password" in combined or "sso" in combined or "login" in combined or "auth" in combined:
                intent = "authentication_failure"
                urgency = "high"
            elif "export" in combined or "data" in combined:
                intent = "data_export"
                urgency = "low"
            elif "security" in combined or "compromise" in combined:
                intent = "security_incident"
                urgency = "high"

            return json.dumps({
                "intent": intent,
                "urgency": urgency,
                "confidence": 0.92,
                "reasoning": f"Mock classification based on detected keywords for {intent}.",
                "alternatives_considered": [{"intent": "configuration_help", "confidence": 0.05}]
            })

        # Answer generation mock
        if "generate" in sys_msg.lower() or "documentation" in sys_msg.lower() or "answer" in sys_msg.lower():
            if "doc-" in combined or "doc" in combined or "documentation" in combined:
                return "Based on our documentation [DOC-DEPLOY-001], to resolve deployment failures caused by container health check issues, ensure your health check endpoint returns an HTTP 200 within 30 seconds."
            return "I'm unable to find relevant documentation to answer this question. Escalating to human support."

        return "Response processed successfully."


# Global client instance
llm_client = LLMClient()
