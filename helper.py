def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team' , 'NOC' , 'Games' ,'City' , 'Sport' ,'Event', 'Medal'])
    
    
    medal_tally=medal_tally.groupby('region').sum()[['Gold' , 'Silver' , 'Bronze']].sort_values(by='Gold' , ascending=False).reset_index()
    
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    
    return medal_tally

#***************************************************************************************************************

def country_year_list(df):
    
    year=df['Year'].unique().tolist()
    year.sort()
    year.insert(0 , 'Overall')
    
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0,'Overall')
    
    return year,country

#***************************************************************************************************************

def fetch_medal_tally(df , year , country):
    
    medal_df = df.drop_duplicates(subset=['Team' , 'NOC' , 'Games' ,'City' , 'Sport' ,'Event', 'Medal'])
    flag=0
    
    # For overall medal tally
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    
    # Performance of a country in all years
    if year == 'Overall' and country != 'Overall':
        flag=1
        temp_df = medal_df[medal_df['region'] == country]
    
    # Performance of all countries in a particular year
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    
    # Performance of a particular country in a particular year
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
        
    
    if flag==1:
        X = temp_df.groupby('Year').sum()[['Gold' , 'Silver' , 'Bronze']].sort_values(by='Year' , ascending=True).reset_index()
    else:
        X = temp_df.groupby('region').sum()[['Gold' , 'Silver' , 'Bronze']].sort_values(by='Gold' , ascending=False).reset_index()
        
    X['Total'] = X['Gold'] + X['Silver'] + X['Bronze']
    
    return X

#***************************************************************************************************************

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(subset=['Year' , col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index':'Year' , 'Year':col} , inplace=True)
    
    return nations_over_time

#***************************************************************************************************************
def most_successfull(df , sport):
    temp_df = df.dropna(subset=['Medal'])
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
        
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df , left_on='index' , right_on='Name' , how='left')[['index' , 'Name_x' , 'region' , 'Sport']].drop_duplicates('index')
    x.rename(columns={'index':'Name' , 'Name_x':'Medals' , 'region':'region'} , inplace=True)
    return x

#***************************************************************************************************************

def yearwise_medal_tally(df , country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team' , 'NOC' , 'Games' , 'Year' , 'City' , 'Sport' , 'Event' , 'Medal'])
    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year')['Medal'].count().reset_index()
    
    return final_df

#***************************************************************************************************************
def country_sport_heatmap(df , country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team' , 'NOC' , 'Games' , 'Year' , 'City' , 'Sport' , 'Event' , 'Medal'])
    new_df = temp_df[temp_df['region']==country]
    x = new_df.pivot_table(index='Sport' , columns='Year' , values='Medal' , aggfunc='count').fillna(0)
    
    return x

#***************************************************************************************************************
def most_successfull_countrywise(df , country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]
        
    x=temp_df['Name'].value_counts().reset_index().head(10).merge(df , left_on='index' , right_on='Name' , how='left')[['index' , 'Name_x' , 'Sport']].drop_duplicates('index')
    x.rename(columns={'index':'Name' , 'Name_x':'Medals'} , inplace=True)
    return x