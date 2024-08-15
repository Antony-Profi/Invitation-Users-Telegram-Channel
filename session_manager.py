import os
import shutil


SESSION_FOLDER = "sessionData"


def ensureSessionFolder():
    if not os.path.exists(SESSION_FOLDER):
        os.makedirs(SESSION_FOLDER)


def moveSessionFiles():
    ensureSessionFolder()
    current_dir = os.getcwd()

    for file in os.listdir(current_dir):
        if file.endswith(".session"):
            src_file = os.path.join(current_dir, file)
            dst_path = os.path.join(current_dir, SESSION_FOLDER, file)
            shutil.move(src_file, dst_path)
            print(f"Moved {file} to {SESSION_FOLDER}/")


def getSessionPath(session_name):
    return os.path.join(SESSION_FOLDER, f"{session_name}.session")
