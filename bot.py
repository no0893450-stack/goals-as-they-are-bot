from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from flask import Flask
import threading
import asyncio
import random
import json
import os
from datetime import datetime

TOKEN = os.getenv("8954629911:AAEWmYf-R2Qxmexi1WL0gVFwgNF6_enIasY")
STATS_FILE = "stats.json"

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set")
    
bot = Bot(token=TOKEN)
dp = Dispatcher()

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_web_server():
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)

def load_stats():
if not os.path.exists(STATS_FILE):
return {"users": [], "goals": []}

```
with open(STATS_FILE, "r", encoding="utf-8") as file:
    return json.load(file)
```

def save_stats(stats):
with open(STATS_FILE, "w", encoding="utf-8") as file:
json.dump(stats, file, ensure_ascii=False, indent=2)

def add_goal(message: Message, goal: str):
stats = load_stats()
user_id = message.from_user.id

```
if user_id not in stats["users"]:
    stats["users"].append(user_id)

stats["goals"].append({
    "user_id": user_id,
    "name": message.from_user.full_name,
    "goal": goal,
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

save_stats(stats)
```

@dp.message(CommandStart())
async def start(message: Message):
await message.answer(
"Опишіть свою ціль, будь ласка.\n\n"
"Ваш помічник допоможе сформулювати її правильно.\n\n"
"Почніть повідомлення зі слів:\n\n"
""Мені потрібно...""
)

@dp.message(Command("stats"))
async def stats_handler(message: Message):
stats = load_stats()

```
users_count = len(stats["users"])
goals_count = len(stats["goals"])
last_goals = stats["goals"][-5:]

text = (
    "📊 Статистика бота\n\n"
    f"👥 Користувачів: {users_count}\n"
    f"📝 Цілей сформульовано: {goals_count}\n\n"
    "Останні цілі:\n"
)

if not last_goals:
    text += "Поки що цілей немає."
else:
    for item in last_goals:
        text += f"— {item['goal']}\n"

await message.answer(text)
```

@dp.message()
async def reply(message: Message):
text = message.text.strip()
lower_text = text.lower()

```
if lower_text.startswith("мені потрібно "):
    goal = text[14:].strip()
elif lower_text.startswith("треба "):
    goal = text[6:].strip()
elif lower_text.startswith("потрібно "):
    goal = text[8:].strip()
else:
    await message.answer(
        'Будь ласка, почніть повідомлення зі слів:\n\n"Мені потрібно..."'
    )
    return

add_goal(message, goal)

score = random.randint(7, 10)

await message.answer(
    f'Спробуйте так:\n\n<b>"А хулі би мені не {goal.lower()}?"</b>',
    parse_mode="HTML"
)

messages = [
    f"💪 Ціль потужна! {score}/10! Але ти впораєшся!",
    f"🚀 Серйозна заявка. {score}/10. Пішла жара!",
    f"🔥 Ціль прийнята. Рівень складності: {score}/10. Але хто, як не ти?",
    f"✨ Непросто, але красиво. {score}/10. Можна робити!",
    f"😎 Ого. Ціль має характер. {score}/10 за драматургію!",
    f"🦾 Схоже на виклик. {score}/10. Виклики існують, щоб їх приймати.",
    f"🐱 План звучить амбітно. {score}/10. Кіт схвалює.",
    "🎯 Це вже не мрія. Це майбутня галочка в списку справ.",
    f"⚡ Потенціал відчувається. {score}/10. Поїхали!",
    f"🏆 Майбутня перемога зафіксована. {score}/10. Залишилось її отримати."
]

gifs = [
    "https://media.giphy.com/media/12XDYvMJNcmLgQ/giphy.gif",
    "https://media.giphy.com/media/ACcXRXwUqJ6Ok/giphy.gif",
    "https://media.giphy.com/media/l41lFw057lAJQMwg0/giphy.gif",
    "https://media.giphy.com/media/26u4cqiYI30juCOGY/giphy.gif",
    "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
    "https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif",
    "https://media.giphy.com/media/111ebonMs90YLu/giphy.gif",
    "https://media.giphy.com/media/ely3apij36BJhoZ234/giphy.gif",
    "https://media.giphy.com/media/artj92V8o75VPL7AeQ/giphy.gif",
    "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif"
]

await message.answer(random.choice(messages))
await message.answer_animation(random.choice(gifs))
```

async def main():
threading.Thread(target=run_web_server, daemon=True).start()
await dp.start_polling(bot)

if **name** == "**main**":
asyncio.run(main())
