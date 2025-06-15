
import streamlit as st
import pandas as pd
import wbdata
import datetime

# Placeholder para futuras integraciones con otras APIs
# from fredapi import Fred
# from tradingeconomics import login, getIndicatorData
# from imfdatapy import Repository

# Título
st.set_page_config(page_title="Consulta de Indicadores Macroeconómicos", layout="centered")
st.title("🌐 Consulta de Indicadores Macroeconómicos")

# Selección de fuente
repositorio = st.selectbox("Selecciona la fuente de datos", ["World Bank", "FRED (EE.UU.)", "TradingEconomics", "IMF"])

# Opciones para World Bank
if repositorio == "World Bank":
    paises = {
        "México": "MEX", "Colombia": "COL", "Argentina": "ARG", "Chile": "CHL", "Perú": "PER",
        "Brasil": "BRA", "Estados Unidos": "USA", "España": "ESP", "Francia": "FRA", "Alemania": "DEU"
    }
    pais = st.selectbox("🌎 País", list(paises.keys()))
    codigo_pais = paises[pais]

    indicadores = {
        "PIB (USD)": "NY.GDP.MKTP.CD",
        "PIB PPA (USD)": "NY.GDP.MKTP.PP.CD",
        "Tasa crecimiento PIB (%)": "NY.GDP.MKTP.KD.ZG",
        "Inflación (%)": "FP.CPI.TOTL.ZG",
        "Desempleo (%)": "SL.UEM.TOTL.ZS",
        "Deuda externa total (USD)": "DT.DOD.DECT.CD",
        "Deuda externa (% PIB)": "DT.DOD.DECT.GN.ZS"
    }

    indicador_nombre = st.selectbox("📊 Indicador", list(indicadores.keys()))
    indicador_codigo = indicadores[indicador_nombre]

    fecha_inicio = st.slider("Selecciona año de inicio", 2000, datetime.datetime.now().year - 1, 2010)
    fecha_fin = st.slider("Selecciona año de fin", fecha_inicio + 1, datetime.datetime.now().year, 2022)

    if st.button("📥 Obtener datos"):
        try:
            df = wbdata.get_dataframe(
                {indicador_codigo: indicador_nombre},
                country=codigo_pais,
                data_date=(datetime.datetime(fecha_inicio, 1, 1), datetime.datetime(fecha_fin, 12, 31)),
                convert_date=True
            )
            df = df.reset_index()
            st.dataframe(df)
            st.line_chart(df.set_index("date")[indicador_nombre])

            file_name = f"{codigo_pais}_{indicador_codigo}_{fecha_inicio}_{fecha_fin}.xlsx"
            df.to_excel(file_name, index=False)
            with open(file_name, "rb") as f:
                st.download_button("📤 Descargar Excel", f, file_name=file_name)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("🚧 Esta fuente aún no está habilitada en la demo. Pronto podrás consultar FRED, IMF y TradingEconomics directamente aquí.")

