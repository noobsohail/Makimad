# Copyright (C) 2021 TeamMakima



from pyrogram import filters

from Makima.function.pluginhelpers import admins_only, get_text
from Makima.services.pyrogram import pbot


@pbot.on_message(
    filters.command("send") & ~filters.edited & ~filters.bot & ~filters.private
)
@admins_only
async def send(client, message):
    args = get_text(message)
    await client.send_message(message.chat.id, text=args)
