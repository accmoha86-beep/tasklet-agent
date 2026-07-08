# Tasklet Agent 🤖

An intelligent AI agent framework that can understand tasks, plan steps, use tools, and execute complex workflows autonomously.

## Features

✅ **Natural Language Understanding** - Parse user requests and extract intent
✅ **Intelligent Planning** - Break down tasks into actionable steps
✅ **Tool Integration** - Execute actions using various tools
✅ **Memory & Context** - Remember conversation history and previous actions
✅ **GitHub Integration** - Create files, manage repos, and more
✅ **Error Handling** - Handle failures gracefully and recover
✅ **Extensible** - Easy to add new tools and capabilities
✅ **Logging** - Track all agent actions and decisions

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- API Key for an LLM (OpenAI, Anthropic, or local model)

### Installation

```bash
# Clone the repository
git clone https://github.com/accmoha86-beep/tasklet-agent.git
cd tasklet-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Basic Usage

```python
from agent import TaskletAgent

# Initialize the agent
agent = TaskletAgent(
    model="gpt-4",
    api_key="your-api-key-here"
)

# Give it a task
result = agent.run("Create a Python script that reads a CSV file")
print(result)
```

## Project Structure

```
tasklet-agent/
├── agent/
│   ├── __init__.py              # Main exports
│   ├── core.py                  # Core agent logic
│   ├── llm.py                   # LLM integration
│   ├── tools.py                 # Tool system
│   ├── memory.py                # Memory management
│   └── utils.py                 # Utilities
├── tools/
│   ├── __init__.py
│   ├── file_tools.py            # File operations
│   └── github_tools.py          # GitHub integration
├── examples/
│   ├── basic_example.py         # Simple usage
│   └── github_example.py        # GitHub integration
├── tests/
│   ├── test_agent.py            # Agent tests
│   └── test_tools.py            # Tool tests
├── config/
│   ├── __init__.py
│   ├── settings.py              # Configuration
│   └── prompts.py               # Agent prompts
├── .env.example                 # Environment template
├── requirements.txt             # Dependencies
├── setup.py                     # Package setup
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## Configuration

Create a `.env` file based on `.env.example`:

```env
# LLM Configuration
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=your-api-key-here
LLM_TEMPERATURE=0.7

# GitHub Configuration
GITHUB_TOKEN=your-github-token
GITHUB_USERNAME=your-username

# Agent Configuration
AGENT_MAX_STEPS=10
DEBUG_MODE=true
```

## How It Works

### Agent Loop

1. **Input** → Receive user request
2. **Understanding** → Parse and extract intent
3. **Planning** → Break down into steps
4. **Execution** → Execute each step with tools
5. **Feedback** → Get results and adjust
6. **Output** → Provide final result

## Available Tools

### File Tools
- `create_file` - Create a new file
- `read_file` - Read file contents
- `delete_file` - Remove a file
- `list_directory` - List files in a directory

### Built-in Tools
- `echo` - Echo back input
- `print` - Print a message

## Examples

### Simple Task

```python
from agent import TaskletAgent

agent = TaskletAgent(debug=True)
result = agent.run("Write a hello world program in Python")
print(result["response"])
```

### With Custom Tool

```python
from agent import TaskletAgent, BaseTool

class MyTool(BaseTool):
    name = "my_tool"
    description = "Does something"
    
    def execute(self, **kwargs):
        return "Result"

agent = TaskletAgent()
agent.register_tool(MyTool())
result = agent.run("Use my_tool")
```

## Advanced Usage

### Custom Tools

Create custom tools by extending `BaseTool`:

```python
from agent.tools import BaseTool

class MyCustomTool(BaseTool):
    name = "my_tool"
    description = "What it does"
    
    def execute(self, param1: str, **kwargs):
        # Your implementation
        return {"result": "success"}

# Register it
agent.register_tool(MyCustomTool())
```

### Memory Management

```python
# Store facts
agent.memory.store_fact("api_key", "secret")

# Recall facts
api_key = agent.memory.recall_fact("api_key")

# Get all memory
all_memory = agent.memory.get_all()

# Clear memory
agent.clear_memory()
```

## Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=agent tests/
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Roadmap

- [ ] Web UI for agent interaction
- [ ] Database integration
- [ ] Scheduled task execution
- [ ] Multi-agent collaboration
- [ ] Advanced reasoning
- [ ] Fine-tuning capabilities
- [ ] More LLM providers

---

Built with ❤️ for developers who want intelligent automation 💪
