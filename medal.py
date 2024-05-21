import numpy as np
def medal_tally(olympic_df):
    medal_tally=olympic_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    return medal_tally

def  year(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')  #inserting an overall value at zeroth index of yars list.
    return years
def country(df):
    country=np.unique(df['region'].dropna().values).tolist() #dropping nan values from region feature.
    country.sort()
    country.insert(0,'Overall')
    return country


def fetch_medal_tally(df,year,country):
     medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
     flag=0
     if year=='Overall' and country=='Overall':
         temp_df=medal_df
     if year=='Overall' and country!='Overall':
         flag=1
         temp_df=medal_df[medal_df['region']==country]
     if year!='Overall' and country=='Overall':
         temp_df=medal_df[medal_df['Year']==year]
     if year!='Overall' and country!='Overall':
         temp_df=medal_df[(medal_df['Year']==year) & (medal_df['region']==country)]



     if flag==1:
        temp1_df=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
     else:
        temp1_df=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
     temp1_df['total']=temp1_df['Gold']+temp1_df['Silver']+temp1_df['Bronze']
     return temp1_df

def data_over_time(df,col):
    nations_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Edition','count':col},inplace=True)
    return nations_over_time

def most_successful_athletes(df, sport):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if specified
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals won by each athlete
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']

    # Merge with the original dataframe to get Sport and region
    merged_df = medal_counts.merge(df[['Name', 'Sport', 'region']], on='Name', how='left')

    # Drop duplicate rows based on 'Name'
    merged_df = merged_df.drop_duplicates(subset='Name')

    # Select the top 15 athletes
    top_athletes = merged_df.head(15)

    top_athletes= top_athletes[['Name', 'Medals', 'Sport', 'region']]
    return top_athletes

def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_wise_heatmap(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_athletes_countrywise(df,country):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if specified
    temp_df = temp_df[temp_df['region'] == country]

    # Count medals won by each athlete
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']

    # Merge with the original dataframe to get Sport and region
    merged_df = medal_counts.merge(df[['Name', 'Sport']], on='Name', how='left')

    # Drop duplicate rows based on 'Name'
    merged_df = merged_df.drop_duplicates(subset='Name')

    # Select the top 15 athletes
    top_athletes = merged_df.head(15)

    top_athletes= top_athletes[['Name', 'Medals', 'Sport']]
    return top_athletes

def height_vs_weight(df,sport):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    
def men_vs_women(df):
     athlete_df=df.drop_duplicates(subset=['Name','region'])
     men=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
     women=athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

     final=women.merge(men,on='Year',how='left')
     final.rename(columns={'Name_x':'Female','Name_y':'Male'},inplace=True)
     final.fillna(0,inplace=True)
     return final


