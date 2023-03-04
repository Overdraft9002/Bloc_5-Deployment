import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

## Set Config
st.set_page_config(
    page_title="Get around analysis",
    layout="wide"
)

st.title("Delay Analysis")

##APP

##Load Data
@st.cache
def load_data():
    data = pd.read_csv('get_around_delay_analysis_data_2.csv')
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")

#Raw data

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

##Plots with type of checkout, state

st.header('For 16276 reccorded reservations')

# First subplot
fig = make_subplots(rows=1, cols=2, subplot_titles=('Types of checkout', 'Status of reservation'))

# Type of chekout
fig1 = px.bar(data.checkin_type.value_counts(),  y=data.checkin_type.value_counts())

# Status of reservation
fig2 = px.bar(data.state.value_counts(), y=data.state.value_counts())

# Type of checkout
fig.add_trace(fig1['data'][0], row=1, col=1)
# Status of reservation 
fig.add_trace(fig2['data'][0], row=1, col=2)

st.plotly_chart(fig, use_container_width=True)

# View delay time only
df_delay = data[data.delay_at_checkout_in_minutes.notna()]

# function to remove outliers
def remove_outliers(df,column,n_std):
    mean = df[column].mean()
    sd = df[column].std()
        
    df = df[(df[column] <= mean+(n_std*sd))]
    df = df[(df[column] >= mean-(n_std*sd))]
        
    return df

# Apply function
df_delay = remove_outliers(df_delay, 'delay_at_checkout_in_minutes', 2)
# dislay line chart for delay at checkout
# Graph with two standard deviations
fig2 = px.line(df_delay, y=df_delay.delay_at_checkout_in_minutes.sort_values(), title='Delay at checkout', labels= {"y" : "Delay in minutes", "index":"number of instances"})
st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2, gap="large")
# Display mean and median delay
with col1:
    st.metric(label="mean delay", value=df_delay.delay_at_checkout_in_minutes.mean(), delta=-0.5, delta_color="inverse")
with col2:
    st.metric(label="median delay", value=df_delay.delay_at_checkout_in_minutes.median(), delta=-0.5, delta_color="inverse")

# Create dataset to to study correlation of features
corr_data = data.copy()
corr_data.state = corr_data.state.map({'canceled':1, 'ended':0})
corr_data.checkin_type = corr_data.checkin_type.map({'connect':1, 'mobile':0 })
del corr_data['Unnamed: 0']

# Form to view correlation between features
with st.form("Study correlations for different columns in dataframe"):
    col_1_name = st.selectbox("Select first feature ", corr_data.columns)
    col_2_name = st.selectbox("Select second feature ", corr_data.columns)
    submit = st.form_submit_button("submit")
    if submit:
        col_1 = corr_data[col_1_name]
        col_2 = corr_data[col_2_name]
        correlation = col_1.corr(col_2)
        st.metric("Correlation with both features", round(correlation,3))