#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install streamlit')
get_ipython().system('pip install pymongo')
get_ipython().system('pip install snscrape')


# In[2]:


get_ipython().run_cell_magic('writefile', 'app.py', 'import pandas as pd\nimport snscrape.modules.twitter as sntwitter\nfrom pymongo import MongoClient\nimport json\nimport base64\nimport streamlit as st\nfrom PIL import Image\nimport datetime\n\n\ndef create_df(scraped_data):\n    tweet_data=pd.DataFrame(scraped_data,columns=["date","id","url","content","user","reply_count","retweet_count","Language","source","like_count"])        \n    return tweet_data   \n\ndef add_bg_from_local(image_file):\n    with open(image_file, "rb") as image_file:\n        encoded_string = base64.b64encode(image_file.read())\n    st.markdown(\n        f"""\n        <style>\n        .stApp {{\n            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});\n            background-size: cover\n        }}\n        </style>\n        """,\n        unsafe_allow_html=True\n    )\n\ndef app():\n    st.title("TWITTER DATA SCRAPING")\n    add_bg_from_local("C:\\\\Users\\\\siddharth\\\\Project\\\\pexels.jpg")\n    option = st.selectbox(\'What type of data do you want to search? \', (\'keyword\', \'hashtag\'))\n    word = st.text_input(\'Please enter a \'+option, \'Example: Politics\')\n    start = st.date_input("Select the start date ", datetime.date(2022, 1, 1),key=\'d1\')\n    end = st.date_input("Select the end date ", datetime.date(2023, 1, 1),key=\'d2\')\n    tweet_c = st.slider(\'How many tweets to scrape\', 0, 1000, 5)\n    tweets_list = []\n\n    # Define the tweet_data variable in the main scope\n    if word:\n        if option==\'keyword\':\n            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f\'{word} + since:{start} until:{end}\').get_items()):\n                if i>tweet_c:\n                    break\n                tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])\n            tweets_df = pd.DataFrame(tweets_list, columns=[\'ID\',\'Date\',\'Content\', \'Language\', \'Username\', \'ReplyCount\', \'RetweetCount\', \'LikeCount\',\'Source\', \'Url\'])\n        else:\n            for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f\'{word} + since:{start} until:{end}\').get_items()):\n                if i>tweet_c:\n                    break\n                tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])\n            tweets_df = pd.DataFrame(tweets_list, columns=[\'ID\',\'Date\',\'Content\', \'Language\', \'Username\', \'ReplyCount\', \'RetweetCount\', \'LikeCount\',\'Source\', \'Url\'])\n    else:\n        st.warning(option,\' cannot be empty\', icon="⚠️")\n            \n            \n\n    if st.button("Upload to MongoDB"):\n        tweet = tweets_df\n        tweets_list = create_df(tweet) \n        client = MongoClient("mongodb://localhost:27017/")\n        db = client["twitter"]\n        collection = db[\'tweets\']\n        tweet_data_json = json.loads(tweets_df.to_json(orient=\'records\'))\n        collection.insert_many(tweet_data_json)\n        st.success(\'Uploaded to MongoDB\')\n\n    @st.cache\n    def convert_df(df):\n        return df.to_csv().encode(\'utf-8\')\n    if not tweets_df.empty:\n        csv = convert_df(tweets_df)\n        st.download_button(label="Download data as CSV",data=csv,file_name=\'Twitter_data.csv\',mime=\'text/csv\')\n        \n        # DOWNLOAD AS JSON\n        json_string = tweets_df.to_json(orient =\'records\')\n        st.download_button(label="Download data as JSON",file_name="Twitter_data.json",mime="application/json",data=json_string) \n                     \nif __name__ == \'__main__\':\n    app()         \n')


# In[ ]:


get_ipython().system('streamlit run app.py & npx localtunnel --port 8501')

