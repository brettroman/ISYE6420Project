import logging
import os
import sys
from datetime import datetime
from project.config import behavior_config

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger()
            cls._instance._setup_verbosity()
        return cls._instance

    def _setup_logger(self):
        log_dir = behavior_config.get('log_path', 'logs')
        os.makedirs(log_dir, exist_ok=True)

        # Get current script name 
        script_name = os.path.basename(sys.argv[0])
        script_base = os.path.splitext(script_name)[0]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{timestamp}_{script_base}.log"
        log_path = os.path.join(log_dir, log_filename)

        log_level_str = behavior_config.get("log_level", "DEBUG").upper()
        log_level = getattr(logging, log_level_str, logging.DEBUG)

        logging.basicConfig(
            filename=log_path,
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        self.logger = logging.getLogger(script_base)
        self.logger.info(f"Logging started for execution of {script_name}")

    def _setup_verbosity(self):
        verbosity_level_str = behavior_config.get("verbosity", "INFO").upper()
        verbosity_level = getattr(logging, verbosity_level_str, logging.INFO)

        if self.logger is not None:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(verbosity_level)
            console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

# Create a global logger instance
logger = Logger().get_logger()