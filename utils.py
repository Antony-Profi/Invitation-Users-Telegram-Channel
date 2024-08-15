import os
from datetime import datetime


def readsUsers(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def getLeastProcessedIndex(progress_file):
    if not os.path.exists(progress_file):
        with open(progress_file, "w") as f:
            f.write("0")
        print(f"Progress file created. Starting from index 0.")
        return 0
    with open(progress_file, "r") as f:
        content = f.read().strip()
        return int(content) if content.isdigit() else 0


def updateProgress(progress_file, index):
    with open(progress_file, "w") as f:
        f.write(str(index()))
    print(f"Progress updated to index {index}.")


def logReport(report_file, start_time, invited_count, failed_count, total_users):
    with open(report_file, "w") as f:
        f.write(f"Start Time: {start_time}\n")
        f.write(f"End Time: {datetime.now()}\n")
        f.write(f"Total Users: {total_users}\n")
        f.write(f"Successfully Invited: {invited_count}\n")
        f.write(f"Failed to Invite: {failed_count}\n")
