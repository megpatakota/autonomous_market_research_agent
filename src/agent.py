from typing import List
from .conversation import Conversation
from .base import Tool
import json
from rich.console import Console

logger = Console()

class Agent(Tool):
    def __init__(
        self,
        name: str,
        description: str,
        fallback_tool: Tool,
        max_turns: int = 3,
        terminating: bool = False,
        tools: List[Tool] = [],
    ):
        super().__init__(name=name, terminating=terminating)
        self.description = description
        self.max_turns = max_turns
        self.available_tools = {tool.name: tool for tool in tools}
        self.fallback_tool = fallback_tool

    def run(self, conversation: Conversation) -> str:
        for turn in range(self.max_turns):
            tool, function_args = self.get_next_action(conversation)
            logger.log(f"[bold cyan]Using the {tool.name} tool with arguments {function_args}[/bold cyan]")
            response = tool.run(conversation, **function_args)
            if tool.terminating:
                return response

            conversation.add_message(
                "user",
                f"The {tool.name} tool has been used with args {function_args} and it responded with {response}",
            )
        return self.fallback_tool.run(conversation)

    def get_next_action(self, conversation: Conversation) -> Tool:
        response = conversation.get_response(
            tool_choice="required",
            tools=[tool.get_config() for tool in self.available_tools.values()],
        )
        tool_calls = response.choices[0].message.tool_calls
        function_name = tool_calls[0].function.name
        function_args = json.loads(tool_calls[0].function.arguments)
        return self.available_tools[function_name], function_args

    def get_config(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
            },
        }
