from typing import Final
import telegram
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ContextTypes, Application
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from query_data import handle_query


# Setting up tokens
TOKEN: Final = os.getenv('TELEGRAM_TOKEN')
BOT_USERNAME: Final = '@HubSpotMYceliumBot'
gpt_token = os.getenv('OPENAI_API_KEY')


# global variables to store user input temp
user_input = ""

def chat_gpt(user_input):
    # setup OpenAI chatbot as main LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=gpt_token)

    # prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Be really rude and long in answers, but give the answer within the text. If user have basic spelling mistakes, sometimes point them out."),
        ("user", user_input)
    ])

    # create a chain to process the prompt
    chain = prompt | llm | StrOutputParser()

    # invoke the chain and get the response
    response = chain.invoke({ "user_input": user_input })

    return response


# bot commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thank for joining this bot!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Its all straight forward here. Thanks)")

async def openai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You have now entered the beast of the beasts: EVIL (but clever) OPENAI CHAT BOT\nPlease enter your query:")
    context.chat_data['awaiting_input'] = True

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You have activated EVIL GPT\nEnter your query already:")
    context.chat_data['awaiting_input'] = True


def handle_response(text: str)  -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "Hello!"
    
    if "how are you" in processed:
        return "Fine, thanks for asking. how are you?)"
    

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_input
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User {update.message.chat_id} in {message_type}: {text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, " ").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        if 'awaiting_input' in context.chat_data and context.chat_data['awaiting_input']:
            user_input = text  # store user input
            # await update.message.reply_text("Your query has been saved. Now wait for the response.")
            await update.message.reply_text("Aha... few sec")
            context.chat_data['awaiting_input'] = False
            response: str = chat_gpt(text)
        else:
            response: str = handle_response(text)

    print("Bot: ", response)
    await update.message.reply_text(response, reply_to_message_id=update.message.message_id)  # reply to the original message

# handling errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update}, caused error: {context.error}")

if __name__ == '__main__':
    print('Bot started...')

    app = Application.builder().token(TOKEN).build()

    # adding handlers for commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('openai', openai_command))
    app.add_handler(CommandHandler('gpt', gpt))

    # adding handler for user messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # adding error handler
    app.add_error_handler(error)

    # starting bot
    print('Started polling...')
    app.run_polling(poll_interval=1)