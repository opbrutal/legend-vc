# Credit DaisyXMusic, Changes By Blaze, Improve Code By Decode

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from helpers.decorators import authorized_users_only, errors
from callsmusic.callsmusic import client as USER
from config import SUDO_USERS


@Client.on_message(filters.command(["userbotjoin", "join"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>𝘼𝙙𝙙 𝙈𝙚 𝘼𝙨 𝘼𝙙𝙢𝙞𝙣 𝙁𝙞𝙧𝙨𝙩 𝙎𝙩𝙪𝙥𝙞𝙙.</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Alone_boy_xd_01"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>𝙃𝙚𝙮 𝙈𝙮 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙄𝙨 𝙅𝙤𝙞𝙣𝙚𝙙. 𝙃𝙪𝙧𝙧𝙧𝙚𝙮 🐬🤞</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 𝙁𝙡𝙤𝙤𝙙 𝙀𝙧𝙧𝙤𝙧 🛑</b> \n\𝙃𝙚𝙮 {user.first_name}, 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝘾𝙤𝙪𝙡𝙙𝙣'𝙩 𝙅𝙤𝙞𝙣 𝙔𝙤𝙪𝙧 𝙂𝙧𝙤𝙪𝙥. 𝙈𝙖𝙮 𝘽𝙚 𝙄𝙩𝙨 𝘽𝙖𝙣𝙣𝙚𝙙 𝙊𝙧 𝘼𝙣𝙮 𝙊𝙩𝙝𝙚𝙧 𝙄𝙨𝙨𝙪𝙚.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} 𝙅𝙤𝙞𝙣𝙚𝙙 𝙎𝙪𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>𝙐𝙨𝙚𝙧 𝘾𝙤𝙪𝙡𝙙𝙣'𝙩 𝙇𝙚𝙖𝙫𝙚 ..𝙏𝙧𝙮 𝘼𝙜𝙖𝙞𝙣 𝙇𝙖𝙩𝙚𝙧.</b>"
        )

        return


@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("**Asisten Meninggalkan semua obrolan**")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝘾𝙤𝙪𝙡𝙙𝙣'𝙩 𝙇𝙚𝙖𝙫𝙚🥺 𝙎𝙤𝙧𝙧𝙮..."
            )
        except:
            failed += 1
            await lol.edit(
                f"𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙇𝙚𝙖𝙫𝙞𝙣𝙜 𝘽𝙗𝙮𝙚.."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"Left {left} chats. Failed {failed} chats."
    )

