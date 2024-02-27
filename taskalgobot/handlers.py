from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from gpt import client as openai_client
from gpt.schemas import TaskDetail
from taskalgobot import keyboards


async def text_with_menu(update: Update, text: str) -> None:
    await update.message.reply_text(
        text=text,
        reply_markup=keyboards.menu_keyboards(),
    )


async def start_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
) -> None:
    text = (
        'Hi! I can convert your task to algorithms. '
        'Start typing your task 📝'
    )
    await text_with_menu(update, text=text)


async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
) -> None:
    text = (
        'Hi! I can convert your task to algorithms.'
        'Commands:\n\n'
        '🙋‍♂️ /help — This is what you see\n'
        '📞 /contact — Contact us if you have any questions :)'
    )
    await update.message.reply_text(text=text)


async def contact_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
) -> None:
    text = (
        'This function is developed as an example.'
    )
    await update.message.reply_text(text=text)


async def handle_task_to_algo(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id,
        action=ChatAction.TYPING,
    )
    await update.message.reply_text('🧠 Processing...')

    task = update.message.text

    task_detail: TaskDetail = await openai_client.divide_task_to_algo(task)

    if not task_detail:
        await update.message.reply_text(
            'I could not convert your task to algorithms. 😔'
        )
        return None

    await update.message.reply_text(task_detail.pretty_text)
