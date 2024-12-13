import uvicorn
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

def main():
    """Run the application."""
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "true").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )

if __name__ == "__main__":
    main() 