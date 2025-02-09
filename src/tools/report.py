from ..base import Tool
from ..conversation import Conversation
from typing import Dict, Any, List
import jinja2
import json
from pydantic import BaseModel
from copy import deepcopy
from rich.console import Console

logger = Console()


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
            logger.log(f"[bold green]Writing section: {section.title}[/bold green]")
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
        logger.log(f"[bold green]Planning a structure for the report.[/bold green]")
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
