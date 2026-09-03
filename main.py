import asyncio
import json
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
import aiosqlite

# ကိုယ့်ရဲ့ BotFather က ပေးထားတဲ့ Token ကို ထည့်ပါ
TOKEN = 8968101786:AAE8DB54no3g_w20rHApKbjzBjMsg1yfzd8

router = Router()
DB_FILE = "cars.db"

# ၁။ Database တည်ဆောက်ခြင်း (စတင်အလုပ်လုပ်ချိန်)
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

# ၂။ Mini App ကနေ Data ပို့လိုက်တာကို လက်ခံဖမ်းယူခြင်း
@router.message(F.web_app_data)
async def process_web_app_data(message: Message):
    try:
        # Mini App က ပို့လိုက်တဲ့ JSON data ကို ဖမ်းယူခြင်း
        data_json = message.web_app_data.data
        car_data = json.loads(data_json)
        
        brand = car_data.get('brand')
        model = car_data.get('model')
        price = car_data.get('price')
        
        # Database ထဲသို့ ထည့်သွင်းခြင်း
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute(
                "INSERT INTO cars (brand, model, price) VALUES (?, ?, ?)",
                (brand, model, price)
            )
            await db.commit()
            
        await message.answer(
            f"✅ ကားအချက်အလက်များကို အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ!\n\n"
            f"🚗 Brand: {brand}\n"
            f"📌 Model: {model}\n"
            f"💰 Price: {price}"
        )
    except Exception as e:
        await message.answer(f"❌ Error ဖြစ်သွားပါသည်: {str(e)}")

# ၃။ Bot စတင် Run မည့် Main Function
async def main():
    await init_db()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
