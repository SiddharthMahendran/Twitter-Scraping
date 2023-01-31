#!/usr/bin/env python
# coding: utf-8

# In[3]:


import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime
import pymongo
import time
from PIL import Image
import base64


# In[4]:


client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["Twitter_Database"]
tweets_df = pd.DataFrame()
dfm = pd.DataFrame()
st.write(" TWITTER DATA SCRAPING ")
img = Image.open("C:\\Users\\siddharth\\Project\\Image1.jpeg")
st.image(img, width=200)
option = st.selectbox('What type of data do you want to search? ', ('keyword', 'hashtag'))
word = st.text_input('Please enter a '+option, 'Example: Politics')
start = st.date_input("Select the start date ", datetime.date(2022, 1, 1),key='d1')
end = st.date_input("Select the end date ", datetime.date(2023, 1, 1),key='d2')
tweet_c = st.slider('How many tweets to scrape', 0, 1000, 5)
tweets_list = []

# Background Image
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
add_bg_from_local("C:\\Users\\siddharth\\Project\\pexels.jpg")    
    
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
        
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

if not tweets_df.empty:
    csv = convert_df(tweets_df)
    st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_data.csv',mime='text/csv',)

    # DOWNLOAD AS JSON
    json_string = tweets_df.to_json(orient ='records')
    st.download_button(label="Download data as JSON",file_name="Twitter_data.json",mime="application/json",data=json_string,)

    # UPLOAD DATA TO DATABASE
    if st.button('Upload Tweets to Database'):
        coll=word
        coll=coll.replace(' ','_')+'_Tweets'
        mycoll=mydb[coll]
        dict=tweets_df.to_dict('records')
        if dict:
            mycoll.insert_many(dict) 
            ts = time.time()
            mycoll.update_many({}, {"$set": {"KeyWord_or_Hashtag": word+str(ts)}}, upsert=False, array_filters=None)
            st.success('Successfully uploaded to database', icon="✅")
            st.balloons()
        else:
            st.warning('Cant upload because there are no tweets', icon="⚠️")
    if st.button('Show Tweets'):
        st.write(tweets_df)

# SIDEBAR
with st.sidebar:   
    st.write('Uploaded Datasets: ')
    for i in mydb.list_collection_names():
        mycollection=mydb[i]
        #st.write(i, mycollection.count_documents({}))        
        if st.button(i):            
            dfm = pd.DataFrame(list(mycollection.find())) 

# DISPLAY THE DOCUMENTS IN THE SELECTED COLLECTION
if not dfm.empty: 
    st.write( len(dfm),'Records Found')
    st.write(dfm)             
    


# In[ ]:




