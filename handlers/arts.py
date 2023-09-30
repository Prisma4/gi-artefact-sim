import aiogram, asyncio, random, PIL
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InputMediaPhoto, FSInputFile
from keyboards.kb import main_keyboard, rarity_keyboard, artefact_level_up_keyboard
from keyboards.kb import ARTEFACTS, LEGENDARY, ARTEFACT_LEVEL_UP, BACK, REROLL
from main import bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from defs.aftefact import actual_substats, artefact_image, artefact_level_up_four

class main(StatesGroup):
    main_state = State()


router = Router()

@router.message(Command("start"))
async def main_menu(message: types.Message, state: FSMContext):
    await state.set_state(main.main_state)
    await message.answer_photo(photo = FSInputFile('artefactsim/pics/background.png'))
    await message.answer(text = "Выберите действие:", reply_markup = await main_keyboard())
    await state.update_data(message_id = message.message_id+2)

@router.callback_query(F.data == ARTEFACTS)
async def artefact_legendary(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_text(message_id=data['message_id'], chat_id = call.message.chat.id, text="Выберите редкость:", reply_markup=await rarity_keyboard())

@router.callback_query(F.data == LEGENDARY)
async def artefact_legendary_simulate(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    substat_list = await actual_substats(5)
    await state.update_data(substate_list = substat_list)
    await artefact_image(0, substat_list, call.from_user.id, 'flower')
    await bot.edit_message_media(message_id=data['message_id']-1,
    chat_id = call.message.chat.id,
    media = InputMediaPhoto(media=FSInputFile(f'artefactsim/pics/artefacts/{call.from_user.id}-artefact.png')))
    await state.update_data(artefact_level = 0)
    await state.update_data(current_substats = substat_list)
    await bot.edit_message_text(message_id=data['message_id'],
    chat_id = call.message.chat.id,
    text="Выберите действие:",
    reply_markup=await artefact_level_up_keyboard(0))
    await call.answer()

@router.callback_query(main.main_state, F.data == ARTEFACT_LEVEL_UP)
async def artefact_level_up(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_substats, artefact_level = await artefact_level_up_four(data['artefact_level'], data['current_substats'])
    await state.update_data(artefact_level = artefact_level)
    data = await state.get_data()
    await artefact_image(data['artefact_level'], current_substats, call.from_user.id, 'flower')
    await bot.edit_message_media(message_id=data['message_id']-1,
    chat_id = call.message.chat.id,
    media = InputMediaPhoto(media=FSInputFile(f'artefactsim/pics/artefacts/{call.from_user.id}-artefact.png')))
    if artefact_level == 20:
        await bot.edit_message_text(message_id=data['message_id'],
        chat_id = call.message.chat.id,
        text="Артефакт достиг максимального потенциала",
        reply_markup=await artefact_level_up_keyboard(20))
    await call.answer()

@router.callback_query(F.data == REROLL)
async def artefact_legendary_simulate(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    substat_list = await actual_substats(5)
    await state.update_data(substate_list = substat_list)
    await artefact_image(0, substat_list, call.from_user.id, 'flower')
    await bot.edit_message_media(message_id=data['message_id']-1,
    chat_id = call.message.chat.id,
    media = InputMediaPhoto(media=FSInputFile(f'artefactsim/pics/artefacts/{call.from_user.id}-artefact.png')))
    await state.update_data(artefact_level = 0)
    await state.update_data(current_substats = substat_list)
    try:
        await bot.edit_message_text(message_id=data['message_id'],
        chat_id = call.message.chat.id,
        text="Выберите действие:",
        reply_markup=await artefact_level_up_keyboard(0))
    except:
        pass
    await call.answer()


@router.callback_query(F.data == BACK)
async def back(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        await bot.edit_message_text(message_id=data['message_id'], chat_id = call.message.chat.id, text="Выберите редкость:", reply_markup=await rarity_keyboard())
    except:
        pass
    await call.answer()