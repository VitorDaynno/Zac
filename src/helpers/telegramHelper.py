from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class TelegramHelper:

    @staticmethod
    def make_keyboard(prefix, items):
        keyboard = []
        lines = []
        for item in items:
            text, data = item.values()
            callback = prefix + str(data)
            button = InlineKeyboardButton(text, callback_data=callback)
            if len(lines) < 2:
                lines.append(button)
            else:
                keyboard.append(lines)
                lines = []
                lines.append(button)
        if len(lines) != 0:
            keyboard.append(lines)
        keyboard_markup = InlineKeyboardMarkup(keyboard)
        return keyboard_markup
