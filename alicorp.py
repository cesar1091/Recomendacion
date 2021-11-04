#from data_conn import get_data
import pandas as pd
import json
import streamlit as st
from recomendacion import Recomendacion

#get_data()

st.image("banner.png")

client_product = pd.read_csv("client_prod.csv",index_col=0,dtype={"CODIGOCLIENTE": str, "CODIGOPRODUCTO": str, "AVGLAG":float, "NR_DAYS_TO_LAST_SELL":float, "AVGLAGUNIT":float})
list_product = pd.read_csv("list_prod.csv",index_col=0,dtype={"CODIGOPRODUCTO":str,"DESCRIPCION":str,"CATEGORIA":object,"AVG_PRICE":float})

test = Recomendacion(client_product,list_product)
st.sidebar.image("logo.png")
data = test.data_final()
data = data[data['Recomendacion']!='No recomendation']
st.title('Sistema de Recomendacion')
choice = st.sidebar.radio('Seleccionar:',('Clientes a llamar','Recomendacion por cliente y pedido'))
if choice == 'Clientes a llamar':
    call_df = test.clientes_call()
    call_df.index = range(len(call_df))
    cliente = st.sidebar.selectbox("Clientes pedidos regular:",list(call_df['CODIGOCLIENTE'].unique()))
    st.table(call_df[call_df['CODIGOCLIENTE']==cliente][['CODIGOPRODUCTO','AVGLAGUNIT']])
if choice == 'Recomendacion por cliente y pedido':
    cliente = st.sidebar.selectbox("Seleccione un cliente:",list(data['CODIGOCLIENTE'].unique()))
    producto = st.sidebar.selectbox("Seleccione a un producto:",list(data[data['CODIGOCLIENTE']==cliente]['CODIGOPRODUCTO'].unique()))
    cantidad = client_product[client_product["CODIGOCLIENTE"]==cliente]["AVGLAGUNIT"].values[0]
    st.write(f'El cliente de código {cliente} se le recomienda {cantidad} unidades de los siguientes productos:')
    a = data[(data['CODIGOCLIENTE']==cliente) & (data['CODIGOPRODUCTO']==producto)]['Recomendacion'].values[0]

    try:
        to_python = json.loads(a)
        tabla = pd.DataFrame(to_python)
        st.table(tabla.iloc[:,:2])
    except json.decoder.JSONDecodeError:
        st.write('No tiene recomendacion')

    

