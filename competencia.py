import pandas as pd
import requests
import streamlit as st

pd.set_option('display.max_columns', None)
seller_id = st.text_input("seller ID", 82985379)
site = st.text_input("site", "MLA")


url = f'https://api.mercadolibre.com/sites/{site}/search?seller_id={seller_id}'

items = []
  
for offset in range(0, 1000, 50): 
        urls = url + '&offset=' + str(offset)
        respuesta = requests.request("GET", urls)
        try:
            rta = respuesta.json()
            items += rta['results']
            seller_info = rta['seller']
            seller_sales = seller_info['seller_reputation']['metrics']['sales']['completed']
            
        except:
            continue
items_df= pd.json_normalize(items)
items_df['pxq'] = items_df.price * items_df.sold_quantity
a = items_df['pxq'].sum()
b = items_df.sold_quantity.sum()
ticket_estimado = a / b
facturacion_60_aprox = ticket_estimado * seller_sales

st.write('Ticket Promedio Aproximado')
st.write(round(ticket_estimado))
st.write('Facturacion 60 días aproximada')
st.write(round(facturacion_60_aprox))
st.write('ventas ultimos 60 días')
st.write(seller_sales)