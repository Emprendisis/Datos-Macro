
import streamlit as st
import wbdata
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# -------- Utilidades --------
def obtener_lista_paises_wb():
    try:
        paises = wbdata.get_country()
        return {p['name']: p['id'] for p in paises}
    except Exception as e:
        st.error(f"No se pudo cargar la lista de países del World Bank: {e}")
        return {}

def obtener_indicadores_wb():
    return {
        "PIB (USD)": "NY.GDP.MKTP.CD",
        "Inflación (%)": "FP.CPI.TOTL.ZG",
        "Desempleo (%)": "SL.UEM.TOTL.ZS",
        "PIB PPA (USD)": "NY.GDP.MKTP.PP.CD",
        "Crecimiento del PIB (%)": "NY.GDP.MKTP.KD.ZG",
        "Deuda total (% del PIB)": "GC.DOD.TOTL.GD.ZS",
        "Deuda total (USD)": "GC.DOD.TOTL.CN",
        "Balanza comercial (USD)": "NE.EXP.GNFS.CD",
        "Balanza comercial (% del PIB)": "NE.EXP.GNFS.ZS",
        "Prima de riesgo país": "FR.INR.RISK"
    }

def obtener_datos_wb(pais, indicador, anio_inicio, anio_fin):
    try:
        datos = wbdata.get_dataframe(
            {indicador: indicador},
            country=pais,
            data_date=(datetime(anio_inicio, 1, 1), datetime(anio_fin, 12, 31)),
            convert_date=True
        )
        return datos
    except Exception as e:
        st.error(f"Error al obtener datos del World Bank: {e}")
        return pd.DataFrame()

# -------- Interfaz --------
st.title("🌍 Explorador de Indicadores Macroeconómicos")
fuente = st.selectbox("Selecciona la fuente de datos:", ["World Bank"])  # futuras: FRED, IMF, etc.

if fuente == "World Bank":
    paises_dict = obtener_lista_paises_wb()
    if paises_dict:
        pais_nombre = st.selectbox("🌐 Selecciona el país:", list(paises_dict.keys()))
        pais_codigo = paises_dict[pais_nombre]

        indicadores = obtener_indicadores_wb()
        indicador_nombre = st.selectbox("📊 Selecciona el indicador:", list(indicadores.keys()))
        indicador_codigo = indicadores[indicador_nombre]

        anio_inicio = st.slider("Año de inicio", 2000, 2023, 2010)
        anio_fin = st.slider("Año de fin", anio_inicio + 1, 2024, 2023)

        if st.button("Consultar"):
            df = obtener_datos_wb(pais_codigo, indicador_codigo, anio_inicio, anio_fin)

            if not df.empty:
                st.line_chart(df)
                csv = df.to_csv().encode('utf-8')
                st.download_button("📥 Descargar datos en CSV", csv, file_name=f"{pais_nombre}_{indicador_nombre}.csv")
            else:
                st.warning("No se encontraron datos para los parámetros seleccionados.")
else:
    st.info("🔧 Esta fuente aún no está habilitada. En futuras versiones se incluirá soporte para FRED, IMF, TradingEconomics.")
