import telebot
import random

# токен бота в Telegram
TELEGRAM_BOT_TOKEN = '6425458022:AAGoMTSsDwGp1OSiJPU7Ao2z7-T-mDYoCKA'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

questions = [
    {
        "question": "Сколько пальцев на руке?",
        "options": ["Пять", "Шесть", "Семь", "Восемь"],
        "correct_option": 0,
    },
    {
        "question": "Какой год был основан Рим?",
        "options": ["750 до н. э.", "100 до н. э.", "500 до н. э.", "200 до н. э."],
        "correct_option": 0,
    },
    {
        "question": "Какая планета является красной?",
        "options": ["Венера", "Марс", "Юпитер", "Сатурн"],
        "correct_option": 1,
    },
    {
        "question": "Сколько дней в феврале в високосном году?",
        "options": ["27", "28", "29", "30"],
        "correct_option": 2,
    },
    {
        "question": "Какое химическое обозначение у воды?",
        "options": ["CO2", "O2", "H2O", "N2"],
        "correct_option": 2,
    },
]

user_answers = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в игру 'Кто хочет стать миллионером?'!\n"
                                      "Отправьте /play, чтобы начать игру.")

@bot.message_handler(commands=['play'])
def handle_play(message):
    user_id = message.from_user.id
    user_answers[user_id] = {"question_index": 0, "score": 0}
    send_question(message.chat.id, user_id)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    if user_id in user_answers:
        handle_answer(message, user_id)
    else:
        bot.send_message(message.chat.id, "Чтобы начать игру, отправьте /play.")

def send_question(chat_id, user_id):
    question_data = questions[user_answers[user_id]["question_index"]]
    question_text = f"Вопрос {user_answers[user_id]['question_index'] + 1}:\n{question_data['question']}\n\n"
    for i, option in enumerate(question_data['options']):
        question_text += f"{i + 1}. {option}\n"
    bot.send_message(chat_id, question_text)

def handle_answer(message, user_id):
    try:
        user_answer = int(message.text)
        question_data = questions[user_answers[user_id]["question_index"]]
        correct_option = question_data["correct_option"]

        if user_answer == correct_option + 1:
            user_answers[user_id]["score"] += 1

        user_answers[user_id]["question_index"] += 1

        if user_answers[user_id]["question_index"] < len(questions):
            send_question(message.chat.id, user_id)
        else:
            bot.send_message(
                message.chat.id,
                f"Игра завершена! Ваш счет: {user_answers[user_id]['score']} из {len(questions)}."
            )
            del user_answers[user_id]

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите номер варианта ответа.")

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
