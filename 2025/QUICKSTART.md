# Quick Start Guide

## 1. First-Time Setup (2 minutes)
```bash
# Clone and setup
git clone <repository-url>
cd note-automation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your API key to .env
echo "OPENAI_API_KEY=your_key_here" > .env
```

## 2. Basic Usage (30 seconds)

### Add a Task
```bash
python3 src/main.py add-task "Your task" --today
```

### Generate a Note
```bash
python3 src/main.py generate \
  --analyze "Quick analysis" \
  --strategize "Basic strategy" \
  --end-state "Goal achieved"
```

### Check Status
```bash
python3 src/main.py status
```

## 3. Common Commands

### Task Management
```bash
# List tasks
python3 src/main.py list-tasks

# Clear all data
python3 src/main.py clear
```

### Automation
```bash
# Start daily scheduler
python3 src/main.py start-scheduler
```

## 4. Output Locations
- Notes: `notes/` directory
- Logs: `logs/app.log`
- Data: `data/` directory

## 5. Need Help?
1. Check `INSTRUCTIONS.md` for detailed documentation
2. Review logs in `logs/app.log`
3. Run `python3 src/main.py status` for system health 