import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import CommandStart

TOKEN = "9143517055:AAFrHORwH0aBXv9G1WIjg6i-huXXXO1y27Q"
CHANNEL = "@relationshipcode_psy"          # или числовой ID, например -1001234567890
GUIDE_FILE = "guide.pdf"         # имя файла гайда в папке со скриптом

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False


def sub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться", url=f"https://t.me/{CHANNEL.lstrip('@')}")],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="check")]
    ])


async def send_guide(message: Message):
    await message.answer_document(FSInputFile(GUIDE_FILE), caption="Спасибо за подписку! Вот твой гайд 🎁")


@dp.message(CommandStart())
async def start(message: Message):
    if await is_subscribed(message.from_user.id):
        await send_guide(message)
    else:
        await message.answer("Чтобы получить гайд, подпишись на канал 👇", reply_markup=sub_keyboard())


@dp.callback_query(F.data == "check")
async def check_sub(call: CallbackQuery):
    if await is_subscribed(call.from_user.id):
        await call.message.delete()
        await send_guide(call.message)
        await call.answer()
    else:
        await call.answer("Ты ещё не подписался 😉", show_alert=True)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())