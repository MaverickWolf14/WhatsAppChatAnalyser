from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import seaborn as sns


#########################

extractor = URLExtract()

###########################

def set_user(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df

def split_words(df):
    words = []
    
    for message in df['message']:
        words.extend(message.split())
    
    return words

###############################

def fetch_stats(selected_user,df):
    
    df=set_user(selected_user, df)
    
    #for no. of messages
    num_messages = df.shape[0]

    # for no. of words
    words = split_words(df)
    
    #for no. of media messages 
    num_of_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #for no. of links
    link = []
    for message in df['message']:
        link.extend(extractor.find_urls(message))

    return num_messages,len(words),num_of_media_messages,len(link)

def busy_user_plt(df):

    # plotig the graph
    x = df['user'].value_counts().head()
    fig, ax = plt.subplots()
    ax.bar(x.index, x.values,color = 'red')
    plt.xticks(rotation='vertical')

    # making the dataframe
    df = round(x/df.shape[0]*100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    
    return fig,df

def create_wordcloud(selected_user,df):
    df = set_user(selected_user, df)
    
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    
    return df_wc

def most_common20(selected_user,df):
    df=set_user(selected_user, df)
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    
    words = []
    
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common20_df = pd.DataFrame(Counter(words).most_common(20))
    
    return most_common20_df

def emojis (selected_user,df):
    df = set_user(selected_user, df)
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    return emoji_df.head(20)

def timeline(selected_user,df):
    df = set_user(selected_user, df)
    
    timeline_df = df.groupby(['year', 'month_num', 'month']).count()[
        'message'].reset_index()
    
    time = []
    
    for i in range(timeline_df.shape[0]):
        time.append(timeline_df['month'][i] + "-" + str(timeline_df['year'][i]))
    
    timeline_df['time'] = time
    
    return timeline_df 

def daily_timeline(selected_user,df):
    df = set_user(selected_user, df)
    daily_timeline_df = df.groupby('daily_date').count()['message'].reset_index()
    
    return daily_timeline_df

def day_timeline(selected_user,df):
    df = set_user(selected_user, df)
    day_timeline_df = df.groupby('day_name').count()['message'].reset_index()

    x = df['day_name'].value_counts()
    figd, ax = plt.subplots()
    ax.bar(x.index, x.values, color='red')
    plt.xticks(rotation='vertical')

    x = df['month'].value_counts()
    figm, ax = plt.subplots()
    ax.bar(x.index, x.values, color='red')
    plt.xticks(rotation='vertical')

    return figd,figm

def period(selected_user,df):

    df = set_user(selected_user, df)

    x = df['period'].value_counts()
    figb, ax = plt.subplots()
    ax.bar(x.index, x.values, color='red')
    plt.xticks(rotation='vertical')

    period_df = df.pivot_table(index='day_name', columns='period',
                               values='message', aggfunc='count').fillna(0)
    
    figh,ax = plt.subplots() 
    ax = sns.heatmap(period_df)

    return figb,figh
