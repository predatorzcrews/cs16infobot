import valve.source.a2s
import telebot

SERVER_ADDRESS = ('185.149.40.91', 27032)  # Заміни 'IP' і 'ПОРТ' на реальні дані

bot = telebot.TeleBot('7185418694:AAG-dwKP1sYGog5QPhzkGDJyasHTcF6b2d8')  # Заміни 'ТОКЕН БОТА' на реальний токен

# Обробник команди /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Привіт! Щоб дізнатися онлайн на сервері, напиши /check або щоб побачити список гравців, напиши /players.'
    )

# Обробник команди /check
@bot.message_handler(commands=['check'])
def check_command(message):
    try:
        with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
            info = server.info()  # Отримання інформації про сервер
        bot.send_message(
            message.chat.id,
            f"Онлайн на сервері: {info['player_count']}/{info['max_players']}\n"
            f"Сервер: {info['server_name']}\nКарта: {info['map']}"
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"Не вдалося отримати дані про сервер: {e}")

# Обробник команди /players
@bot.message_handler(commands=['players'])
def players_command(message):
    try:
        with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
            players = server.players()  # Отримання інформації про гравців
        if players["players"]:
            player_list = '\n'.join(
                [f"{player['name']} (Очки: {player['score']}) Час в грі: {player['duration']:.2f} хв." for player in sorted(players["players"], key=lambda p: p["score"], reverse=True)]
            )
            bot.send_message(message.chat.id, f"Гравці на сервері:\n{player_list}")
        else:
            bot.send_message(message.chat.id, "На сервері немає гравців.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Не вдалося отримати дані про гравців: {e}")

# Обробник команди /info
@bot.message_handler(commands=['info'])
def info_command(message):
    bot.send_message(
        message.chat.id,
        """❤️ AutoMix|5x5 - 185.149.40.91:27032
♥️ Работает 24/7
♥️ Заходи и играй
♥️ 185.149.40.91:37032 - IP HLTV для тех кто хочет смотреть матч с задержкой 5 секунд
♥️ http://185.149.40.91/hltv1346/demos - Ссылка на демо ХЛТВ для скачивания
♥️ bind "n" "say /ready" - для открытия меню и готовности к игре
♥️ 💳 4211130500551512 - карта для продления хоста

♥️Також наші партнери та друзі - 🇺🇦 Бандерштат IP - 195.211.60.213:27018⚡️
Ласкаво просимо 👍

☺️ Реклама нашего Автомикса приветствуется ♥️

Бан лист - https://mixello5x5.1game.in.ua/csbans/bans/index.html"""
    )

# Запуск бота
bot.polling(none_stop=True, interval=0)
