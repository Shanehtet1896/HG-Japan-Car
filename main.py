import asyncio
import json
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
import aiosqlite

TOKEN = "8968101785:AAEb8N54m3g-u81mSl4ydIgl1p7y1tzKd"

router = Router()
DB_FILE = "cars.db"

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT,
                model TEXT,
                price TEXT
            )
        """)
        await db.commit()

@router.message(F.web_app_data)
async def process_web_app_data(message: Message):
    try:
        data_json = message.web_app_data.data
        car_data = json.loads(data_json)

        brand = car_data.get('brand')
        model = car_data.get('model')
        price = car_data.get('price')

        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute(
                "INSERT INTO cars (brand, model, price) VALUES (?, ?, ?)",
                (brand, model, price)
            )
            await db.commit()

        await message.answer(
            f"Success! Data saved.\n\n"
            f"Brand: {brand}\n"
            f"Model: {model}\n"
            f"Price: {price}"
        )
    except Exception as e:
        await message.answer(f"Error: {str(e)}")

async def main():
    await init_db()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
