import streamlit as st
import numpy as np
import pandas as pd
from preprocessor import preprocess
from helper import medal_tally , country_year_list , fetch_medal_tally , data_over_time , most_successfull , yearwise_medal_tally , country_sport_heatmap , most_successfull_countrywise
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns




df = pd.read_csv('datasets/athlete_events.csv')
region_df = pd.read_csv('datasets/noc_regions.csv')



df = preprocess(df , region_df)


st.sidebar.title('Olympics Analysis')


user_menu = st.sidebar.radio(
    "Select an option",
    ("Medal Tally" , "Overall Analysis" , "Country-wise Analysis" , "Athelete-wise Analysis")
)


if user_menu == "Medal Tally":
    
    st.sidebar.header('Medal Tally')
    year,country = country_year_list(df)
    
    selected_year = st.sidebar.selectbox('Select Year' , year)
    selected_country = st.sidebar.selectbox('Select Country' , country)
    
    medal_tally = fetch_medal_tally(df , selected_year , selected_country)
    
    if selected_year=='Overall' and selected_country == 'Overall':
        st.title("Overall")
    if selected_year!='Overall' and selected_country == 'Overall':
        st.title("Medal Tally in" + " " +  str(selected_year))
    if selected_year=='Overall' and selected_country != 'Overall':
        st.title("Medal Tally of" + " " +  selected_country)
    if selected_year!='Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in" + " " +  str(selected_year))
      
    st.table(medal_tally) 
    
    
if user_menu == 'Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    countries=df['region'].unique().shape[0]
    
    st.title("Top Statistics")
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
        
    with col2:
        st.header("Hosts")
        st.title(cities)
        
    with col3:
        st.header("Sports")
        st.title(sports)
        
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
        
    with col2:
        st.header("Athletes")
        st.title(athletes)
        
    with col3:
        st.header("Nations")
        st.title(countries)
        
    # Nations participated over time    
    nations_over_time = data_over_time(df,'region')
    fig = px.line(nations_over_time , x='Year' , y='region')
    st.title("Participating nations over the years")
    st.plotly_chart(fig)
    
    # Events over time
    events_over_time = data_over_time(df,'Event')
    fig = px.line(events_over_time , x='Year' , y='Event')
    st.title("Number of Events over the years")
    st.plotly_chart(fig)
    
    # Athletes participated over time
    athletes_over_time = data_over_time(df,'Name')
    fig = px.line(athletes_over_time , x='Year' , y='Name')
    st.title("Participation of Athletes over the years")
    st.plotly_chart(fig)
    
    # Heatmap
    st.title("Number of Events over time(Each Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(subset=['Year' , 'Sport' , 'Event'])
    x=x.pivot_table(index='Sport' , columns='Year' , values = 'Event' , aggfunc='count').fillna(0).astype('int')
    ax = sns.heatmap(x , annot=True)
    st.pyplot(fig)
    
    # Most successfull athletes
    st.title("Most successfull Athletes")
         # select box
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    
    selected_sport = st.selectbox("Select a Sport" , sports_list)
    
    x=most_successfull(df , selected_sport)
    st.table(x)
    
    
if user_menu == 'Country-wise Analysis':
    
    st.sidebar.title("Country-wise Analysis")
    
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    
    selected_country = st.sidebar.selectbox("Select a country" , country_list)
    
    country_df = yearwise_medal_tally(df ,selected_country)
    fig = px.line(country_df , x='Year' , y='Medal')
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)
    
    # Heatmap
    st.title(selected_country + " Performance in different sports")
    x = country_sport_heatmap(df , selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(x , annot=True)
    st.pyplot(fig)
    
    # Top Athletes Countrywise
    st.title("Most successfull Athletes of " + selected_country)
    top10 = most_successfull_countrywise(df , selected_country)
    st.table(top10)