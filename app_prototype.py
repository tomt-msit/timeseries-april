# Retail Sales Forecasting App - Upgrade C: Model selection (final version)
# Run: python -m streamlit run app_prototype.py
# STOP the app (Ctrl+C) and restart it after running this cell.

import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

PROJECT_DIR = r'C:\\Users\\tthem\\timeseries-april'
DATA_DIR    = os.path.join(PROJECT_DIR, 'data')
MODELS_DIR  = os.path.join(PROJECT_DIR, 'models')
FEATURES = [
    'year','month','day','dayofweek','quarter','week_of_year',
    'is_weekend','is_month_start','is_month_end',
    'lag_1','lag_7','lag_14','lag_30',
    'rolling_7d_mean','rolling_14d_mean','rolling_30d_mean','rolling_7d_std',
    'dcoilwtico','oil_lag_1','oil_rolling_7d_mean',
    'is_national_holiday','is_regional_holiday','is_local_holiday',
]
TARGET     = 'unit_sales'
SPLIT_DATE = '2014-01-01'

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, 'timeseries_with_features.csv'))
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date').set_index('date').dropna()

@st.cache_resource
def load_xgb_model():
    pkl = os.path.join(MODELS_DIR, 'best_model.pkl')
    return joblib.load(pkl) if os.path.exists(pkl) else None

def train_model(choice, df_train, df_test):
    "Train the chosen model. Returns (test_predictions, trained_model)."
    if choice == 'ARIMA':
        m   = SARIMAX(df_train[TARGET], order=(1,1,1), seasonal_order=(1,1,1,7))
        fit = m.fit(disp=False)
        return fit.forecast(steps=len(df_test)).values, fit
    elif choice == 'Holt-Winters':
        m   = ExponentialSmoothing(df_train[TARGET], trend='add',
                                   seasonal='add', seasonal_periods=7)
        fit = m.fit()
        return fit.forecast(len(df_test)).values, fit
    elif choice == 'Prophet':
        pt = df_train[[TARGET]].reset_index().rename(columns={'date':'ds',TARGET:'y'})
        te = df_test[[TARGET]].reset_index().rename(columns={'date':'ds',TARGET:'y'})
        m  = Prophet(weekly_seasonality=True, yearly_seasonality=True)
        m.fit(pt)
        fo = m.predict(m.make_future_dataframe(periods=len(te), freq='D'))
        return fo['yhat'].values[-len(te):], m
    else:
        m     = load_xgb_model()
        preds = m.predict(df_test[FEATURES])
        return preds, m

def make_forecast(df, model, features, cutoff_date, n_days=1):
    cutoff = pd.to_datetime(cutoff_date)
    mt = type(model).__name__
    if 'SARIMAXResults' in mt or 'ARIMAResults' in mt:
        p = model.forecast(steps=n_days)
        return pd.DataFrame([{'date':cutoff+pd.Timedelta(days=i+1),
            'forecast':round(float(max(0,v)),2)} for i,v in enumerate(p)]).set_index('date')
    elif 'HoltWinters' in mt or 'ExponentialSmoothing' in mt:
        p = model.forecast(n_days)
        return pd.DataFrame([{'date':cutoff+pd.Timedelta(days=i+1),
            'forecast':round(float(max(0,v)),2)} for i,v in enumerate(p)]).set_index('date')
    elif 'Prophet' in mt:
        fd = pd.date_range(start=cutoff+pd.Timedelta(days=1), periods=n_days, freq='D')
        fo = model.predict(pd.DataFrame({'ds': fd}))
        return pd.DataFrame([{'date':r['ds'],'forecast':round(float(max(0,r['yhat'])),2)}
            for _,r in fo.iterrows()]).set_index('date')
    else:
        h, fc = df.loc[df.index <= cutoff].copy(), []
        for i in range(n_days):
            nd  = cutoff + pd.Timedelta(days=i+1)
            row = df.loc[[nd],features] if nd in df.index else h.iloc[[-1]][features].copy()
            row.index = [nd]
            fc.append({'date':nd,'forecast':round(float(max(0,model.predict(row)[0])),2)})
        return pd.DataFrame(fc).set_index('date')

def calc_metrics(actual, predicted):
    a, p = np.array(actual), np.array(predicted)
    mae  = mean_absolute_error(a, p)
    rmse = np.sqrt(mean_squared_error(a, p))
    bias = np.mean(p - a)
    r2   = r2_score(a, p)
    mask = a != 0
    mape = np.mean(np.abs((a[mask]-p[mask])/a[mask]))*100
    return {'MAE':round(mae,2),'RMSE':round(rmse,2),
            'MAPE':round(mape,1),'Bias':round(bias,2),'R2':round(r2,3)}

st.set_page_config(page_title='Sales Forecast', layout='wide')
st.title('Retail Sales Forecasting')
st.write('Corporacion Favorita - Guayas region')

st.sidebar.header('Forecast settings')
model_choice = st.sidebar.selectbox(
    'Choose a model',
    options=['XGBoost', 'ARIMA', 'Holt-Winters', 'Prophet'],
    help='XGBoost loads the pre-trained model instantly. Others retrain live (10-60 sec).')
cutoff_date  = st.sidebar.date_input('Cutoff date', value=date(2014,1,15),
    min_value=date(2013,6,1), max_value=date(2014,3,30),
    help='Forecast starts the day after this date.')
n_days       = st.sidebar.slider('Days to forecast', 1, 30, 7)
history_days = st.sidebar.slider('History days to show', 14, 120, 60)
run_button   = st.sidebar.button('Run Forecast', type='primary')

if run_button:
    with st.spinner(f'Training {model_choice} and generating forecast...'):
        df       = load_data()
        split    = pd.to_datetime(SPLIT_DATE)
        cutoff   = pd.to_datetime(cutoff_date)
        df_train = df.loc[df.index < split]
        df_test  = df.loc[df.index >= split]
        test_preds, trained_model = train_model(model_choice, df_train, df_test)
        history_plot = df.loc[
            (df.index >= cutoff-pd.Timedelta(days=history_days)) &
            (df.index <= cutoff)][TARGET]
        forecast_df = make_forecast(df, trained_model, FEATURES, cutoff, n_days)

    st.success(f'{model_choice} ready!')

    fig, ax = plt.subplots(figsize=(13,4))
    ax.plot(history_plot.index, history_plot.values,
            label='Historical', color='steelblue', linewidth=1.5)
    ax.plot(forecast_df.index, forecast_df['forecast'].values,
            label=f'{n_days}-day forecast', color='orange',
            linestyle='--', linewidth=2, marker='o', markersize=4)
    ax.axvline(cutoff, color='red', linestyle=':', linewidth=1.5, label='Cutoff')
    ax.set_title(f'{model_choice} Forecast from {cutoff.date()}')
    ax.set_ylabel('Unit Sales')
    ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader('Forecast values')
    st.dataframe(forecast_df.reset_index().rename(
        columns={'date':'Date','forecast':'Predicted Sales'}))
    st.download_button('Download forecast as CSV',
        forecast_df.reset_index().to_csv(index=False),
        file_name=f'forecast_{model_choice}_{cutoff_date}.csv', mime='text/csv')

    st.divider()
    st.subheader('Evaluation metrics')
    st.write(f'How well {model_choice} fitted the test period (Jan-Mar 2014).')
    m = calc_metrics(df_test[TARGET].values, test_preds)
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric('MAE',  m['MAE'],  help='Average error. Lower is better.')
    c2.metric('RMSE', m['RMSE'], help='Penalises large errors. Lower is better.')
    c3.metric('MAPE', f"{m['MAPE']}%", help='Error as %. Under 20% is strong.')
    c4.metric('Bias', m['Bias'], help='+ = over-predicting. Target: 0.')
    c5.metric('R2',   m['R2'],   help='Closer to 1.0 is better.')

    st.divider()
    st.subheader('Residuals chart')
    st.write('Residuals = actual minus predicted. Randomly scattered around zero is good.')
    residuals = df_test[TARGET].values - test_preds
    colours   = ['coral' if r < 0 else 'steelblue' for r in residuals]
    fig2, ax2 = plt.subplots(figsize=(13, 3))
    ax2.bar(df_test.index, residuals, color=colours, alpha=0.75)
    ax2.axhline(0, color='black', linewidth=1)
    ax2.set_title('Residuals - Actual minus Predicted')
    ax2.set_ylabel('Residual (units)')
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2)
    st.caption('Blue = model over-predicted. Coral = model under-predicted.')

else:
    st.info('Choose a model in the sidebar and click Run Forecast.')
    st.write('**Data range:** January 2013 - March 2014')
    st.write('XGBoost loads instantly. ARIMA, Holt-Winters, Prophet retrain live (10-60 sec).')