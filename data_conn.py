import pyodbc
import pandas as pd

def get_data():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=147.135.39.147;DATABASE=STRATEGIO_OLAP_INTRADEVCO;UID=CesarVS;PWD=Cesar@VS!')
    client_product = pd.read_sql_query("WITH tabla as (SELECT CODIGOCLIENTE,CODIGOPRODUCTO,TIPOUNIDADMIN,AVGLAG = AVG(CONVERT(DECIMAL(7,0),DATEDIFF(DAY,PRIORDAY,FECHA))),NR_DAYS_TO_LAST_SELL = CONVERT(DECIMAL(7,0),DATEDIFF(DAY,MAX(FECHA),GETDATE())),AVGLAGUNIT = AVG(PRIORSELL) FROM (SELECT CODIGOCLIENTE,CODIGOPRODUCTO,TIPOUNIDADMIN,FECHA,PRIORDAY=LAG(FECHA,1) OVER (PARTITION BY CODIGOCLIENTE,CODIGOPRODUCTO,TIPOUNIDADMIN ORDER BY FECHA),PRIORSELL=LAG(CANTIDADUNIDADMINIMA,1) OVER (PARTITION BY CODIGOCLIENTE,CODIGOPRODUCTO,TIPOUNIDADMIN ORDER BY FECHA) FROM VENTAS WHERE FECHA<=GETDATE()) AS LAGGED GROUP BY CODIGOCLIENTE,CODIGOPRODUCTO,TIPOUNIDADMIN) SELECT * FROM tabla WHERE AVGLAG IS NOT NULL AND AVGLAG>NR_DAYS_TO_LAST_SELL AND AVGLAG<300",conn)
    list_product = pd.read_sql_query("SELECT M.CodigoProducto as CODIGOPRODUCTO,M.DescripcionProducto as DESCRIPCION,M.Categoria as CATEGORIA,CASE WHEN SUM(V.CANTIDADUNIDADMINIMA)>0 AND SUM(V.VENTASINIGV)>0 THEN CONVERT(DECIMAL(7,2),AVG(V.VENTASINIGV/V.CANTIDADUNIDADMINIMA)) ELSE NULL END AS AVG_PRICE FROM MAESTROGENERAL AS M INNER JOIN VENTAS AS V ON V.CODIGOPRODUCTO=M.CodigoProducto WHERE V.CANTIDADUNIDADMINIMA > 0 GROUP BY M.CodigoProducto,M.DescripcionProducto,M.Categoria",conn)
    list_product.dropna(inplace=True)
    client_product.to_csv('client_prod.csv')
    list_product.to_csv('list_prod.csv')
    print("Done!!!")

get_data()