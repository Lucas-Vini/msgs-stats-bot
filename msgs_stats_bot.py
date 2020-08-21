import messages_db
import data_visualization
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater(token='bot-token', use_context=True)
dispatcher = updater.dispatcher

start_msg = '''Welcome to @msgs_stats_bot!
Please, add me to a group and type some command to see some statistics.
To see the commands available, send me /help.'''
help_msg = '''The following commands are availabe:
/start - Says what you have to do to start using the StatsBot
/help - Gives you information about the available commands
/groupwords - Generates a word cloud with all messages available
/mywords - Generates a word cloud with all of your messages available in the group
/interaction - Creates a pie chart of who sent more messages'''

def start(update, context):
    '''Answer to the command /start'''
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=start_msg)
    
def help_bot(update, context):
    '''Answer to the command /help'''
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=help_msg)

def save_message(update, context):
    '''Save any message the bot read'''
    msg = update.message.text
    date = update.message.date
    user = update.message.from_user['id']
    chat = update.effective_chat['id']
    messages_db.save_message(msg, str(date), user, chat)

def group_words(update, context):
    '''Answer to the command /groupwords'''
    data_visualization.make_group_wordcloud(update.effective_chat['id'])
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open('image.png', 'rb'))

def my_words(update, context):
    '''Answer to the command /mywords'''
    user = update.message.from_user['id']
    chat = update.effective_chat['id']
    data_visualization.make_my_wordcloud(user, chat)
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open('image.png', 'rb'))

def interaction(update, context):
    '''Answer to the command /interaction'''
    data_visualization.make_interaction_pie_chart(update.effective_chat['id'],
                                                  context.bot)
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open('image.png', 'rb'))

def main():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help_bot)
    dispatcher.add_handler(help_handler)

    group_words_handler = CommandHandler('groupwords', group_words)
    dispatcher.add_handler(group_words_handler)

    my_words_handler = CommandHandler('mywords', my_words)
    dispatcher.add_handler(my_words_handler)

    interaction_handler = CommandHandler('interaction', interaction)
    dispatcher.add_handler(interaction_handler)

    save_message_handler = MessageHandler(Filters.text, save_message)
    dispatcher.add_handler(save_message_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()
