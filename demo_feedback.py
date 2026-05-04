import streamlit as st
import time
st.set_page_config(page_title='Feedback Demo')
st.title('Feedback and Status Components')
st.divider()
# Coloured message boxes
st.subheader('Message boxes')
st.info('st.info() - blue box for general information')
st.success('st.success() - green box for success')
st.warning('st.warning() - yellow box for caution')
st.error('st.error() - red box for errors')
st.divider()
# Spinner
st.subheader('st.spinner() - loading indicator')
if st.button('Simulate model training'):
    with st.spinner('Training model - please wait...'):
        time.sleep(2)
        st.success('Model trained!')
st.divider()
# Progress bar
st.subheader('st.progress() - step by step progress')
if st.button('Show progress bar'):
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        bar.progress(i + 1)
    st.success('Complete!')
st.divider()
# Metric with delta arrow
st.subheader('st.metric() with delta - shows change')
col1, col2, col3 = st.columns(3)
col1.metric('MAE',  '95.6',  delta='-12.4', help='Lower is better - green delta is good')
col2.metric('RMSE', '141.8', delta='-29.6')
col3.metric('R2',   '0.402', delta='+0.123', help='Higher is better - green delta is good')
st.caption('Green delta = improvement. delta_color="inverse" flips the colour logic.')