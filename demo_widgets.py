import streamlit as st
import datetime

st.set_page_config(page_title='Widgets Demo', layout='wide')
st.title('Input Widgets')
st.write('Every widget returns a value you can use directly in Python.')
st.divider()

st.subheader('st.date_input()')
cutoff = st.date_input(
    'Select a cutoff date',
    value=datetime.date(2014, 1, 15),
    min_value=datetime.date(2013, 1, 1),
    max_value=datetime.date(2014, 3, 31),
    help='The forecast starts from the day after this date.'
)
st.write(f'You picked: {cutoff}')
st.divider()

st.subheader('st.slider()')
n_days = st.slider('Days to forecast?', min_value=1, max_value=30, value=7)
st.write(f'Forecasting {n_days} days ahead.')
st.divider()

st.subheader('st.selectbox()')
model = st.selectbox(
    'Choose a forecasting model',
    options=['ARIMA', 'Holt-Winters', 'Prophet', 'XGBoost'],
    help='Each model uses a different approach.'
)
st.write(f'You selected: {model}')
st.divider()

st.subheader('st.radio()')
metric = st.radio('Which metric to prioritise?', ['MAE', 'RMSE', 'MAPE'], horizontal=True)
st.write(f'Prioritising: {metric}')
st.divider()

st.subheader('st.checkbox()')
show = st.checkbox('Show residuals chart', value=False)
st.write('Chart would appear here.' if show else 'Tick the box to show it.')
st.divider()

st.subheader('st.button()')
if st.button('Run Forecast', type='primary'):
    st.success(f'Running {model} for {n_days} days from {cutoff}!')
else:
    st.write('Click the button above to trigger an action.')
