import yaml
import logging
import os
from pathlib import Path
from typing import Dict, Any
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file with environment variable substitution."""
    try:
        # Load environment variables
        load_dotenv()
        
        with open(config_path, 'r') as f:
            # Load YAML content
            config = yaml.safe_load(f)
            
        # Substitute environment variables in API keys
        config["ai"]["openai_api_key"] = os.getenv("OPENAI_API_KEY", "")
        config["ai"]["anthropic_api_key"] = os.getenv("ANTHROPIC_API_KEY", "")
        
        return config
    except Exception as e:
        raise Exception(f"Error loading config: {str(e)}")

def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """Set up logging with rotation."""
    logger = logging.getLogger("cursor_notes")
    logger.setLevel(config["logging"]["level"])

    # Create logs directory if it doesn't exist
    Path(config["logging"]["file"]).parent.mkdir(exist_ok=True)

    handler = RotatingFileHandler(
        config["logging"]["file"],
        maxBytes=config["logging"]["max_size"],
        backupCount=config["logging"]["backup_count"]
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def ensure_directory(path: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)
