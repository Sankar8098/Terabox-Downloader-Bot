import asyncio
import os
import time
from uuid import uuid4
import json
import redis
import telethon
import telethon.tl.types
from telethon import TelegramClient, events
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.types import Message, UpdateNewMessage

from cansend import CanSend
from config import *
from terabox import get_data
from tools import (
    convert_seconds,
    download_file,
    download_image_to_bytesio,
    extract_code_from_url,
    get_formatted_size,
    get_urls_from_string,
    is_user_on_chat,
)

import logging
import sys

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('bot.log')

# Set the logging level
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add them to the handlers
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

bot = TelegramClient("tele", API_ID, API_HASH)

db = redis.Redis(
    host=HOST,
    port=PORT,
    password=PASSWORD,
    decode_responses=True,
)

@bot.on(events.NewMessage(pattern="/start$", incoming=True, outgoing=False, func=lambda x: x.is_private))
async def start(event: UpdateNewMessage):
    user_id = event.sender_id
    logger.info(f"Received /start command from user {user_id}")
    try:
        # Check if the user is already in the database
        if not db.exists(f"user:{user_id}"):
            # Serialize user details into a JSON string
            user_details = json.dumps({"username": event.sender.username, "first_name": event.sender.first_name, "last_name": event.sender.last_name})
            # Add user details to the database
            db.set(f"user:{user_id}", user_details)

        reply_text = f"""
        🤖 **Hello! I am your Terabox Downloader Bot** 🤖

        📥 **Send me the Terabox link and I will start downloading it for you.** 📥

        🔗 **Join [Official Channel](https://t.me/VijayTv_SerialVideos) for Updates** 🔗

        🤖 **Make Your Own Private Terabox Bot at [UltroidxTeam](https://t.me/VijayTv_SerialVideos)** 🤖
        """
        check_if_ultroid_official = await is_user_on_chat(bot, "@VijayTv_SerialVideos", event.peer_id)
        if not check_if_ultroid_official:
            await event.reply("Please join @VijayTv_SerialVideos then send me the link again.")
            return

        check_if_ultroid_official_chat = await is_user_on_chat(bot, "@VijayTv_SerialVideos", event.peer_id)
        if not check_if_ultroid_official_chat:
            await event.reply("Please join @VijayTv_SerialVideos then send me the link again.")
            return

        await event.reply(reply_text, link_preview=False, parse_mode="markdown")
    except Exception as e:
        logger.error(f"Error in /start command: {str(e)}")
        await event.reply("An error occurred. Please try again later.")

@bot.on(events.NewMessage(pattern="/start (.*)", incoming=True, outgoing=False, func=lambda x: x.is_private))
async def start(event: UpdateNewMessage):
    text = event.pattern_match.group(1)
    fileid = db.get(str(text))
    logger.info(f"Received /start {text} command from user {event.sender_id}")
    try:
        check_if = await is_user_on_chat(bot, "@VijayTv_SerialVideos", event.peer_id)
        if not check_if:
            return await event.reply("Please join @VijayTv_SerialVideos then send me the link again.")
        check_if = await is_user_on_chat(bot, "@VijayTv_SerialVideos", event.peer_id)
        if not check_if:
            return await event.reply(
                "Please join @VijayTv_SerialVideos then send me the link again."
            )
        await bot(
            ForwardMessagesRequest(
                from_peer=PRIVATE_CHAT_ID,
                id=[int(fileid)],
                to_peer=event.chat.id,
                drop_author=True,
                # noforwards=True,  # Uncomment it if you dont want to forward the media. or do urdo
                background=True,
                drop_media_captions=False,
                with_my_score=True,
            )
        )
    except Exception as e:
        logger.error(f"Error in forwarding message: {str(e)}")
        await event.reply("An error occurred. Please try again later.")

@bot.on(events.NewMessage(pattern="/remove (.*)", incoming=True, outgoing=False, from_users=ADMINS))
async def remove(event: UpdateNewMessage):
    user_id = event.pattern_match.group(1)
    logger.info(f"Received /remove {user_id} command from admin {event.sender_id}")
    try:
        if db.get(f"check_{user_id}"):
            db.delete(f"check_{user_id}")
            await event.reply(f"Removed {user_id} from the list.")
        else:
            await event.reply(f"{user_id} is not in the list.")
    except Exception as e:
        logger.error(f"Error in /remove command: {str(e)}")
        await event.reply("An error occurred. Please try again later.")

@bot.on(events.NewMessage(incoming=True, outgoing=False, func=lambda message: message.text and get_urls_from_string(message.text) and message.is_private))
async def get_message(event: Message):
    logger.info(f"Received message with URL from user {event.sender_id}")
    asyncio.create_task(handle_message(event))

async def handle_message(event: Message):
    try:
        url = get_urls_from_string(event.text)
        if not url:
            return await event.reply("Please enter a valid url.")
        check_if = await is_user_on_chat(bot, "@VijayTv_SerialVideos", event.peer_id)
        if not check_if:
            return await event.reply("Please join @VijayTv_SerialVideos then send me the link again.")
        check_if = await is_user_on_chat(bot, "@VijayTv_SerialVideos", event.peer_id)
        if not check_if:
            return await event.reply(
                "Please join @VijayTv_SerialVideos then send me the link again."
            )
        is_spam = db.get(event.sender_id)
        if is_spam and event.sender_id not in [6695586027]:
            return await event.reply("You are spamming. Please wait a 1 minute and try again.")
        hm = await event.reply("Sending you the media wait...")
        count = db.get(f"check_{event.sender_id}")
        if count and int(count) > 5:
            return await hm.edit(
                "You are limited now. Please come back after 2 hours or use another account."
            )
        shorturl = extract_code_from_url(url)
        if not shorturl:
            return await hm.edit("Seems like your link is invalid.")
        fileid = db.get(shorturl)
        if fileid:
            try:
                await hm.delete()
            except:
                pass

            await bot(
                ForwardMessagesRequest(
                    from_peer=PRIVATE_CHAT_ID,
                    id=[int(fileid)],
                    to_peer=event.chat.id,
                    drop_author=True,
                    # noforwards=True, #Uncomment it if you dont want to forward the media.
                    background=True,
                    drop_media_captions=False,
                    with_my_score=True,
                )
            )
            db.set(event.sender_id, time.monotonic(), ex=60)
            db.set(
                f"check_{event.sender_id}",
                int(count) + 1 if count else 1,
                ex=7200,
            )

            return

        data = get_data(url)
        if not data:
            return await hm.edit("Sorry! API is dead or maybe your link is broken.")
        db.set(event.sender_id, time.monotonic(), ex=60)
        if (
            not data["file_name"].endswith(".mp4")
            and not data["file_name"].endswith(".mkv")
            and not data["file_name"].endswith(".Mkv")
            and not data["file_name"].endswith(".webm")
        ):
            return await hm.edit(
                f"Sorry! File is not supported for now. I can download only .mp4, .mkv and .webm files."
            )
        if int(data["sizebytes"]) > 524288000 and event.sender_id not in [6695586027]:
            return await hm.edit(
                f"Sorry! File is too big. I can download only 500MB and this file is of {data['size']} ."
            )

        start_time = time.time()
        cansend = CanSend()

        async def progress_bar(current_downloaded, total_downloaded, state="Sending"):

            if not cansend.can_send():
                return
            bar_length = 20
            percent = current_downloaded / total_downloaded
            arrow = "█" * int(percent * bar_length)
            spaces = "░" * (bar_length - len(arrow))

            elapsed_time = time.time() - start_time

            head_text = f"{state} `{data['file_name']}`"
            progress_bar = f"[{arrow + spaces}] {percent:.2%}"
            upload_speed = current_downloaded / elapsed_time if elapsed_time > 0 else 0
            speed_line = f"Speed: **{get_formatted_size(upload_speed)}/s**"

            time_remaining = (
                (total_downloaded - current_downloaded) / upload_speed
                if upload_speed > 0
                else 0
            )
            time_line = f"Time Remaining: `{convert_seconds(time_remaining)}`"

            size_line = f"Size: **{get_formatted_size(current_downloaded)}** / **{get_formatted_size(total_downloaded)}**"

            await hm.edit(
                f"{head_text}\n{progress_bar}\n{speed_line}\n{time_line}\n{size_line}",
                parse_mode="markdown",
            )

        uuid = str(uuid4())
        thumbnail = download_image_to_bytesio(data["thumb"], "thumbnail.png")

        try:
            file = await bot.send_file(
                PRIVATE_CHAT_ID,
                file=data["direct_link"],
                thumb=thumbnail if thumbnail else None,
                progress_callback=progress_bar,
                caption=f"""
        File Name: `{data['file_name']}`
        Size: **{data["size"]}** 
        Direct Link: [Click Here](https://t.me/Terabox_download_SK_Bot?start={uuid})

        @VijayTv_SerialVideos
        """,
                supports_streaming=True,
                spoiler=True,
            )

            # pm2 start python3 --name "terabox" -- main.py
        except telethon.errors.rpcerrorlist.WebpageCurlFailedError:
            download = await download_file(
                data["direct_link"], data["file_name"], progress_bar
            )
            if not download:
                return await hm.edit(
                    f"Sorry! Download Failed but you can download it from [here]({data['direct_link']}).",
                    parse_mode="markdown",
                )
            file = await bot.send_file(
                PRIVATE_CHAT_ID,
                download,
                caption=f"""
        File Name: `{data['file_name']}`
        Size: **{data["size"]}** 
        Direct Link: [Click Here](https://t.me/Terabox_download_SK_Bot?start={uuid})

        Share : @VijayTv_SerialVideos
        """,
                progress_callback=progress_bar,
                thumb=thumbnail if thumbnail else None,
                supports_streaming=True,
                spoiler=True,
            )
            try:
                os.unlink(download)
            except Exception as e:
                print(e)
        except Exception as e:
            logger.error(f"Error in downloading file: {str(e)}")
            return await hm.edit(
                f"Sorry! Download Failed but you can download it from [here]({data['direct_link']}).",
                parse_mode="markdown",
            )
        try:
            os.unlink(download)
        except Exception as e:
            pass
        try:
            await hm.delete()
        except Exception as e:
            logger.error(f"Error in deleting message: {str(e)}")

        if shorturl:
            db.set(shorturl, file.id)
        if file:
            db.set(uuid, file.id)

            await bot(
                ForwardMessagesRequest(
                    from_peer=PRIVATE_CHAT_ID,
                    id=[file.id],
                    to_peer=event.chat.id,
                    top_msg_id=event.id,
                    drop_author=True,
                    # noforwards=True,  #Uncomment it if you dont want to forward the media.
                    background=True,
                    drop_media_captions=False,
                    with_my_score=True,
                )
            )
            db.set(event.sender_id, time.monotonic(), ex=60)
            db.set(
                f"check_{event.sender_id}",
                int(count) + 1 if count else 1,
                ex=7200,
            )
    except Exception as e:
        logger.error(f"Error in handling message: {str(e)}")
        await event.reply("An error occurred. Please try again later.")

@bot.on(events.NewMessage(pattern="/broadcast (.+)", incoming=True, outgoing=False, from_users=ADMINS))
async def broadcast_message(event: UpdateNewMessage):
    message = event.pattern_match.group(1)
    logger.info(f"Received /broadcast command from admin {event.sender_id}")
    try:
        # Retrieve all users from the database
        all_users = db.keys("user:*")
        for user_key in all_users:
            user_id = user_key.split(":")[-1]
            try:
                # Send the broadcast message to each user
                await bot.send_message(int(user_id), message)
            except Exception as e:
                logger.error(f"Failed to send message to user {user_id}: {str(e)}")
        await event.reply("Broadcast sent successfully!")
    except Exception as e:
        logger.error(f"Error in /broadcast command: {str(e)}")
        await event.reply("An error occurred. Please try again later.")

@bot.on(events.NewMessage(pattern="/total_users", incoming=True, outgoing=False, from_users=ADMINS))
async def total_users(event: UpdateNewMessage):
    logger.info(f"Received /total_users command from admin {event.sender_id}")
    try:
        # Retrieve all users from the database
        all_users = db.keys("user:*")
        total_users_count = len(all_users)
        await event.reply(f"Total number of users: {total_users_count}")
    except Exception as e:
        logger.error(f"Error in /total_users command: {str(e)}")
        await event.reply("An error occurred. Please try again later.")

bot.start(bot_token=BOT_TOKEN)
bot.run_until_disconnected()
                          
