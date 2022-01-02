from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class StartKeyboard:
    global_btn = KeyboardButton("Global📊")
    top10_btn = KeyboardButton("Top10📈")
    portfolio_btn = KeyboardButton("Personal Portfolio💼")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(global_btn, top10_btn, portfolio_btn)


class PersonalPortfolioKeyboard:
    return_btn = KeyboardButton("Log out from a personal portfolio🔙")
    check_btn = KeyboardButton("Check my watching list🔄")
    balance_btn = KeyboardButton("Check my balance📊")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(StartKeyboard.global_btn, StartKeyboard.top10_btn).row(
        check_btn).row(balance_btn).row(return_btn)


class InlineKeyboard:
    refresh_btn = InlineKeyboardButton(text="Refresh🔄", callback_data="refresh")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[refresh_btn]])
