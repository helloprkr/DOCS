import schedule
import time
import logging
from typing import Dict, Any, Callable
from datetime import datetime
import pytz

class NoteScheduler:
    def __init__(self, config: Dict[str, Any], logger: logging.Logger, note_generator_callback: Callable):
        self.config = config
        self.logger = logger
        self.note_generator_callback = note_generator_callback
        self.timezone = pytz.timezone(config["automation"]["timezone"])
        
    def _generate_note(self) -> None:
        """Wrapper for note generation callback with error handling."""
        try:
            self.logger.info("Scheduled note generation started")
            self.note_generator_callback()
            self.logger.info("Scheduled note generation completed")
        except Exception as e:
            self.logger.error(f"Error in scheduled note generation: {str(e)}")
            
    def start(self) -> None:
        """Start the scheduler."""
        try:
            if not self.config["automation"]["enabled"]:
                self.logger.info("Automation is disabled in config")
                return
                
            schedule_time = self.config["automation"]["schedule_time"]
            
            # Schedule daily note generation
            schedule.every().day.at(schedule_time).do(self._generate_note)
            
            self.logger.info(f"Scheduler started, will run daily at {schedule_time} {self.config['automation']['timezone']}")
            
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except Exception as e:
            self.logger.error(f"Error starting scheduler: {str(e)}")
            raise
            
    def stop(self) -> None:
        """Stop the scheduler."""
        try:
            schedule.clear()
            self.logger.info("Scheduler stopped")
        except Exception as e:
            self.logger.error(f"Error stopping scheduler: {str(e)}")
            raise
            
    def get_next_run(self) -> datetime:
        """Get the next scheduled run time."""
        try:
            next_run = schedule.next_run()
            if next_run:
                return self.timezone.localize(next_run)
            return None
        except Exception as e:
            self.logger.error(f"Error getting next run time: {str(e)}")
            raise
            
    def run_now(self) -> None:
        """Trigger note generation immediately."""
        try:
            self.logger.info("Manual note generation triggered")
            self._generate_note()
        except Exception as e:
            self.logger.error(f"Error in manual note generation: {str(e)}")
            raise
