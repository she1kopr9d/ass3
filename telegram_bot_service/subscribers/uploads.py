import aiogram

import deps
import rabbit
import schemas


@rabbit.broker.subscriber("add_file_answer")
async def add_file_answer_handler(
    data: schemas.LinkData,
):
    bot: aiogram.Bot = await deps.get_bot()

    await bot.send_message(
        chat_id=data.user_id,
        text=f"`{data.link}`",
        parse_mode="Markdown",
    )
