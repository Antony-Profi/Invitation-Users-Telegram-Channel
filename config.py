import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

        self.API_ID = int(os.environ.get("API_ID"))
        self.API_HASH = os.environ.get("API_HASH")
        self.PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
        self.CHANNEL_USERNAME = "anycars_ukraine"
        self.USERS_FILE = "User_base/InviteUsersTGChannel.txt"
        self.PROGRESS_FILE = "progress.txt"
        self.REPORT_FILE = "report.txt"


def loadConfig():
    return Config()
