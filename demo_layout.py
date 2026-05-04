import streamlit as st

st.set_page_config(page_title='Layout Demo', layout='wide')

# always first
# Text hierarchy
st.title('st.title() - the biggest heading')
st.header('st.header() - section heading')
st.subheader('st.subheader() - smaller heading')
st.write('st.write() - displays text, numbers, DataFrames, or charts')
st.caption('st.caption() - small grey text, good for footnotes')
st.divider()  # draws a horizontal line

# Columns - place content side by side
st.subheader('st.columns() - side by side layout')
col1, col2, col3 = st.columns(3)
col1.metric('MAE', '95.6', help='Mean Absolute Error - lower is better')
col2.metric('RMSE', '141.8', help='Root Mean Squared Error')
col3.metric('R2', '0.402', help='R-squared - closer to 1.0 is better')
st.divider()

# Expander - collapsible section
st.subheader('st.expander() - collapsible section')
with st.expander('Click to see more details'):
    st.write('This content is hidden until the user clicks.')
    st.write('Useful for optional information that would clutter the page.')
st.divider()

# Tabs - multiple views in one panel
st.subheader('st.tabs() - tabbed layout')
tab1, tab2 = st.tabs(['Chart view', 'Table view'])
sample = pd.DataFrame({'Sales': np.random.randint(300, 700, 14)})
with tab1:
    st.line_chart(sample)
with tab2:
    st.dataframe(sample)
