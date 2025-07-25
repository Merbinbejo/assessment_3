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
html_temp="""<div style="background-color:tomato;padding:10px">
                <h2 style="color:white;text-align:center;">streamlit Crop Production Prediction ML App</h2>
                </div>
                """
st.markdown(html_temp,unsafe_allow_html=True)
with st.container():
    col1,col2,col3=st.columns(3)
    with col2:
        query1="""SELECT DISTINCT Area
                    FROM crop_data
                    ORDER BY Area ASC;"""
        area_data=get_data(query1)
        area_data2=st.selectbox("Area",area_data)
        query2="""SELECT DISTINCT Item
                    FROM crop_data
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
                FROM crop_data
                WHERE Area = %s;
            """
            area = get_data(query3, params=(area_data2,))  # assuming area_data is a Series or DataFrame
        
            query4 = """
                SELECT DISTINCT Item_Code_CPC
                FROM crop_data
                WHERE Item = %s;
            """
            item = get_data(query4, params=(item_data2,))  # same here
            df=[area.iloc[0],item.iloc[0], year, harvested, yield_1]
            df1=list(map(int,df))
            df2=abs(prediction(df1))
            df3=df2.astype(str)
            st.markdown(f"""<div style="background-color:#C00025; padding:20px; border-radius:10px;
                                border: 1px solid #ddd; box-shadow: 2px 2px 8px rgba(0,0,0,0.05);">
                                <h4 style="color:white;text-align:center;">Crop Production of {item_data2} in {area_data2} during the year {year} is <br>{float(df3[0]):.2f} ton</h4>
                                """, unsafe_allow_html=True)
