import argparse
import jinja2
import sys
from dotenv import load_dotenv

from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown

from src.conversation import Conversation
from src.agent import Agent
from src.tools import Respond, Search, Extract, Reasoning, Report



load_dotenv()


def main():
    # Parse CLI arguments for max turns for agents.
    parser = argparse.ArgumentParser(description="CLI Chat Application")
    parser.add_argument(
        "--main_turns",
        type=int,
        default=3,
        help="Max turns for the main agent (default: 3)",
    )
    parser.add_argument(
        "--research_turns",
        type=int,
        default=15,
        help="Max turns for the research agent (default: 15)",
    )
    args = parser.parse_args()

    # Read and render the system message template.
    try:
        with open("templates/system_message.jinja2", "r") as file:
            system_message = jinja2.Template(file.read()).render(tools="")
    except Exception as e:
        print(f"Error reading system_message template: {e}")
        sys.exit(1)

    # Initialize the conversation with the system message.
    conversation = Conversation()
    conversation.add_message("system", system_message)

    # Create the report tool.
    write_report = Report(terminating=True)

    # Set up the research agent with its tools.
    research_agent = Agent(
        name="research_agent",
        description="This agent is designed to autonomously carry out market research.",
        tools=[Search(), Extract(), Reasoning(), write_report],
        max_turns=args.research_turns,
        terminating=True,
        fallback_tool=write_report,
    )

    # Create the respond tool.
    respond = Respond(response_types=["respond", "clarification"])

    # Set up the main agent with its tools (including the research agent).
    main_agent = Agent(
        name="main_agent",
        description="This agent is designed to help users with market research.",
        tools=[Reasoning(), respond, research_agent],
        max_turns=args.main_turns,
        terminating=True,
        fallback_tool=respond,
    )

    # Set up Rich console for a rich CLI experience.
    console = Console()
    console.print("[bold magenta]Market Research Agent[/bold magenta]")
    console.print(
        "Type your message and press Enter to chat.\n"
        "Special commands: [bold green]reset[/bold green] to clear conversation (system message is retained), "
        "[bold red]exit[/bold red] or [bold red]quit[/bold red] to exit the chat."
    )

    # Chat loop.
    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")
        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting the chat. Goodbye![/bold red]")
            break

        # Check for exit command.
        if user_input.strip().lower() in ["exit", "quit"]:
            console.print("[bold red]Exiting the chat. Goodbye![/bold red]")
            break

        # Special command to reset the conversation (keeping the system prompt).
        if user_input.strip().lower() == "reset":
            if conversation.messages:
                conversation.messages = [
                    conversation.messages[0]
                ]  # Retain only the system message.
            else:
                conversation.messages = []
            console.print("[bold yellow]Conversation has been reset.[/bold yellow]")
            continue

        # Add the user's message to the conversation.
        conversation.add_message("user", user_input)
        console.print("[bold blue]Agent is thinking...[/bold blue]")

        try:
            # Run the main agent to get its response.
            response = main_agent.run(conversation)
        except Exception as e:
            console.print(f"[bold red]Error during agent processing: {e}[/bold red]")
            continue

        # Add and display the agent's response.
        conversation.add_message("assistant", response)
        console.print("[bold blue]Agent:[/bold blue]")
        console.print(Markdown(response))


if __name__ == "__main__":
    main()
