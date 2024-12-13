# Notes API Backend

A FastAPI-based backend for a note-taking application with gamification features.

## Features

- Note Management
  - Create, read, update, and delete notes
  - Tag support
  - Full-text search
  - User-specific notes

- Gamification
  - User progress tracking
  - Achievement system
  - Skill progression
  - Daily streaks
  - Points and levels

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- SQLite (default) or PostgreSQL

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create environment file:

```bash
cp .env.example .env
```

5. Initialize the database:

```bash
python init_data.py
```

## Configuration

Edit the `.env` file to configure:

- Server settings (host, port)
- Database connection
- Security settings
- CORS configuration
- Logging level

## Running the Application

1. Start the development server:

```bash
python run.py
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Notes

- `POST /api/notes` - Create a new note
- `GET /api/notes/{note_id}` - Get a note by ID
- `PUT /api/notes/{note_id}` - Update a note
- `DELETE /api/notes/{note_id}` - Delete a note
- `GET /api/users/{user_id}/notes` - Get all notes for a user
- `GET /api/users/{user_id}/notes/search` - Search user's notes
- `GET /api/users/{user_id}/tags` - Get all tags for a user
- `GET /api/users/{user_id}/notes/tag/{tag_name}` - Get notes by tag

### Gamification

- `GET /api/users/{user_id}/progress` - Get user progress
- `POST /api/users/{user_id}/points` - Award points
- `POST /api/users/{user_id}/streak` - Update streak
- `GET /api/users/{user_id}/achievements` - Get achievements
- `GET /api/users/{user_id}/skills` - Get user skills
- `POST /api/users/{user_id}/skills/{skill_id}/points` - Add skill points
- `GET /api/users/{user_id}/stats` - Get comprehensive stats

## Testing

1. Run the test suite:

```bash
python run_tests.py
```

2. View test coverage:

```bash
open htmlcov/index.html
```

## Development

### Project Structure

```
backend/
├── api/
│   ├── notes.py
│   └── gamification.py
├── database/
│   └── db.py
├── models/
│   ├── note.py
│   └── gamification.py
├── services/
│   ├── note_service.py
│   └── gamification_service.py
├── tests/
│   ├── test_notes.py
│   └── test_gamification.py
├── main.py
├── run.py
└── init_data.py
```

### Adding New Features

1. Create/modify models in `models/`
2. Implement business logic in `services/`
3. Add API endpoints in `api/`
4. Write tests in `tests/`
5. Update documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 