import asyncio
import os

from datetime import datetime

from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, UserNotMutualContactError
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantRequest
from telethon.tl.types import ChannelParticipantsAdmins
from utils import updateProgress
from session_manager import getSessionPath, moveSessionFiles
from logger import logger


class TelegramInviter:
    def __init__(self, config):
        self.config = config
        session_folder = os.path.abspath('sessionData')
        if not os.path.exists(session_folder):
            os.makedirs(session_folder)

        session_file = os.path.join(session_folder, 'session_name.session')
        logger.info(f"Using session file: {session_file}")

        try:
            self.client = TelegramClient(session_file, config.API_ID, config.API_HASH)
            self.start_time = None
            logger.info("TelegramClient instance created successfully")
        except Exception as e:
            logger.error(f"Error creating TelegramClient: {str(e)}")
            raise

    async def start(self):
        self.start_time = datetime.now()
        try:
            await self.client.start(self.config.PHONE_NUMBER)
            logger.info("Client started successfully")
        except Exception as e:
            logger.error(f"Error starting client: {str(e)}")
            raise
        moveSessionFiles()

    async def getChannel(self):
        return await self.client.get_entity(self.config.CHANNEL_USERNAME)

    async def checkAdminRights(self, channel):
        admins = await self.client.get_participants(channel, filter=ChannelParticipantsAdmins)
        me = await self.client.get_me()
        return any(admin.id == me.id for admin in admins)

    async def invitesUsersToChannel(self, channel, users, start_index, batch_size=100):
        if not await self.checkAdminRights(channel):
            logger.warning("У вас нет прав администратора для добавления пользователей в этот канал.")
            return 0, 0

        end_index = min(start_index + batch_size, len(users))
        invited_count = 0
        failed_count = 0

        for i in range(start_index, end_index):
            user = users[i]
            try:
                logger.info(f"Inviting {user} to {channel.username} (User {i + 1}/{len(users)})")
                await self.client(InviteToChannelRequest(channel, [user]))
                invited_count += 1
                # updateProgress(self.config.PROGRESS_FILE, i + 1)
                # logger.info(f"Successfully invited {user}")
                await asyncio.sleep(40)

            except Exception as e:
                logger.error(f"Error inviting {user}: {e}")
                failed_count += 1
                await asyncio.sleep(15)

        logger.info(f"Batch completed. Invited: {invited_count}, Failed: {failed_count}")
        return invited_count, failed_count
