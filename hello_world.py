import streamlit as st
import pandas as pd
import numpy as np

# ── Title and introduction ────────────────────────────────────
st.title("Hello, Streamlit!")
st.write("This is your first Streamlit app. Every line of Python you already know works here.")

# ── A simple text display ─────────────────────────────────────
st.header("1. Displaying text")
st.write("Use st.write() to show text, numbers, or tables.")
st.write("Today we are building a forecasting app step by step.")

# ── A date input widget ───────────────────────────────────────
st.header("2. Getting input from the user")
selected_date = st.date_input("Pick a date")
st.write(f"You selected: {selected_date}")

# ── A selectbox ───────────────────────────────────────────────
model_choice = st.selectbox("Choose a model", ["XGBoost", "ARIMA", "Prophet", "Holt-Winters"])
st.write(f"You chose: {model_choice}")

# ── A slider ─────────────────────────────────────────────────
days_ahead = st.slider("How many days to forecast?", min_value=1, max_value=30, value=7)
st.write(f"Forecasting {days_ahead} days ahead.")

# ── A button ─────────────────────────────────────────────────
st.header("3. Buttons and actions")
if st.button("Click me"):
    st.success("Button clicked! In the real app, this will run the forecast.")

# ── A simple chart ────────────────────────────────────────────
st.header("4. Charts")
sample_data = pd.DataFrame({
    "Day":   range(1, 31),
    "Sales": np.random.randint(300, 700, 30)
}).set_index("Day")

st.line_chart(sample_data)
st.write("This is a placeholder chart. On Day 3 it will show real forecast data.")
