import numpy as np
import messages_db
from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

words_to_remove = ['eu', 'da', 'de', 'se', 'kk', 'kkk', 'kkkk', 'kkkkk',
                   'kkkkkk', 'kkkkkkk', 'kkkkkkkk', 'kkkkkkkkk',
                   'kkkkkkkkkk', 'na', 'que', 'pra', 'tá', 'essa', 'não',
                   'tem', 'tbm', 'mesmo', 'tô', 'mas', 'vou', 'no', 'mó',
                   'você', 'sua', 'esse', 'como', 'pq', 'sim', 'ai', 'vi',
                   'mais', 'vai', 'isso', 'uma', 'por', 'mano', 'assim',
                   'uns', 'quem', 'aí', 'só', 'dá', 'foi', 'tava', 'vc',
                   'nao', 'um', 'já', 'ja']

def make_word_cloud(words):    
    words = words.lower()
    stopwords = set(STOPWORDS)
    stopwords.update(words_to_remove)
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 8,
                max_words = 200,
                relative_scaling = 0.35).generate(words)
    wordcloud.to_file('image.png')

def make_group_wordcloud(chat):
    messages = messages_db.get_all_messages(chat)
    make_word_cloud(messages)

def make_my_wordcloud(user, chat):
    messages = messages_db.get_user_messages(user, chat)
    make_word_cloud(messages)

def make_interaction_pie_chart(chat, bot):
    members = []
    users_messages_count = messages_db.count_users_messages(chat)
    for id_member in users_messages_count.keys():
        member = bot.getChatMember(chat, id_member)
        members.append(member.user['first_name'])
    fig = plt.figure()
    plt.title('Group interaction')
    plt.pie(users_messages_count.values(), labels=members)
    fig.savefig('image.png')
