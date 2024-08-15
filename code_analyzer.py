import os
import psutil
import time

from datetime import datetime


class CodeAnalyzer:
    def __init__(self):
        self.start_time = time.time()
        self.start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        self.analysis_folder = "codeAnalysis"
        if not os.path.exists(self.analysis_folder):
            os.makedirs(self.analysis_folder)

    def endAnalysis(self):
        end_time = time.time()
        end_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

        duration = end_time - self.start_time
        memory_used = end_memory - self.start_memory

        analysis_file = os.path.join(self.analysis_folder, f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

        with open(analysis_file, "w") as f:
            f.write(f"Start time: {datetime.fromtimestamp(self.start_time)}\n")
            f.write(f"End time: {datetime.fromtimestamp(end_time)}\n")
            f.write(f"Duration: {duration:.2f} seconds\n")
            f.write(f"Memory usage: {memory_used:.2f} MB\n")

        return {
            "start_time": datetime.fromtimestamp(self.start_time),
            "end_time": datetime.fromtimestamp(end_time),
            "duration": duration,
            "memory_used": memory_used
        }
