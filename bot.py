import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
import asyncio
import requests
from datetime import datetime

API_TOKEN = "7989080143:AAExHZjW36Oh603PL1RbNBA9ZnAay-I2OM0"  # ← ضع توكن البوت هنا

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def format_time(unix_time):
    try:
        dt = datetime.fromtimestamp(int(unix_time))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "غير معروف"

def format_player_info(data):
    b = data.get("basicInfo", {})
    s = data.get("socialInfo", {})
    p = data.get("petInfo", {})
    c = data.get("clanBasicInfo", {})
    profile = data.get("profileInfo", {})
    credit = data.get("creditScoreInfo", {})
    diamond = data.get("diamondCostRes", {})

    pet_name = p.get("name", "لا يوجد")
    skills = ', '.join(str(i) for i in profile.get("equipedSkills", [])) or "لا يوجد"
    weapons = ', '.join(str(i) for i in b.get("weaponSkinShows", [])) or "لا يوجد"

    msg = f"""🎮 <b>Player Info</b> 🎮
🆔 <b>Account ID:</b> {b.get("accountId", "غير معروف")}
📛 <b>Nickname:</b> {b.get("nickname", "غير معروف")}
🌍 <b>Region:</b> {b.get("region", "غير معروف")}
🏆 <b>Level:</b> {b.get("level", "غير معروف")}
⭐ <b>EXP:</b> {b.get("exp", "؟")}
📅 <b>Account Created:</b> {format_time(b.get("createAt", 0))}
⏰ <b>Last Login:</b> {format_time(b.get("lastLoginAt", 0))}

🔥 <b>BR Rank:</b> {b.get("rank", "؟")} (Max: {b.get("maxRank", "؟")})
🏅 <b>CS Rank:</b> {b.get("csRank", "؟")} (Max: {b.get("csMaxRank", "؟")})
📊 <b>Ranking Points:</b> {b.get("rankingPoints", "؟")}
📈 <b>CS Points:</b> {b.get("csRankingPoints", "؟")}
❤️ <b>Likes:</b> {b.get("liked", "؟")}
🎖️ <b>Badge ID:</b> {b.get("badgeId", "؟")} | Count: {b.get("badgeCnt", "؟")}
📌 <b>Pin ID:</b> {b.get("pinId", "؟")}
🎯 <b>Season ID:</b> {b.get("seasonId", "؟")}
📜 <b>Title:</b> {b.get("title", "؟")}
🧩 <b>Release Version:</b> {b.get("releaseVersion", "؟")}

🧰 <b>Weapons:</b> {weapons}
🎒 <b>Bag Skin:</b> {b.get("gameBagShow", "؟")}
👗 <b>Skills:</b> {skills}
🎨 <b>Avatar ID:</b> {profile.get("avatarId", "؟")}

🐾 <b>Pet:</b> {pet_name} (Level: {p.get("level", "؟")}, Skin ID: {p.get("skinId", "؟")})

👥 <b>Clan:</b> {c.get("clanName", "بدون")}
🆔 <b>Clan ID:</b> {c.get("clanId", "؟")}
⭐ <b>Clan Level:</b> {c.get("clanLevel", "؟")}
👤 <b>Captain ID:</b> {c.get("captainId", "؟")}
👥 <b>Members:</b> {c.get("memberNum", "؟")}/{c.get("capacity", "؟")}

📝 <b>Signature:</b> {s.get("signature", "بدون")}
💎 <b>Diamond Cost:</b> {diamond.get("diamondCost", "؟")}
🏅 <b>Credit Score:</b> {credit.get("creditScore", "؟")}

🖼️ <b>Banner ID:</b> {b.get("bannerId", "؟")}
👤 <b>Head Pic ID:</b> {b.get("headPic", "؟")}
"""
    return msg

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.reply("أرسل رقم UID الخاص باللاعب لعرض معلوماته 🎮")

@dp.message(F.text.regexp(r'^\d{6,}$'))
async def handle_uid(message: Message):
    uid = message.text.strip()
    url = f"https://alibot-production.up.railway.app/accinfo?uid={uid}&region=default"

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        if "basicInfo" not in data:
            await message.reply("❌ لم يتم العثور على بيانات لهذا الحساب.")
            return

        # أرسل صورة اللاعب أولًا
        image_url = f"https://genprofile.vercel.app/generate?uid={uid}"
        try:
            await message.reply_photo(photo=image_url, caption="📸 صورة اللاعب")
        except Exception:
            await message.reply("⚠️ لم يتم عرض صورة اللاعب.")

        # ثم أرسل المعلومات النصية
        info_text = format_player_info(data)
        await message.reply(info_text)

    except Exception as e:
        logging.exception("Error fetching data:")
        await message.reply("❌ حدث خطأ أثناء جلب البيانات. حاول لاحقًا.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
