from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Тексты для разделов журнала Шортрид
TEXTS = {
    'main_menu': '📚 Добро пожаловать в юридический онлайн-журнал "Шортрид"! Выберите интересующий вас раздел:',

    'about': '''
ℹ️ **Что такое Шортрид**

ШОРТРИД — это юридический онлайн-журнал.

Мы отбираем самые важные юридические новости и объясняем простым языком сложные правовые вопросы для юристов-практиков, руководителей компаний и тех, кто работает с бизнесом.

Подробнее здесь: https://shortread.ru/o-portale/
''',

    'author': '''
✍️ **Как стать автором**

Если Вы хотите опубликовать свой материал, мы всегда «за». Единственное – нужно быть готовым к тому, что мы перерабатываем все материалы под формат ШОРТРИД.

Напишите свое предложение на info@shortread.ru, и мы расскажем о формате материалов подробнее.
''',

    'subscription': '''
💰 **Как купить подписку**

Оформить подписку на 1 месяц или на 1 год можно по этой ссылке: https://shortread.ru/product/podpiska/
'''
}


# Клавиатуры
def get_main_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton('ℹ️ Что такое Шортрид')],
        [KeyboardButton('✍️ Как стать автором')],
        [KeyboardButton('💰 Как купить подписку')]
    ], resize_keyboard=True)


def get_back_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton('⬅️ Главное меню')]], resize_keyboard=True)


# Обработчики команд
async def start(update, context):
    await update.message.reply_text(
        TEXTS['main_menu'],
        reply_markup=get_main_keyboard()
    )


async def handle_message(update, context):
    text = update.message.text
    user = update.message.from_user

    print(f"Сообщение от {user.first_name} ({user.id}): {text}")

    response_map = {
        'ℹ️ Что такое Шортрид': TEXTS['about'],
        '✍️ Как стать автором': TEXTS['author'],
        '💰 Как купить подписку': TEXTS['subscription'],
        '⬅️ Главное меню': TEXTS['main_menu']
    }

    response = response_map.get(text)

    if text == '⬅️ Главное меню':
        await update.message.reply_text(
            response,
            reply_markup=get_main_keyboard()
        )
    elif response:
        await update.message.reply_text(
            response,
            reply_markup=get_back_keyboard()
        )
    else:
        await update.message.reply_text(
            'Пожалуйста, используйте кнопки меню для навигации.',
            reply_markup=get_main_keyboard()
        )


# Основная функция
def main():
    # Замените "YOUR_BOT_TOKEN" на реальный токен вашего бота
    application = Application.builder().token("7983437178:AAF1rC3JugB0sTpnSl3VHft-CGu6jONQydM").build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Бот Шортрид запущен...")
    application.run_polling()


if __name__ == '__main__':
    main()