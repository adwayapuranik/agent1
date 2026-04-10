import os
from datetime import datetime


class Logger:
    def __init__(self, log_dir):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"run_{timestamp}.log")

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}"

        print(line)

        with open(self.log_file, "a") as f:
            f.write(line + "\n")