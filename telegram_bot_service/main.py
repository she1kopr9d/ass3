import asyncio
import logging

import aiogram
import deps
import handlers.uploads
import rabbit
import subscribers.uploads  # noqa

dp = aiogram.Dispatcher()
logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_router(handlers.uploads.router)
    async with rabbit.broker:
        await rabbit.broker.start()
        await dp.start_polling(deps.bot)


if __name__ == "__main__":
    asyncio.run(main())
