from telegram import ReplyKeyboardMarkup


def menu_keyboards():
    reply_keyboard = [
        [
            'Create task 📝',
            'Help 🙋‍♂️',
        ],
        [
            'Contact us 📞',
        ]
    ]
    return ReplyKeyboardMarkup(
        reply_keyboard,
        one_time_keyboard=False,
        resize_keyboard=True,
    )
