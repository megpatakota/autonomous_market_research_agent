# AI-Powered Conversational Agent

[![Personal Project](https://img.shields.io/badge/Project-Personal-green)](https://meg-patakota.github.io)
[![by Meg Patakota](https://img.shields.io/badge/by-Meg%20Patakota-blue)](https://meg-patakota.github.io)
[![Project Status](https://img.shields.io/badge/Status-In%20Development-orange)](https://github.com/yourusername/autonomous_market_research_agent)

> ⚠️ **Disclaimer:** This project is a work in progress. Features, documentation, and code structure may evolve.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Next Steps](#next-steps)
- [Contributing](#contributing)

---

## Overview


This project is an **AI-powered autonomous agent** designed for **market research**. It leverages advanced reasoning, search capabilities, and structured response generation to dynamically interact with user queries.

The agent is designed to:
- Conduct **multi-step reasoning** before generating responses.
- Search and retrieve **relevant data** using the **Tavily API**.
- Handle multiple **conversation turns** while maintaining context.
- Generate structured **market research reports**.

The system runs **through a CLI interface**, where users input queries, and the agent autonomously determines the best tools to execute.


---

## Installation

### Prerequisites
- Python 3.13
- Poetry (for dependency management)
- API Keys:
    - **OPENAI_API_KEY** (for reasoning and response generation)
    - **TAVILY_API_KEY** (for external search capabilities)
        - Go to the [Tavily website](https://docs.tavily.com/api-reference/introduction) to get an API Key.

### Setup
Run the following in your command line/terminal

```bash
# Clone the repository
git clone https://github.com/yourusername/autonomous_market_research_agent.git
cd autonomous_market_research_agent

# Install dependencies
poetry install

# Run the app
export OPENAI_API_KEY="your-api-key-here"
export TAVILY_API_KEY="your-tavily-api-key-here"
poetry run python app.py
```

---
## Architecture

This agent follows a **modular architecture**, selecting actions dynamically based on user queries and conversation history.

![Architecture](./images/ProcessDiagram.png)

### Key Components:
1. **CLI Program (`app.py`)**  
   - Handles user input and manages the conversational flow.
   - Stores conversation history.
   
2. **Main Agent (`agent.py`)**  
   - Selects the best **tool** to use at each step.
   - Can perform multiple actions per query (reasoning, research, clarification).
   - Terminates when a valid response is generated.

3. **Available Tools**  
   - **Reasoning (`reasoning.py`)** → Processes user queries logically.
   - **Search (`search.py`)** → Uses **TavilyClient** to find relevant data.
   - **Extract (`extract.py`)** → Uses **TavilyClient** and extracts insights from retrieved documents.
   - **Respond (`respond.py`)** → Generates final structured responses.
   - **Research Agent (`research.py`)** → Conducts iterative searches and summarizes results.
   - **Report (`report.py`)** → Generates structured **market research reports**.

---

## Next Steps
A few to consider:

- [ ] Improve prompt templates used. E.g: Consider using one reasoning template for main agent and research agent
- [ ] Expand to a **multi-agent** approach. E.g: model drafts a research plan → produces different research directions → one direction per agent running at the same time →c ompile and write report
- [ ] Evaluate the performance of the agent

---
## Contributing

1. Fork the repository.
2. Open an issue for discussion.
3. Submit a Pull Request with clear descriptions.

For further discussions or feedback, reach out via [my website](https://megpatakota.com).

---

## License

This project is maintained by **Meg Patakota**. Not licensed for redistribution without explicit permission.

---
