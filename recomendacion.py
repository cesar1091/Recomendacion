import numpy as np

class Recomendacion:
    def __init__(self,client_df,prod_df):
        self.client_df = client_df
        self.prod_df = prod_df
        
    def clientes_call(self):
        self.client_df['diff'] = self.client_df['AVGLAG'].astype(int) - self.client_df['NR_DAYS_TO_LAST_SELL'].astype(int)
        list_client_prod = self.client_df[self.client_df['diff']==0][['CODIGOCLIENTE','CODIGOPRODUCTO','AVGLAGUNIT']]
        return list_client_prod
    
    def prod_relacionados(self,prod_cod):
        try:
            category = self.prod_df[self.prod_df['CODIGOPRODUCTO']==prod_cod]['CATEGORIA'].values[0]
            price = self.prod_df[self.prod_df['CODIGOPRODUCTO']==prod_cod]['AVG_PRICE'].values[0]
            relacionados = self.prod_df[(self.prod_df['CATEGORIA']==category) & (self.prod_df['CODIGOPRODUCTO']!=prod_cod)][['CODIGOPRODUCTO','DESCRIPCION','AVG_PRICE']]
            relacionados['diff'] = np.abs(relacionados['AVG_PRICE']-price)
            relacionados = relacionados.sort_values(by='diff',ascending=True)
            return relacionados[['CODIGOPRODUCTO','DESCRIPCION','AVG_PRICE']].iloc[:20].to_json(orient="records")
        except:
            return 'No recomendation'

    def data_final(self):
        data = self.clientes_call()
        data['Recomendacion'] = data.apply(lambda row : self.prod_relacionados(row['CODIGOPRODUCTO']),axis=1)
        return data