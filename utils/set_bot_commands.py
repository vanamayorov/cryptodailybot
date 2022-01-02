from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Starts bot"),
            types.BotCommand("help", "Shows general info about bot"),
            types.BotCommand("global", "Returns daily information about crypto market📊"),
            types.BotCommand("top10", "Returns top10 coins by capitalization📈"),
            types.BotCommand("p", "Returns the current &lt;coin&gt; price in $💵(by default, bitcoin)"),
        ]
    )