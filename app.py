import streamlit as st
import pandas as pd
import wbdata
import datetime
import matplotlib.pyplot as plt

# --- Configuración inicial ---
st.set_page_config(page_title="Indicadores Macroeconómicos", layout="centered")
st.title("📊 Consulta de Indicadores Macroeconómicos Mundiales")

# --- Diccionario de indicadores del Banco Mundial ---
indicadores = {
    "Deuda externa total (USD)": "DT.DOD.DECT.CD",
    "Deuda externa total (% del PIB)": "DT.DOD.DECT.GN.ZS",
    "PIB (USD)": "NY.GDP.MKTP.CD",
    "Balanza comercial (USD)": "NE.EXP.GNFS.CD",  # Exportaciones como proxy
    "Balanza comercial (% PIB)": "NE.EXP.GNFS.ZS",
    "Tasa de desempleo": "SL.UEM.TOTL.ZS",
    "Inflación (IPC anual %)": "FP.CPI.TOTL.ZG",
    "PIB (PPA, USD internacionales)": "NY.GDP.MKTP.PP.CD",
    "Crecimiento del PIB (%)": "NY.GDP.MKTP.KD.ZG",
    "Prima de riesgo (bonos soberanos, %)": "CM.MKT.LDOM.NO"
}

# --- Widgets de selección ---
with st.sidebar:
    st.header("Filtros")
    # Obtener el diccionario de países {código: nombre}
    paises_dict = wbdata.get_country()
    paises = {pais['id']: pais['name'] for pais in paises_dict}

# Menú desplegable con los nombres
    pais_nombre = st.selectbox("🌍 País", list(paises.values()))

# Recuperar el código del país seleccionado
    pais_codigo = [codigo for codigo, nombre in paises.items() if nombre == pais_nombre][0]   
    indicador = st.selectbox("Indicador", list(indicadores.keys()))
    anio_inicio, anio_fin = st.slider("Rango de años", 2000, 2023, (2010, 2022))

# --- Descarga de datos ---
try:
    codigo = indicadores[indicador]
    data = wbdata.get_dataframe({codigo: indicador}, country=pais, data_date=(datetime.datetime(anio_inicio, 1, 1), datetime.datetime(anio_fin, 12, 31)))
    data.reset_index(inplace=True)
    data = data.dropna()

    st.success(f"Datos encontrados: {len(data)} años disponibles")

    # --- Gráfica ---
    st.subheader(f"{indicador} en {pais.upper()}")
    fig, ax = plt.subplots()
    ax.plot(data['date'], data[indicador], marker="o")
    ax.set_xlabel("Año")
    ax.set_ylabel(indicador)
    ax.set_title(f"{indicador} ({anio_inicio} - {anio_fin})")
    ax.invert_xaxis()
    st.pyplot(fig)

    # --- Exportar a Excel ---
    excel = data.to_excel(index=False)
    st.download_button("📥 Descargar Excel", excel, file_name=f"{pais}_{codigo}.xlsx")

    # --- Mostrar tabla ---
    st.dataframe(data)

except Exception as e:
    st.error(f"Error al obtener datos: {e}")
