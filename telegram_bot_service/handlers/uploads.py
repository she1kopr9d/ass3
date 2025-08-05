import aiogram
import aiogram.types

import rabbit


router: aiogram.Router = aiogram.Router()


@router.message(aiogram.F.document)
async def handle_document(message: aiogram.types.Message):
    document = message.document

    file = await message.bot.get_file(document.file_id)
    file_path = file.file_path
    file_bytes = await message.bot.download_file(file_path)

    raw_bytes = file_bytes.read()
    encoded_bytes = raw_bytes.decode("latin1")

    data = {
        "filebytes": encoded_bytes,
        "user_id": message.from_user.id,
    }

    await rabbit.broker.publish(data, queue="add_file")
