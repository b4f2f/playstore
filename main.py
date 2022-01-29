import os
import play_scraper
from pyrogram import Client, filters
from pyrogram.types import *


Bot = Client(
    "Play-Store-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.private & filters.all)
async def filter_all(bot, update):
    text = "Aşağıdaki butonları kullanarak play store arama yapa bilirsiniz.\n\n🐧 @b4f2f"
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Burada ara", switch_inline_query_current_chat="")],
            [InlineKeyboardButton(text="Başka bir sohbette ara", switch_inline_query="")]
        ]
    )
    await update.reply_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_inline_query()
async def search(bot, update):
    results = play_scraper.search(update.query)
    answers = []
    for result in results:
        details = "**Title:** `{}`".format(result["title"]) + "\n" \
        "**Açıklama:** `{}`".format(result["description"]) + "\n" \
        "**Uygulama Kimliği:** `{}`".format(result["app_id"]) + "\n" \
        "**Geliştirici:** `{}`".format(result["developer"]) + "\n" \
        "**Geliştirici Kimliği:** `{}`".format(result["developer_id"]) + "\n" \
        "**Puan:** `{}`".format(result["score"]) + "\n" \
        "**Price:** `{}`".format(result["price"]) + "\n" \
        "**Full Price:** `{}`".format(result["full_price"]) + "\n" \
        "**Free:** `{}`".format(result["free"]) + "\n" \
        "\n" + "Made by @FayasNoushad"
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Play Store", url="https://play.google.com"+result["url"])]]
        )
        try:
            answers.append(
                InlineQueryResultArticle(
                    title=result["title"],
                    description=result.get("description", None),
                    thumb_url=result.get("icon", None),
                    input_message_content=InputTextMessageContent(
                        message_text=details, disable_web_page_preview=True
                    ),
                    reply_markup=reply_markup
                )
            )
        except Exception as error:
            print(error)
    await update.answer(answers)


Bot.run()
