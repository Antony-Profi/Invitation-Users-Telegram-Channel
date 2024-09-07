import asyncio
import time

from config import loadConfig
from utils import readsUsers, getLeastProcessedIndex, updateProgress, logReport, displayReportStatistics
from telegram_channel import TelegramInviter
from session_manager import moveSessionFiles
from code_analyzer import CodeAnalyzer
from logger import logger


async def main():
    analyzer = CodeAnalyzer()
    logger.info("Starting the program")
    await asyncio.sleep(5)

    config = loadConfig()
    logger.info("Configuration loaded")
    await asyncio.sleep(5)

    users = readsUsers(config.USERS_FILE)
    logger.info(f"Loaded {len(users)} users from file {'InviteUsersTGChannel.txt'}")

    start_index = getLeastProcessedIndex(config.PROGRESS_FILE)
    logger.info(f"Starting from index {start_index}")

    inviter = TelegramInviter(config)
    await inviter.start()

    channel = await inviter.getChannel()
    logger.info(f"Connected to channel: {channel.title}")
    await asyncio.sleep(5)

    try:
        invited_count, failed_count = await inviter.invitesUsersToChannel(channel, users, start_index)
        logger.info(f"Invitation process completed. Invited: {invited_count}, Failed: {failed_count}")
    except Exception as err:
        logger.error(f"An error occurred during invitation process: {str(err)}")
        raise

    logReport(config.REPORT_FILE, inviter.start_time, invited_count, failed_count, len(users))
    displayReportStatistics(config.REPORT_FILE)

    moveSessionFiles()
    logger.info("Session files moved")

    analysis_result = analyzer.endAnalysis()
    logger.info("Program finished. Analysis completed.")
    logger.info(f"Duration: {analysis_result['duration']:.2f} seconds")
    logger.info(f"Memory used: {analysis_result['memory_used']:.2f} MB")


if __name__ == "__main__":
    config = loadConfig()
    try:
        asyncio.run(main())
    except Exception as error:
        logger.critical(f"Critical error occurred: {str(error)}")
    finally:
        logger.info("Program execution ended")
        displayReportStatistics(config.REPORT_FILE)
