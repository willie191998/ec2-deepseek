from langchain.llms.base import LLM
import requests
import re
from typing import Any, Dict, List, Optional

class CustomLLM(LLM):
    api_url: str = "https://superearner.online/generate"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Call the custom API and clean up the response."""
        payload = {
            "prompt": prompt,
            "model": "deepseek-r1:7b",
            "stream": False,
            "max_tokens": 300,
            "temperature": 0.4
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            raw_response = response.json().get("response", "No response received.")

            # Remove <think>...</think> from the response
            clean_response = re.sub(r"<think>.*?</think>", "", raw_response, flags=re.DOTALL).strip()
            return clean_response

        except requests.exceptions.RequestException as e:
            return f"API Error: {str(e)}"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return model parameters."""
        return {"api_url": self.api_url}

    @property
    def _llm_type(self) -> str:
        return "custom_api"

# Create an instance of CustomLLM
llm = CustomLLM()