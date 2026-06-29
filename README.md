# 🎮 Telegram-бот: опитування «Хто коли гратиме сьогодні?»

Щодня **об 11:00 за Києвом** бот кидає в чат опитування з варіантами часу
(можна обрати кілька, видно хто за що проголосував).

Зроблено під **безкоштовний PythonAnywhere** — тією ж схемою, що й ProjectRita:
**webhook + Flask (WSGI) + проксі**, бо на free long polling вбивається.

Варіанти опитування: 12-14, 13-16, 16-18, 18-20, 20-22, 21-00,
+1 година з вибору, -1 година з вибору, зайнятий весь день,
вільний весь день/кличте, нічний час.

---

## Структура

| Файл | Що це |
|------|-------|
| `wsgi.py` | точка входу для вкладки **Web** PythonAnywhere |
| `app/webhook.py` | Flask-додаток, приймає оновлення від Telegram |
| `app/handlers.py` | команди `/start`, `/poll`, `/chatid` |
| `app/set_webhook.py` | одноразово реєструє вебхук у Telegram |
| `send_poll.py` | щоденна відправка о 11:00 (Scheduled task) |
| `app/poll.py` | текст і варіанти опитування |

---

## Деплой на free PythonAnywhere

**1. Залити код.** У Bash-консолі PythonAnywhere:
```bash
git clone <твій-репозиторій> ~/ProjectForLudmila
cd ~/ProjectForLudmila
pip install --user -r requirements.txt
cp .env.example .env   # і вписати BOT_TOKEN, CHAT_ID, WEBHOOK_SECRET
```

**2. Створити веб-додаток.** Вкладка **Web → Add a new web app → Manual config**
(версія Python як у консолі). Потім **WSGI configuration file** → замінити вміст на:
```python
import sys
path = "/home/<username>/ProjectForLudmila"
if path not in sys.path:
    sys.path.insert(0, path)
from wsgi import application
```
Натиснути **Reload**. Перевір: відкрий `https://<username>.pythonanywhere.com/`
— має бути «Bot is running».

> Якщо `.env` не підхоплюється веб-додатком — пропиши змінні в WSGI-файлі
> через `os.environ[...]` перед імпортом, або в Web → Environment variables.

**3. Зареєструвати вебхук** (один раз, у консолі):
```bash
cd ~/ProjectForLudmila
WEBHOOK_URL=https://<username>.pythonanywhere.com/webhook python -m app.set_webhook
```
Тепер у чаті працюють `/poll`, `/chatid`, `/start`.

**4. Щоденна відправка о 11:00.** Вкладка **Tasks → Scheduled task**:
```
python /home/<username>/ProjectForLudmila/send_poll.py
```
Час задається **в UTC**:
- **08:00 UTC** = 11:00 Київ влітку (EEST, UTC+3)
- **09:00 UTC** = 11:00 Київ взимку (EET, UTC+2)

> Free-акаунт дає один щоденний task — цього й треба. Постав 08:00 UTC.

---

## Локальний тест
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # вписати BOT_TOKEN, CHAT_ID

python send_poll.py    # разова відправка опитування в CHAT_ID
```
Щоб дізнатись `CHAT_ID`: додай бота в чат і напиши `/chatid`
(для цього бот має приймати оновлення — або тимчасово підніми webhook).
