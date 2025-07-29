import numpy as np
import pickle
import streamlit as st
import mysql.connector
import pandas as pd

# Creating prediction function
filename1 = 'scaler_model.sav'
filename = 'regression_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
loaded_scaler=pickle.load(open(filename1,'rb'))
def prediction(data):
    input_data=np.array(data)
    reshaped=input_data.reshape(1,-1)
    log_np=np.log1p(reshaped)
    scal=loaded_scaler.transform(log_np)
    predict1=loaded_model.predict(scal)
    return np.expm1(predict1)    

def get_data(query, params=None):
    # Establish connection to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",        # Replace with your host
        user="root",    # Replace with your username
        password="Prabhudhas@1",# Replace with your password
        database="crop_production_data"    # Replace with your database name
    )
    
    # Execute the query with or without parameters
    if params:
        df = pd.read_sql(query, conn, params=params)
    else:
        df = pd.read_sql(query, conn)
    # Close the connection
    conn.close()
    
    return df

st.set_page_config(page_title="Crop production prediction", layout="wide")
html_temp="""<div style="background-color:#706C26;padding:10px">
                <h2 style="color:white;text-align:center;">streamlit Crop Production Prediction ML App</h2>
                </div>
                """
st.markdown(html_temp,unsafe_allow_html=True)
st.sidebar.title("Filters")
query11="""SELECT DISTINCT Area
            FROM crop_data
            ORDER BY Area ASC;"""
country=st.sidebar.selectbox("Select Country",get_data(query11))
query12="""SELECT DISTINCT Element
            FROM crop_data
            ORDER BY Element;
"""
element=st.sidebar.selectbox("Select Element",get_data(query12))
query13="""SELECT DISTINCT Item
            FROM crop_data
            ORDER BY Item ASC;
"""
Item=st.sidebar.selectbox("Select Item",get_data(query13))
range1=st.sidebar.slider("Value Range",0,100000,100)
Filter1=st.sidebar.button("Apply Filter")
st.markdown("""
    <style>
    /* Tabs container */
    .stTabs {
        display: flex;
        justify-content: center;
    }

    /* All tab styles */
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 6px;
        padding: 30px 80px;
        margin-right: 50px;
        font-size: 18px;
        font-weight: 600;              /* Bold */
        font-style: italic;            /* Italic */
        font-family: 'Segoe UI', sans-serif;  /* Font family */
        text-transform: uppercase;     /* Make text uppercase */
        color: #333333;
    }

    /* Selected tab style */
    .stTabs [aria-selected="true"] {
        background-color: #2c7be5;
        color: white;
        font-weight: 700;
        font-style: normal;
    }
    </style>
    """, unsafe_allow_html=True)
tab1,tab2=st.tabs(["🏚️Home","🔍Prediction"])
with tab1:
    if Filter1:
        filter_query="""SELECT Area,Element,Year,Item,Value,Unit,Flag,Flag Description
                        FROM crop_data
                        WHERE Area=%s AND Element=%s AND Item=%s AND Value<=%s;"""
        st.table(get_data(filter_query,params=(country,element,Item,range1,)))
    else:

        st.markdown(f"""<h2 style="color: #706C26; font-size: 36px;">CROP PRODUCTION</h2>
                        <p style="font-size:18px; font-family: 'Segoe UI', sans-serif;word-spacing: 15px font-style: italic;"> &nbsp;&nbsp;&nbsp;Crop production prediction, also known as crop yield prediction, is the process of forecasting the amount of crops that will be harvested from a specific area during a particular season. It's a crucial application in agriculture that helps farmers, governments, and businesses make informed decisions about resource allocation, risk management, and market strategies. This prediction relies on analyzing various factors and employing sophisticated models. 
                        </p>
                        <p style="color: #706C26; font-size: 36px;">Factors Influencing Yield:</p>
                            <p style="font-size:18px; font-family: 'Segoe UI', sans-serif;word-spacing: 15px font-style: italic;">Crop production is influenced by a multitude of factors, including weather patterns (rainfall, temperature, humidity), soil conditions (fertility, type), crop variety, and farm management practices (irrigation, pest control). </p>
                            <p style="color: #706C26; font-size: 36px;">Data Collection:</p>
                            <p style="font-size:18px; font-family: 'Segoe UI', sans-serif;word-spacing: 15px font-style: italic;">Accurate prediction requires gathering data from diverse sources, including historical records, weather forecasts, soil surveys, and potentially satellite imagery. </p>
                            <p style="color: #706C26; font-size: 36px;">Modeling Techniques:</p>
                            <p style="font-size:18px; font-family: 'Segoe UI', sans-serif;word-spacing: 15px font-style: italic;">Various techniques are used for crop yield prediction, including statistical methods, machine learning algorithms (like Random Forest, Support Vector Machines, and Neural Networks), and deep learning approaches (such as Convolutional Neural Networks and Long Short-Term Memory).  </p>"""
                            ,unsafe_allow_html=True)
        st.image("Architecture-diagram-of-crop-yield-prediction.png", caption="Crop production prediction Flow chart", use_column_width=True)
        
with tab2:
    query1="""SELECT DISTINCT Area
                FROM crop_data1
                ORDER BY Area ASC;"""
    area_data=get_data(query1)
    area_data2=st.selectbox("Area",area_data)
    query2="""SELECT DISTINCT Item
                FROM crop_data1
                ORDER BY Item ASC;"""
    item_data=get_data(query2)
    item_data2=st.selectbox("Item",item_data)
            
    year = st.number_input(
        "Enter a year:",
        min_value=1900,
        max_value=2100,
        value=2024,
        step=1
    )
            
    harvested=st.number_input("Area Harvested")
    yield_1=st.number_input("Yield")
    button1=st.button("Predict")
    if button1:
        query3 = """
            SELECT DISTINCT Area_Code_M49
            FROM crop_data1
            WHERE Area = %s;
        """
        area = get_data(query3, params=(area_data2,))  # assuming area_data is a Series or DataFrame
            
        query4 = """
            SELECT DISTINCT Item_Code_CPC
            FROM crop_data1
            WHERE Item = %s;
        """
        item = get_data(query4, params=(item_data2,))  # same here
        df=[area.iloc[0],item.iloc[0], year, harvested, yield_1]
        df1=list(map(lambda x: int(float(x)), df))
        df2=abs(prediction(df1))
        df3=df2.astype(str)
        st.markdown(f"""<div style="background-color:#C00025; padding:20px; border-radius:10px;
                            border: 1px solid #ddd; box-shadow: 2px 2px 8px rgba(0,0,0,0.05);">
                            <h4 style="color:white;text-align:center;"><br>Crop Production of {item_data2} in {area_data2} during the year {year} is <br>{float(df3[0]):.2f} ton</h4>
                            """, unsafe_allow_html=True)
