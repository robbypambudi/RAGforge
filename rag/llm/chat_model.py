import random
from abc import ABC

import openai
from openai import OpenAI

from rag.utils import num_tokens_from_string


class Base(ABC):
    def __init__(self, key, model_name, base_url):
        timeout = 600
        self.client = OpenAI(api_key=key, base_url=base_url, timeout=timeout)
        self.model_name = model_name
        self.max_retries = 5
        self.base_delay = 2
        self.is_tools = False

    def _get_delay(self, attempt):
        """
        Calculate the delay before the next retry based on the attempt number.

        Args:
            attempt (int): The current attempt number.

        Returns:
            float: The delay in seconds.
        """
        return self.base_delay * (2 ** (attempt - 1) + random.uniform(0, 1))

    def total_token_count(self, response) -> int:
        """
        Calculate the total token count from the response.

        Args:
            response: The response object from the OpenAI API.

        Returns:
            int: The total token count.
        """
        try:
            return response.usage.total_tokens
        except Exception:
            pass
        try:
            return response["usage"]["total_tokens"]
        except Exception:
            pass
        return 0

    def chat_streamly(self, system: str, history: list, gen_conf: dict):
        """
        Generate a response using the OpenAI chat completion API with streaming.
        Args:
            system (str): The system message to set the context.
            history (list): The conversation history.
            gen_conf (dict): Additional generation configuration.
        Yields:
            str: The generated response.
            int: The total token count.
        """
        if system:
            history.insert(0, {"role": "system", "content": system})
        if "max_tokens" in gen_conf:
            del gen_conf["max_tokens"]

        ans = ""
        total_tokens = 0
        reasoning_start = False

        try:
            response = self.client.chat.completions.create(model=self.model_name, messages=hikstory, stream=True,
                                                           **gen_conf)
            for resp in response:
                if not resp.choices:
                    continue
                if not resp.choices[0].delta.content:
                    resp.choices[0].delta.content = ""
                if hasattr(resp.choices[0].delta, "reasoning_content" and resp.choices[0].delta.reasoning_content):
                    ans = ""
                    if not reasoning_start:
                        reasoning_start = True
                        ans = "<think>"
                    ans += resp.choices[0].delta.reasoning_content + "</think>"
                else:
                    reasoning_start = False
                    ans += resp.choices[0].delta.content

                temp_total_tokens = self.total_token_count(resp)

                if not total_tokens:
                    total_tokens += num_tokens_from_string(resp.choices[0].delta.content)
                else:
                    total_tokens += temp_total_tokens

                if resp.choices[0].finish_reason == "length":
                    ans += "...\n Jawaban akan terpotong oleh LLM yang Anda pilih karena keterbatasannya dalam hal panjang konteks."
                yield ans
        except openai.APIError as e:
            yield ans + f"API Error: {str(e)}"

        yield total_tokens
