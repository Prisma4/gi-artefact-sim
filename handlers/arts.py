import aiogram, asyncio, random, PIL
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InputMediaPhoto, FSInputFile
from keyboards.kb import main_keyboard, type_keyboard, artifact_level_up_keyboard
from keyboards.kb import ARTIFACTS, FLOWER, BACK, REROLL, ARTIFACT_LEVEL_UP
from main import bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from defs.artifact import actual_substats, artifact_image, artifact_level_up_four

class main(StatesGroup):
    main_state = State()


router = Router()

@router.message(Command("start"))
async def main_menu(message: types.Message, state: FSMContext):
    await state.set_state(main.main_state)
    await message.answer_photo(photo = FSInputFile('artifactsim/pics/background.png'))
    await message.answer(text = "Выберите действие:", reply_markup = await main_keyboard())
    await state.update_data(message_id = message.message_id+2)

@router.callback_query(F.data.in_((ARTIFACTS, BACK)))
async def artifact_legendary(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        await bot.edit_message_text(message_id=data['message_id'], chat_id = call.message.chat.id, text="Выберите тип:", reply_markup=await type_keyboard())
        await bot.edit_message_media(message_id=data['message_id']-1,chat_id = call.message.chat.id, media = InputMediaPhoto(media=(FSInputFile('artifactsim/pics/background.png'))))
    except:
        pass
    await call.answer()

@router.callback_query(F.data.in_((FLOWER, REROLL)))
async def artifact_simulate(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    substat_list = await actual_substats()
    await state.update_data(substate_list = substat_list)
    await artifact_image(0, substat_list, call.from_user.id, 'flower')
    try:
        await bot.edit_message_media(message_id=data['message_id']-1,
        chat_id = call.message.chat.id,
        media = InputMediaPhoto(media=FSInputFile(f'artifactsim/pics/artifacts/{call.from_user.id}-artifact.png')))
        
        await state.update_data(artifact_level = 0)
        await state.update_data(current_substats = substat_list)
        await bot.edit_message_text(message_id=data['message_id'],
        chat_id = call.message.chat.id,
        text="Выберите действие:",
        reply_markup=await artifact_level_up_keyboard(0))
    except:
        pass
    await call.answer()

@router.callback_query(main.main_state, F.data == ARTIFACT_LEVEL_UP)
async def artifact_level_up(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_substats, artifact_level = await artifact_level_up_four(data['artifact_level'], data['current_substats'])
    await state.update_data(artifact_level = artifact_level)
    data = await state.get_data()
    await artifact_image(data['artifact_level'], current_substats, call.from_user.id, 'flower')
    await bot.edit_message_media(message_id=data['message_id']-1,
    chat_id = call.message.chat.id,
    media = InputMediaPhoto(media=FSInputFile(f'artifactsim/pics/artifacts/{call.from_user.id}-artifact.png')))
    if artifact_level == 20:
        await bot.edit_message_text(message_id=data['message_id'],
        chat_id = call.message.chat.id,
        text="Артефакт достиг максимального потенциала",
        reply_markup=await artifact_level_up_keyboard(20))
    await call.answer()