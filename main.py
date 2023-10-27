import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
bot = telebot.TeleBot("6447118255:AAFjA4eiuVhcSUCwwITOszVJl7L3HJvmXqo",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Начать"  # Можно менять текст
text_button_1 = "Интересные факты"  # Можно менять текст
text_button_2 = "Письмо в будущее"  # Можно менять текст
text_button_3 = "Фразы философов"  # Можно менять текст


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Приветствую тебя дорогой друг! Что тебя интересует?',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, '*Напиши* как тебя зовут?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! [Факты про имя](https://adme.media/svoboda-kultura/15-faktov-ob-imenah-kotorye-perevorachivayut-mir-s-nog-na-golovu-2516431/?ysclid=lnuo1pnsfm803672327) *Какой твой возраст?*')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо! Давай узнавать _мир_', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, """1. Бетховен никогда не умел ни умножать, ни делить.
2. Пчелы могут летать выше Эвереста.
3. Вафельница вдохновила на создание одной из первых пар кроссовок Nike.
4. Стив Джобс, Стив Возняк и Рон Уэйн основали Apple Inc. в День дурака
5. Омертвевшие клетки кожи являются основным компонентом домашней пыли.
6. Длина кровеносной системы составляет более 96 500 км.
7. У кошек меньше пальцев на задних лапах.
8.  Коровы, которых называют по кличке, дают на 258 л молока в год больше, чем те, которых никак не зовут.
9. Уборка дома так же вредна для здоровья, как и курение пачки сигарет.
10. Существует так много сортов яблок, что если съедать по 1 в день, то ушло бы 20 лет на то, чтобы перепробовать все.""", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "(https://future-mail.org/add.php)", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Самое сложное - познать себя; проще всего плохо говорить о других (Фалес Милетский). Я никого ничему не могу научить. Я могу только заставить тебя думать (Сократ). Мы не судим людей, которых любим (Жан-Поль Сартр). Знание - сила (Фрэнсис Бэкон).", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()

