#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import snscrape.modules.twitter as sntwitter
from pymongo import MongoClient
import json
import base64
import streamlit as st
from PIL import Image
import datetime


# In[3]:


def create_df(scraped_data):
    tweet_data=pd.DataFrame(scraped_data,columns=["date","id","url","content","user","reply_count","retweet_count","Language","source","like_count"])        
    return tweet_data   


# In[4]:


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# In[5]:


st.title("TWITTER DATA SCRAPING")
add_bg_from_local("C:\\Users\\siddharth\\Project\\pexels.jpg")
option = st.selectbox('What type of data do you want to search? ', ('keyword', 'hashtag'))
word = st.text_input('Please enter a '+option, 'Example: Politics')
start = st.date_input("Select the start date ", datetime.date(2022, 1, 1),key='d1')
end = st.date_input("Select the end date ", datetime.date(2023, 1, 1),key='d2')
tweet_c = st.slider('How many tweets to scrape', 0, 1000, 5)
tweets_list = []


# In[6]:


# Define the tweet_data variable in the main scope
if word:
    if option=='keyword':
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweet_c:
                break
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
    else:
        for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweet_c:
                break
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
else:
    st.warning(option,' cannot be empty', icon="⚠️")


# In[7]:


if st.button("Upload to MongoDB"):
    tweet = tweets_df
    tweets_list = create_df(tweet) 
    client = MongoClient("mongodb://localhost:27017/")
    db = client["twitter"]
    collection = db['tweets']
    tweet_data_json = json.loads(tweets_df.to_json(orient='records'))
    collection.insert_many(tweet_data_json)
    st.success('Uploaded to MongoDB')


# In[8]:


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')
if not tweets_df.empty:
    csv = convert_df(tweets_df)
    st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_data.csv',mime='text/csv')    
# DOWNLOAD AS JSON
json_string = tweets_df.to_json(orient ='records')
st.download_button(label="Download data as JSON",file_name="Twitter_data.json",mime="application/json",data=json_string)      

