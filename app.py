import streamlit as st
import pandas as pd
import Preprocessor,medal
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

olympic_df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
st.sidebar.header('Olympics Analysis')


df=Preprocessor.preprocess(olympic_df,region_df)

user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country wise Analysis', 'Athlete wise Analysis')
)
if user_menu=='Medal Tally':
         st.sidebar.header('Medal Tally')
         years= medal.year(df)
         country = medal.country(df)

         selected_year = st.sidebar.selectbox("Select Year",years)
         selected_country = st.sidebar.selectbox("Select Country",country)
         medal_tally=  medal.fetch_medal_tally(df,selected_year,selected_country)
         if selected_year=='Overall' and selected_country=='Overall':
            st.title('Overall Tally')
         elif selected_year!='Overall' and selected_country=='Overall':
            st.title('Medal Tally in'+selected_year+' Olympics ')
         elif selected_year=='Overall' and selected_country!='Overall':
            st.title('Medal Tally for'+selected_country+' Olympics ')
         elif selected_year!='Overall' and selected_country!='Overall':
            st.title('Medal Tally for'+selected_country+'in'+selected_year+'Olympics')
        

         st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions=df['Year'].unique().shape[0]
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title('Overall Analysis')

    col1,col2,col3 =st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col4,col5,col6 =st.columns(3)
    with col4:
        st.header('Events')
        st.title(events)
    with col5:
        st.header('Nations')
        st.title(nations)
    with col6:
        st.header('Athletes')
        st.title(athletes)


    nations_over_time= medal.data_over_time(df,'region')
    st.title('Participating Nations over the Years')
    fig1=px.line(nations_over_time,x='Edition',y='region')
    st.plotly_chart(fig1)

    
    events_over_time= medal.data_over_time(df,'Event')
    st.title('Number of Events emerging over the Years')
    fig2=px.line(events_over_time,x='Edition',y='Event')
    st.plotly_chart(fig2)


    athletes_over_time= medal.data_over_time(df,'Name')
    st.title('Participation of Athletes over the Years')
    fig3=px.line(athletes_over_time,x='Edition',y='Name')
    st.plotly_chart(fig3)


    st.title('Most Successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    x=medal.most_successful_athletes(df,selected_sport)
    st.table(x)

if user_menu=='Country wise Analysis':
        st.sidebar.title('Country-wise Analysis')
        country_list=df['region'].dropna().unique().tolist()
        country_list.sort()
        selected_country=st.sidebar.selectbox('Select a country',country_list)



        country_df=medal.yearwise_medal_tally(df,selected_country)
        st.title ('Medal Tally for '+selected_country)
        st.table(country_df)
        st.title('Line Chart Analysis for '+selected_country)
        fig4=px.line(country_df,x='Year',y='Medal')
        st.plotly_chart(fig4)



        st.title('Heatmap Visualisation for '+selected_country)
        pt=medal.country_wise_heatmap(df,selected_country)
        fig5 ,heat= plt.subplots(figsize=(20,20))
        ax=sns.heatmap(pt,annot=True)
        st.pyplot(fig5)

        top_athletes=medal.most_successful_athletes_countrywise(df,selected_country)
        st.title('Top 15 Athletes of '+selected_country)
        st.table(top_athletes)

if user_menu=='Athlete wise Analysis':
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()


    
    fig1=ff.create_distplot([x1,x2,x3,x4],['Overall','Gold','Silver','Bronze'],show_hist=False,show_rug=False)
    fig1.update_layout(autosize=False,width=700,height=500)
    st.title('Distplot for Age-wise Medal Distribution')
    st.write('This plot indicates the probability of wining a medal at a particular age')
    st.plotly_chart(fig1)


    
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    temp1_df=medal.height_vs_weight(df,selected_sport)
    fig3,ax1=plt.subplots(figsize=(12,15))
    ax1 = sns.scatterplot(data=temp1_df, x='Weight', y='Height', hue='Medal', style='Sex', s=50)
    st.pyplot(fig3)
    st.write('This plot depicts the medal won by diffrent athletes with diffrent height and weight this helps us analyise accurate height and weight required for a particular sport to win medal')


    st.title('Men Vs Women')
    st.write('This plot is for depicting the probablity of winning a medal be it gold,silver or bronze for a male as well as a female athlete')
    temp2_df=medal.men_vs_women(df)
    fig=px.line(temp2_df,x='Year',y=['Male','Female'])
    fig1.update_layout(autosize=False,width=700,height=500)
    st.plotly_chart(fig1)

    


    
    
       
        