# Cursor Note Automation

An automated note-taking system that generates daily notes in the McCormick/Carmack style using AI assistance.

## Features

- Automated daily note generation
- AI-powered content generation using OpenAI or Anthropic
- Task tracking with status indicators
- Flexible scheduling options
- Rich command-line interface
- Configurable templates and formats

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cursor-note-automation
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the application:
   - Copy `config/config.yaml` to create your own configuration
   - Add your API keys for OpenAI or Anthropic
   - Adjust other settings as needed

## Usage

### Generate a Note

```bash
python src/main.py generate --analyze "Your analysis" --strategize "Your strategy"
```

### Add a Task

```bash
python src/main.py add-task "Task description" --today  # Mark as completed today
python src/main.py add-task "Task description" --later  # Mark as completed later
python src/main.py add-task "Task description" --against  # Mark as decided against
```

### Start the Scheduler

```bash
python src/main.py start-scheduler
```

### Check System Status

```bash
python src/main.py status
```

## Configuration

The `config.yaml` file contains all configurable options:

- AI provider settings (OpenAI/Anthropic)
- Note generation settings
- Automation schedule
- Logging preferences

## Task Prefixes

- `*` - Tasks completed on the current day
- `+` - Tasks completed on a later day
- `-` - Tasks decided against on a later day
- No prefix - Tasks mentioned but not yet addressed

## Directory Structure

```
cursor_note_automation/
├── src/               # Source code
├── config/            # Configuration files
├── templates/         # Note templates
├── logs/             # Application logs
├── notes/            # Generated notes
└── scripts/          # Utility scripts
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 