import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

# py -m streamlit run app.py

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data =  bytes_data.decode("utf-8")
    #st.text(data)
    df = preprocessor.preprocess(data)
    
    st.header("Your chat : ")
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # stats of the chat

        st.title("Here's your chat analysis :)")

        st.title("Status of the chat : ")

        num_messages, words, num_of_media_messages, num_link = helper.fetch_stats(
            selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.subheader(num_messages)

        with col2:
            st.header("Total Words")
            st.subheader(words)
        with col3:
            st.header("Media Shared")
            st.subheader(num_of_media_messages)
        with col4:
            st.header("Links Shared")
            st.subheader(num_link)

        #time line Monthly
        st.title("Chat Timeline : Monthly")
        timeline_df = helper.timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline_df['time'], timeline_df['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #time line Daily
        st.title("Chat Timeline : Daily")
        daily_timeline_df = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline_df['daily_date'], daily_timeline_df['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity map
        st.title("Activity map")
        figd,figm = helper.day_timeline(selected_user, df)
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most active days")
            st.pyplot(figd)
        with col2:
            st.header("Most active months")
            st.pyplot(figm)

        # period 
        st.header("most active Period")
        figb,figh = helper.period(selected_user, df) 
        
        st.subheader("Bar graph")
        st.pyplot(figb)

        st.subheader("Heatm map")
        st.pyplot(figh)

        

        # finding the most active user
        if selected_user == 'Overall':
            
            fig,busy_df = helper.busy_user_plt(df)
            
            st.title('Most actie users in the group')

            col1,col2 = st.columns(2)
            with col1:
                st.pyplot(fig)
            with col2:
                st.dataframe(busy_df)

        # for wordcloud 
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        wc_plt, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(wc_plt)


        #for most common
        st.title("Most common words ")
        most_common20_df = helper.most_common20(selected_user, df)
        fig,ax = plt.subplots()
        ax.bar(most_common20_df[0],most_common20_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # emojis
        st.title("Favourite emojis")
        emoji_df =  helper.emojis(selected_user, df)
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(10), labels = emoji_df[0].head(10),autopct = "%0.2f")
            st.pyplot(fig)
        
        
