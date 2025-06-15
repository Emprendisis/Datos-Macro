
import streamlit as st
import pandas as pd
import wbdata
import datetime
from fredapi import Fred
import requests

# Configuración inicial
st.set_page_config(page_title="Macro Data Explorer", layout="centered")
st.title("📊 Explorador de Indicadores Macroeconómicos")

# Menú de selección de fuente de datos
fuente = st.selectbox("Selecciona la fuente de datos:", ["World Bank", "FRED", "IMF (simulado)", "TradingEconomics (simulado)"])

# Parámetros por fuente
if fuente == "World Bank":
    paises = {
        "México": "MEX",
        "Colombia": "COL",
        "Estados Unidos": "USA",
        "España": "ESP"
    }
    indicadores = {
        "PIB (USD)": "NY.GDP.MKTP.CD",
        "Desempleo (%)": "SL.UEM.TOTL.ZS",
        "Inflación (%)": "FP.CPI.TOTL.ZG",
        "Deuda total (% PIB)": "GC.DOD.TOTL.GD.ZS",
        "Crecimiento del PIB (%)": "NY.GDP.MKTP.KD.ZG"
    }

    pais = st.selectbox("🌎 Selecciona el país:", list(paises.keys()))
    indicador = st.selectbox("📈 Selecciona el indicador:", list(indicadores.keys()))
    anio_inicio = st.slider("Año de inicio", 2000, 2023, 2010)
    anio_fin = st.slider("Año de fin", anio_inicio, 2024, 2023)

    if st.button("Consultar"):
        try:
            fecha_inicio = datetime.datetime(anio_inicio, 1, 1)
            fecha_fin = datetime.datetime(anio_fin, 12, 31)
            df = wbdata.get_dataframe({indicadores[indicador]: indicador}, 
                                       country=paises[pais], data_date=(fecha_inicio, fecha_fin))
            df = df.dropna().sort_index()
            df.index = df.index.year
            st.line_chart(df)
            st.dataframe(df)

            excel_file = f"{pais}_{indicador}_macro.xlsx"
            df.to_excel(excel_file)
            with open(excel_file, "rb") as f:
                st.download_button("📥 Descargar Excel", f, file_name=excel_file)
        except Exception as e:
            st.error(f"Error: {e}")

elif fuente == "FRED":
    st.info("🔐 Requiere API Key de FRED configurada en entorno local.")

elif fuente == "IMF (simulado)":
    st.success("IMF habilitado. Próximamente integración real.")

elif fuente == "TradingEconomics (simulado)":
    st.success("TradingEconomics habilitado. Requiere API Key para integración real.")
