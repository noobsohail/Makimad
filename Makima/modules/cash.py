# Copyright (C) 2021 TeamMakima



import requests
from telethon import types
from telethon.tl import functions

from Makima.config import get_str_key
from Makima.services.events import register
from Makima.services.telethon import tbot

CASH_API_KEY = get_str_key("CASH_API_KEY", required=False)


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


@register(pattern="^/cash")
async def _(event):
    if event.fwd_from:
        return
    """this method of approve system is made by @AyushChatterjee, god will curse your family if you kang it motherfucker"""
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        else:
            return

    cmd = event.text

    args = cmd.split(" ")

    if len(args) == 4:
        try:
            orig_cur_amount = float(args[1])

        except ValueError:
            await event.reply("Invalid Amount Of Currency")
            return

        orig_cur = args[2].upper()

        new_cur = args[3].upper()

        request_url = (
            f"https://www.alphavantage.co/query"
            f"?function=CURRENCY_EXCHANGE_RATE"
            f"&from_currency={orig_cur}"
            f"&to_currency={new_cur}"
            f"&apikey={CASH_API_KEY}"
        )
        response = requests.get(request_url).json()
        try:
            current_rate = float(
                response["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
            )
        except KeyError:
            await event.reply("Currency Not Supported.")
            return
        new_cur_amount = round(orig_cur_amount * current_rate, 5)
        await event.reply(f"{orig_cur_amount} {orig_cur} = {new_cur_amount} {new_cur}")

    elif len(args) == 1:
        await event.reply(__help__)

    else:
        await event.reply(
            f"**Invalid Args!!:** Required 3 But Passed {len(args) -1}",
        )
