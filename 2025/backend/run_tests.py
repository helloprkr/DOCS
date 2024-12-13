import pytest
import asyncio
import os
from dotenv import load_dotenv

# Load test environment variables
load_dotenv(".env.test")

def run_tests():
    """Run the test suite."""
    # Set test database URL
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"
    
    # Run pytest with async support
    pytest.main([
        "tests",
        "-v",
        "--asyncio-mode=auto",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=html"
    ])

if __name__ == "__main__":
    run_tests() 