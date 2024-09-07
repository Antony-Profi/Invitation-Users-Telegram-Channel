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


def updateProgress(progress_file, current_index):
    with open(progress_file, "w") as f:
        f.write(str(current_index))
    print(f"Progress updated to index {current_index}.")


def logReport(report_file, start_time, invited_count, failed_count, total_users):
    end_time = datetime.now()
    duration = end_time - start_time

    with open(report_file, "w") as f:
        f.write("\n" + "="*50 + "\n")
        f.write(f"Report Date: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Start Time: {start_time}\n")
        f.write(f"End Time: {datetime.now()}\n")
        f.write(f"Duration: {duration}\n")
        f.write(f"Total Users: {total_users}\n")
        f.write(f"Successfully Invited: {invited_count}\n")
        f.write(f"Failed to Invite: {failed_count}\n")
        f.write(f"Progress: {invited_count + failed_count} / {total_users}\n")

    print(f"Report appended to {report_file}")


def displayReportStatistics(report_file):
    try:
        with open(report_file, "r") as file:
            content = file.read()

        reports = content.split("="*50)
        total_invited = 0
        total_failed = 0

        print("\nReport Statistics:")
        for report in reports:
            if report.strip():
                lines = report.strip().split("\n")
                date = next((line.split(': ')[1] for line in lines if line.startswith("Report Date")), "Unknown")
                invited = int(next((line.split(': ')[1] for line in lines if line.startswith("Successfully Invited")), 0))
                failed = int(next((line.split(': ')[1] for line in lines if line.startswith("Failed to Invite")), 0))

                total_invited += invited
                total_failed += failed
                print(f"Date: {date}, Invited: {invited}, Failed {failed}")

        print(f"\nTotal Invited: {total_invited}")
        print(f"Total Failed: {total_failed}")
        print(f"Overall Success Rate: {total_invited / (total_invited + total_failed) * 100:.2f}%")

    except FileNotFoundError:
        print(f"Report file {report_file} not found.")
    except Exception as e:
        print(f"Error reading report file: {str(e)}")
