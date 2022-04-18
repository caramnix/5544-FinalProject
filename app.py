


# Application for CSE 5544 Final Project 

import pandas as pd 
import numpy as np 
import altair as alt 
import streamlit as st 
from datetime import datetime
from vega_datasets import data

st.set_page_config(
    layout= "wide"
)

st.markdown("<div style='background:#e6e6e6'><h3 style='font-weight:bold; color:#ec4420'>  Gun Violence in the United States, 1965-2021</h3></div>", unsafe_allow_html=True)

df_data = pd.read_csv("https://raw.githubusercontent.com/caramnix/CSE-5544/main/Final%20Project/data_geospatial.csv")
df_data['Year'] = df_data['Year'].astype(int)

#df_data

race_dictionary = {
   'category' : 'Race',
   '0.0' : 'White',
   '1.0' : 'Black',
   '2.0' : 'Latinx',
   '3.0' : 'Asian',
   '4.0' : 'Middle Eastern',
   '5.0' : 'Native American',
   '6.0' : 'Other',
   'nan' : 'No Information'
}

religion_dictionary = {
   'category' : 'Relgion',
   '0.0' : 'None',
   '1.0' : 'Christian',
   '2.0' : 'Muslim',
   '3.0' : 'Buddhist',
   '4.0' : 'Atheist',
   '5.0' : 'Cultural/ Spirituality',
   '6.0' : 'Jewish',
   'nan' : 'No Information' 
}

# Education column seems to create an index of ints, not floats like other 2
education_dictionary = {
   'category' : 'Education',
   '0' : 'Less than High School',
   '1' : 'High School/ GED',
   '2' : 'Some college/ trade school',
   '3' : 'Bachelor\'s degree',
   '4' : 'Graduate School',
   'nan' : 'No Information',
   ' ' : 'Unknown'
}

def create_pie_df(df, race_dictionary, education_dictionary, religion_dictionary):
  
  # create race df
  race_counts = df['Race'].value_counts(dropna=False) # get counts of each value 
  df_race = pd.DataFrame(race_counts) # turn to df
  df_race.reset_index(inplace=True) # shift index over to column
  df_race['index'] = df_race['index'].astype(str) 
  df_race.replace({"index": race_dictionary}, inplace=True) # replace index values with categorical values from dictionary
  df_race.rename(columns={"Race": "Race_counts", "index": "Race"}, inplace=True)

  # create education df
  Education_counts = df['Education'].value_counts(dropna=False)
  df_Education = pd.DataFrame(Education_counts)
  df_Education.reset_index(inplace=True)
  df_Education['index'] = df_Education['index'].astype(str)
  df_Education.replace({"index": education_dictionary}, inplace=True)
  df_Education.rename(columns={"Education": "Education_counts", "index": "Education"}, inplace=True)


  # create religion df
  Religion_counts = df['Religion'].value_counts(dropna=False)
  df_Religion = pd.DataFrame(Religion_counts)
  df_Religion.reset_index(inplace=True)
  df_Religion['index'] = df_Religion['index'].astype(str)
  df_Religion.replace({"index": religion_dictionary}, inplace=True)
  df_Religion.rename(columns={"Religion": "Religion_counts", "index": "Religion"}, inplace=True)

  return df_race, df_Education, df_Religion

r_= ['#4c78a8', '#f58518','#ec4420', '#72b7b2', '#54a24b', '#eeca3b', '#b279a2','#ff9da6', '#9d755d', '#bab0ac'] 

from datetime import time

gun_panel = st.container() 
with gun_panel:
    columns= st.columns([3, .2, 2, 5])
    with columns[0]: 
        start_time= st.slider("Select Range of Years:",
                1965, 2021, (2000, 2021))
        #start_time
        min_year = start_time[0]
        max_year = start_time[1]
        current_data= df_data.loc[df_data['Year'] >= min_year] 
        current_data= current_data.loc[current_data['Year'] <= max_year] 
    #current_data 

    chart1, chart2, chart3 = st.columns([5,2,2])

    airports = data.airports.url
    states = alt.topo_feature(data.us_10m.url, feature='states')

    with chart1: 
        background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
        #).properties(
        #width=500,
        #height=300
        ).project('albersUsa')
   
        base = alt.Chart(current_data).encode(
            longitude='longitude:Q',
            latitude='latitude:Q'
        )
        points = base.mark_circle(opacity=0.3).encode(
            color=alt.value('#ec4420'),
            size=alt.Size('Number of Victims:Q', title='Number of Victims'),
            tooltip=['location:N', 'Full Date', 'Number of Victims']
        )
        st.altair_chart(background + points, use_container_width=True)
   
    df_race, df_Education, df_Religion = create_pie_df(current_data, race_dictionary, education_dictionary, religion_dictionary)
    with chart2: 
  
        # Race
        race_dictionary.pop("category")
        d_ = np.sort(list(race_dictionary.values())) #np.sort(np.unique(df_race["Race"]))
        race_chart= alt.Chart(df_race).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Race_counts",  type="quantitative"),
            
            color=alt.Color(field="Race", type="nominal", scale=alt.Scale(domain=d_, range=r_[0:len(d_)])),
            tooltip=["Race", "Race_counts"],
            opacity=alt.value(0.7),
        ).properties(title = 'Race Profile'
        ).configure_view(
            strokeWidth=0
        )

        st.altair_chart(race_chart, use_container_width=True)
    with chart3: 
        # Religion
        religion_dictionary.pop("category")
        d_ = np.sort(list(religion_dictionary.values())) #np.sort(np.unique(df_Religion["Religion"]))
        relig_chart= alt.Chart(df_Religion).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Religion_counts",  type="quantitative"),
            color=alt.Color(field="Religion", type="nominal", scale=alt.Scale(domain=d_, range=r_[0:len(d_)])),
            tooltip=["Religion", "Religion_counts"],
            opacity=alt.value(0.7),
        ).properties(title = 'Religion Profile'
        ).configure_view(
            strokeWidth=0
        )
        
        st.altair_chart(relig_chart, use_container_width=True)

gun_row2 = st.container()

with gun_row2:

    columns = st.columns([4, 1, 1.5, 2.5])
    with columns[1]: 
        timespan = columns[1].radio(
            'Display',
            ('Number of Victims', 'Number of Shootings')
            )

    with columns[0]:

        if timespan == 'Number of Victims':
            input= 'sum(Number of Victims)'
            t= "Number of Victims"
        else:
            input = 'sum(Shooting)' 
            t= "Number of Shootings"
            
        bar_graph= alt.Chart(df_data).mark_bar().encode(
            x='Year:O',
             y=alt.Y(input, title=t),
            tooltip=[alt.Tooltip(input, title= t)]
        ).configure_bar(
         opacity=.7,
        color='#ec4420'
        )
        st.altair_chart(bar_graph,  use_container_width=True)

    with columns[2]: 
        victim= alt.Chart(current_data).mark_bar().encode(
            #x='Relationship with Other Shooting(s)',
            y = alt.Y('count(Relationship with Other Shooting(s))', title=" ", axis=None),
            color=alt.Color(field="Relationship with Other Shooting(s)", type="nominal", legend=alt.Legend(title='Shooter Relationship'), scale=alt.Scale(scheme='set1')),
            tooltip=[alt.Tooltip("count(Relationship with Other Shooting(s))", title='Count')],
            opacity=alt.value(0.8),
        ).configure_view(strokeOpacity=0)
        st.altair_chart(victim, use_container_width = True)

    with columns[3]:
        # Education
        education_dictionary.pop("category")
        d_ =  np.sort(list(education_dictionary.values())) #np.sort(np.unique(df_Education["Education"]))
        ed_chart= alt.Chart(df_Education).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Education_counts",  type="quantitative"),
            color=alt.Color(field="Education", type="nominal", scale=alt.Scale(domain=d_, range=r_[0:len(d_)])),
            tooltip=["Education", "Education_counts"],
            opacity=alt.value(0.7),
        ).properties(title = 'Education Profile'
        ).configure_view(
            strokeWidth=0
        )

        st.altair_chart(ed_chart, use_container_width=True) 


st.caption("Data from [The Violence Project](https://www.theviolenceproject.org/)")