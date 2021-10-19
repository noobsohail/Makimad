# Copyright (C) 2018 - 2020 MrYacha. All rights reserved. Source code available under the AGPL.
# Copyright (C) 2021 TeamMakima
# Copyright (C) 2020 Inuka Asith


import random
from contextlib import suppress

from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

from Makima.decorator import register
from Makima.modules.utils.disable import disableable_dec

from . import MOD_HELP
from .language import select_lang_keyboard
from .utils.disable import disableable_dec
from .utils.language import get_strings_dec

helpmenu_cb = CallbackData("helpmenu", "mod")


def help_markup(modules):
    markup = InlineKeyboardMarkup()
    for module in modules:
        markup.insert(
            InlineKeyboardButton(module, callback_data=helpmenu_cb.new(mod=module))
        )
    return markup


STICKERS = (
    "CAACAgUAAxkBAAEDDX5hYuhMv9O8qu_KDHwxGjXKuhP_hgACggMAA1MZV6hb7s33v4FyIQQ",
    "CAACAgUAAxkBAAEDDX9hYuhMHCmZl_sHuZE5P-PUpr62bwACpAMAAmJlGFcHqjhtjG4NqSEE",
    "CAACAgUAAxkBAAEDDYBhYuhMCwpDX-vMTwABam8P_avfVDUAApkDAAK2oBlX0y6NdMMcGGIhBA",
    "CAACAgUAAxkBAAEDDYFhYuhM9ki2HjHjWtlMP20AAbQmr5oAAqYEAAKSARFX25e7d-5bsnAhBA",
    "CAACAgUAAxkBAAEDDYJhYuhMmiTFiHfIR-ElNUdIlF5TZwACCgUAAmr9GFe1J2Lx-DSOiyEE",
    "CAACAgUAAxkBAAEDDYNhYuhMO5WVOchFBc4aTx992L1mIgACfQQAAiUCGVfTJB5uxY-CrSEE",
    "CAACAgUAAxkBAAEDDYRhYuhMi-JQfs3YX-7BGwl93qqNLwACyAMAAlqQGFfueONShp2m9iEE",
    "CAACAgUAAxkBAAEDDYVhYuhM5fiWh7z8WlfMLy-MkQ6l6wACXwQAAmDgGVedwIJn_ss02iEE",
    "CAACAgUAAxkBAAEDDYZhYuhMxDs2hYlHpxUq-SCmkF5FkgACgwMAAkB9GVcX_qsEe76DeSEE",
    "CAACAgUAAxkBAAEDDYdhYuhM9Vr1n8wDghfx05vNf5WCuQACDQMAAqVPGVct4YiaqgvYhCEE",
    "CAACAgUAAxkBAAEDDX1hYuhMg_4C4OItq1yUwhjlHhw-GgACZQMAAqgdGFcfdbIEv_1PoCEE",
)


@register(cmds="start", no_args=True, only_groups=True)
@disableable_dec("start")
@get_strings_dec("pm_menu")
async def start_group_cmd(message, strings):
    await message.reply(strings["start_hi_group"])


@register(cmds="start", no_args=True, only_pm=True)
async def start_cmd(message):
    await message.reply_sticker(random.choice(STICKERS))
    await get_start_func(message)


@get_strings_dec("pm_menu")
async def get_start_func(message, strings, edit=False):
    msg = message.message if hasattr(message, "message") else message

    task = msg.edit_text if edit else msg.reply
    buttons = InlineKeyboardMarkup()
    buttons.add(InlineKeyboardButton(strings["btn_help"], callback_data="get_help"))
    buttons.add(
        InlineKeyboardButton(strings["btn_lang"], callback_data="lang_btn"),
        InlineKeyboardButton(
            strings["btn_source"], url="https://github.com/noobsohail/Makima"
        ),
    )
    buttons.add(
        InlineKeyboardButton(strings["btn_channel"], url="https://t.me/Makima_Devil_Updates"),
        InlineKeyboardButton(
            strings["btn_group"], url="https://t.me/Makima_Devil_Support"
        ),
    )
    buttons.add(
        InlineKeyboardButton(
            "👸🏼 Add Makima to your group",
            url=f"https://telegram.me/Makima_Devil_bot?startgroup=true",
        )
    )
    # Handle error when user click the button 2 or more times simultaneously
    with suppress(MessageNotModified):
        await task(strings["start_hi"], reply_markup=buttons)


@register(regexp="get_help", f="cb")
@get_strings_dec("pm_menu")
async def help_cb(event, strings):
    button = help_markup(MOD_HELP)
    button.add(InlineKeyboardButton(strings["back"], callback_data="go_to_start"))
    with suppress(MessageNotModified):
        await event.message.edit_text(strings["help_header"], reply_markup=button)


@register(regexp="lang_btn", f="cb")
async def set_lang_cb(event):
    await select_lang_keyboard(event.message, edit=True)


@register(regexp="go_to_start", f="cb")
async def back_btn(event):
    await get_start_func(event, edit=True)


@register(cmds="help", only_pm=True)
@disableable_dec("help")
@get_strings_dec("pm_menu")
async def help_cmd(message, strings):
    button = help_markup(MOD_HELP)
    button.add(InlineKeyboardButton(strings["back"], callback_data="go_to_start"))
    await message.reply(strings["help_header"], reply_markup=button)


@register(cmds="help", only_groups=True)
@disableable_dec("help")
@get_strings_dec("pm_menu")
async def help_cmd_g(message, strings):
    text = strings["btn_group_help"]
    button = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=text, url="https://t.me/Makima_devil_bot?start")
    )
    await message.reply(strings["help_header"], reply_markup=button)


@register(helpmenu_cb.filter(), f="cb", allow_kwargs=True)
async def helpmenu_callback(query, callback_data=None, **kwargs):
    mod = callback_data["mod"]
    if not mod in MOD_HELP:
        await query.answer()
        return
    msg = f"Help for <b>{mod}</b> module:\n"
    msg += f"{MOD_HELP[mod]}"
    button = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🏃‍♂️ Back", callback_data="get_help")
    )
    with suppress(MessageNotModified):
        await query.message.edit_text(
            msg, disable_web_page_preview=True, reply_markup=button
        )
        await query.answer("Help for " + mod)
