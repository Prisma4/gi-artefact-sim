import aiogram
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

ARTEFACTS = "артефакты"

LEGENDARY = "5"

ARTEFACT_LEVEL_UP = "уровень"
REROLL = "заново"
BACK = "назад"

async def main_keyboard():
    a = InlineKeyboardButton(text = "Артефакты", callback_data=ARTEFACTS)
    z = InlineKeyboardMarkup(inline_keyboard=[[a]])
    return z
async def rarity_keyboard():
    a = InlineKeyboardButton(text="Легендарная", callback_data=LEGENDARY)
    z = InlineKeyboardMarkup(inline_keyboard=[[a]])
    return z
async def artefact_level_up_keyboard(artefact_level):
    if artefact_level < 20:
        a = InlineKeyboardButton(text="Новый артефакт", callback_data=REROLL)
        b = InlineKeyboardButton(text="Повысить уровень", callback_data=ARTEFACT_LEVEL_UP)
        c = InlineKeyboardButton(text="Назад", callback_data=BACK)
        z = InlineKeyboardMarkup(inline_keyboard=[[b],[a,c]])
    elif artefact_level == 20:
        a = InlineKeyboardButton(text="Новый артефакт", callback_data=REROLL)
        c = InlineKeyboardButton(text="Назад", callback_data=BACK)
        z = InlineKeyboardMarkup(inline_keyboard=[[a,c]])
    return z