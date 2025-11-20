import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import random

TOKEN = "vk1.a.J8QKwJ4SUDZ--OcxLQUOx14xx8OyPyVbdik2pLbrV97fDD22Vkc240Up0Kt1NBJi4yi7diYcUliiNArTUB_C-ei7ddmJwiwJiju149RCgRMad1q9DwFErPEvYXolpEIW4pKSW5mipcjCBdONThE-ORCtnKJ4kqj1jJ2D94in5H8KG59uO2XKQhQCwl5mEk93dn0uV0GI4wT-kiYevfSOFA"
GROUP_ID = 234072772   # без кавычек

vk = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk, GROUP_ID)
vk_send = vk.get_api()

def send_message(user_id, text, keyboard=None):
    vk_send.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1, 999999),
        keyboard=keyboard
    )

# Пример клавиатуры
keyboard_main = '''
{
    "one_time": false,
    "buttons": [
        [
            { "action": { "type": "text", "label": "Котик" }, "color": "primary" }
        ],
        [
            { "action": { "type": "text", "label": "Помощь" }, "color": "secondary" }
        ]
    ]
}
'''

def get_cat():
    url = "https://api.thecatapi.com/v1/images/search"
    data = requests.get(url).json()
    return data[0]["url"]

print("Бот запущен...")

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.obj.message['text'].lower()
        user = event.obj.message['from_id']

        if text in ("начать", "start", "привет"):
            send_message(user, "Привет! Я бот.", keyboard=keyboard_main)

        elif text == "помощь":
            send_message(user,
            "Команды:\n"
            "— котик\n"
            "— погода <город>\n"
            "— курс\n"
            "— перевод <текст>\n"
            "— предсказание\n"
            )

        elif text == "котик":
            img = get_cat()
            send_message(user, img)

        elif text.startswith("погода"):
            city = text.replace("погода", "").strip()
            if city:
                api = "https://wttr.in/"+city+"?format=3"
                weather = requests.get(api).text
                send_message(user, weather)
            else:
                send_message(user, "Укажите город: погода Москва")

        elif text == "предсказание":
            facts = ["Сегодня всё получится!", "Вас ждёт подарок.", "Остерегайтесь странных людей."]
            send_message(user, random.choice(facts))

        else:
            send_message(user, "Я не понимаю команду. Напиши «помощь».")
