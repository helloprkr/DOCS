# Note Automation System - User Instructions

## Environment Setup

### Local Installation
1. Clone the repository to your local machine
2. Ensure Python 3.8+ is installed
3. Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### API Keys
1. Copy your API keys to `.env`:
```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

## Running the Application

### Command Line Interface
The application runs as a CLI tool. All commands are run through `src/main.py`.

#### Basic Commands:

1. Generate a Note:
```bash
python3 src/main.py generate \
  --analyze "Your analysis" \
  --strategize "Your strategy" \
  --pre-problem-solve "Pre-problem solving" \
  --outlining "Your outline" \
  --outcome "Your outcome" \
  --end-state "Your end state"
```

2. Add Tasks:
```bash
# Add a pending task
python3 src/main.py add-task "Your task description"

# Add a completed task
python3 src/main.py add-task "Your task description" --today

# Add a task completed later
python3 src/main.py add-task "Your task description" --later

# Add a decided against task
python3 src/main.py add-task "Your task description" --against
```

3. List Tasks:
```bash
python3 src/main.py list-tasks
```

4. Clear All Data:
```bash
python3 src/main.py clear
```

5. Check System Status:
```bash
python3 src/main.py status
```

### Task Status Symbols
- `*` - Task completed today
- `+` - Task completed later
- `-` - Task decided against
- No symbol - Pending task

## Directory Structure
```
.
├── src/               # Source code
├── data/              # Persistent data storage
├── notes/             # Generated notes
├── logs/              # Application logs
└── templates/         # Note templates
```

## Note Format
Notes are generated in Markdown format with the following sections:
- Analysis
- Strategy
- Pre-Problem Solving
- Outline
- Outcomes
- End State
- Tasks

## Automation

### Starting the Scheduler
```bash
python3 src/main.py start-scheduler
```

### Configuration
Edit `config/config.yaml` to customize:
- AI provider (OpenAI/Anthropic)
- Note generation settings
- Automation schedule
- Logging preferences

## Integration with Cursor

### Current Implementation
The system currently runs as a standalone CLI application. To integrate with Cursor:

1. Clone the repository into your Cursor workspace
2. Open a terminal in Cursor
3. Run commands directly from Cursor's terminal

### Future Web Integration (Planned)
To enable web access:

1. Create a FastAPI/Flask wrapper around the current functionality
2. Add REST endpoints for each command
3. Create a web UI using React/Next.js
4. Run on localhost:3000

Example web integration code (planned):
```python
from fastapi import FastAPI
from src.main import app as cli_app

app = FastAPI()

@app.post("/generate")
async def generate_note(content: dict):
    # Call CLI functionality
    pass

@app.post("/tasks")
async def add_task(task: dict):
    # Call CLI functionality
    pass
```

## Troubleshooting

### Common Issues

1. API Key Issues:
```bash
# Check API configuration
python3 src/main.py status
```

2. Data Persistence Issues:
```bash
# Clear data and start fresh
python3 src/main.py clear
```

3. Task Management Issues:
```bash
# List all tasks to verify state
python3 src/main.py list-tasks
```

### Logs
Check `logs/app.log` for detailed error information.

## Best Practices

1. Note Generation:
- Keep section content concise and focused
- Use descriptive task names
- Update task statuses regularly

2. Task Management:
- Add tasks as they come up
- Mark completions promptly
- Clear old tasks regularly

3. Automation:
- Set scheduler time to match your workflow
- Check status regularly
- Monitor log files

## Performance Optimization

1. API Usage:
- Tasks use GPT-3.5-turbo for cost efficiency
- Batch processing for multiple tasks
- Token limits per request

2. Storage:
- Regular cleanup of old data
- Efficient JSON storage
- Automated log rotation

## Security Notes

1. API Keys:
- Store in `.env` file
- Never commit API keys
- Rotate keys regularly

2. Data Storage:
- Local storage only
- No sensitive data in notes
- Regular backups recommended

## Future Enhancements

1. Web Interface:
- React/Next.js frontend
- Real-time updates
- Rich text editing

2. Advanced Features:
- Task categories
- Note templates
- Export functionality

3. Integration:
- Calendar sync
- Git integration
- Cloud backup

## Support

For issues or questions:
1. Check logs in `logs/app.log`
2. Run status check
3. Clear data if needed
4. Reinstall if persistent issues 