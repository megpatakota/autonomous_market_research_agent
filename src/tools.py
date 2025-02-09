from .base import Tool
from .conversation import Conversation
from typing import Dict, Any, List
import jinja2
import json
import os
from pydantic import BaseModel
from copy import deepcopy
from tavily import TavilyClient


class Reasoning(Tool):
    def __init__(self, terminating: bool = False):
        super().__init__(name="reasoning", terminating=terminating)

    def run(self, conversation: Conversation) -> str:
        with open("templates/reasoning.jinja2", "r") as file:
            reasoning_template = jinja2.Template(file.read()).render()
        conversation.add_message("system", reasoning_template)
        response = conversation.get_response(tool_choice=None)
        conversation.messages.pop()  # remove the reasoning message
        return response.choices[0].message.content

    def get_config(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "This tool provides reasoning for the given context.",
            },
        }


# Respond tool (terminating) – note the extra parameter `response_type`
class Respond(Tool):
    def __init__(self, response_types: List[str], terminating: bool = True):
        # Mark this tool as terminating since its response is meant to be final.
        super().__init__(name="respond", terminating=terminating)
        self.response_types = response_types

    def run(self, conversation: Conversation, response_type: str = "") -> str:
        if not response_type:
            response_type = "respond"

        with open(f"templates/{response_type}.jinja2", "r") as file:
            template_content = jinja2.Template(file.read()).render()
        conversation.add_message("system", template_content)
        response = conversation.get_response(tool_choice=None)
        conversation.messages.pop()
        return response.choices[0].message.content

    def get_config(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "This tool provides responses for the given user message.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "response_type": {
                            "type": "string",
                            "description": "The type of response to be generated.",
                            "enum": self.response_types,
                        },
                    },
                    "required": ["response_type"],
                },
            },
        }


class Section(BaseModel):
    title: str
    description: str


class Outline(BaseModel):
    title: str
    sections: List[Section]


class Report(Tool):
    def __init__(self, terminating: bool = True):
        super().__init__(name="report", terminating=terminating)

    def run(self, conversation: Conversation) -> str:
        outline = self.generate_outline(conversation)
        return self.write_report(conversation, outline)

    def write_report(self, conversation: Conversation, outline: Outline) -> str:

        report_conversation = deepcopy(conversation)

        report_so_far = f"# {outline.title}\n\n"

        for section in outline.sections:
            print(f"Writing section: {section.title}")

            with open("templates/write_report.jinja2", "r") as file:
                template = jinja2.Template(file.read()).render(
                    {
                        "outline": outline,
                        "current_section": section,
                        "report_so_far": report_so_far,
                    }
                )

            report_conversation.add_message("user", template)
            response = report_conversation.get_response(tool_choice=None)
            report_so_far += response.choices[0].message.content + "\n\n"

        return report_so_far

    def generate_outline(self, conversation: Conversation) -> Outline:
        with open("templates/report_outline.jinja2", "r") as file:
            template = jinja2.Template(file.read()).render()
        conversation.add_message("user", template)
        response = conversation.get_response(tool_choice=None, response_format=Outline)
        conversation.messages.pop()
        return Outline(**json.loads(response.choices[0].message.content))

    def get_config(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Generate a comprehensive report based on the research.",
            },
        }


# Search tool (non‐terminating)
class Search(Tool):
    def __init__(self, terminating: bool = False):
        super().__init__(name="search", terminating=terminating)
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def run(self, conversation: Conversation, query: str) -> str:
        response = self.tavily_client.search(query)
        return response

    def get_config(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Execute a search query using Tavily Search",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to search for",
                        },
                    },
                    "required": ["query"],
                },
            },
        }


class Extract(Tool):
    def __init__(self, terminating: bool = False):
        super().__init__(name="extract", terminating=terminating)
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def run(self, conversation: Conversation, urls: list[str]) -> str:
        response = self.tavily_client.extract(urls)
        return response

    def get_config(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Extract web page content from one or more specified URLs using Tavily Extract",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "urls": {
                            "type": "string",
                            "description": "The urls to extract from",
                        },
                    },
                    "required": ["urls"],
                },
            },
        }
