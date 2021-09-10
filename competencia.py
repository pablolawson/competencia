import pandas as pd
import numpy as np
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
            seller_name = seller_info['nickname']
        except:
            continue
items_df= pd.json_normalize(items)

items_df['pxq'] = items_df.price * items_df.sold_quantity
a = items_df['pxq'].sum()
b = items_df.sold_quantity.sum()
ticket_estimado = a / b
facturacion_60_aprox = ticket_estimado * seller_sales

st.write(seller_name)
st.write('Ticket promedio aproximado:')
st.write("${:,.0f}". format(round(ticket_estimado)))
st.write('Facturación 60 días aproximada:')
st.write("${:,.0f}". format(round(facturacion_60_aprox)))
st.write('Ventas últimos 60 días:')
st.write(seller_sales)
