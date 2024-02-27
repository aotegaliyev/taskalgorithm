from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    Updater,
)

from taskalgobot import handlers


from settings import Config
from telegram.ext import Application

ptb = Application.builder().token(Config.BOT_TOKEN).updater(None).build()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not Config.URL:
        updater = Updater(ptb.bot, update_queue=ptb.update_queue)
        await updater.initialize()
        await updater.start_polling(poll_interval=1)
    else:
        await ptb.bot.set_webhook(
            url=f'{Config.URL}/telegram',
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
        )

    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()


app = FastAPI(lifespan=lifespan)


@app.post('/telegram')
async def process_update(request: Request):
    req = await request.json()
    await ptb.update_queue.put(Update.de_json(data=req, bot=ptb.bot))
    return Response(status_code=200)


ptb.add_handler(CommandHandler('start', handlers.start_command))
ptb.add_handler(CommandHandler('help', handlers.help_command))
ptb.add_handler(CommandHandler('contact', handlers.contact_command))

ptb.add_handler(
    MessageHandler(filters.Regex('^(Create task 📝)'), handlers.start_command)
)
ptb.add_handler(MessageHandler(filters.Regex('^(Help 🙋‍♂️)'), handlers.help_command))
ptb.add_handler(
    MessageHandler(filters.Regex('^(Contact us 📞)'), handlers.contact_command)
)

ptb.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_task_to_algo)
)
