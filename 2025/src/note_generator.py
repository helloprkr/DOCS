from typing import Dict, Any, List
import openai
import anthropic
from datetime import datetime
import logging
from pathlib import Path
import json

class NoteGenerator:
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self._setup_ai_client()
        
    def _setup_ai_client(self):
        """Set up the AI client based on configuration."""
        if self.config["ai"]["provider"] == "openai":
            openai.api_key = self.config["ai"]["openai_api_key"]
            self.client = openai.Client()
        else:
            self.client = anthropic.Client(api_key=self.config["ai"]["anthropic_api_key"])
    
    def _batch_process_tasks(self, tasks: List[Dict[str, Any]], max_batch_size: int = 5) -> List[str]:
        """Process tasks in batches to optimize API calls."""
        processed_tasks = []
        for i in range(0, len(tasks), max_batch_size):
            batch = tasks[i:i + max_batch_size]
            batch_descriptions = [task["description"] for task in batch]
            
            # Create a concise prompt for the batch
            prompt = (
                "For each task, provide a very brief (10-15 words) analysis. Tasks:\n" +
                "\n".join(f"- {desc}" for desc in batch_descriptions)
            )
            
            try:
                if self.config["ai"]["provider"] == "openai":
                    response = self.client.chat.completions.create(
                        model="gpt-3.5-turbo",  # Using cheaper model for tasks
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=100 * len(batch),  # Limit tokens per task
                        temperature=0.7
                    )
                    analyses = response.choices[0].message.content.split("\n")
                else:
                    response = self.client.messages.create(
                        model="claude-instant-1.2",  # Using cheaper model for tasks
                        max_tokens=100 * len(batch),
                        messages=[{"role": "user", "content": prompt}]
                    )
                    analyses = response.content.split("\n")
                
                # Clean up and validate analyses
                cleaned_analyses = []
                for analysis in analyses:
                    analysis = analysis.strip()
                    if analysis and not analysis.startswith("-"):
                        cleaned_analyses.append(analysis)
                    elif analysis.startswith("- "):
                        cleaned_analyses.append(analysis[2:])
                
                processed_tasks.extend(cleaned_analyses[:len(batch)])
                
                # If we don't have enough analyses, pad with defaults
                if len(cleaned_analyses) < len(batch):
                    processed_tasks.extend(["Task recorded"] * (len(batch) - len(cleaned_analyses)))
                
            except Exception as e:
                self.logger.error(f"Error processing task batch: {str(e)}")
                processed_tasks.extend(["Task recorded"] * len(batch))
        
        return processed_tasks
    
    def generate_section_content(self, section: str, context: Dict[str, Any]) -> str:
        """Generate content for a specific section using AI."""
        try:
            # Convert section name to match variable names
            section_key = section.lower().replace(" ", "_").replace("-", "_")
            
            # Get content from context if available
            if section_key in context.get("variables", {}):
                return context["variables"][section_key]
            
            # Try alternate key formats
            alt_key = section_key.replace("_", "-")
            if alt_key in context.get("variables", {}):
                return context["variables"][alt_key]
                
            # Try the exact section name as a key
            if section.lower() in context.get("variables", {}):
                return context["variables"][section.lower()]
            
            self.logger.debug(f"No content found for section {section} (tried keys: {section_key}, {alt_key}, {section.lower()})")
            return f"No content provided for {section}"
                
        except Exception as e:
            self.logger.error(f"Error generating content for {section}: {str(e)}")
            return f"No content provided for {section}"
    
    def format_tasks(self, tasks: List[Dict[str, Any]]) -> str:
        """Format tasks with appropriate prefixes and AI-generated insights."""
        if not tasks:
            return "No tasks recorded"
            
        # Get AI analysis for tasks
        task_analyses = self._batch_process_tasks(tasks)
        
        formatted_tasks = []
        prefixes = self.config["notes"]["prefix_symbols"]
        
        for task, analysis in zip(tasks, task_analyses):
            prefix = prefixes["pending"]
            if task.get("completed_today"):
                prefix = prefixes["completed_today"]
            elif task.get("completed_later"):
                prefix = prefixes["completed_later"]
            elif task.get("decided_against"):
                prefix = prefixes["decided_against"]
                
            # Format task with analysis
            formatted_tasks.append(f"{prefix} {task['description']}\n   → {analysis.strip()}")
            
        return "\n\n".join(formatted_tasks)
    
    def generate_daily_note(self, context: Dict[str, Any], tasks: List[Dict[str, Any]]) -> str:
        """Generate a complete daily note."""
        try:
            with open(self.config["notes"]["template_path"], 'r') as f:
                template = f.read()
            
            # Generate content for each section
            sections = {
                "analyze": self.generate_section_content("Analysis", context),
                "strategize": self.generate_section_content("Strategy", context),
                "pre_problem_solve": self.generate_section_content("Pre-Problem Solving", context),
                "outlining": self.generate_section_content("Outline", context),
                "outcome": self.generate_section_content("Outcomes", context),
                "end_state": self.generate_section_content("End State", context),
                "tasks": self.format_tasks(tasks)
            }
            
            # Add date
            date = datetime.now().strftime(self.config["notes"]["date_format"])
            sections["date"] = date
            
            # Fill template
            note_content = template.format(**sections)
            
            # Save note
            output_dir = Path(self.config["notes"]["output_directory"])
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_file = output_dir / f"note_{date}.md"
            with open(output_file, 'w') as f:
                f.write(note_content)
                
            self.logger.info(f"Generated note for {date}")
            return note_content
            
        except Exception as e:
            self.logger.error(f"Error generating daily note: {str(e)}")
            raise
