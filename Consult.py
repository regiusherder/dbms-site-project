# Core Pkgs
import streamlit as st 
import base64
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
# DB Mgmt
import sqlite3 
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Fxn Make Execution
def sql_executor(raw_code):
	c.execute(raw_code)
	data = c.fetchall()
	return data 

def main():
    st.title("Realistica Consultants")
    st.subheader("Construction Cost Estimation")
    col1,col2 = st.columns(2)
    with col1:
        with st.form(key='query_form'):
            land_option = st.selectbox( "Where do you want to build",('Coimbatore','Mumbai','Delhi','Chennai'))
            land_type = st.selectbox( "What kind of land do you want to build in",('Industrial','Commercial','Agricultural'))
            land_size = st.number_input("What size of land do you want")
            submit_code = st.form_submit_button("Submit")
			
		# Results Layouts
    with col2:
        if submit_code:
            if land_size<0:
                land_size = abs(land_size)
                st.write("Error : negative land size detected, using absolute value")
            if land_size==0:
                st.write("Error : land size 0, showing minimum cost estimate")

            total = 0
            st.info("The estimated construction cost is ")
            land_q = "SELECT SIZE,COST FROM LAND WHERE LOCATION = '" + land_option +"'  AND TYPE = '" +land_type+"'"
            land_price_v_size = sql_executor(land_q)

            df_land = pd.DataFrame(land_price_v_size)

            X_land = df_land[0].to_numpy().reshape(-1,1)
            y_land = df_land[1].to_numpy().reshape(-1,1)
            reg = LinearRegression().fit(X_land,y_land)
            land_result = reg.predict([[land_size]])[0][0]

            total += land_result

            land_id_q = "SELECT LAND_ID FROM LAND WHERE LOCATION = '" + land_option +"'  AND TYPE = '" +land_type+"'"
            land_ids = sql_executor(land_id_q)
            df_land_ids = pd.DataFrame(land_ids)
            current_pros = []
            for i in df_land_ids.to_numpy().tolist():
                for j in i:
                    current_pros.append(j)

            items = sql_executor("SELECT I.PROJECT_ID,I.TYPE,I.QUANTITY,I.COST,L.SIZE FROM ITEM I, LAND L WHERE I.PROJECT_ID = L.PROJECT_ID")
            df_items = pd.DataFrame(items)
            df_items[5] = df_items[2]*df_items[3]
            df_items = df_items[df_items[0].isin(current_pros)]

            df_unique_items=df_items[1].unique().tolist()
            price_items = dict.fromkeys(df_unique_items)

            for i in df_unique_items:
                X_item = df_items[df_items[1]==i][4].to_numpy().reshape(-1,1)
                y_item = df_items[df_items[1]==i][5].to_numpy().reshape(-1,1)
                reg = LinearRegression().fit(X_item,y_item)
                pred = int(reg.predict([[land_size]])[0][0])
                total+=pred
                price_items[i] = pred
            
            items = sql_executor("SELECT I.PROJECT_ID,I.TYPE,I.QUANTITY,I.SALARY,L.SIZE FROM LABOR I, LAND L WHERE I.PROJECT_ID = L.PROJECT_ID")
            df_items = pd.DataFrame(items)
            df_items = df_items[df_items[0].isin(current_pros)]
            df_unique_labor=df_items[1].unique().tolist()
            price_labor = {}

            import math
            for i in df_unique_labor:
                X_no = df_items[df_items[1]==i][4].to_numpy().reshape(-1,1)
                y_no = df_items[df_items[1]==i][2].to_numpy().reshape(-1,1)
                X_sal = df_items[df_items[1]==i][4].to_numpy().reshape(-1,1)
                y_sal = df_items[df_items[1]==i][3].to_numpy().reshape(-1,1)
                reg_no = LinearRegression().fit(X_no,y_no)
                reg_sal = LinearRegression().fit(X_sal,y_sal)

                pred_no = math.ceil(reg_no.predict([[land_size]])[0][0])
                pred_sal = int(reg_sal.predict([[land_size]])[0][0])

                time = LinearRegression().fit(np.array([500,1000,5000]).reshape(-1,1),np.array([6,10,15]).reshape(-1,1))
                time = time.predict([[land_size]])[0][0]

                total += (pred_no*pred_sal)*time

                price_labor["No. of "+i+" workers"] = pred_no
                price_labor["Salary(-/mo) of "+i+" workers"] = pred_sal
            
            st.markdown("<h3>₹"+str(int(total))+"</h2>",unsafe_allow_html =True)

            with st.expander("Cost of Land"):
                st.write('₹'+str(land_result))
            with st.expander("Item's Cost Segmentation"):
                st.write(price_items)
            with st.expander("Labor Cost"):
                st.write(price_labor)



if __name__ == '__main__':
	main()
