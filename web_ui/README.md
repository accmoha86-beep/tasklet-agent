# Tasklet Agent - Web UI

Interactive web interface for the Tasklet Agent framework.

## Features

- 🎯 **Task Execution** - Submit tasks and watch the agent work in real-time
- 📊 **Execution History** - View all previous task executions
- 🧠 **Memory Viewer** - Inspect agent memory and stored facts
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- ⚡ **Real-time Updates** - Live status and progress indicators
- 🎨 **Modern UI** - Clean, intuitive interface with smooth animations

## Installation

### Prerequisites

- Python 3.8+
- Tasklet Agent installed and configured
- API keys set up in `.env`

### Setup

1. Install web UI dependencies:

```bash
pip install -r web_ui/requirements.txt
```

2. Ensure your `.env` file is configured:

```env
# LLM Configuration
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=your-api-key-here

# Web UI Configuration
WEB_UI_PORT=5000
DEBUG_MODE=false
```

## Running the Web UI

### Development

```bash
cd web_ui
python app.py
```

The web UI will be available at `http://localhost:5000`

### Production

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_ui.app:app
```

## API Endpoints

### Execute Task

**POST** `/api/execute`

Execute a task with the agent.

```json
{
  "task": "Create a Python script that reads a CSV file"
}
```

Response:

```json
{
  "status": "success",
  "task": "Create a Python script that reads a CSV file",
  "response": "Here's a Python script...",
  "plan": [...],
  "results": [...],
  "duration_seconds": 2.34,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Get History

**GET** `/api/history`

Retrieve execution history (last 20 executions).

Response:

```json
{
  "count": 5,
  "executions": [...]
}
```

### Get Memory

**GET** `/api/memory`

Retrieve agent memory.

Response:

```json
{
  "facts": {...},
  "results": {...}
}
```

### Clear Memory

**POST** `/api/clear-memory`

Clear all agent memory.

Response:

```json
{
  "status": "success",
  "message": "Memory cleared"
}
```

### Get Status

**GET** `/api/status`

Get agent status and configuration.

Response:

```json
{
  "status": "running",
  "model": "gpt-4",
  "provider": "openai",
  "max_steps": 10,
  "executions": 5,
  "timestamp": "2024-01-15T10:30:00"
}
```

## File Structure

```
web_ui/
├── app.py              # Flask application and API endpoints
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Main HTML page
├── static/
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
└── README.md           # This file
```

## Configuration

### Environment Variables

Set these in your `.env` file:

```env
# LLM Configuration
LLM_PROVIDER=openai|anthropic|local
LLM_MODEL=gpt-4|claude-3-sonnet|etc
LLM_API_KEY=your-api-key
LLM_TEMPERATURE=0.7

# Agent Configuration
AGENT_MAX_STEPS=10
DEBUG_MODE=false|true

# Web UI Configuration
WEB_UI_PORT=5000
```

## Usage Examples

### From the Web UI

1. Open `http://localhost:5000` in your browser
2. Enter a task in the text area
3. Click "Execute Task" or press Ctrl+Enter
4. View results, history, and agent memory

### Programmatic API Usage

```bash
# Execute a task
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Create a hello world Python script"}'

# Get history
curl http://localhost:5000/api/history

# Get agent memory
curl http://localhost:5000/api/memory

# Clear memory
curl -X POST http://localhost:5000/api/clear-memory

# Get status
curl http://localhost:5000/api/status
```

## Keyboard Shortcuts

- **Ctrl+Enter** - Execute task (when focused in task input)
- **Click history item** - Load task back into input field

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Connection Error

**Issue:** "Disconnected" status

**Solution:** 
- Ensure the Flask app is running: `python app.py`
- Check the port configuration (default: 5000)
- Verify firewall settings

### Task Execution Fails

**Issue:** Task execution returns error

**Solutions:**
- Check LLM API credentials in `.env`
- Verify LLM provider is configured correctly
- Check agent logs for detailed error messages
- Ensure sufficient API quota/credits

### Memory Issues

**Issue:** Agent memory grows too large

**Solution:** Click "Clear Memory" button to reset

## Performance Tips

- Use a faster LLM model for quick tasks
- Set appropriate `AGENT_MAX_STEPS` to limit execution time
- Use `DEBUG_MODE=false` in production for better performance
- Consider caching frequently used prompts

## Contributing

Contributions welcome! Please:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License - See LICENSE file in root directory
