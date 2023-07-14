# Prueba Pyhton N°1

# # Se necesita realizar una conciliación entre dos sistemas que maneja el banco actualmente. Especificamente se tiene dos insumos (Insumo N1, Insumo N2) los cuales deben ser comparados siguiendo las reglas a continuación.
# 1. Importe los insumos más el catalogo que se encuentran dentro de la carpeta Insumos y guardelos en Dataframes.
# 2. Pase los saldos EUR a USD en los dataframes donde sea necesario con la tasa de conversión  1 EUR = 1.09 USD
# 3. Usando el dataframe que contiene la data del Insumo N1, cree un dataframe que muestre la cantidad de prestamos unicos y el total del saldo agrupado por el status.
# 4. Mediante el uso del dataframe con la data del Catalogo N1, traiga la descripción de la cuenta al dataframe que contiene la data del Insumo N1 (Use como llave ID Cuenta). 
# 5. Traiga al dataframe del Insumo N1 los saldos del dataframe del Insumo N2 (Use como llave el ID Cliente, Cuenta y ID Prestamo), y cree una columna que contenga la diferencia de los mismos. Adicional, cree una columna que 
# contenga el valor "CORRECTO", si la diferencia es 0, "SOBRE EL VALOR" si la diferencia es >0 y "DEBAJO DEL VALOR" si la diferencia es <0.
# 6. Por último: 
    # - Cree un archivo de excel dónde en la primera hoja coloque el Dataframe agrupado por status, el contedo distintivo de los prestamos y la suma de los totales de estos.
    # - En la segunda hoja coloque el dataframe que contiene la data del Insumo N1 junto con las modificaciones de los pasos 2,4,5 (LLeve solo la información filtrada por Status 1 y 2)


# Prueba Pyhton N°1
## librery
import pandas as pd

# Leer el archivo .xlsx y convertirlo en un DataFrame
dfN1 = pd.read_excel('Insumos/Insumo N1.xlsx')
dfN2 = pd.read_excel('Insumos/Insumo N2.xlsx')
dfC1 = pd.read_excel('Insumos/Catalogo N1.xlsx')

#print(df1)
# conversion de saldos de EUR a USD -- punto 2
dfN1.loc[dfN1['Moneda'] == 'EUR', 'Saldo'] *= 1.09
dfN1.loc[dfN1['Moneda'] == 'EUR', 'Moneda'] = 'USD'

dfN2.loc[dfN2['Moneda'] == 'EUR', 'Saldo'] *= 1.09
dfN2.loc[dfN2['Moneda'] == 'EUR', 'Moneda'] = 'USD'


# sando el dataframe que contiene la data del Insumo N1, cree un dataframe que muestre 
# la cantidad de prestamos unicos y el total del saldo agrupado por el status. -- 3
df4 = dfN1.groupby('Status').agg({'ID Cliente': 'count', 'Saldo': 'sum'}).reset_index()
# 4. Mediante el uso del dataframe con la data del Catalogo N1, 
# traiga la descripción de la cuenta al dataframe que contiene la data del Insumo N1 (Use como llave ID Cuenta). --4
dfN1['Tipo Cuenta'] = dfN1['Tipo Cuenta'].map(dfC1.set_index('ID Cuenta')['Descripcion cuenta'])

## 5. Traiga al dataframe del Insumo N1 los saldos del dataframe del Insumo N2 (Use como llave el ID Cliente, Cuenta y ID Prestamo),
# y cree una columna que contenga la diferencia de los mismos. Adicional, cree una columna que 
# contenga el valor "CORRECTO", si la diferencia es 0, "SOBRE EL VALOR" si la diferencia es >0 y 
# "DEBAJO DEL VALOR" si la diferencia es <0. --5
dfN1 = pd.merge(dfN1, dfN2, on=['ID Cliente', 'Cuenta', 'ID Prestamo'], how='left')
dfN1['Saldo_y'] = dfN1['Saldo_y'].fillna(0)
dfN1 = dfN1.drop('Moneda_y', axis=1)
dfN1['Diferencia'] = dfN1['Saldo_x'] - dfN1['Saldo_y']
dfN1['Estado'] = dfN1['Diferencia'].apply(lambda x: 'CORRECTO' if x == 0 else 'SOBRE EL VALOR' if x > 0 else 'DEBAJO DEL VALOR')
dfN1 = dfN1.rename(columns={'Moneda_x': 'Moneda'})


#6. Por último: 
# - Cree un archivo de excel dónde en la primera hoja coloque el Dataframe agrupado por status,
# el contedo distintivo de los prestamos y la suma de los totales de estos.
# - En la segunda hoja coloque el dataframe que contiene la data del Insumo N1 junto con las modificaciones de los pasos 2,4,5
# (LLeve solo la información filtrada por Status 1 y 2)
with pd.ExcelWriter("Conciliacion.xlsx") as writer:
    df4.to_excel(writer, sheet_name='Hoja1', index=False)
    df2_filtered = dfN1[(dfN1['Status'] == 2) | (dfN1['Status'] == 1)]  
    df2_filtered.to_excel(writer, sheet_name='Hoja2', index=False)

# Mostrar el DataFrame
#print(dfN1)
#print(dfN2)
#print(dfC1)
print(df2_filtered)








