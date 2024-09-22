import pickle
import pandas as pd
import streamlit as st
import pickle

from streamlit import number_input

st.title('IPL')
teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Hyderabad', 'Pune', 'Indore', 'Bangalore', 'Mumbai', 'Kolkata',
       'Delhi', 'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town',
       'Port Elizabeth', 'Durban', 'Centurion', 'East London',
       'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad',
       'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Raipur',
       'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru']
pipe = pickle.load(open('pipe.pkl','rb'))
col1 , col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('select the batting teams',sorted(teams))


with col2:
    bowling_team = st.selectbox('select the bowling  teams',sorted(teams))

selected_city =  st.selectbox('select host city ',sorted(cities))

target = st.number_input('target',value=1)

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Score',value=1)

with col4:
    overs = st.number_input('Overs',value=1)
    if overs == 0:
        st.warning("You entered 0 for overs so run should also be zero. For calculation purposes,"
                   "Entering 0 can lead to undefined behavior in calculating rates, "
                   " Please ensure the input reflects the "
                   "actual overs bowled.")


with col5:
    wickets = st.number_input('Wickets')

if st.button('Predict Probability'):
  runs_left = target - score
  balls_left = 120 -(overs*6)
  wickets = 10 - wickets
  crr = score/overs
  rrr = (runs_left*6)/balls_left

  input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],
                'ball_left':[balls_left],'wickets':[wickets],
                'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

  st.table(input_df)

  result = pipe.predict_proba(input_df)
  loss = result[0][0]
  win = result[0][1]
  st.text(batting_team+"-"+str(round(win*100))+"%")
  st.text(bowling_team+"-"+str(round(loss*100))+"%")
