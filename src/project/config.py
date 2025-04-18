import json
import os
import numpy as np

class Config:
    def __init__(self, config_choice="datasets", config_obj=None):

        if config_obj is not None:
            self.config = config_obj
        else:
            filepath = f"config/{config_choice}.json"

            if not os.path.exists(filepath):
                raise FileNotFoundError(f"JSON file not found: {filepath}")
        
            with open(f"config/{config_choice}.json") as f:
                self.config = json.load(f)

    def get(self, key=None, fallback=None):
        if key is None and fallback is None:
            return self.config
        
        return self.config.get(key, fallback)

behavior_config = Config("behavior")
experiments_config = Config("experiments")
auth_config = Config("auth")