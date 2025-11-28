from pathlib import Path

from aiogram import Bot, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from config import Config, get_config


config: Config = get_config()
BOT_TOKEN: str = config.tg_bot.token


TEMP_DIR = Path("temp_audio")
TEMP_DIR.mkdir(exist_ok=True)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class AudioProcessing(StatesGroup):
    waiting_for_audio = State()
    waiting_for_instruction = State()


@dp.message(CommandStart(), StateFilter(default_state))
async def process_start(message: Message, state: FSMContext):
    await state.set_state(AudioProcessing.waiting_for_audio)
    await message.answer(text="This bot is programmed for make change in any audio\n\n"
                              "Send a voice message or audio in mp3 or WAV"
                         )


@dp.message(
    StateFilter(AudioProcessing.waiting_for_audio),
    F.voice | F.audio | (F.document & F.document.mime_type.startswith("audio/"))
            )
async def process_audio(message: Message, state: FSMContext):
    if message.voice:
        file = await bot.get_file(message.voice.file_id)
    elif message.audio:
        file = await bot.get_file(message.audio.file_id)
    else:
        file = await bot.get_file(message.document.file_id)

    file_path = TEMP_DIR / f"{message.from_user.id}_input{Path(file.file_path).suffix}"
    await bot.download_file(file.file_path, destination=file_path)

    await state.update_data(audio_path=str(file_path))
    await state.set_state(AudioProcessing.waiting_for_instruction)
    await message.answer(text="Now describe what to do with the audio.")


@dp.message(Command(commands='cancel'))
async def process_cancel(message: Message, state: FSMContext):
    await message.answer(text="Cancelled")
    await state.clear()

