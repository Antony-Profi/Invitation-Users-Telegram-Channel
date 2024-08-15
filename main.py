import asyncio
import time

from config import loadConfig
from utils import readsUsers, getLeastProcessedIndex, updateProgress, logReport
from telegram_channel import TelegramInviter
from session_manager import moveSessionFiles
from code_analyzer import CodeAnalyzer
from logger import logger


async def main():
    analyzer = CodeAnalyzer()
    logger.info("Starting the program")
    time.sleep(5)

    config = loadConfig()
    logger.info("Configuration loaded")
    time.sleep(5)

    users = readsUsers(config.USERS_FILE)
    logger.info(f"Loaded {len(users)} users from file")

    start_index = getLeastProcessedIndex(config.PROGRESS_FILE)
    logger.info(f"Starting from index {start_index}")

    inviter = TelegramInviter(config)
    await inviter.start()
    logger.info("Telegram client started")
    time.sleep(5)

    channel = await inviter.getChannel()
    logger.info(f"Connected to channel: {channel.title}")
    time.sleep(5)

    try:
        invited_count, failed_count = await inviter.invitesUsersToChannel(channel, users, start_index)
        logger.info(f"Invitation process completed. Invited: {invited_count}, Failed: {failed_count}")
    except Exception as e:
        logger.info(f"An error occurred during invitation process: {str(e)}")
        raise

    updateProgress(config.PROGRESS_FILE, len(users))
    logReport(config.REPORT_FILE, inviter.start_time, invited_count, failed_count, len(users))
    logger.info("Session files moved")

    moveSessionFiles()
    logger.info("Session files moved")

    analysis_result = analyzer.endAnalysis()
    logger.info("Program finished. Analysis completed.")
    logger.info(f"Duration: {analysis_result['duration']:.2f} seconds")
    logger.info(f"Memory used: {analysis_result['memory_used']:.2f} MB")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Critical error occurred: {str(e)}")
    finally:
        logger.info("Program execution ended")
