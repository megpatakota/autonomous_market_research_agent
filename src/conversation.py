from typing import List, Optional
from pydantic import BaseModel
from litellm import completion


class Conversation:
    def __init__(self, model: str = "gpt-4o"):  # gemini/gemini-2.0-flash
        self.model = model
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_response(
        self,
        tool_choice: str = "auto",
        tools: Optional[List] = None,
        response_format: BaseModel = None,
    ):
        if tools is None:
            tool_choice = None

        return completion(
            model=self.model,
            messages=self.messages,
            tools=tools,
            tool_choice=tool_choice,
            response_format=response_format,
        )
