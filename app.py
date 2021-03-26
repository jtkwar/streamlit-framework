import pandas as pd
import streamlit as st
import plotly.express as px
import json
#import python-dotenv
import requests

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
          'Jun', 'Jul', 'Aug', 'Sept',
          'Oct', 'Nov', 'Dec']
months_dict = {'Jan': "01", 'Feb': "02", 'Mar': "03", 'Apr': "04", 'May': "05",
               'Jun': "06", 'Jul': "07", 'Aug': "08", 'Sept': "09",
               'Oct': "10", 'Nov': "11", 'Dec': "12"}
def extract_Data(symbol):
    URL = "https://www.alphavantage.co/query"
    KEY = "JQOC3O5PWQ6PAF2S"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "full",
        "apikey": KEY}
    r = requests.get(URL, params=params)
    return(r)
@st.cache
def JSON_to_df(data, columns=['Open', 'High', 'Low', 'Close', 'Volume']):
    def conv_JSON(d):
        """
        Convert json string into DateTime records for selected stock
        json object is parsed by Pandas
        """
        for dt, prec in d['Time Series (Daily)'].items():
            r = { 'DateTime': dt}
            r.update(prec)
            yield r

    # pass your json string in and conv to DataFrame
    df = pd.DataFrame(conv_JSON(data))
    # Rename Columns    
    df = df.rename(columns={'1. open': 'Open',
                            '2. high': 'High',
                            '3. low': 'Low',
                            '4. close': 'Close',
                            '5. volume': 'Volume'})
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.set_index('DateTime', inplace=True, drop=True)
    df.sort_index(inplace=True)
    df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].apply(pd.to_numeric)
    # extract the default columns
    df = df[columns]
    return df


st.title("The Data Incubator Spring Cohort 2021 Milestone Project")
st.sidebar.header("Input Plot Parameters")
user_input = st.sidebar.text_input('Ticker (e.g. AAPL for Apple, Inc.)')
year = st.sidebar.selectbox('Select Year', list(range(2010,2022,1)))
month = st.sidebar.selectbox('Select Month', months)

try:
    data = extract_Data(user_input)
except ValueError:
    st.error("Please enter a valid ticker.")


df = JSON_to_df(data.json())
st.header("Queried Data")
selection = str(year) + "-"  + months_dict[month]
st.dataframe(df.loc[selection])

df1 = df.loc[selection]
df1["Close"] = pd.to_numeric(df["Close"])
#df1.reset_index(drop=True)
st.header("Line Chart of Queried Data")
f = px.line(df1, x=df1.index, y="Close",
            title='{0} Close Prices: {1} {2}'.format(user_input, month, year))
f.update_xaxes(title="Date")
f.update_yaxes(title="Close Price")
f.update_traces(mode='markers+lines')
st.plotly_chart(f)