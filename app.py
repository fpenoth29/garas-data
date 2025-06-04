import streamlit as st
import pandas as pd
import os

# Archivos en el mismo directorio
ARCHIVO_GARANTIAS = "GarantiasBOb.xlsx"
ARCHIVO_PRECIOS = "Precios de Titulos Valores.xlsx"
ARCHIVO_AFOROS = "LISTA DE GARANTIAS.xlsx"

# si el archivo de garantias no existe, crearlo
if not os.path.exists(ARCHIVO_GARANTIAS):
    df_vacio = pd.DataFrame(columns=['Comitente - Número', 'Custodia', 'Instrumento - Código Caja', 'Saldo'])
    df_vacio.to_excel(ARCHIVO_GARANTIAS, index=False)

# Cargar datos
df_garantias = pd.read_excel(ARCHIVO_GARANTIAS)
df_precios = pd.read_excel(ARCHIVO_PRECIOS)
df_aforos = pd.read_excel(ARCHIVO_AFOROS)

df_precios["Cód."] = df_precios["Cód."].astype(str)
df_garantias["Instrumento - Código Caja"] = df_garantias["Instrumento - Código Caja"].astype(str)

df_merged = df_garantias.merge(df_precios, left_on="Instrumento - Código Caja", right_on="Cód.", how="left")
df_merged["ValorTotal"] = df_merged["Saldo"] * df_merged["Valor"]

st.title("Visualizador de Garantías (Datos Compartidos con Mesa)")
st.subheader("Datos actuales:")
columnas = ['Comitente - Número', 'Custodia', 'Instrumento - Código Caja', 'Saldo', 'Valor', 'ValorTotal']
st.dataframe(df_merged[columnas])

st.subheader("Agregar nueva fila:")
nuevo_comitente = st.text_input("Comitente - Número")
nueva_custodia = st.text_input("Custodia")
nuevo_codigo = st.text_input("Instrumento - Código Caja")
nuevo_saldo = st.number_input("Saldo", value=0.0)

if st.button("Agregar fila"):
    nueva_fila = {
        'Comitente - Número': nuevo_comitente,
        'Custodia': nueva_custodia,
        'Instrumento - Código Caja': nuevo_codigo,
        'Saldo': nuevo_saldo
    }
    df_garantias = pd.concat([df_garantias, pd.DataFrame([nueva_fila])], ignore_index=True)
    df_garantias.to_excel(ARCHIVO_GARANTIAS, index=False)
    st.success("Fila agregada correctamente. Refrescar app.")

st.subheader("Egresar saldo:")
comitente_egreso = st.text_input("Comitente para egreso")
codigo_egreso = st.text_input("Código Caja para egreso")
saldo_egreso = st.number_input("Saldo a egresar", value=0.0)

if st.button("Egresar"):
    mask = (
        (df_garantias['Comitente - Número'].astype(str) == comitente_egreso) &
        (df_garantias['Instrumento - Código Caja'].astype(str) == codigo_egreso)
    )
    if df_garantias[mask].empty:
        st.error("No se encontró esa combinación para egreso.")
    else:
        index = df_garantias[mask].index[0]
        if df_garantias.at[index, 'Saldo'] < saldo_egreso:
            st.error("El saldo a egresar excede el disponible.")
        else:
            df_garantias.at[index, 'Saldo'] -= saldo_egreso
            df_garantias.to_excel(ARCHIVO_GARANTIAS, index=False)
            st.success("Refrescar app para ver los cambios.")

st.info("Ya Esta Cargada la data")